# Semiotica e teoria della comunicazione — 2026/27

Sito Quarto con Home (calendario), Overview, Lezioni, Dispensa, Lavoro di gruppo, Esame e Supporto. Il vecchio indirizzo `calendario.html` rimanda alla Home.

## Pubblicazione su GitHub

1. In **Settings → Pages → Build and deployment → Source**, seleziona **GitHub Actions**. La pubblicazione da un branch con Jekyll non genera le pagine dai sorgenti Quarto.
2. Assicurati che su `main` sia presente `.github/workflows/publish.yml`, insieme ai sorgenti e alle risorse del sito.
3. Ogni push su `main` avvia **Actions → Pubblica il sito**. Per avviare la prima pubblicazione dopo il cambio di Source, oppure ripeterla senza nuovi commit, usa **Run workflow** sul branch `main`.
4. Il workflow usa Quarto **1.10.18**, esegue `quarto render` (compreso il ricalcolo del calendario), verifica la presenza dei otto HTML (sette pagine e il reindirizzamento) e pubblica il contenuto di `_site/` su https://semiotica2026unipd.github.io/.

`_quarto.yml` elenca già tutte le pagine. Non occorre generare o caricare manualmente gli HTML nella radice: quelli già presenti non sono la fonte della pubblicazione con questo workflow. Modifica i sorgenti indicati sotto; `_site/` viene generata durante ogni esecuzione e non deve essere aggiunta alla repository.

Questo pacchetto sostituisce la precedente versione con menu orizzontale. Se l'avevi caricata, sovrascrivi i file con lo stesso nome; `programma.qmd`, `materiali.qmd` e `presentazioni.qmd` non fanno più parte del sito e possono essere eliminati.

## Modificare i contenuti

Apri il file su GitHub, premi la matita, modifica il testo e premi **Commit changes**. Con GitHub Pages configurato come sopra, ogni modifica su `main` rigenera e pubblica automaticamente tutte le pagine.

| Contenuto | File da modificare |
|---|---|
| Home, contatti, ricevimento | `index.qmd` |
| Date, argomenti e letture delle lezioni | `_data/calendario.csv` |
| Testo sopra la tabella del calendario | `index.qmd` |
| Materiali delle lezioni e date associate | `_data/slides.json` |
| News datate, dalla più recente | `_data/news.json` |
| Elenco dei capitoli della dispensa | `dispensa.qmd` |
| PDF pubblicati | `dispensa/introduzione.pdf` |
| Informazioni sugli appelli | `esame.qmd` |
| Immagine in alto a sinistra | `assets/semiotica.png` |
| Voci del menu | `_quarto.yml` |

## Aggiornare il calendario

In `_data/calendario.csv` ogni riga è una data. `lezione` distingue gli incontri (`si`) dai giorni senza lezione (`no`); `provvisoria` vale `si` soltanto per il 30 novembre. Le coppie `gruppo_1`/`letture_1` e `gruppo_2`/`letture_2` contengono le assegnazioni dei gruppi, utilizzate sia nella Home sia nella pagina Lavoro di gruppo.

Lo script `scripts/calendario.py` calcola le scadenze sette giorni prima di ogni presentazione, anticipandole all'ultima lezione precedente se necessario. I giorni senza lezione sono esclusi dal calcolo. Non modificare direttamente i file generati in `_includes`.

## Inserire le slide

Inserisci in `_data/slides.json` una voce per ciascun insieme di materiali, indicando `id` (univoco), `title`, `dates` (date ISO) e `files` (elenchi di `href` e `text`). Più date consecutive con lo stesso materiale condividono una sola cella Slides nel calendario. Se ci sono più file, l’icona del calendario apre l’entrata nella pagina Lezioni con tutti i collegamenti; con un solo file apre direttamente quel file. I file sono conservati in `materiali/` e vanno elencati anche nelle risorse di `_quarto.yml` e nei controlli del workflow.

## Aggiornare le News

Aggiungi una voce con `date` (formato `AAAA-MM-GG`) e `text` in `_data/news.json`. `scripts/news.py` ordina gli avvisi dalla data più recente e genera `_includes/news.md`. La Home mostra tre avvisi, poi altri cinque a ogni clic su “Vedi altre”. Il pulsante scompare quando tutti gli avvisi sono visibili; senza JavaScript sono visibili tutti. Non modificare il file generato.

## Dispensa

Della dispensa è distribuita soltanto l’Introduzione. Gli altri PDF sono conservati in una copia di lavoro esterna alla cartella del sito. Per pubblicare un nuovo capitolo, reinserisci il PDF in `dispensa/`, aggiorna `HANDOUTS` in `scripts/calendario.py`, la lista `resources` in `_quarto.yml`, l'indice `dispensa.qmd` e il controllo dei PDF nel workflow.

I file `_includes/calendario.md`, `_includes/presentazioni.md` e `_includes/lezioni.md` sono generati: modifica il CSV e il JSON, non questi file.

## Anteprima

Apri `anteprima/index.html` nel pacchetto estratto. È la versione già generata con Quarto; i file da modificare e caricare sono quelli della cartella `sito`.

Per lavorare localmente con la stessa versione usata dal workflow, installa Quarto 1.10.18: `quarto preview` per l'anteprima e `quarto render` per rigenerare il sito. Python 3 serve a ricalcolare la tabella; su GitHub Actions è già disponibile.

I caratteri Open Sans e Noto Emoji sono distribuiti con le rispettive licenze nella cartella `assets`.

Il testo sulla valutazione è condiviso fra Esame e Lavoro di gruppo tramite `_includes/valutazione.md`.
