"""
build.py — regenerate every profile SVG in one pass.

run locally:   python3 scripts/build.py
run in CI:     same, with GITHUB_TOKEN in the environment for higher rate limits.
"""

import sys
import gen_hero
import gen_stats
import gen_ops
import gen_contrib


def main():
    print("== rebuilding profile assets ==")
    for name, mod in [("hero", gen_hero), ("stats", gen_stats),
                      ("ops", gen_ops), ("contrib", gen_contrib)]:
        try:
            mod.build()
        except Exception as e:  # noqa: BLE001 — never let one panel sink the build
            print(f"[error] {name}: {e}", file=sys.stderr)
            raise
    print("== done ==")


if __name__ == "__main__":
    main()
