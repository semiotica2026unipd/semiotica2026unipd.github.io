"""Genera Home, entrate delle lezioni e presentazioni dal calendario condiviso."""
import csv
import json
import re
from collections import defaultdict
from datetime import date, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Disponibilità esplicitamente richiesta, senza inferire altri abbinamenti.
HANDOUTS = {'2026-09-29':('Introduzione','dispensa/introduzione.pdf'),
            '2026-09-30':('Capitolo 1','dispensa/capitolo-01.pdf')}
with (ROOT/'_data/calendario.csv').open(encoding='utf-8',newline='') as f:
    events = sorted(csv.DictReader(f),key=lambda row:row['data'])
slides = json.loads((ROOT/'_data/slides.json').read_text(encoding='utf-8'))
dates = [date.fromisoformat(row['data']) for row in events]
if len(dates)!=len(set(dates)):
    raise ValueError('Il calendario contiene due righe con la stessa data.')
lesson_dates = [d for row,d in zip(events,dates) if row['lezione']=='si']
if set(slides)-{d.isoformat() for d in lesson_dates}:
    raise ValueError('Una data delle slide non corrisponde a una lezione.')

def groups(row):
    return [(row[f'gruppo_{i}'],row[f'letture_{i}']) for i in (1,2) if row[f'gruppo_{i}']]

deadlines = defaultdict(list)
for row,day in zip(events,dates):
    if not groups(row):continue
    if day not in lesson_dates:raise ValueError('Presentazione in un giorno senza lezione.')
    prior = [d for d in lesson_dates if d<=day-timedelta(days=7)]
    if not prior:raise ValueError('Nessuna lezione disponibile prima della scadenza.')
    deadlines[max(prior)].append(row)

weekdays=['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica']
months=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
def full_date(day):return f'{weekdays[day.weekday()]} {day.day} {months[day.month-1]}'
def italic(text):return re.sub(r'\*([^*]+)\*',r'<em>\1</em>',escape(text))
def icon(kind,label,href=None):
    symbol={'preparazione':'book','slides':'easel','dispensa':'file-earmark-pdf'}[kind]
    glyph=f'<i class="bi bi-{symbol}" aria-hidden="true"></i>'
    label=escape(label,quote=True)
    if href:return f'<a class="material-icon" href="{escape(href,quote=True)}" aria-label="{label}" title="{label}">{glyph}</a>'
    return f'<span class="material-icon unavailable" role="img" aria-label="{label}" title="{label}">{glyph}</span>'
def table(headers,rows):
    lines=['| '+' | '.join(headers)+' |','| '+' | '.join([':---']*len(headers))+' |']
    lines+=['| '+' | '.join(cell.replace('|','&#124;') for cell in row)+' |' for row in rows]
    return '\n'.join(lines)+'\n'

calendar, presentations, entries = [],[],[]
for row,day in zip(events,dates):
    key=row['data'];date_text=full_date(day)
    if row['provvisoria']=='si':date_text+='<br><span class="tentative">da confermare</span>'
    topic=escape(row['argomento'])
    for group,reading in groups(row):
        topic+=f'<span class="presentation-group">Gruppo {group}: {italic(reading)}</span>'
        presentations.append([date_text,group,reading])
    preparation=icon('preparazione','Preparazione non disponibile')
    slide=icon('slides',f'Slide — {full_date(day)}'+('' if slides.get(key) else ' — non disponibili'),slides.get(key))
    name,pdf=HANDOUTS.get(key,('Dispensa non disponibile',None))
    handout=icon('dispensa',name,pdf)
    due=[]
    for presentation in deadlines[day]:
        numbers=' e '.join(group for group,_ in groups(presentation))
        due.append('<span class="deadline"><span class="deadline-icon" aria-hidden="true">💬</span> '
                   f'Postare sul blog domande per i gruppi {numbers}.</span>')
    calendar.append([date_text,topic,preparation,slide,handout,'<br>'.join(due)])
    if key in ('2026-09-29','2026-09-30') or slides.get(key):
        entries.append(f'''::: {{.lesson-entry}}
::: {{.lesson-date}}
{full_date(day)} 2026
:::

## {row['argomento']}

::: {{.lesson-materials}}
<span>Slides {slide}</span> <span>Dispensa {handout}</span>
:::
:::
''')
includes=ROOT/'_includes';includes.mkdir(exist_ok=True)
for name,content in {
 'calendario.md':table(['Data','Argomento','Preparazione','Slides','Dispensa','Compiti'],calendar),
 'presentazioni.md':table(['Data','Gruppo','Letture assegnate'],presentations),
 'lezioni.md':'\n'.join(entries),
}.items():(includes/name).write_text(content,encoding='utf-8')
print(f'Calendario: {len(events)} righe, {len(lesson_dates)} incontri, {len(presentations)} gruppi, {sum(map(len,deadlines.values()))} scadenze.')
