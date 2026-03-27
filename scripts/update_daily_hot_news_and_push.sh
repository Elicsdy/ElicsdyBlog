#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/vol2/@apphome/trim.openclaw/data/workspace/ElicsdyBlog"
HOME_DIR="/vol2/@apphome/trim.openclaw/data/home"
SSH_CFG="$HOME_DIR/.ssh/config"
KNOWN_HOSTS="$HOME_DIR/.ssh/known_hosts"

export HOME="$HOME_DIR"
export TZ="Asia/Shanghai"
export GIT_SSH_COMMAND="ssh -F $SSH_CFG -o UserKnownHostsFile=$KNOWN_HOSTS -o StrictHostKeyChecking=yes"

cd "$REPO_DIR"

git config user.name "Elicsdy"
git config user.email "2903204554@qq.com"

REPORT_DATE=$(python3 scripts/generate_hot_news.py)

if git diff --quiet -- docs/news; then
  echo "No news changes to commit."
  exit 0
fi

git add docs/news
git commit -m "chore(news): update daily hot news for $REPORT_DATE"
git push origin main

echo "Updated and pushed daily news for $REPORT_DATE"
