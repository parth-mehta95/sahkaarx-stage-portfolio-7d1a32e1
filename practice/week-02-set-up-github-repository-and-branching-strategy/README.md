# Task Manager CLI

A robust Command Line Interface (CLI) application for managing tasks, tracking deadlines, and organizing projects efficiently.

---

## 📌 Repository Overview & Branching Strategy

To maintain high code quality, facilitate team collaboration, and guarantee production stability, this repository follows a structured **Git Flow** branching model.

```
 [main] ---------------------------● (v1.0.0 release) -------● (v1.0.1 hotfix)
   │                               ▲                         ▲
   │                               │                         │
 [develop] ---●-------------●------● (release/1.0.0)         │
              │             ▲                                │
   [feature]  └──●───────●──┘ (PR: squash & merge)           │
                                                             │
   [hotfix]   ───────────────────────────────────────────────┘
```

---

## 🌳 Branch Hierarchy & Roles

### 1. Permanent Branches

| Branch | Protection | Default | Description |
| :--- | :---: | :---: | :--- |
| `main` | **Yes (Protected)** | No | Contains production-ready code. Direct pushes and force pushes are strictly disabled. Changes only enter via approved release/hotfix PRs. |
| `develop` | Recommended | **Yes** | Active development & integration branch. All feature branches branch off and merge into `develop`. This is the default target for all daily PRs. |

### 2. Supporting (Temporary) Branches

| Branch Prefix | Source Branch | Target Branch | Purpose & Lifecycle |
| :--- | :--- | :--- | :--- |
| `feature/<name>` | `develop` | `develop` | New functionality or user stories. Deleted after PR is merged. |
| `bugfix/<name>` | `develop` | `develop` | Non-critical defect fixes found during development. |
| `hotfix/<name>` | `main` | `main` & `develop` | Critical production issues requiring immediate patch. |
| `release/<version>`| `develop` | `main` & `develop` | Preparation for a production release (version bumping, final QA). |

---

## 🏷️ Naming Conventions

All branch names must be lowercase and use kebab-case with descriptive ticket or feature tags:

```text
feature/TMC-101-add-task-priority
feature/task-search-filter
bugfix/TMC-204-fix-date-parsing
hotfix/TMC-911-crash-on-empty-db
release/v1.0.0
```

### Commit Message Standard (Conventional Commits)
All commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short description>

Examples:
- feat(tasks): add priority flag to task creation
- fix(storage): handle missing JSON database file gracefully
- docs(readme): update branching and contribution guidelines
- test(cli): add unit tests for task completion command
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.

---

## 🔄 Pull Request (PR) Workflow

### 1. Opening a Pull Request
1. Branch off the latest `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/TMC-101-add-task-priority
   ```
2. Commit your changes with meaningful commit messages.
3. Push your feature branch:
   ```bash
   git push -u origin feature/TMC-101-add-task-priority
   ```
4. Open a Pull Request targeting **`develop`** as the base branch.

### 2. PR Review Checklist
Every PR must satisfy the following checklist before merge:
- [ ] Base branch is set to `develop` (or `main` for hotfixes).
- [ ] PR title follows the Conventional Commit standard.
- [ ] Description clearly explains the *why* and *what* of the change.
- [ ] Code passes all existing and new unit tests.
- [ ] Code has been self-reviewed and linted.
- [ ] At least **1 peer code review approval** has been received.

### 3. Merge Policy
- **Feature/Bugfix to `develop`**: Use **Squash and Merge** to maintain a clean, linear commit history on `develop`.
- **Release/Hotfix to `main`**: Use **Create a Merge Commit** to preserve full release history and tag semantic versions.
- Always delete the head branch after merging.

---

## 🛡️ GitHub Branch Protection Configuration

To guarantee code integrity, the following branch protection rules are configured on GitHub under **Settings > Branches**:

### Rule Pattern: `main`
- **Require a pull request before merging**: Enabled
  - **Require approvals**: At least `1` approval required.
  - **Dismiss stale pull request approvals when new commits are pushed**: Enabled.
- **Require status checks to pass before merging**: Enabled (if CI/tests are configured).
- **Require conversation resolution before merging**: Enabled.
- **Do not allow bypassing the above settings**: Enabled (enforced on administrators).
- **Allow force pushes**: Disabled.
- **Allow deletions**: Disabled.

---

## 🚀 Quick Reference: Common Git Commands

### Start a New Feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Keep Feature Branch Up-to-Date with `develop`
```bash
git checkout feature/your-feature-name
git fetch origin
git rebase origin/develop
# Resolve any conflicts if prompted, then git rebase --continue
```

### Emergency Hotfix
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix
# Commit fix...
git push -u origin hotfix/critical-bug-fix
# Open PR against 'main', and once approved/merged, cherry-pick/merge into 'develop'
```

---

## 📋 Project Deliverables & Submission Info

- **Repository**: Public GitHub Repository
- **Default Branch**: `develop`
- **Protected Branch**: `main`
- **Repository URL**: `https://github.com/<your-username>/task-manager-cli`