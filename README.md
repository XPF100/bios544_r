# BIOS 544: R Programming — course website

Quarto website for BIOS 544 (Rollins School of Public Health, Emory University).
Adapted from [Data Science in a Box](https://datasciencebox.org) (CC BY-SA 4.0); this site is shared under the same license.

**Live site:** https://xpf100.github.io/bios544_r/

## Layout
- `_build/weeks.py`: the topic map. **The order of this list is the course order.**
- `weeks/week-NN.qmd`, `schedule.qmd`, sidebar: generated; the only places that tie a topic to a week, an assignment number, or a due date
- `slides/<topic>.qmd`: plain revealjs decks (no webR); slide links open in a new tab
- `labs/<topic>.qmd`, `cheatsheets/<topic>.qmd`: [Quarto Live](https://github.com/r-wasm/quarto-live) pages, where R runs in the browser via webR
- `homework/<topic>.qmd`: plain Quarto pages; students complete `homework/starters/<topic>-starter.qmd` in RStudio
- `data/`: datasets shipped with the site (used by the live pages)
- `_build/weeks.py`: the 14-week topic map; `_build/make_site.py` regenerates stub pages and never overwrites a finished page

## Working on it
- Preview: open `bios544.Rproj` in RStudio and run `quarto preview` in the Terminal (needs R with knitr, rmarkdown, dplyr)
- Publish: `quarto publish gh-pages`
- Answer keys live in a local `instructor/` folder, which is git-ignored so keys never become public

## Modularity rules
- Slides, labs, cheat sheets, and assignments never mention week numbers, assignment numbers, due dates, or "next week".
- Files are named by topic, never by week. To reorder the course, reorder `_build/weeks.py` and rerun `python3 _build/make_site.py .`; no module file changes.

## Exercise conventions (labs and slide "Your turn" slides)
- Every exercise prompt ends with a **Use:** box (`::: {.use-box}`) naming the exact column names, values (with quotes for text), functions, and new column names, so students never need the codebook open.
- Lab exercises have a hint, a solution, and a check block with targeted feedback for common mistakes.
- Slide "Your turn" code is static with blanks; the answer and its output appear on the next click.
- No clock-time questions (24-hour times confuse beginners).
