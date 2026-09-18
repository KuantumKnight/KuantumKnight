"""
gen_ascii.py — a rotating spade, raymarched in pure python, shot as ascii.

the spade is a 2d signed distance field (two lobes + a point + a stem,
smooth-unioned), extruded with rounded edges and turned about the y axis.
each character cell casts one ray; lambert + a hard specular pick a glyph from
the ramp. frames are deterministic, so they are cached on disk keyed by a hash
of the parameters — the 6-hourly ci run never re-renders them.

frames() -> list of frames, each a list of row strings.
"""

import hashlib
import json
import math
import os

COLS, ROWS = 60, 26
FRAMES = 30
CELL_ASPECT = 0.545          # glyph width / line height (mono 10px on 11px)
RAMP = " .:-=+*#%@"
TILT = 0.22                  # slight downward camera tilt, radians
CACHE = os.path.join(os.path.dirname(__file__), "cache", "spade_frames.json")

PARAMS = dict(cols=COLS, rows=ROWS, frames=FRAMES, aspect=CELL_ASPECT,
              ramp=RAMP, tilt=TILT, v=5)


# ------------------------------------------------------------------ sdf ----

def _circle(px, py, cx, cy, r):
    return math.hypot(px - cx, py - cy) - r


def _triangle(px, py, a, b, c):
    """exact 2d triangle sdf (after iq)."""
    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1])

    def dot(p, q):
        return p[0] * q[0] + p[1] * q[1]

    p = (px, py)
    e0, e1, e2 = sub(b, a), sub(c, b), sub(a, c)
    v0, v1, v2 = sub(p, a), sub(p, b), sub(p, c)

    def seg(v, e):
        t = max(0.0, min(1.0, dot(v, e) / dot(e, e)))
        return (v[0] - e[0] * t, v[1] - e[1] * t)

    q0, q1, q2 = seg(v0, e0), seg(v1, e1), seg(v2, e2)
    s = 1.0 if e0[0] * e2[1] - e0[1] * e2[0] > 0 else -1.0
    dist = min(dot(q0, q0), dot(q1, q1), dot(q2, q2))
    side = min(s * (v0[0] * e0[1] - v0[1] * e0[0]),
               s * (v1[0] * e1[1] - v1[1] * e1[0]),
               s * (v2[0] * e2[1] - v2[1] * e2[0]))
    return -math.sqrt(dist) if side > 0 else math.sqrt(dist)


def _smin(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * 0.25


def _spade2d(x, y):
    x = abs(x)                                   # symmetric about y
    lobe = _circle(x, y, 0.43, -0.06, 0.47)
    point = _triangle(x, y, (-0.86, 0.06), (0.0, 1.12), (0.86, 0.06))
    body = _smin(lobe, point, 0.18)
    stem = _triangle(x, y, (-0.36, -1.0), (0.0, -0.05), (0.36, -1.0))
    return _smin(body, stem, 0.10)


def _sdf(x, y, z):
    d = _spade2d(x, y)
    # pillowed depth: thin at the rim, domed toward the middle, so light
    # rolls across the face like poured metal. not an exact sdf — the
    # marcher takes shorter steps to compensate.
    inner = min(1.0, max(0.0, -d) / 0.42)
    h = 0.04 + 0.26 * math.sqrt(inner)           # half depth
    r = 0.03                                     # edge rounding
    wx, wz = d + r, abs(z) - h + r
    return (min(max(wx, wz), 0.0)
            + math.hypot(max(wx, 0.0), max(wz, 0.0)) - r)


# ------------------------------------------------------------- renderer ----

def _render(angle):
    ca, sa = math.cos(angle), math.sin(angle)
    ct, st = math.cos(TILT), math.sin(TILT)
    light = (-0.45, 0.55, -0.70)
    ln = math.sqrt(sum(c * c for c in light))
    light = tuple(c / ln for c in light)

    def world_to_obj(x, y, z):
        # tilt about x, then spin about y
        y, z = y * ct - z * st, y * st + z * ct
        return x * ca + z * sa, y, -x * sa + z * ca

    def f(x, y, z):
        return _sdf(*world_to_obj(x, y, z))

    ch = 2.55 / ROWS
    cw = ch * CELL_ASPECT
    cam_z = -4.0
    rows = []
    for j in range(ROWS):
        row = []
        for i in range(COLS):
            sx = (i + 0.5 - COLS / 2) * cw
            sy = (ROWS / 2 - j - 0.5) * ch
            # pinhole camera; focal == distance, so the frame spans the
            # screen extent at z=0
            dx, dy, dz = sx, sy, -cam_z
            n = math.sqrt(dx * dx + dy * dy + dz * dz)
            dx, dy, dz = dx / n, dy / n, dz / n
            ox, oy, oz = 0.0, 0.0, cam_z
            t, hit = 0.0, False
            for _ in range(140):
                px, py, pz = ox + dx * t, oy + dy * t, oz + dz * t
                d = f(px, py, pz)
                if d < 0.004:
                    hit = True
                    break
                t += d * 0.55
                if t > 8.0:
                    break
            if not hit:
                row.append(" ")
                continue
            e = 0.003
            nx = f(px + e, py, pz) - f(px - e, py, pz)
            ny = f(px, py + e, pz) - f(px, py - e, pz)
            nz = f(px, py, pz + e) - f(px, py, pz - e)
            nn = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            nx, ny, nz = nx / nn, ny / nn, nz / nn
            diff = max(0.0, (nx * light[0] + ny * light[1] + nz * light[2]))
            # specular: reflect the view ray, compare with the light
            dn = dx * nx + dy * ny + dz * nz
            rx, ry, rz = dx - 2 * dn * nx, dy - 2 * dn * ny, dz - 2 * dn * nz
            spec = max(0.0, (rx * light[0] + ry * light[1] + rz * light[2])) ** 18
            lum = min(1.0, 0.10 + 0.70 * diff + 0.55 * spec)
            row.append(RAMP[1 + int(lum * (len(RAMP) - 2) + 0.5)])
        rows.append("".join(row).rstrip())
    return rows


def frames():
    key = hashlib.sha1(json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()
    try:
        with open(CACHE, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("key") == key:
            return cached["frames"]
    except (OSError, ValueError):
        pass

    out = [_render(2 * math.pi * k / FRAMES) for k in range(FRAMES)]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump({"key": key, "frames": out}, fh)
    print(f"[ok] rendered {FRAMES} spade frames -> {CACHE}")
    return out


if __name__ == "__main__":
    fr = frames()
    print("\n".join(fr[2]))
