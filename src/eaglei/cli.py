"""`eye` — the command. One word. The hawk answers."""

import sys


def main() -> int:
    try:
        from eaglei.app import EagleEyeApp
    except ImportError as exc:
        print(f"eaglei: broken install ({exc}); reinstall:\n  pipx install git+https://github.com/haricodes2970/EagaleEye.git", file=sys.stderr)
        return 1
    EagleEyeApp().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
