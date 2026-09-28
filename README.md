# Semiotica e teoria della comunicazione — 2026/27

Sito Quarto con cinque pagine: Home, Calendario, Lezioni, Dispensa ed Esame.

## Pubblicazione su GitHub

1. Apri la repository `semiotica2026unipd/semiotica2026unipd.github.io`.
2. In **Settings → Pages → Build and deployment → Source**, scegli **GitHub Actions**.
3. In **Code → Add file → Upload files**, carica il contenuto della cartella `sito` del pacchetto, compresa `.github`. Non caricare lo ZIP, la cartella contenitore, `anteprima` o `immagini`.
4. Su Mac, **Cmd + Maiusc + punto** mostra la cartella nascosta `.github`.
5. Premi **Commit changes**. La scheda **Actions** mostra l'avanzamento di “Pubblica il sito”. Quando è concluso, il sito è disponibile su https://semiotica2026unipd.github.io/.

Se `.github` non viene caricata, usa **Add file → Create new file**, inserisci come nome `.github/workflows/publish.yml` e incolla il contenuto del file omonimo del pacchetto.

Questo pacchetto sostituisce la precedente versione con menu orizzontale. Se l'avevi caricata, sovrascrivi i file con lo stesso nome; `programma.qmd`, `materiali.qmd` e `presentazioni.qmd` non fanno più parte del sito e possono essere eliminati.

## Modificare i contenuti

Apri il file su GitHub, premi la matita, modifica il testo e premi **Commit changes**. Il sito viene rigenerato e pubblicato automaticamente.

| Contenuto | File da modificare |
|---|---|
| Home, contatti, ricevimento | `index.qmd` |
| Date, argomenti e letture delle lezioni | `_data/calendario.csv` |
| Testo sopra la tabella del calendario | `calendario.qmd` |
| Collegamenti alle slide | `lezioni.qmd` |
| Elenco dei capitoli della dispensa | `dispensa.qmd` |
| PDF dei capitoli | cartella `dispensa` |
| Informazioni sugli appelli | `esame.qmd` |
| Immagine in alto a sinistra | `assets/semiotica.png` |
| Voci del menu | `_quarto.yml` |

## Aggiornare il calendario

In `_data/calendario.csv` ogni riga è una lezione. Le colonne sono `data`, `argomento`, `letture`, `gruppi`, `provvisoria`. Le date hanno formato `2026-10-28`; i campi che contengono virgole vanno racchiusi fra virgolette doppie, come nelle righe esistenti.

`gruppi` è compilato soltanto per gli incontri con presentazioni, per esempio `1–2`. `provvisoria` vale `si` per le date delle presentazioni ancora da confermare.

Le scadenze sono calcolate da `scripts/calendario.py` prima di ogni generazione del sito: sette giorni prima della presentazione; se quel giorno non c'è lezione, viene scelta l'ultima lezione precedente. Dopo una modifica alle date, non occorre spostare a mano le scadenze. Anche gli incontri con presentazioni sono considerati lezioni.

Non modificare direttamente `_includes/calendario.md`, che viene rigenerato dal CSV.

## Inserire le slide

In `lezioni.qmd`, sostituisci `[Da caricare]{.pending}` nella riga desiderata con `[Slide](INDIRIZZO)`, usando l'indirizzo effettivo. Sono predisposte soltanto le lezioni del 29 e del 30 settembre.

## Dispensa

I tredici PDF derivano dal file fornito dal docente: introduzione, capitoli 1–11 e bibliografia. Mantengono l'impaginazione e i numeri di pagina originali. I riferimenti interni a pagine appartenenti a un altro capitolo non sono collegamenti fra file: la bibliografia è disponibile separatamente.

## Anteprima

Apri `anteprima/index.html` nel pacchetto estratto. È la versione già generata con Quarto; i file da modificare e caricare sono quelli della cartella `sito`.

Per lavorare localmente, se Quarto è installato: `quarto preview` per l'anteprima e `quarto render` per rigenerare il sito. Python 3 serve a ricalcolare la tabella; su GitHub Actions è già disponibile.

I caratteri Open Sans e Noto Emoji sono distribuiti con le rispettive licenze nella cartella `assets`.
