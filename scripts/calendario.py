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
HANDOUTS = {'2026-09-29':('Introduzione','dispensa/introduzione.pdf')}
with (ROOT/'_data/calendario.csv').open(encoding='utf-8',newline='') as f:
    events = sorted(csv.DictReader(f),key=lambda row:row['data'])
materials = json.loads((ROOT/'_data/slides.json').read_text(encoding='utf-8'))
exercises = json.loads((ROOT/'_data/esercizi.json').read_text(encoding='utf-8'))
slides = {}
for material in materials:
    for day in material['dates']:
        if day in slides: raise ValueError('Materiali duplicati per una lezione.')
        slides[day] = material
dates = [date.fromisoformat(row['data']) for row in events]
if len(dates)!=len(set(dates)):
    raise ValueError('Il calendario contiene due righe con la stessa data.')
lesson_dates = [d for row,d in zip(events,dates) if row['lezione']=='si']
if set(slides)-{d.isoformat() for d in lesson_dates}:
    raise ValueError('Una data delle slide non corrisponde a una lezione.')
if set(exercises)-{d.isoformat() for d in lesson_dates}:
    raise ValueError('Una data degli esercizi non corrisponde a una lezione.')

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
    symbol={'preparazione':'book','slides':'easel','dispensa':'file-earmark-pdf','esercizi':'file-earmark-pdf'}[kind]
    glyph=f'<span class="bi bi-{symbol}" aria-hidden="true"></span>'
    label=escape(label,quote=True)
    if href:return f'<a class="material-icon" href="{escape(href,quote=True)}" aria-label="{label}" title="{label}">{glyph}</a>'
    return f'<span class="material-icon unavailable" role="img" aria-label="{label}" title="{label}">{glyph}</span>'
def table(headers,rows):
    lines=['| '+' | '.join(headers)+' |','| '+' | '.join([':---']*len(headers))+' |']
    lines+=['| '+' | '.join(cell.replace('|','&#124;') for cell in row)+' |' for row in rows]
    return '\n'.join(lines)+'\n'

def calendar_table(rows):
    names = ['Data','Argomento','Preparazione','Slides','Dispensa','Esercizi visti in classe','Compiti e scadenze']
    classes = ['data','argomento','preparazione','slides','dispensa','esercizi','compiti']
    lines = ['```{=html}', '<table class="table course-calendar">', '<thead><tr>']
    lines += [f'<th id="cal-{cls}" scope="col">{name}</th>' for cls,name in zip(classes,names)]
    lines += ['</tr></thead>', '<tbody>']
    keys = [row['data'] for row in events]
    for index,cells in enumerate(rows):
        lines.append(f'<tr data-date="{keys[index]}">')
        for col,(cls,cell) in enumerate(zip(classes,cells)):
            rowspan = 1
            material = slides.get(keys[index]) if col == 3 else None
            if material:
                if index and slides.get(keys[index-1]) is material: continue
                while index+rowspan < len(rows) and slides.get(keys[index+rowspan]) is material:
                    rowspan += 1
            span = f' rowspan="{rowspan}"' if rowspan > 1 else ''
            lines.append(f'<td class="{cls}-cell" headers="cal-{cls}"{span}>{cell}</td>')
        lines.append('</tr>')
    lines += ['</tbody></table>', '```', '']
    return '\n'.join(lines)

calendar, presentations, entries = [],[],[]
for row,day in zip(events,dates):
    key=row['data'];date_text=full_date(day)
    if row['provvisoria']=='si':date_text+='<br><span class="tentative">da confermare</span>'
    topic=escape(row['argomento'])
    for group,reading in groups(row):
        topic+=f'<span class="presentation-group">Gruppo {group}: {italic(reading)}</span>'
        presentations.append([date_text,group,reading])
    preparation=icon('preparazione','Preparazione non disponibile')
    material=slides.get(key)
    target = None
    label = f'Slide — {full_date(day)} — non disponibili'
    if material:
        target = material['files'][0]['href'] if len(material['files']) == 1 else f"lezioni.html#{material['id']}"
        label = f"Materiali — {material['title']}"
    slide=icon('slides',label,target)
    name,pdf=HANDOUTS.get(key,('Dispensa non disponibile',None))
    handout=icon('dispensa',name,pdf)
    exercise_links=' '.join(icon('esercizi',file['text'],file['href']) for file in exercises.get(key,[]))
    due=[]
    if key == "2026-10-05":
        due.append('<a href="https://forms.gle/uiVe4Yv5rFTqnxkk8">Scadenza per l’iscrizione al lavoro di gruppo.</a>')
    if key == "2026-10-14":
        due.append('Termine per comunicare gli scambi di data tra gruppi e i nominativi del referente per le comunicazioni e del responsabile dell’organizzazione.')
    for presentation in deadlines[day]:
        numbers=' e '.join(group for group,_ in groups(presentation))
        due.append('<span class="deadline"><span class="deadline-icon" aria-hidden="true">💬</span> '
                   f'Postare sul blog domande per i gruppi {numbers}.</span>')
    calendar.append([date_text,topic,preparation,slide,handout,exercise_links,'<br>'.join(due)])
    if material and key == material['dates'][0]:
        lesson_rows = [event for event in events if event['data'] in material['dates']]
        dates_text = ' e '.join(full_date(date.fromisoformat(event['data'])) for event in lesson_rows) + ' 2026'
        heading = material['title']
        if len(lesson_rows) == 1:
            heading += '. ' + lesson_rows[0]['argomento']
            topics = ''
        else:
            topics = '\n\n'.join(f"{full_date(date.fromisoformat(event['data']))}: {event['argomento']}" for event in lesson_rows)
        links = '\n'.join(f"- [{file['text']}]({file['href']})" for file in material['files'])
        for event in lesson_rows:
            for file in exercises.get(event['data'],[]):
                links += f"\n- [{file['text']}]({file['href']})"
        if len(lesson_rows) == 1 and key in HANDOUTS:
            links += f"\n- [Dispensa: {name}]({pdf})"
        entries.append(f"::: {{.lesson-entry}}\n::: {{.lesson-date}}\n{dates_text}\n:::\n\n## {heading} {{#{material['id']}}}\n\n{topics}\n\n{links}\n\n:::\n")
includes=ROOT/'_includes';includes.mkdir(exist_ok=True)
for name,content in {
 'calendario.md':calendar_table(calendar),
 'presentazioni.md':table(['Data','Gruppo','Letture assegnate'],presentations),
 'lezioni.md':'\n'.join(entries),
}.items():(includes/name).write_text(content,encoding='utf-8')
print(f'Calendario: {len(events)} righe, {len(lesson_dates)} incontri, {len(presentations)} gruppi, {sum(map(len,deadlines.values()))} scadenze.')
