"""Genera le News datate; la paginazione viene applicata nel browser."""
from datetime import date
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
          'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
news = json.loads((ROOT / '_data/news.json').read_text(encoding='utf-8'))
news.sort(key=lambda item: date.fromisoformat(item['date']), reverse=True)
lines = ['```{=html}', '<div class="course-news">', '<ul id="news-list">']

def inline_links(text):
    """Accetta testo e collegamenti Markdown; tutto il resto è testo letterale."""
    parts, start = [], 0
    for match in re.finditer(r'\[([^\]]+)\]\((https?://[^\s)]+|mailto:[^\s)]+)\)', text):
        parts += [escape(text[start:match.start()]),
                  f'<a href="{escape(match[2], quote=True)}">{escape(match[1])}</a>']
        start = match.end()
    parts.append(escape(text[start:]))
    return ''.join(parts)

for item in news:
    day = date.fromisoformat(item['date'])
    label = f'{day.day} {months[day.month - 1]} {day.year}'
    if 'sections' in item:
        lines.append(f'<li><time datetime="{day.isoformat()}">{label}</time><ul class="news-sections">')
        for section in item['sections']:
            lines.append(f'<li><strong>{escape(section["title"])}</strong><ul>')
            lines += [f'<li>{inline_links(text)}</li>' for text in section['items']]
            lines.append('</ul></li>')
        lines.append('</ul></li>')
    else:
        lines.append(f'<li><time datetime="{day.isoformat()}">{label}</time>: {inline_links(item["text"])}</li>')
lines += ['</ul>', '<button id="news-more" type="button" aria-controls="news-list" hidden>Vedi altre</button>',
          '</div>', '<script src="assets/news.js" defer></script>', '```', '']
(ROOT / '_includes/news.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'News: {len(news)} avvisi datati.')
