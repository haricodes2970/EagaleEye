"""`eye` — the command. One word. The hawk answers."""

import sys


def main() -> int:
    import sys

    if "--version" in sys.argv or "-v" in sys.argv:
        from eaglei import __version__

        print(f"eagaleeye {__version__}")
        return 0
    try:
        from eaglei.app import EagleEyeApp
    except ImportError as exc:
        print(f"eaglei: broken install ({exc}); reinstall:\n  pipx install git+https://github.com/haricodes2970/EagaleEye.git", file=sys.stderr)
        return 1
    EagleEyeApp().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
