#!/usr/bin/env python3
import json
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


def fetch_jsonp(url: str, callback: str):
    req = Request(url, headers={'User-Agent': USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        text = resp.read().decode('utf-8', 'ignore')
    m = re.match(rf'{callback}\((.*)\)\s*$', text, re.S)
    if not m:
        raise RuntimeError(f'Unexpected JSONP payload from {url}')
    return json.loads(m.group(1))


def normalize_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text or '').strip()
    return text


def choose_report_date() -> datetime:
    override = __import__('os').environ.get('NEWS_DATE', '').strip()
    if override:
        return datetime.strptime(override, '%Y-%m-%d').replace(tzinfo=TZ)
    now = datetime.now(TZ)
    if now.hour < 1:
        now = now - timedelta(days=1)
    return now


def format_date_cn(dt: datetime) -> str:
    return dt.strftime('%Y年%m月%d日')


def unique_items(items: list, limit: int = 5) -> list:
    seen = set()
    result = []
    for item in items:
        key = normalize_text(item.get('title', ''))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
        if len(result) >= limit:
            break
    return result


def item_block(idx: int, item: dict, section: str) -> str:
    title = normalize_text(item.get('title', ''))
    brief = normalize_text(item.get('brief', ''))
    url = item.get('url', '').strip()
    focus_date = normalize_text(item.get('focus_date', ''))
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

    lines = [
        '---',
        f'title: {title}',
        f'description: {title}，整理国内外 10 条值得关注的热点新闻。',
        '---',
        '',
        f'# {title}',
        '',
        f'> 生成时间：{generated_at}（Asia/Shanghai）',
        '>',
        '> 口径说明：默认整理 **国内 5 条 + 国际 5 条**，来源为央视网公开新闻列表，方便日后回看。',
        '',
        '## 今日速览',
        '',
    ]

    china_items = unique_items(china_items, 5)
    world_items = unique_items(world_items, 5)
    all_items = [(item, '国内') for item in china_items] + [(item, '国际') for item in world_items]
    for idx, (item, section) in enumerate(all_items, start=1):
        lines.append(f'{idx}. **{normalize_text(item.get("title", ""))}**（{section}）')
    lines.extend(['', '## 详细整理', ''])

    idx = 1
    for item in china_items:
        lines.append(item_block(idx, item, '国内'))
        lines.append('')
        idx += 1
    for item in world_items:
        lines.append(item_block(idx, item, '国际'))
        lines.append('')
        idx += 1

    lines.extend([
        '## 备注',
        '',
        '- 国内来源：央视网中国新闻公开列表',
        '- 国际来源：央视网国际新闻公开列表',
        '- 这份页面偏向“每日热点整理”，后续如果你想改成更偏时政、财经、科技，脚本也可以再细分。',
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
        '- **国内 5 条**：来自央视网中国新闻频道公开列表',
        '- **国际 5 条**：来自央视网国际新闻频道公开列表',
        '',
        '> 这是一份适合博客阅读的“每日热点整理”，不是完整新闻数据库。重点是帮你快速回看当天最值得注意的 10 条新闻。',
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
