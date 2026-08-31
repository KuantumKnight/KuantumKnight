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
from pathlib import Path

LOGIN = "KuantumKnight"

# ---------------------------------------------------------------- palette ----
# signature: neon green on near-black. evolve, don't replace.
BG        = "#050706"   # ink-black paper
PANEL     = "#0b0d0c"   # lifted black
BORDER    = "#30342f"   # photocopy edge
GRID      = "#171a17"   # empty contribution cell
GREEN     = "#b7ff2a"   # signal green
GREEN_DIM = "#6d9b2a"   # dim signal
GREEN_LO  = "#283818"   # low intensity
CYAN      = "#67f4d2"   # telemetry accent
WHITE     = "#eeeade"   # dirty paper
GREY      = "#858880"   # muted copy
RED       = "#e63229"   # proofing red
AMBER     = "#e7b43a"   # secondary mark
LIME      = "#b7ff2a"   # signal dot
PAPER     = "#e7e1d3"   # pasted paper
SILVER    = "#c9cdc8"   # liquid-metal type

# green ramp for contribution intensity (level 0..4)
RAMP = [GRID, "#263517", "#47651d", "#729f22", GREEN]

# universal monospace stack — resolves on the viewer's machine, no web fonts.
MONO = ("'SFMono-Regular',ui-monospace,'JetBrains Mono','Fira Code',"
        "'Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace")

# ----------------------------------------------------------------- fetch ----

_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
_UA = "kuantumknight-profile-pipeline"
_ROOT = Path(__file__).resolve().parent.parent
_PROFILE_CACHE = None


def profile():
    """Load hand-maintained profile copy from one source of truth."""
    global _PROFILE_CACHE
    if _PROFILE_CACHE is None:
        with (_ROOT / "profile.json").open(encoding="utf-8") as f:
            _PROFILE_CACHE = json.load(f)
    return _PROFILE_CACHE


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


# ----------------------------------------------------------- aggregation ----

_CACHE = None

# known-good fallbacks (from the live profile) so nothing ships blank
_FALLBACK = {
    "repos": 0,
    "stars": 0,
    "followers": 0,
    "following": 0,
    "bugbouncer_stars": None,
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
    d["api_ok"] = False
    d["calendar_ok"] = False
    d["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M utc")
    d["generated_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    user = _api(f"/users/{LOGIN}")
    if user:
        d["api_ok"] = True
        d["followers"] = user.get("followers", d["followers"])
        d["following"] = user.get("following", d["following"])
        d["repos"] = user.get("public_repos", d["repos"])

    repos = _api(f"/users/{LOGIN}/repos?per_page=100&sort=pushed")
    if isinstance(repos, list) and repos:
        d["api_ok"] = True
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
                        "kind": "push",
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
                    "kind": "repo",
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
    cal = _scrape_contributions()
    d["calendar_ok"] = bool(cal)
    d["calendar"] = cal or []
    d["contrib_total"] = (sum(
        1 for c in cal if c.get("level", 0) > 0
    ) if cal else None)

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
