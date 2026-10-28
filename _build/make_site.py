"""Generate the BIOS 544 Quarto website skeleton from weeks.py."""
import sys, pathlib, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weeks import WEEKS, UNITS

OUT = pathlib.Path(sys.argv[1])
DSBOX = "https://github.com/rstudio-education/datascience-box/tree/main/course-materials"

def w(path, text):
    p = OUT / path
    # never overwrite a page that has real content (no stub marker left)
    if p.exists() and p.suffix == ".qmd" and "::: stub" not in p.read_text() \
            and not path in ("schedule.qmd", "index.qmd", "project/index.qmd"):
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip())

def nn(n): return f"{n:02d}"
def hw_num(n): return n - 1 if n >= 2 else None  # HW 01 belongs to week 2

def dsbox_link(item):
    folder = "_slides" if item.startswith("u") else "application-exercises"
    return f"[`{item}`]({DSBOX}/{folder}/{item})"

# ---------------------------------------------------------------- _quarto.yml
week_nav = "\n".join(
    f'          - text: "Week {nn(x["n"])}: {x["title"]}"\n            href: weeks/week-{nn(x["n"])}.qmd'
    for x in WEEKS)
w("_quarto.yml", f"""
project:
  type: website
  output-dir: _site
  resources:
    - data/
    - homework/starters/
  render:
    - "*.qmd"
    - "!README.md"
    - "!homework/starters/"
    - "!instructor/"

website:
  title: "BIOS 544: R Programming"
  page-navigation: true
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: syllabus.qmd
        text: Syllabus
      - href: schedule.qmd
        text: Schedule
      - href: project/index.qmd
        text: Project
      - href: resources.qmd
        text: Resources
  sidebar:
    style: docked
    contents:
      - section: "Weeks"
        contents:
{week_nav}
      - section: "Cheat sheets"
        contents: cheatsheets/*.qmd
      - section: "Assignments"
        contents: homework/*.qmd
  page-footer:
    left: "Adapted from [Data Science in a Box](https://datasciencebox.org) (CC BY-SA 4.0)."
    right: "Rollins School of Public Health, Emory University"

format:
  html:
    theme: [cosmo, styles.scss]
    toc: true
    code-copy: true
    code-overflow: wrap

execute:
  freeze: auto
""")

w("styles.scss", """
/*-- scss:defaults --*/
$primary: #012169;   // Emory blue
$link-color: #0033a0;
$font-size-root: 17px;

/*-- scss:rules --*/
.unit-badge { display:inline-block; padding:.15rem .55rem; border-radius:999px;
  font-size:.8rem; font-weight:600; color:#fff; }
.material-links a { margin-right: 1rem; font-weight: 600; }
.stub { border-left: 4px solid #f2a900; background: #fff8e6; padding: .6rem 1rem; }
.cheat-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; margin: 1rem 0 2rem; }
.cheat-card { border: 1px solid #dee2e6; border-top: 4px solid $primary; border-radius: 6px; padding: .75rem 1rem; background: #fff; }
.cheat-card h3 { margin-top: 0; font-size: 1.1rem; color: $primary; }
.cheat-card pre { font-size: .8rem; }
.cheat-card table { font-size: .85rem; }
@media print {
  .cheat-grid { grid-template-columns: 1fr 1fr; gap: .5rem; }
  .cheat-card { break-inside: avoid; }
  #try-it, #try-it ~ *, .callout-tip, .callout-danger, nav, #quarto-sidebar, #quarto-margin-sidebar, footer { display: none !important; }
}
""")

# ---------------------------------------------------------------- home
w("index.qmd", """
---
title: "BIOS 544: R Programming"
subtitle: "Department of Biostatistics and Bioinformatics · Rollins School of Public Health"
toc: false
---

Welcome! This course teaches R for public health data analysis: importing, wrangling,
visualizing, and modeling real health data, and reporting it reproducibly with Quarto
and GitHub.

## How each week works

| Material | What it's for |
|---|---|
| **Slides** | Concepts and live-coding examples from class |
| **Lab** | Guided, in-class practice with a partner |
| **Cheat sheet** | One page of the week's key functions, for reference |
| **Assignment** | Independent practice, due Wednesday 11:59 pm (weeks 2–14) |

Start with the [Schedule](schedule.qmd) to see the whole semester.

## Course units

```{=html}
<p>
<span class="unit-badge" style="background:#6c757d">Hello world</span>
<span class="unit-badge" style="background:#6f42c1">Reproducible research</span>
<span class="unit-badge" style="background:#0d6efd">Exploring data</span>
<span class="unit-badge" style="background:#198754">Making rigorous conclusions</span>
</p>
```

Ethics is woven through the semester: misleading graphs (week 4), privacy (week 7),
and algorithmic bias (week 13).
""")

# ---------------------------------------------------------------- schedule
rows = []
for x in WEEKS:
    uname, ucol = UNITS[x["unit"]]
    hn = hw_num(x["n"])
    hw = f"[HW {nn(hn)}](homework/hw-{nn(hn)}.qmd)" if hn else "—"
    ms = x.get("milestone", "")
    rows.append(f"| {x['n']} | [{x['title']}](weeks/week-{nn(x['n'])}.qmd) | {uname} | {x['data']} | {hw} | {ms} |")
w("schedule.qmd", f"""
---
title: "Schedule"
page-layout: full
tbl-colwidths: [6, 34, 14, 22, 10, 14]
---

Assignments are released with each weekly module and are due the following
**Wednesday at 11:59 pm**.

| Week | Topic | Unit | Data | Assignment | Project |
|---:|---|---|---|---|---|
{chr(10).join(rows)}
""")

# ---------------------------------------------------------------- syllabus / resources
w("syllabus.qmd", """
---
title: "Syllabus"
---

::: stub
Placeholder. Paste the final BIOS 544 Fall 2026 syllabus text here, or link the PDF.
:::

## Grading

| Component | Weight |
|---|---|
| Assignments and labs | 60% |
| Final group project | 40% |
""")

w("resources.qmd", """
---
title: "Resources"
---

## Textbook
- [R for Data Science (2e)](https://r4ds.hadley.nz) (required)

## Public health R references
- [The Epidemiologist R Handbook](https://epirhandbook.com/en/index.html)
- [R Cookbook](https://rc2e.com/)
- [R Graphics Cookbook](https://r-graphics.org/)

## Course datasets (R packages)
- `NHANES`: US National Health and Nutrition Examination Survey
- `medicaldata`: teaching datasets from published medical studies
- `mosaicData`: includes the Whickham smoking study
- `tidyr::who2`, `tidyr::population`: WHO tuberculosis surveillance

```r
install.packages(c("tidyverse", "NHANES", "medicaldata", "mosaicData",
                   "janitor", "readxl", "broom", "gtsummary", "rsample"))
```

## Acknowledgement and license
Much of this course is adapted from [Data Science in a Box](https://datasciencebox.org)
by Mine Çetinkaya-Rundel and contributors, licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Adapted materials on this site are shared under the same license.
""")

# ---------------------------------------------------------------- project
mil = "\n".join(f"| {x['n']} | {x['milestone']} |" for x in WEEKS if x.get("milestone"))
w("project/index.qmd", f"""
---
title: "Final group project"
---

Teams of up to 4 complete a public health data analysis from question to reproducible
report. The project is worth 40% of the final grade.

## Milestones

| Week | Milestone |
|---:|---|
{mil}

::: stub
Placeholder. Add the proposal guidelines, dataset suggestions, rubric, and presentation format.
:::
""")

# ---------------------------------------------------------------- per-week files
for x in WEEKS:
    n = x["n"]; k = nn(n)
    uname, ucol = UNITS[x["unit"]]
    hn = hw_num(n)
    topics = "\n".join(f"- {t}" for t in x["topics"])
    objs = "\n".join(f"- {o}" for o in x["objectives"])
    src = "\n".join(f"- {dsbox_link(d)}" for d in x["dsbox"])
    hw_link = f'<a href="../homework/hw-{nn(hn)}.html">Assignment (HW {nn(hn)})</a>' if hn else ""
    ms = f"\n## Project\n\n**{x['milestone']}**\n" if x.get("milestone") else ""

    # week overview page
    w(f"weeks/week-{k}.qmd", f"""
---
title: "Week {n}: {x['title']}"
---

```{{=html}}
<span class="unit-badge" style="background:{ucol}">{uname}</span>
<p class="material-links" style="margin-top:1rem">
<a href="../slides/week-{k}.html">Slides</a>
<a href="../labs/lab-{k}.html">Lab</a>
<a href="../cheatsheets/cheatsheet-{k}.html">Cheat sheet</a>
{hw_link}
</p>
```

## Topics
{topics}

## Learning objectives
By the end of this week you should be able to:

{objs}

## Data
{x['data']}
{ms}
## Adapted from Data Science in a Box
{src}
""")

    # slides (revealjs)
    sections = "\n\n".join(f"# {t}\n\n::: stub\nSlides to come.\n:::" for t in x["topics"])
    w(f"slides/week-{k}.qmd", f"""
---
title: "{x['title']}"
subtitle: "BIOS 544 · Week {n}"
format:
  revealjs:
    slide-number: true
    code-copy: true
    footer: "BIOS 544 · Week {n}"
---

## This week

{objs}

{sections}

## Before next class

- Review the [cheat sheet](../cheatsheets/cheatsheet-{k}.html)
""" + (f"- Start [HW {nn(hn)}](../homework/hw-{nn(hn)}.html)\n" if hn else ""))

    # lab
    w(f"labs/lab-{k}.qmd", f"""
---
title: "Lab {k}: {x['title']}"
---

**Data:** {x['data']}

## Learning goals
{objs}

## Getting started

::: stub
Setup instructions and starter repo link to come.
:::

## Exercises

::: stub
Guided exercises to come.
:::
""")

    # cheat sheet
    cs = "\n\n".join(f"## {c}\n\n::: stub\nTo come.\n:::" for c in x["cheats"])
    w(f"cheatsheets/cheatsheet-{k}.qmd", f"""
---
title: "Cheat sheet {k}: {x['title']}"
toc: false
---

{cs}
""")

    # homework (weeks 2-14)
    if hn:
        w(f"homework/hw-{nn(hn)}.qmd", f"""
---
title: "HW {nn(hn)}: {x['title']}"
subtitle: "Week {n} · due Wednesday 11:59 pm"
---

**Data:** {x['data']}

## What this assignment practices
{objs}

## Instructions

::: stub
Questions to come. Submit the rendered HTML and the .qmd on Canvas.
:::
""")

w("README.md", """
# BIOS 544 course website (Quarto)

- Edit the topic map in `_build/weeks.py`; `_build/make_site.py` regenerates the stub
  pages. Don't rerun it after you start writing real content, because it overwrites the stubs.
- Preview: open `bios544.Rproj` in RStudio, then run `quarto preview` in the Terminal.
- Publish: `quarto publish gh-pages` (GitHub Pages) or `quarto publish quarto-pub`.

Adapted from Data Science in a Box (CC BY-SA 4.0).
""")
w("bios544.Rproj", """
Version: 1.0

RestoreWorkspace: No
SaveWorkspace: No
AlwaysSaveHistory: No

BuildType: Website
""")
w(".gitignore", "_site/\n.quarto/\n.Rproj.user/\n*_files/\ninstructor/\n")
print("done")
