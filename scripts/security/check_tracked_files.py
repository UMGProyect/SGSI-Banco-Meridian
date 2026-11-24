#!/usr/bin/env python3
"""Detect filenames that must never be versioned, including reachable history.
This is a complementary check, not a secret scanner. Output is count-only.
"""
import re
import subprocess
import sys
from pathlib import PurePosixPath


def git(*args):
    return subprocess.check_output(["git", *args])


def forbidden(path):
    p = PurePosixPath(path.lower())
    n = p.name
    if any(part in {".terraform", ".ssh", "secrets", "backups"} for part in p.parts):
        return True
    if any(p.parts[i:i + 2] in {("evidencias", "raw"), ("evidencias", "privadas"), (".config", "gcloud")} for i in range(len(p.parts) - 1)):
        return True
    if n == ".env.example" or n == "terraform.tfvars.example" or n.endswith((".example.tfvars", ".example.tfvars.json")):
        return False
    if n == ".env" or n.startswith(".env."):
        return True
    if n in {"credentials.json", "application_default_credentials.json", "id_rsa", "id_ed25519"}:
        return True
    if re.match(r"^(service-account|gha-creds-).*\.json$", n):
        return True
    if re.search(r"\.tf(state|plan)(\.|$)", n):
        return True
    return n.endswith((".pem", ".key", ".pfx", ".p12", ".jks", ".tfvars", ".tfvars.json", ".sqlite", ".sqlite3", ".db", ".dump", ".bak", ".log", ".pcap", ".pcapng", ".retry"))


def paths(data):
    return {item.decode("utf-8", "surrogateescape") for item in data.split(b"\0") if item}


def main():
    tracked = paths(git("ls-files", "-z"))
    # Inspect actual trees to cover renamed/deleted paths and all reachable refs.
    commits = git("rev-list", "--all", "HEAD").splitlines()
    historical = set()
    for commit in commits:
        historical.update(paths(git("ls-tree", "-r", "-z", "--name-only", commit.decode("ascii"))))
    hits = {p for p in tracked | historical if forbidden(p)}
    print(f"Tracked paths: {len(tracked)}; reachable commits: {len(commits)}; historical paths: {len(historical)}")
    print(f"Blocked paths: {len(hits)}")
    if hits:
        print("FAIL: review prohibited paths locally; no path or secret values emitted in CI.")
        return 1
    print("PASS: filename policy (does not establish absence of secrets).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
