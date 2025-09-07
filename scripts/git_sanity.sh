#!/usr/bin/env bash
# Purpose: make Git repo healthy, normalize eol, and push to GitHub via SSH.
# Why strict: fail fast; avoid silent errors.
set -euo pipefail

log() { printf "\033[1;32m==>\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[warn]\033[0m %s\n" "$*"; }
err()  { printf "\033[1;31m[err ]\033[0m %s\n" "$*"; }

# Ensure we are inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  err "Not inside a Git repository. Run from your project root."
  exit 1
fi

# Repo root
cd "$(git rev-parse --show-toplevel)"

log "Rebuild index & cleanup"
rm -f .git/index || true
# Mixed reset: rebuilds index from HEAD without touching working tree
git reset --mixed

# Repack & GC (safe)
git repack -Ad || true
git gc --aggressive --prune=now || true

# Normalize line endings
if [[ ! -f .gitattributes ]]; then
  printf '* text=auto eol=lf\n' > .gitattributes
  log "Created .gitattributes (LF normalization)"
fi

# Re-index after normalization
# Why: ensure Git re-evaluates text files with new eol rules
git rm -r --cached . >/dev/null 2>&1 || true

log "Stage all changes"
if ! git add -A; then
  err "git add failed. Check unreadable files above."
  exit 1
fi

git status -s || true

# Commit only if there is something staged
if ! git diff --cached --quiet; then
  log "Committing staged changes"
  git commit -m "chore: normalize line endings & repair repo"
else
  warn "No changes to commit"
fi

# Remote setup
USER_GH="${USER_GH:-AKA-founder}"         # change via env if needed
REPO="${REPO:-dj_backend_server}"         # change via env if needed
REMOTE_URL="git@github.com:${USER_GH}/${REPO}.git"

log "Configure remote origin -> ${REMOTE_URL}"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "${REMOTE_URL}"
else
  git remote add origin "${REMOTE_URL}"
fi

# Standardize branch name
log "Ensure branch is 'main'"
git branch -M main

# Optional: test SSH (non-fatal)
warn "SSH check with GitHub (non-fatal). You may be asked to confirm host key."
ssh -T git@github.com || true

# Push upstream
log "Pushing to GitHub"
if ! git push -u origin main; then
  err "Push failed. Ensure the repo '${USER_GH}/${REPO}' exists and your SSH key has access."
  warn "Create repo on GitHub and re-run: git push -u origin main"
  exit 1
fi

log "Done. Repo pushed to ${REMOTE_URL}"

