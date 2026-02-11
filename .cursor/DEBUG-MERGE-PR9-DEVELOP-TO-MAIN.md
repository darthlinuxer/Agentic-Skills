# Debug: Why can't I merge PR #9 (develop → main)?

## 1. Symptom

- PR #9 "Develop to main" is open but cannot be merged.
- `gh pr merge 9` fails.

## 2. Information Gathered

- **gh pr merge 9** output:
  ```
  X Pull request #9 is not mergeable: the merge commit cannot be cleanly created.
  To have the pull request merged after all the requirements have been met, add the `--auto` flag.
  Run the following to resolve the merge conflicts locally:
    gh pr checkout 9 && git fetch origin main && git merge origin/main
  ```
- **GitHub API** (`/repos/.../pulls/9`): `mergeable: false`, `mergeable_state: "dirty"`.
- **Reproduced locally:** Ran `gh pr checkout 9`, `git fetch origin main`, `git merge origin/main` → **merge failed with many conflicts** (see list below). Then ran `git merge --abort` to restore a clean state.

## 3. Root Cause

**Merge conflicts between `develop` and `main`.**  
Both branches have diverged: `main` has commits (e.g. v.1.0.1) and `develop` has different changes (e.g. "improved skills and agents"). Git cannot create a merge commit automatically because the same files were changed in incompatible ways on both branches. GitHub therefore reports the PR as not mergeable (`mergeable_state: "dirty"`).

## 4. Conflicting Paths (summary)

Conflicts affect many files under `.agent/`, `.claude/`, and `.cursor/` (agents, commands, skills, workflows), plus `README.md`. Examples:

- **.agent:** skills (api-patterns, app-builder, backend-development, brainstorming, deployment-procedures, frontend-design, geo-fundamentals, mcp-builder, mobile-design, nextjs-react-expert, nodejs-best-practices, performance-profiling, python-patterns, research, seo-fundamentals, testing-patterns, vulnerability-scanner, web-design-guidelines), workflows (deploy, docs, enhance, plan, refactor, test, ui-ux-pro-max).
- **.claude:** agents (agent-orchestrator, explorer-agent), commands (deploy, docs, test, ui-ux-pro-max), scripts/README.md, skills (same pattern as .agent), add/add conflict in agent-orchestrator and scripts/README.
- **.cursor:** agents (backend-specialist, code-archaeologist, database-architect, debugger, devops-engineer, documentation-writer, explorer-agent, frontend-specialist, game-developer, mobile-developer, orchestrator, penetration-tester, performance-optimizer, product-manager, project-planner, security-auditor, seo-specialist, test-engineer), verifier (add/add), commands (brainstorm, create, debug, deploy, docs, enhance, fix, implement, orchestrate, plan, refactor, review, test, ui-ux-pro-max), rules/entry-point.mdc (add/add), skills (same pattern plus gemini, mcp-builder, web-design-guidelines, writing-skills/anthropic-best-practices), writing-skills/examples/LLM_MD_TESTING.md (modify/delete), README.md.
- **Rename/delete:** .cursor/skills/gemini/SKILL.md, .cursor/skills/mcp-builder/SKILL.md, .cursor/skills/web-design-guidelines/SKILL.md, writing-skills/examples (CLAUDE_MD_TESTING → LLM_MD_TESTING).

## 5. Fix Options

### Option A – Resolve conflicts on `develop` (recommended if you want to keep develop → main)

1. Check out the PR branch and merge `main` into it:
   ```bash
   gh pr checkout 9
   git fetch origin main
   git merge origin/main
   ```
2. Resolve every conflict (edit conflicted files, remove `<<<<<<<`, `=======`, `>>>>>>>`, keep or combine content as intended).
3. For rename/delete conflicts: decide whether to keep the file, delete it, or keep both and rename; then `git add` or `git rm` as appropriate.
4. After all conflicts are resolved:
   ```bash
   git add .
   git commit -m "Merge origin/main into develop"
   git push origin develop
   ```
5. PR #9 will become mergeable; then run:
   ```bash
   gh pr merge 9
   ```
   (or merge via the GitHub UI.)

### Option B – Merge on GitHub after resolving elsewhere

- Resolve conflicts in a different branch (e.g. a `develop-merge-main` branch), push that branch, then either:
  - Change PR #9’s head to that branch, or
  - Open a new PR from that branch into `main` and merge it.

### Option C – Close PR #9 and merge another way

- If you prefer to bring `develop` into `main` via a different strategy (e.g. rebase develop onto main in a new branch and open a new PR), close PR #9 and use that new branch for the PR.

## 6. Prevention

- Keep long-lived branches (e.g. `develop`) in sync with `main` regularly: e.g. `git checkout develop && git fetch origin main && git merge origin/main` (or rebase), then push.
- Merge or rebase from `main` before opening a PR so the PR stays mergeable and conflict resolution is smaller and more frequent.
