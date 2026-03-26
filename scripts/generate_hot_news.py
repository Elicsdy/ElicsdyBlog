#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Shanghai')
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
NEWS_DIR = DOCS / 'news'
CHINA_URL = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp'
WORLD_URL = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_1.jsonp'
USER_AGENT = 'Mozilla/5.0 (OpenClaw News Bot)'
TOTAL_LIMIT = 20
FETCH_LIMIT_PER_SOURCE = 24


def fetch_jsonp(url: str, callback: str):
    req = Request(url, headers={'User-Agent': USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        text = resp.read().decode('utf-8', 'ignore')
    m = re.match(rf'{callback}\((.*)\)\s*$', text, re.S)
    if not m:
        raise RuntimeError(f'Unexpected JSONP payload from {url}')
    return json.loads(m.group(1))


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def choose_report_date() -> datetime:
    override = os.environ.get('NEWS_DATE', '').strip()
    if override:
        return datetime.strptime(override, '%Y-%m-%d').replace(tzinfo=TZ)
    now = datetime.now(TZ)
    if now.hour < 1:
        now = now - timedelta(days=1)
    return now


def format_date_cn(dt: datetime) -> str:
    return dt.strftime('%Y年%m月%d日')


def parse_focus_date(text: str) -> datetime:
    text = normalize_text(text)
    if not text:
        return datetime(1970, 1, 1, tzinfo=TZ)
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=TZ)
        except ValueError:
            pass
    return datetime(1970, 1, 1, tzinfo=TZ)


def merge_hot_items(china_items: list, world_items: list, limit: int = TOTAL_LIMIT) -> list:
    merged = []
    for item in china_items[:FETCH_LIMIT_PER_SOURCE]:
        x = dict(item)
        x['section'] = '国内'
        merged.append(x)
    for item in world_items[:FETCH_LIMIT_PER_SOURCE]:
        x = dict(item)
        x['section'] = '国际'
        merged.append(x)

    merged.sort(key=lambda x: parse_focus_date(x.get('focus_date', '')), reverse=True)

    seen = set()
    result = []
    for item in merged:
        key = normalize_text(item.get('title', ''))
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
        if len(result) >= limit:
            break
    return result


def item_block(idx: int, item: dict) -> str:
    title = normalize_text(item.get('title', ''))
    brief = normalize_text(item.get('brief', ''))
    url = item.get('url', '').strip()
    focus_date = normalize_text(item.get('focus_date', ''))
    section = normalize_text(item.get('section', '')) or '未分类'
    lines = [f'### {idx}. {title}', '', f'- 分类：{section}']
    if focus_date:
        lines.append(f'- 发布时间：{focus_date}')
    if brief:
        lines.append(f'- 摘要：{brief}')
    if url:
        lines.append(f'- 链接：[{title}]({url})')
    return '\n'.join(lines)


def write_news_page(report_date: datetime, china_items: list, world_items: list) -> Path:
    title = f'{format_date_cn(report_date)}热点新闻'
    file_name = report_date.strftime('%Y-%m-%d') + '.md'
    target = NEWS_DIR / file_name
    generated_at = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')
    hot_items = merge_hot_items(china_items, world_items, TOTAL_LIMIT)

    lines = [
        '---',
        f'title: {title}',
        f'description: {title}，整理当天最热的 20 条新闻。',
        '---',
        '',
        f'# {title}',
        '',
        f'> 生成时间：{generated_at}（Asia/Shanghai）',
        '>',
        '> 口径说明：默认汇总当天最热的 **20 条新闻**，国内与国际混排展示，并保留分类标记。来源为央视网公开新闻列表，方便日后回看。',
        '',
        '## 今日速览',
        '',
    ]

    for idx, item in enumerate(hot_items, start=1):
        lines.append(f'{idx}. **{normalize_text(item.get("title", ""))}**（{item.get("section", "未分类")}）')
    lines.extend(['', '## 详细整理', ''])

    for idx, item in enumerate(hot_items, start=1):
        lines.append(item_block(idx, item))
        lines.append('')

    lines.extend([
        '## 备注',
        '',
        '- 来源池：央视网中国新闻公开列表 + 央视网国际新闻公开列表',
        '- 排序方式：优先按发布时间混排，去重后取当天最热的 20 条',
        '- 页面中仍保留“国内 / 国际”分类标记，方便快速扫读。',
        ''
    ])
    target.write_text('\n'.join(lines), encoding='utf-8')
    return target


def write_news_index():
    posts = sorted([p for p in NEWS_DIR.glob('*.md') if p.name != 'README.md'], reverse=True)
    lines = [
        '# 热点新闻',
        '',
        '这里会每天自动更新一篇新闻汇总，标题格式固定为：',
        '',
        '- `YYYY年MM月DD日热点新闻`',
        '',
        '默认口径：',
        '',
        '- **当天最热 20 条新闻**：国内与国际混排展示',
        '- 来源池：央视网中国新闻频道公开列表 + 央视网国际新闻频道公开列表',
        '',
        '> 这是一份适合博客阅读的“每日热点整理”，不是完整新闻数据库。重点是帮你快速回看当天最值得注意的 20 条新闻。',
        '',
        '## 最新新闻',
        ''
    ]
    if posts:
        for p in posts[:60]:
            date_text = p.stem
            try:
                dt = datetime.strptime(date_text, '%Y-%m-%d')
                cn = dt.strftime('%Y年%m月%d日') + '热点新闻'
            except ValueError:
                cn = p.stem
            lines.append(f'- [{cn}](/news/{p.stem}.html)')
    else:
        lines.append('- 暂无内容，等第一篇自动生成后会显示在这里。')
    lines.append('')
    (NEWS_DIR / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = choose_report_date()
    china = fetch_jsonp(CHINA_URL, 'china')['data']['list']
    world = fetch_jsonp(WORLD_URL, 'world')['data']['list']
    write_news_page(report_date, china, world)
    write_news_index()
    print(report_date.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
