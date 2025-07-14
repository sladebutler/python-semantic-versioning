import subprocess
import re
import os
import sys
import json

def git(cmd, cwd):
    try:
        return subprocess.check_output(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{cmd}': {e.output.decode().strip()}", file=sys.stderr)
        sys.exit(1)

def sanitize_branch(branch):
    return branch.replace("/", ".").replace(" ", "_")

def print_help():
    help_message = """
Usage: pysemver.py [REPO_PATH]

Arguments:
  REPO_PATH   Path to the Git repository (default: current directory)

Description:
  This script calculates the semantic version of a Git repository based on
  commit messages and tags. It uses the following conventions in commit messages:
    - +semver: breaking or +semver: major  -> Increments the major version
    - +semver: feature or +semver: minor  -> Increments the minor version
    - +semver: fix or +semver: patch      -> Increments the patch version

Environment Variables:
  MAIN_BRANCHES   Comma-separated list of main branches (default: "main,master")
"""
    print(help_message.strip())

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(repo_path):
        print(f"Error: The specified path '{repo_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    version_info = {
        "latest_tag": "0.0.0",
        "commits_since_tag": 0,
        "branch": "unknown",
        "semver": ""
    }

    try:
        version_info["latest_tag"] = git("git describe --tags --abbrev=0", repo_path)
    except Exception:
        version_info["latest_tag"] = "0.0.0"

    try:
        version_info["commits_since_tag"] = int(git(f"git rev-list {version_info['latest_tag']}..HEAD --count", repo_path))
    except Exception:
        version_info["commits_since_tag"] = 0

    try:
        version_info["branch"] = git("git rev-parse --abbrev-ref HEAD", repo_path)
    except Exception:
        version_info["branch"] = "unknown"

    try:
        msgs = git(f"git log {version_info['latest_tag']}..HEAD --pretty=%B", repo_path)
    except Exception:
        msgs = ""

    try:
        maj, mino, pat = map(int, version_info["latest_tag"].lstrip('v').split('.'))
    except ValueError:
        maj, mino, pat = 0, 0, 0

    # Compile regex patterns for better readability
    breaking_change_pattern = re.compile(r'\+semver:\s?(breaking|major)')
    feature_change_pattern = re.compile(r'\+semver:\s?(feature|feat|minor)')
    fix_change_pattern = re.compile(r'\+semver:\s?(fix|patch)')

    if breaking_change_pattern.search(msgs):
        maj += 1
        mino = pat = 0
    elif feature_change_pattern.search(msgs):
        mino += 1
        pat = 0
    elif fix_change_pattern.search(msgs):
        pat += 1
    else:
        pat += 1

    # Configurable list of main branches from an environment variable
    main_branches = os.getenv("MAIN_BRANCHES", "main,master").split(",")

    branch_label = sanitize_branch(version_info["branch"])
    label = ''
    if branch_label not in main_branches:
        label = f"-{branch_label}.{version_info['commits_since_tag']}"
    elif version_info["commits_since_tag"] > 0:
        label = f"+{version_info['commits_since_tag']}"

    version_info["semver"] = f"{maj}.{mino}.{pat}{label}"

    print(json.dumps(version_info, indent=2))

if __name__ == "__main__":
    main()
