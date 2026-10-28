# BIOS 544: R Programming — course website

Quarto website for BIOS 544 (Rollins School of Public Health, Emory University).
Adapted from [Data Science in a Box](https://datasciencebox.org) (CC BY-SA 4.0); this site is shared under the same license.

**Live site:** https://xpf100.github.io/bios544_r/

## Layout
- `weeks/`: one overview page per week (topics, objectives, data, links)
- `slides/`: Quarto revealjs decks (`live-revealjs` where a deck has "Your turn" boxes)
- `labs/`, `cheatsheets/`: [Quarto Live](https://github.com/r-wasm/quarto-live) pages, where R runs in the browser via webR
- `homework/`: plain Quarto pages; students complete the `starters/` .qmd in RStudio
- `data/`: datasets shipped with the site (used by the live pages)
- `_build/weeks.py`: the 14-week topic map; `_build/make_site.py` regenerates stub pages and never overwrites a finished page

## Working on it
- Preview: open `bios544.Rproj` in RStudio and run `quarto preview` in the Terminal (needs R with knitr, rmarkdown, dplyr)
- Publish: `quarto publish gh-pages`
- Answer keys live in a local `instructor/` folder, which is git-ignored so keys never become public

## Exercise conventions (labs and slide "Your turn" boxes)
- Every exercise prompt ends with a **Use:** box (`::: {.use-box}`) naming the exact column names, values (with quotes for text), functions, and new column names, so students never need the codebook open.
- Every exercise has a hint, a solution, and a check block with targeted feedback for common mistakes.
- No clock-time questions (24-hour times confuse beginners).
