"""Genera la tabella e ricalcola le scadenze a partire dal calendario CSV."""

import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "_data/calendario.csv").open(encoding="utf-8", newline="") as stream:
    lessons = list(csv.DictReader(stream))
lessons.sort(key=lambda row: row["data"])
dates = [date.fromisoformat(row["data"]) for row in lessons]
if len(dates) != len(set(dates)):
    raise ValueError("Il calendario contiene due righe con la stessa data.")

deadlines = defaultdict(list)
for row, presentation_date in zip(lessons, dates):
    if not row["gruppi"]:
        continue
    target = presentation_date - timedelta(days=7)
    previous_lessons = [day for day in dates if day <= target]
    if not previous_lessons:
        raise ValueError(f"Nessuna lezione disponibile prima della scadenza per i gruppi {row['gruppi']}.")
    deadlines[max(previous_lessons)].append(row)

weekdays = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
lines = [
    "| Data | Argomento | Letture in preparazione | Scadenze |",
    "|:-----|:----------|:------------------------|:---------|",
]
for row, day in zip(lessons, dates):
    topic = row["argomento"]
    if row["provvisoria"].lower() == "si":
        topic += "<br><span class='tentative'>Presentazione da confermare</span>"
    due = []
    for event in deadlines[day]:
        suffix = " (provvisoria)" if event["provvisoria"].lower() == "si" else ""
        due.append(
            "<span class='deadline'><span class='deadline-icon' aria-hidden='true'>💬</span> "
            f"Domande per i gruppi {event['gruppi']}{suffix}</span>"
        )
    cells = [f"{weekdays[day.weekday()]} {day:%d/%m}", topic, row["letture"], "<br>".join(due)]
    lines.append("| " + " | ".join(cell.replace("|", "&#124;") for cell in cells) + " |")

destination = ROOT / "_includes/calendario.md"
destination.parent.mkdir(exist_ok=True)
destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Calendario: {len(lessons)} lezioni, {sum(map(len, deadlines.values()))} scadenze.")

