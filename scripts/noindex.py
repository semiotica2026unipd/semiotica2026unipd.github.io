"""Non distribuire la sitemap automatica di un sito che richiede noindex."""
from pathlib import Path

site = Path(__file__).resolve().parents[1] / '_site'
(site / 'sitemap.xml').unlink(missing_ok=True)
