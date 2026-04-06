#!/usr/bin/env python3
from datetime import datetime, timedelta

from auto_digest_common import (
    DOCS,
    TZ,
    choose_daily_report_date,
    ensure_dir,
    format_date_cn,
    hn_search,
    normalize_hn_item,
    normalize_text,
    write_lines,
    write_section_index,
)

SECTION_DIR = DOCS / 'ai-digest'
AI_KEYWORDS = ['OpenAI', 'Anthropic', 'LLM', 'AI agent', 'MCP', 'Copilot']
DEV_KEYWORDS = ['TypeScript', 'React', 'Docker', 'Kubernetes', 'Postgres', 'Rust']
AI_LIMIT = 10
DEV_LIMIT = 10


def stem_to_title(stem: str) -> str:
    year, month, day = stem.split('-')
    return f'{year}年{month}月{day}日 AI / 开发资讯精选'


def collect_hits(keywords: list[str], start_ts: int, end_ts: int, limit: int, exclude_keys: set[str] | None = None) -> list[dict]:
    pool: dict[str, dict] = {}
    exclude_keys = exclude_keys or set()
    for kw in keywords:
        for raw in hn_search(kw, start_ts, end_ts, hits_per_page=20):
            item = normalize_hn_item(raw)
            if not item['title']:
                continue
            key = item['url'] or item['title']
            if key in exclude_keys:
                continue
            old = pool.get(key)
            if old is None or (item['points'], item['comments']) > (old['points'], old['comments']):
                pool[key] = item
    items = sorted(pool.values(), key=lambda x: (x['points'], x['comments'], x['created_at_i']), reverse=True)
    return items[:limit]


def block(idx: int, item: dict) -> list[str]:
    return [
        f"### {idx}. {item['title']}",
        '',
        f"- 热度：{item['points']} points · {item['comments']} comments",
        f"- 作者：{normalize_text(item['author']) or '未知'}",
        f"- 发布时间：{normalize_text(item['created_at']) or '未知'}",
        f"- 链接：[{item['title']}]({item['url']})",
        '',
    ]


def main():
    ensure_dir(SECTION_DIR)
    report_date = choose_daily_report_date()
    start_dt = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_dt = start_dt + timedelta(days=1)
    start_ts = int(start_dt.timestamp())
    end_ts = int(end_dt.timestamp())
    generated_at = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')

    ai_hits = collect_hits(AI_KEYWORDS, start_ts, end_ts, AI_LIMIT)
    ai_keys = {item['url'] or item['title'] for item in ai_hits}
    dev_hits = collect_hits(DEV_KEYWORDS, start_ts, end_ts, DEV_LIMIT, exclude_keys=ai_keys)

    title = f'{format_date_cn(report_date)} AI / 开发资讯精选'
    target = SECTION_DIR / f"{report_date.strftime('%Y-%m-%d')}.md"

    lines = [
        '---',
        f'title: {title}',
        f'description: {title}，整理 AI 与开发领域值得关注的资讯。',
        '---',
        '',
        f'# {title}',
        '',
        f'> 生成时间：{generated_at}（Asia/Shanghai）',
        '>',
        '> 口径说明：基于 Hacker News 公开搜索接口，按 AI / 开发关键词抓取当天讨论度较高的故事，方便快速扫读。',
        '',
        '## 今日速览',
        '',
    ]

    for idx, item in enumerate((ai_hits[:5] + dev_hits[:5]), start=1):
        lines.append(f"{idx}. **{item['title']}**（{item['points']} points）")

    lines.extend(['', '## AI 资讯精选', ''])
    for idx, item in enumerate(ai_hits, start=1):
        lines.extend(block(idx, item))

    lines.extend(['## 开发资讯精选', ''])
    for idx, item in enumerate(dev_hits, start=1):
        lines.extend(block(idx, item))

    lines.extend([
        '## 备注',
        '',
        '- 来源：Hacker News Algolia API',
        f"- AI 关键词：{', '.join(AI_KEYWORDS)}",
        f"- 开发关键词：{', '.join(DEV_KEYWORDS)}",
        '- 排序方式：按 points / comments 综合排序后取前列',
        '',
    ])
    write_lines(target, lines)

    write_section_index(
        SECTION_DIR,
        'AI / 开发资讯精选',
        [
            '这里会每天自动更新一篇 AI / 开发资讯精选。',
            '',
            '- 标题格式：`YYYY年MM月DD日 AI / 开发资讯精选`',
            '- 默认口径：基于 AI / 开发关键词抓取当天讨论度较高的内容',
            '',
            '> 适合快速看当天值得跟进的 AI / 工具链 / 开发圈话题。',
        ],
        stem_to_title,
    )

    print(report_date.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
