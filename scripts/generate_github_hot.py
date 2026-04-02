#!/usr/bin/env python3
from datetime import timedelta
from pathlib import Path

from auto_digest_common import (
    DOCS,
    TZ,
    choose_daily_report_date,
    ensure_dir,
    format_date_cn,
    github_search_repositories,
    normalize_text,
    write_lines,
    write_section_index,
)

SECTION_DIR = DOCS / 'github-hot'
LIMIT = 20


def stem_to_title(stem: str) -> str:
    year, month, day = stem.split('-')
    return f'{year}年{month}月{day}日 GitHub 热门项目'


def main():
    ensure_dir(SECTION_DIR)
    report_date = choose_daily_report_date()
    since = (report_date - timedelta(days=7)).strftime('%Y-%m-%d')
    query = f'created:>{since} stars:>20 archived:false'
    repos = github_search_repositories(query, per_page=LIMIT)

    title = f'{format_date_cn(report_date)} GitHub 热门项目'
    generated_at = report_date.astimezone(TZ).strftime('%Y-%m-%d %H:%M:%S')
    target = SECTION_DIR / f"{report_date.strftime('%Y-%m-%d')}.md"

    lines = [
        '---',
        f'title: {title}',
        f'description: {title}，整理近期最受关注的 GitHub 项目。',
        '---',
        '',
        f'# {title}',
        '',
        f'> 生成时间：{generated_at}（Asia/Shanghai）',
        '>',
        '> 口径说明：默认抓取近 7 天创建、按 star 排序靠前的 GitHub 项目，适合快速浏览近期值得关注的新仓库。',
        '',
        '## 今日速览',
        '',
    ]

    for idx, repo in enumerate(repos, start=1):
        full_name = normalize_text(repo.get('full_name'))
        lang = normalize_text(repo.get('language')) or '未标注'
        stars = int(repo.get('stargazers_count') or 0)
        lines.append(f'{idx}. **{full_name}**（{lang} · ★ {stars}）')

    lines.extend(['', '## 详细整理', ''])

    for idx, repo in enumerate(repos, start=1):
        full_name = normalize_text(repo.get('full_name'))
        desc = normalize_text(repo.get('description')) or '暂无简介。'
        lang = normalize_text(repo.get('language')) or '未标注'
        stars = int(repo.get('stargazers_count') or 0)
        url = normalize_text(repo.get('html_url'))
        updated = normalize_text(repo.get('updated_at'))
        lines.extend([
            f'### {idx}. {full_name}',
            '',
            f'- 语言：{lang}',
            f'- Stars：{stars}',
            f'- 最近更新：{updated}',
            f'- 简介：{desc}',
            f'- 链接：[{full_name}]({url})',
            '',
        ])

    lines.extend([
        '## 备注',
        '',
        '- 来源：GitHub Search API',
        f'- 查询口径：`{query}`',
        '- 排序方式：按 star 降序，取前 20 个结果',
        '',
    ])
    write_lines(target, lines)

    write_section_index(
        SECTION_DIR,
        'GitHub 热门项目',
        [
            '这里会每天自动更新一篇 GitHub 热门项目汇总。',
            '',
            '- 标题格式：`YYYY年MM月DD日 GitHub 热门项目`',
            '- 默认口径：近 7 天创建、按 star 排序的热门新仓库',
            '',
            '> 适合快速了解近期值得关注的开源项目。',
        ],
        stem_to_title,
    )

    print(report_date.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
