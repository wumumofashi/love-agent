#!/usr/bin/env python3
"""WeChat environment check for the customer onboarding step 1.
Reports facts only; never fakes a connected state."""
import json, platform, sys

def main() -> int:
    checks = {"platform": platform.system(), "python": sys.version.split()[0]}
    checks["is_windows"] = platform.system() == "Windows"
    try:
        import wxauto  # noqa
        checks["wxauto_installed"] = True
        checks["wxauto_version"] = getattr(wxauto, "__version__", "unknown")
    except Exception as e:
        checks["wxauto_installed"] = False
        checks["wxauto_error"] = str(e)
    checks["ready_for_live_wechat"] = bool(checks["is_windows"] and checks["wxauto_installed"])
    checks["next_step"] = ("Start WeChat (logged in), then run adapters/wechat/runner.py --chat <name> --mode confirm"
                           if checks["ready_for_live_wechat"] else
                           "Needs a Windows machine with WeChat logged in and wxauto installed (pip install wxauto; wxauto4 for WeChat 4.x). Until then use suggest/confirm analysis only.")
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
