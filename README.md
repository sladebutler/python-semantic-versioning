# PySemVer

PySemVer is a small Python tool that creates a semantic version number from your Git repository.

It looks at your latest Git tag, number of commits since the tag, branch name, and commit messages to build a version like `1.2.4-feature.new-ui.3`.

## Prerequisites

- Python 3.x installed
- `pip` for managing Python packages
- `jq` installed for JSON parsing (optional, for script usage)

## What it does

- Finds the most recent tag like `1.2.3`
- Counts commits since that tag
- Formats the branch name
- Uses commit messages to bump versions:
  - `+semver: major`
  - `+semver: minor`
  - `+semver: patch`
- Outputs the result as JSON

## Example Output

```json
{
  "latest_tag": "1.2.3",
  "commits_since_tag": 5,
  "branch": "feature/new-ui",
  "semver": "1.2.4-feature.new-ui.5"
}
```

## How to use it
 
1. Install dependencies by running:

```bash
pip install -r requirements.txt
```

2. Navigate to the folder containing `pysemver.py`.  
3. In the terminal, run:

```bash
python pysemver.py /path/to/repo
```

If you omit the path, it uses the current folder.

## Using it in a script

```bash
SEM_VER=$(python pysemver.py . | jq -r .semver)
echo $SEM_VER
```

## Notes

- Tags should be in `x.y.z` format.
- If there are no tags, it starts from `0.0.0`.
- Works best with commit messages that follow semantic versioning hints.
