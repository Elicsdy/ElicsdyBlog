#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

export TZ="${TZ:-Asia/Shanghai}"

cd "$REPO_DIR"

git config user.name "${GIT_AUTHOR_NAME:-Elicsdy}"
git config user.email "${GIT_AUTHOR_EMAIL:-2903204554@qq.com}"

REPORT_DATE=$(python3 "$SCRIPT_DIR/generate_hot_news.py")

if git diff --quiet -- docs/news; then
  echo "No news changes to commit."
  exit 0
fi

git add docs/news
git commit -m "chore(news): update daily hot news for $REPORT_DATE"
git push "${GIT_REMOTE:-origin}" "HEAD:${GIT_BRANCH:-main}"

echo "Updated and pushed daily news for $REPORT_DATE"
