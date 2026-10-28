"""Generate the BIOS 544 Quarto website from weeks.py.

Files for each module are named by its slug (slides/<slug>.qmd, labs/<slug>.qmd,
cheatsheets/<slug>.qmd, homework/<slug>.qmd) and never mention week numbers or
due dates. The schedule, week pages, home page, and navigation are the only
places that map modules to weeks; they are regenerated every run.
Module pages are only (re)written while they are still stubs.
"""
import sys, pathlib, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weeks import WEEKS, UNITS, EPI

OUT = pathlib.Path(sys.argv[1])
DSBOX = "https://github.com/rstudio-education/datascience-box/tree/main/course-materials"

def w(path, text, always=False):
    p = OUT / path
    if (not always) and p.exists() and p.suffix == ".qmd" and "::: stub" not in p.read_text():
        return  # finished page: never overwrite
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip())

def nn(n): return f"{n:02d}"

# assignment numbers follow module order (only modules with an assignment)
k = 0
for m in WEEKS:
    if m["assignment"]:
        k += 1; m["hw"] = k
    else:
        m["hw"] = None
BY_SLUG = {m["slug"]: m for m in WEEKS}
def wk(slug): return BY_SLUG[slug]["n"]

def dsbox_link(item):
    folder = "_slides" if item.startswith("u") else "application-exercises"
    return f"[`{item}`]({DSBOX}/{folder}/{item})"

# ---------------------------------------------------------------- _quarto.yml
week_nav = "\n".join(
    f'          - text: "Week {nn(m["n"])}: {m["title"]}"\n            href: weeks/week-{nn(m["n"])}.qmd'
    for m in WEEKS)
cheat_nav = "\n".join(
    f'          - text: "{m["title"]}"\n            href: cheatsheets/{m["slug"]}.qmd' for m in WEEKS)
hw_nav = "\n".join(
    f'          - text: "HW {nn(m["hw"])}: {m["title"]}"\n            href: homework/{m["slug"]}.qmd'
    for m in WEEKS if m["hw"])
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
        contents:
{cheat_nav}
      - section: "Assignments"
        contents:
{hw_nav}
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
""", always=True)

w("styles.scss", always=True, text="""
/*-- scss:defaults --*/
$primary: #012169;   // Emory blue
$link-color: #0033a0;
$font-size-root: 17px;

/*-- scss:rules --*/
.use-box { background: #eef3fb; border-left: 4px solid $primary; border-radius: 4px; padding: .5rem .9rem; margin: .5rem 0 1rem; font-size: .95rem; }
.use-box p, .use-box ul { margin-bottom: 0; }
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
w("index.qmd", f"""
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
| **Slides** | Concepts and live-coding examples from class (open in a new tab) |
| **Lab** | Guided, in-class practice; code runs right in your browser |
| **Cheat sheet** | One page of key functions, for reference |
| **Assignment** | Independent practice in RStudio; due dates are on the [Schedule](schedule.qmd) |

Start with the [Schedule](schedule.qmd) to see the whole semester.

## Course units

```{{=html}}
<p>
<span class="unit-badge" style="background:#6c757d">Hello world</span>
<span class="unit-badge" style="background:#6f42c1">Reproducible research</span>
<span class="unit-badge" style="background:#0d6efd">Exploring data</span>
<span class="unit-badge" style="background:#198754">Making rigorous conclusions</span>
</p>
```

Ethics is woven through the semester: misleading graphs (week {wk("viz-types")}),
privacy (week {wk("dates-cleaning")}), and algorithmic bias (week {wk("logistic-regression")}).
""", always=True)

# ---------------------------------------------------------------- schedule
rows = []
for m in WEEKS:
    uname, ucol = UNITS[m["unit"]]
    hw = f"[HW {nn(m['hw'])}](homework/{m['slug']}.qmd)" if m["hw"] else "—"
    rows.append(f"| {m['n']} | [{m['title']}](weeks/week-{nn(m['n'])}.qmd) | {uname} | {m['data']} | {hw} | {m.get('milestone', '')} |")
w("schedule.qmd", f"""
---
title: "Schedule"
page-layout: full
tbl-colwidths: [6, 34, 14, 22, 10, 14]
---

Each assignment is released with its week's module and is due the following
**Wednesday at 11:59 pm**.

| Week | Topic | Unit | Data | Assignment | Project |
|---:|---|---|---|---|---|
{chr(10).join(rows)}
""", always=True)

# ---------------------------------------------------------------- syllabus / resources
w("syllabus.qmd", """
---
title: "Syllabus"
---

::: stub
Placeholder. Paste the final BIOS 544 syllabus text here, or link the PDF.
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

## Recommended references
- [The Epidemiologist R Handbook](https://epirhandbook.com/en/index.html): R for applied
  epidemiology. Each week page links the chapters that go with that topic. Especially useful:
  - [Transition to R](https://epirhandbook.com/en/new_pages/transition_to_R.html) (coming from SAS, Stata, or Excel)
  - [Common errors](https://epirhandbook.com/en/new_pages/errors.html)
  - [Getting help](https://epirhandbook.com/en/new_pages/help.html)
- [R Cookbook](https://rc2e.com/)
- [R Graphics Cookbook](https://r-graphics.org/)

## Course datasets
- `NHANES`: US National Health and Nutrition Examination Survey
- `medicaldata`: teaching datasets from published medical studies
- `outbreaks`: real outbreak line lists (H7N9 influenza, China 2013; MERS, South Korea 2015)
- `mosaicData`: includes the Whickham smoking study
- `tidyr::who2`, `tidyr::population`: WHO tuberculosis surveillance
- CDC PLACES: county-level chronic disease estimates (provided as CSV files)

```r
install.packages(c("tidyverse", "NHANES", "medicaldata", "outbreaks", "mosaicData",
                   "janitor", "readxl", "broom", "gtsummary", "rsample"))
```

## Acknowledgement and license
Much of this course is adapted from [Data Science in a Box](https://datasciencebox.org)
by Mine Çetinkaya-Rundel and contributors, licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Adapted materials on this site are shared under the same license.
""", always=True)

# ---------------------------------------------------------------- project
mil = "\n".join(f"| {m['n']} | {m['milestone']} |" for m in WEEKS if m.get("milestone"))
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

# ---------------------------------------------------------------- per-module files
for m in WEEKS:
    n, slug = m["n"], m["slug"]
    uname, ucol = UNITS[m["unit"]]
    topics = "\n".join(f"- {t}" for t in m["topics"])
    objs = "\n".join(f"- {o}" for o in m["objectives"])
    src = "\n".join(f"- {dsbox_link(d)}" for d in m["dsbox"])
    epi = "\n".join(f"- [{t}]({EPI}{u})" for t, u in m["epi"])
    epi_sec = f"\n## Further reading: The Epidemiologist R Handbook\n{epi}\n" if epi else ""
    hw_link = f'<a href="../homework/{slug}.html">Assignment (HW {nn(m["hw"])})</a>' if m["hw"] else ""
    ms = f"\n## Project\n\n**{m['milestone']}**\n" if m.get("milestone") else ""

    # week page: the ONLY place a module is tied to a week
    w(f"weeks/week-{nn(n)}.qmd", f"""
---
title: "Week {n}: {m['title']}"
---

```{{=html}}
<span class="unit-badge" style="background:{ucol}">{uname}</span>
<p class="material-links" style="margin-top:1rem">
<a href="../slides/{slug}.html" target="_blank" rel="noopener">Slides &#8599;</a>
<a href="../labs/{slug}.html">Lab</a>
<a href="../cheatsheets/{slug}.html">Cheat sheet</a>
{hw_link}
</p>
```

## Topics
{topics}

## Learning objectives
By the end of this module you should be able to:

{objs}

## Data
{m['data']}
{ms}{epi_sec}
## Adapted from Data Science in a Box
{src}
""", always=True)

    # ---- module files: no week numbers, no due dates ----
    sections = "\n\n".join(f"# {t}\n\n::: stub\nSlides to come.\n:::" for t in m["topics"])
    w(f"slides/{slug}.qmd", f"""
---
title: "{m['title']}"
subtitle: "BIOS 544"
format:
  revealjs:
    slide-number: true
    code-copy: true
    footer: "BIOS 544 · {m['title']}"
execute:
  echo: true
---

## Learning objectives

{objs}

{sections}

## Practice

- [Lab](../labs/{slug}.html)
- [Cheat sheet](../cheatsheets/{slug}.html)
""")

    w(f"labs/{slug}.qmd", f"""
---
title: "Lab: {m['title']}"
---

**Data:** {m['data']}

## Learning goals
{objs}

## Exercises

::: stub
Guided exercises to come. Each exercise gets a **Use:** box naming exact columns and values,
plus a hint, a solution, and a check.
:::
""")

    cs = "\n\n".join(f"## {c}\n\n::: stub\nTo come.\n:::" for c in m["cheats"])
    w(f"cheatsheets/{slug}.qmd", f"""
---
title: "Cheat sheet: {m['title']}"
toc: false
---

{cs}
""")

    if m["hw"]:
        w(f"homework/{slug}.qmd", f"""
---
title: "Assignment: {m['title']}"
---

**Data:** {m['data']}

## What this assignment practices
{objs}

## Instructions

::: stub
Questions to come. Students work in RStudio from a starter .qmd and submit the rendered HTML and the .qmd on Canvas.
:::
""")

w("bios544.Rproj", """
Version: 1.0

RestoreWorkspace: No
SaveWorkspace: No
AlwaysSaveHistory: No

BuildType: Website
""")
w(".gitignore", "_site/\n.quarto/\n.Rproj.user/\n*_files/\ninstructor/\n", always=True)
print("done")
