# Debug: Why can't I open a PR to develop?

## 1. Symptom

- `gh pr create --base develop` fails.
- Terminal shows: `git checkout -b develop` → `fatal: a branch named 'develop' already exists`.
- Error from `gh`: *"Head sha can't be blank, Base sha can't be blank, No commits between develop and main, Base ref must be a branch (createPullRequest)"*.

## 2. Information Gathered

- **gh auth**: Logged in as `darthlinuxer`, token has `repo`.
- **Branches on GitHub** (from `gh api repos/.../branches` and `git ls-remote origin`):
  - `main`, `feature/simplify`, `cursor/simplifica-o-de-skills-e-agentes-9baf`, `dependabot/pip/pip-d1091effbf`
  - **No `develop` branch on the remote.**
- **Local/remote-tracking**:
  - Local branch `develop` exists (commit `ac2d958`).
  - `git remote show origin`: **"refs/remotes/origin/develop - stale (use 'git remote prune' to remove)"**.
- **git ls-remote origin develop**: (empty) — `develop` is not on the server.
- **Git tip**: `git branch -R` is wrong; correct flag is `-r` (remotes).

## 3. Hypotheses

1. **develop does not exist on GitHub** → gh cannot use it as base (Base ref must be a branch). **CONFIRMED**
2. User ran `git checkout -b develop` while local `develop` already existed → "branch already exists". **CONFIRMED** (use `git checkout develop` to switch, not `-b`).
3. "No commits between develop and main" is a side effect of gh resolving base to a missing/invalid ref. **CONFIRMED** (base branch missing).
4. Stale remote-tracking ref `origin/develop` left after branch was deleted (or never pushed) on GitHub. **CONFIRMED** (`git remote show origin` reports develop as stale).

## 4. Investigation

**Hypothesis 1 (develop missing on GitHub):**  
- `git ls-remote origin develop` → no output.  
- `gh api repos/darthlinuxer/Agentic-Skills/branches` → no `develop`.  
- **Result: CONFIRMED.**

**Hypothesis 2 (checkout -b vs checkout):**  
- Terminal log: `git checkout -b develop` → `fatal: a branch named 'develop' already exists`.  
- **Result: CONFIRMED** — use `git checkout develop` to switch to existing branch.

**Hypothesis 3 & 4:**  
- Explains gh error and stale ref; no further tests needed.

## 5. Root Cause

- **The branch `develop` does not exist on GitHub.** Your local `develop` and remote-tracking `origin/develop` point to a ref that no longer exists on the server (stale).  
- **gh pr create --base develop** fails because the base branch must exist on the remote; GitHub returns errors like "Base ref must be a branch" and "Base sha can't be blank".  
- The "No commits between develop and main" message is a consequence of the invalid base ref, not the main cause.

## 6. Fix

**Option A – Re-create `develop` on GitHub (if you want a develop branch):**

```bash
# Ensure local develop is the branch you want (e.g. from main)
git checkout develop
git merge main --no-edit   # or reset to main: git reset --hard main
# Push and set upstream (creates develop on GitHub)
git push -u origin develop
# Then open PRs to develop as usual, e.g.:
gh pr create --base develop --head feature/simplify --title "Your title" --body "Description"
```

**Option B – Use an existing base branch (e.g. main):**

```bash
# Open PR into main instead
gh pr create --base main --head feature/simplify --title "Your title" --body "Description"
```

**Clean up stale ref (optional):**

```bash
git remote prune origin
# Then: git branch -d develop  only if you no longer need local develop
```

## 7. Prevention

- Before opening a PR to a branch, ensure that branch exists on the remote:  
  `git ls-remote origin <branch>` or `gh api repos/OWNER/REPO/branches`.
- Use `git checkout <branch>` to switch to an existing branch; use `git checkout -b <branch>` only when creating a new one.
- After deleting a branch on GitHub, run `git remote prune origin` so local remote-tracking refs stay in sync.
- Correct flag for listing remote branches: `git branch -r` (lowercase), not `-R`.
