# makefun-news-image-20261120-v2

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/syachrielsd/makefun-news-image-20261120-v2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/syachrielsd/makefun-news-image-20261120-v2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

THE WORLD TODAY — Friday 20 November 2026. One 1024×1024 PNG front page
summing up the world's news of Friday 20 November 2026 (UTC), second
version. All 50 verified stories of the day are on the page, and every
story is marked how sure it is, with its source: CONFIRMED where two or
more independent named sources carry it, REPORTED where a single source
or the wires carry it. Three illustrated leads (Cyclone Akvan's landfall
in Odisha, the global market rout, Trump teasing a "historic" noon press
conference), ten illustrated mid stories with two-line titles, briefs
14–50, a world map with stories 1–14 pinned, a UTC timeline strip, and a
DATE CHECK box that lists the stories left out — an ICJ ruling, the
Shenzhen peace declaration, Anthropic's Nasdaq debut, the Pete Rose
pardon, the Senate Iran war-powers vote and the Tbilisi explosion — each
with the 19 November date that excluded it. Nothing on the page is from
any other day. `render.py` draws the page deterministically with PIL at
build time and writes `entry.png` (1024×1024, ~749 KB); `main.py` is a
stdlib-only copy-only entrypoint that hands the committed `entry.png`
from its own directory to `MAKEFUN_OUTPUT_DIR`. Full story list with
sources and tags: STORIES.md.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=72mse6nm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
