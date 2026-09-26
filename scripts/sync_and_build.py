#!/usr/bin/env python3
"""
Sync upstream updates from https://github.com/sunface/rust-course and rebuild ebooks.
"""

import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
UPSTREAM_URL = "https://github.com/sunface/rust-course.git"

def run_git(args, check=True):
    res = subprocess.run(["git"] + args, cwd=ROOT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and res.returncode != 0:
        print(f"Git command failed: git {' '.join(args)}")
        print(res.stderr)
        sys.exit(res.returncode)
    return res

def ensure_upstream_remote():
    res = run_git(["remote", "-v"], check=False)
    if "upstream" not in res.stdout:
        print(f"[INFO] Adding upstream remote: {UPSTREAM_URL} ...")
        run_git(["remote", "add", "upstream", UPSTREAM_URL])
    else:
        print("[INFO] Upstream remote already configured.")

def sync_upstream():
    ensure_upstream_remote()
    print("[INFO] Fetching latest updates from upstream/main ...")
    run_git(["fetch", "upstream"])

    # Check differences
    diff_check = run_git(["rev-list", "HEAD..upstream/main", "--count"], check=False)
    count = int(diff_check.stdout.strip()) if diff_check.returncode == 0 and diff_check.stdout.strip().isdigit() else 0

    if count > 0:
        print(f"[INFO] Found {count} new commit(s) in upstream/main. Merging...")
        merge_res = run_git(["merge", "upstream/main", "-m", "Merge upstream updates from sunface/rust-course"], check=False)
        if merge_res.returncode != 0:
            print("[WARN] Merge conflict detected! Please resolve conflicts manually before rebuilding.")
            print(merge_res.stdout)
            print(merge_res.stderr)
            sys.exit(1)
        print("[OK] Merge successful!")
        return True
    else:
        print("[INFO] Up to date with upstream/main. No new commits found.")
        return False

def main():
    force_build = "--force" in sys.argv or "-f" in sys.argv
    has_updates = sync_upstream()

    if has_updates or force_build:
        print("\n🚀 Triggering ebook rebuild...")
        build_script = ROOT_DIR / "scripts" / "build_ebooks.py"
        res = subprocess.run([sys.executable, str(build_script)] + [arg for arg in sys.argv[1:] if arg not in ("--force", "-f")], cwd=ROOT_DIR)
        sys.exit(res.returncode)
    else:
        print("\n💡 Tips: Upstream has no new changes. If you wish to rebuild anyway, run:")
        print("   python scripts/sync_and_build.py --force")
        print("   or directly:")
        print("   python scripts/build_ebooks.py")

if __name__ == "__main__":
    main()
