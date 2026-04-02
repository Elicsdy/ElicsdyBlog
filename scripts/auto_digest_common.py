#!/usr/bin/env python3
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Shanghai')
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
USER_AGENT = 'Mozilla/5.0 (OpenClaw Blog Automation)'


def fetch_json(url: str, headers: dict | None = None, timeout: int = 30):
    req_headers = {'User-Agent': USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))


def build_url(base: str, **params) -> str:
    return f"{base}?{urlencode(params)}"


def normalize_text(text: str | None) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def format_date_cn(dt: datetime) -> str:
    return dt.strftime('%Y年%m月%d日')


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_lines(path: Path, lines: list[str]):
    path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')


def parse_report_date(env_name: str = 'REPORT_DATE') -> datetime | None:
    import os
    value = os.environ.get(env_name, '').strip()
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=TZ)


def choose_daily_report_date(env_name: str = 'REPORT_DATE') -> datetime:
    override = parse_report_date(env_name)
    if override:
        return override
    now = datetime.now(TZ)
    if now.hour < 1:
        now = now - timedelta(days=1)
    return now


def choose_completed_week_reference(env_name: str = 'REPORT_DATE') -> datetime:
    override = parse_report_date(env_name)
    if override:
        return override
    now = datetime.now(TZ)
    days_back = now.weekday() + 1
    return (now - timedelta(days=days_back)).replace(hour=0, minute=0, second=0, microsecond=0)


def write_section_index(section_dir: Path, title: str, intro_lines: list[str], stem_to_title):
    ensure_dir(section_dir)
    posts = sorted([p for p in section_dir.glob('*.md') if p.name != 'README.md'], reverse=True)
    lines = [f'# {title}', '']
    lines.extend(intro_lines)
    lines.extend(['', '## 最新内容', ''])
    if posts:
        for p in posts[:60]:
            lines.append(f'- [{stem_to_title(p.stem)}](/{section_dir.name}/{p.stem}.html)')
    else:
        lines.append('- 暂无内容，等第一篇自动生成后会显示在这里。')
    lines.append('')
    write_lines(section_dir / 'README.md', lines)


def github_search_repositories(query: str, per_page: int = 20) -> list[dict]:
    url = build_url(
        'https://api.github.com/search/repositories',
        q=query,
        sort='stars',
        order='desc',
        per_page=str(per_page),
    )
    data = fetch_json(url, headers={'Accept': 'application/vnd.github+json'})
    return data.get('items', [])


def hn_search(query: str, start_ts: int, end_ts: int, hits_per_page: int = 20) -> list[dict]:
    url = build_url(
        'https://hn.algolia.com/api/v1/search',
        query=query,
        tags='story',
        hitsPerPage=str(hits_per_page),
        numericFilters=f'created_at_i>{start_ts},created_at_i<{end_ts}',
    )
    data = fetch_json(url)
    return data.get('hits', [])


def hn_search_by_date(start_ts: int, end_ts: int, page: int = 0, hits_per_page: int = 100) -> list[dict]:
    url = build_url(
        'https://hn.algolia.com/api/v1/search_by_date',
        tags='story',
        hitsPerPage=str(hits_per_page),
        page=str(page),
        numericFilters=f'created_at_i>{start_ts},created_at_i<{end_ts}',
    )
    data = fetch_json(url)
    return data.get('hits', [])


def normalize_hn_item(item: dict) -> dict:
    title = normalize_text(item.get('title') or item.get('story_title'))
    url = item.get('url') or item.get('story_url') or f"https://news.ycombinator.com/item?id={item.get('objectID')}"
    return {
        'title': title,
        'url': url,
        'points': int(item.get('points') or 0),
        'comments': int(item.get('num_comments') or 0),
        'author': normalize_text(item.get('author')),
        'created_at': normalize_text(item.get('created_at')),
        'created_at_i': int(item.get('created_at_i') or 0),
    }
