#!/usr/bin/env python3
from datetime import datetime, timedelta

from auto_digest_common import (
    DOCS,
    TZ,
    choose_completed_week_reference,
    ensure_dir,
    format_date_cn,
    github_search_repositories,
    hn_search_by_date,
    normalize_hn_item,
    normalize_text,
    write_lines,
    write_section_index,
)

SECTION_DIR = DOCS / 'weekly'
HN_LIMIT = 10
GH_LIMIT = 10


def stem_to_title(stem: str) -> str:
    year, week = stem.split('-W')
    return f'{year}年第{int(week)}周技术周报'


def fetch_weekly_hn(start_ts: int, end_ts: int) -> list[dict]:
    pool: dict[str, dict] = {}
    for page in range(6):
        hits = hn_search_by_date(start_ts, end_ts, page=page, hits_per_page=100)
        if not hits:
            break
        for raw in hits:
            item = normalize_hn_item(raw)
            if not item['title']:
                continue
            key = item['url'] or item['title']
            old = pool.get(key)
            if old is None or (item['points'], item['comments']) > (old['points'], old['comments']):
                pool[key] = item
    return sorted(pool.values(), key=lambda x: (x['points'], x['comments'], x['created_at_i']), reverse=True)[:HN_LIMIT]


def main():
    ensure_dir(SECTION_DIR)
    reference = choose_completed_week_reference()
    week_start = reference - timedelta(days=reference.weekday())
    week_end = week_start + timedelta(days=6)
    iso_year, iso_week, _ = week_start.isocalendar()
    generated_at = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')

    start_ts = int(week_start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    end_ts = int((week_end.replace(hour=23, minute=59, second=59, microsecond=0)).timestamp())
    since = week_start.strftime('%Y-%m-%d')
    until = week_end.strftime('%Y-%m-%d')

    hn_items = fetch_weekly_hn(start_ts, end_ts)
    gh_items = github_search_repositories(f'created:{since}..{until} stars:>20 archived:false', per_page=GH_LIMIT)

    title = f'{iso_year}年第{iso_week}周技术周报'
    target = SECTION_DIR / f'{iso_year}-W{iso_week:02d}.md'

    lines = [
        '---',
        f'title: {title}',
        f'description: {title}，整理一周内值得关注的技术讨论与开源项目。',
        '---',
        '',
        f'# {title}',
        '',
        f'> 周期：{format_date_cn(week_start)} - {format_date_cn(week_end)}',
        f'> 生成时间：{generated_at}（Asia/Shanghai）',
        '>',
        '> 口径说明：每周汇总一份技术周报，前半部分看技术讨论热度，后半部分看新冒头的开源项目。',
        '',
        '## 本周速览',
        '',
    ]

    for idx, item in enumerate(hn_items[:5], start=1):
        lines.append(f"{idx}. **讨论**：{item['title']}（{item['points']} points）")
    for idx, repo in enumerate(gh_items[:5], start=6):
        full_name = normalize_text(repo.get('full_name'))
        stars = int(repo.get('stargazers_count') or 0)
        lines.append(f'{idx}. **开源**：{full_name}（★ {stars}）')

    lines.extend(['', '## 本周技术讨论', ''])
    for idx, item in enumerate(hn_items, start=1):
        lines.extend([
            f"### {idx}. {item['title']}",
            '',
            f"- 热度：{item['points']} points · {item['comments']} comments",
            f"- 作者：{normalize_text(item['author']) or '未知'}",
            f"- 发布时间：{normalize_text(item['created_at']) or '未知'}",
            f"- 链接：[{item['title']}]({item['url']})",
            '',
        ])

    lines.extend(['## 本周热门开源项目', ''])
    for idx, repo in enumerate(gh_items, start=1):
        full_name = normalize_text(repo.get('full_name'))
        desc = normalize_text(repo.get('description')) or '暂无简介。'
        lang = normalize_text(repo.get('language')) or '未标注'
        stars = int(repo.get('stargazers_count') or 0)
        url = normalize_text(repo.get('html_url'))
        lines.extend([
            f'### {idx}. {full_name}',
            '',
            f'- 语言：{lang}',
            f'- Stars：{stars}',
            f'- 简介：{desc}',
            f'- 链接：[{full_name}]({url})',
            '',
        ])

    lines.extend([
        '## 备注',
        '',
        '- 技术讨论来源：Hacker News Algolia API',
        '- 开源项目来源：GitHub Search API',
        f'- 统计周期：{since} ~ {until}',
        '',
    ])
    write_lines(target, lines)

    write_section_index(
        SECTION_DIR,
        '每周技术周报',
        [
            '这里会按周自动更新技术周报。',
            '',
            '- 标题格式：`YYYY年第WW周技术周报`',
            '- 默认口径：技术讨论热度 + 一周内冒头的开源项目',
            '',
            '> 适合周末或周一快速扫一眼过去一周技术圈发生了什么。',
        ],
        stem_to_title,
    )

    print(f'{iso_year}-W{iso_week:02d}')


if __name__ == '__main__':
    main()
