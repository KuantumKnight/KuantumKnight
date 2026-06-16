"""
shared helpers for the KuantumKnight profile pipeline.

design goals:
  - stdlib only. no pip install in the action -> nothing to break.
  - everything fails soft. if the github api is down or rate-limited,
    generators fall back to sane known values so the readme never ships blank.
  - one network pass, memoized, shared across all generators in a single run.
"""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

LOGIN = "KuantumKnight"

# ---------------------------------------------------------------- palette ----
# signature: neon green on near-black. evolve, don't replace.
BG        = "#0a0e0d"   # near-black, faint green tint
PANEL     = "#0d1411"   # slightly lifted panel
BORDER    = "#16241e"   # hairline border
GRID      = "#11201a"   # empty contribution cell
GREEN     = "#00ff9c"   # primary neon
GREEN_DIM = "#1f8a63"   # dim green (mid intensity)
GREEN_LO  = "#0f3b2c"   # low intensity
CYAN      = "#5ef2ff"   # sparing secondary accent (numbers)
WHITE     = "#e6f2ec"   # bright text
GREY      = "#5c6b64"   # muted / comments
RED       = "#ff5f56"   # window dot
AMBER     = "#febc2e"   # window dot
LIME      = "#27c93f"   # window dot

# green ramp for contribution intensity (level 0..4)
RAMP = [GRID, "#0f3b2c", "#11623f", "#159f63", GREEN]

# universal monospace stack — resolves on the viewer's machine, no web fonts.
MONO = ("'SFMono-Regular',ui-monospace,'JetBrains Mono','Fira Code',"
        "'Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace")

# ----------------------------------------------------------------- fetch ----

_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
_UA = "kuantumknight-profile-pipeline"


def _req(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={
        "User-Agent": _UA,
        "Accept": accept,
    })
    if _TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {_TOKEN}")
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def _api(path):
    try:
        return json.loads(_req(f"https://api.github.com{path}"))
    except Exception as e:  # noqa: BLE001 — fail soft on purpose
        print(f"[warn] api {path}: {e}")
        return None


# --------------------------------------------------------- contributions ----

def _scrape_contributions():
    """
    pull the public contribution calendar from the profile html.
    no token, no api. returns list of {date, count, level} or None.
    """
    try:
        html = _req(f"https://github.com/users/{LOGIN}/contributions",
                    accept="text/html")
    except Exception as e:  # noqa: BLE001
        print(f"[warn] contributions scrape: {e}")
        return None

    cells = []
    # modern github markup: <td ... data-date="2026-06-15" data-level="3">
    # tolerate attribute order with two passes.
    for m in re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*', html):
        chunk = m.group(0)
        date = m.group(1)
        lvl = re.search(r'data-level="(\d)"', chunk)
        level = int(lvl.group(1)) if lvl else 0
        cells.append({"date": date, "level": level})
    # some markup puts data-level before data-date; second pass if empty
    if not cells:
        for m in re.finditer(r'data-level="(\d)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', html):
            cells.append({"date": m.group(2), "level": int(m.group(1))})
    return cells or None


def _synthetic_calendar():
    """deterministic fallback grid so contrib art renders even offline."""
    cells = []
    # 53 weeks x 7 days, a calm believable pattern (no randomness allowed here)
    for w in range(53):
        for d in range(7):
            n = (w * 7 + d)
            level = (n * 37 % 5)
            # taper the far past, busier recent
            if w < 12:
                level = max(0, level - 2)
            cells.append({"date": f"w{w}d{d}", "level": level})
    return cells


# ----------------------------------------------------------- aggregation ----

_CACHE = None

# known-good fallbacks (from the live profile) so nothing ships blank
_FALLBACK = {
    "repos": 14,
    "stars": 73,
    "followers": 13,
    "following": 13,
    "bugbouncer_stars": 65,
    "langs": [("Python", 34), ("TypeScript", 28), ("C", 16),
              ("JavaScript", 14), ("HTML", 8)],
    "events": [],
}

def collect():
    """gather everything once, memoized for the whole build run."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    d = dict(_FALLBACK)
    d["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M utc")
    d["generated_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    user = _api(f"/users/{LOGIN}")
    if user:
        d["followers"] = user.get("followers", d["followers"])
        d["following"] = user.get("following", d["following"])
        d["repos"] = user.get("public_repos", d["repos"])

    repos = _api(f"/users/{LOGIN}/repos?per_page=100&sort=pushed")
    if isinstance(repos, list) and repos:
        own = [r for r in repos if not r.get("fork")]

        # count stars on repos you actually authored, not forks you starred-by-proxy
        d["stars"] = sum(r.get("stargazers_count", 0) for r in own)

        for r in repos:
            if r.get("name", "").lower() == "bugbouncer":
                d["bugbouncer_stars"] = r.get(
                    "stargazers_count",
                    d["bugbouncer_stars"]
                )

        # language breakdown by actual code bytes
        bytes_by_lang = {}

        for r in own[:25]:
            ld = _api(f"/repos/{LOGIN}/{r['name']}/languages")

            if isinstance(ld, dict):
                for k, v in ld.items():
                    bytes_by_lang[k] = bytes_by_lang.get(k, 0) + v

        if not bytes_by_lang:
            for r in own[:30]:
                lang = r.get("language")

                if lang:
                    bytes_by_lang[lang] = (
                        bytes_by_lang.get(lang, 0)
                        + max(r.get("size", 1), 1)
                    )

        if bytes_by_lang:
            total = sum(bytes_by_lang.values()) or 1

            ranked = sorted(
                bytes_by_lang.items(),
                key=lambda x: -x[1]
            )

            langs = [
                (k, round(v * 100 / total))
                for k, v in ranked
            ]

            langs = [
                (k, p)
                for k, p in langs
                if p >= 1
            ][:5]

            if langs:
                d["langs"] = langs

        # ----------------------------------------------------------
        # recent ops feed — actual commit activity
        # ----------------------------------------------------------

        feed = []
        seen = set()

        events = _api(f"/users/{LOGIN}/events?per_page=100")

        if isinstance(events, list):
            for e in events:
                if e.get("type") != "PushEvent":
                    continue

                full_repo = e.get("repo", {}).get("name", "")
                owner = full_repo.split("/")[0] if "/" in full_repo else ""

                # show commits pushed to ANY repo, not just your own.
                # your own repos display as just the repo name; pushes to
                # someone else's repo display as owner/repo so the source is clear.
                if owner.lower() == LOGIN.lower():
                    repo_name = full_repo.split("/")[-1]
                else:
                    repo_name = full_repo

                created = (e.get("created_at") or "")[:10]

                commits = e.get("payload", {}).get("commits", [])

                # the events feed only contains pushes you performed, so every
                # commit here is yours; list newest first (a push payload is
                # ordered oldest→newest)
                for c in reversed(commits):
                    sha = (c.get("sha") or "")[:7]

                    msg = (
                        (c.get("message") or "")
                        .splitlines()[0]
                        .strip()
                    )

                    key = f"{full_repo}:{sha}"

                    if key in seen:
                        continue

                    seen.add(key)

                    desc = f"{sha} · {msg}" if sha else msg

                    feed.append({
                        "name": repo_name,
                        "date": created,
                        "desc": desc,
                        "lang": "",
                        "stars": None,
                    })

                    if len(feed) >= 7:
                        break

                if len(feed) >= 7:
                    break

        # fallback if events API fails
        if not feed:
            for r in repos:
                if r.get("fork"):
                    continue

                feed.append({
                    "name": r.get("name", "?"),
                    "date": (r.get("pushed_at") or "")[:10],
                    "desc": (r.get("description") or "").strip(),
                    "lang": r.get("language") or "",
                    "stars": r.get("stargazers_count", 0),
                })

                if len(feed) >= 7:
                    break

        d["events"] = feed

    # contributions (scraped, no token)
    cal = _scrape_contributions() or _synthetic_calendar()

    d["calendar"] = cal
    d["contrib_total"] = sum(
        1 for c in cal
        if c.get("level", 0) > 0
    )

    _CACHE = d
    return d

# -------------------------------------------------------------- svg utils ----

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def write_svg(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"[ok] wrote {path} ({len(body)} bytes)")
