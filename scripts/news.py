"""Genera le News datate; la paginazione viene applicata nel browser."""
from datetime import date
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
          'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
news = json.loads((ROOT / '_data/news.json').read_text(encoding='utf-8'))
news.sort(key=lambda item: date.fromisoformat(item['date']), reverse=True)
lines = ['```{=html}', '<div class="course-news">', '<ul id="news-list">']
for item in news:
    day = date.fromisoformat(item['date'])
    label = f'{day.day} {months[day.month - 1]} {day.year}'
    lines.append(f'<li><time datetime="{day.isoformat()}">{label}</time>: {escape(item["text"])}</li>')
lines += ['</ul>', '<button id="news-more" type="button" aria-controls="news-list" hidden>Vedi altre</button>',
          '</div>', '<script src="assets/news.js" defer></script>', '```', '']
(ROOT / '_includes/news.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'News: {len(news)} avvisi datati.')
