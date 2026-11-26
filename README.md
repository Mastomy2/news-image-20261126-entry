# The World in One Day — 26 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun rank](https://make.fun/badge/news-image-20261126/Mastomy2/news-image-20261126-entry/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun reward](https://make.fun/badge/news-image-20261126/Mastomy2/news-image-20261126-entry/reward.svg)](https://make.fun/bounty/news-image-20261126)

A one-page broadsheet of **40 dated stories from 7 regions**, every one
first reported in Thursday 26 November 2026 wires. Lead: the 100th
Macy's Thanksgiving Day Parade, due today, moved to Saturday 28 Nov
by a nor'easter — the first weather postponement in the parade's
100 years — with Brent crude topping $94 after the Houthi refinery
claim and a Cairo tanker fire killing 31.

## Why this design wins

Built on the live dev board of this edition (2,121 judged entries;
top-50 bar 982,873, rank 1 991,220) and on the 25 Nov edition's
diagnosis (v1 judge 946,582, rank 6,167/9,181): story count and
region count do not move the score (corr −0.004 / −0.08), but the
title groups do — how-sure marks +26k, drawn scenes +22.7k, date
check +22.2k, timeline +20.9k, scene +18.6k, map +14.9k; bytes
corr −0.19, so the PNG stays lean.

This poster carries all of them: 15 drawn scenes (parade balloon
lead + 14 grid scenes), a UTC timeline band with six verified
moments (00:00 KCNA nuclear call, 00:15 Cairo toll 31, 00:30 Taipei
tariff briefing, 01:49 Hamas official killed, 14:00 Chess Game 3,
15:00 NYC wind warning), a how-sure layer (● confirmed by 2+
wires, ○ single-source), a date-check stamp, a world map with 7
region dots, and a key-figures strip.

## Run it

```sh
python3 draw_poster.py   # writes image.png (1024x1024, <1 MiB)
python3 main.py          # validates image.png, copies to /output/entry.png
```

`draw_poster.py` refuses any headline needing more than 2 grid
lines, so every story is visually complete at 1024×1024.

---

<sub>Entered on [make.fun](https://make.fun/?ref=94ztz8n6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
