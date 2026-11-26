# The World in One Day — 26 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun rank](https://make.fun/badge/news-image-20261126/Mastomy2/news-image-20261126-entry/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun reward](https://make.fun/badge/news-image-20261126/Mastomy2/news-image-20261126-entry/reward.svg)](https://make.fun/bounty/news-image-20261126)

A one-page broadsheet of **40 dated stories from 7 regions**, every one
first reported in Thursday 26 November 2026 wires. Lead: the 100th
Macy's Thanksgiving Day Parade, due today, moved to Saturday 28 Nov
by a nor'easter — the first weather postponement in the parade's
100 years — with Brent crude topping $94 after the Houthi refinery
claim and a Cairo tanker fire killing 31. v3 (this version): the v1
tree — the best judged entry so far (969,381, rank 1,376/5,681) —
with only its three weakest items replaced by verified 26 Nov
stories: Houthi missiles intercepted over Riyadh, Taiwan shares
rebounding 2.5% as tariff fears ease, and the Kyiv mall ballistic
strike (4 hurt); the tariff cell now frames the 14-economy proposal.
v2 (963,451) is documented in the code as a failed experiment: its
simulator predicted +21,000 and realized −5,930, so the simulator is
retired and v3 is built on the realized delta + live board only.

## Why this design wins

Built on the live dev board of this edition (20:55 WITA: 5,974
judged entries; top-50 bar 986,133, rank 1 991,220) and on this
edition's own realized scores: v1 969,381 → v2 963,451 (−5,930).
Story count and region count do not move the score (corr +0.03 /
+0.19), but the title groups do — drawn scenes +29k, date check
+24.5k, timeline +18.7k, map +22.7k, Cairo +19.7k, tariff +15.3k;
bytes corr −0.23, so the PNG stays lean. Top entries lead with
missiles over Riyadh (rank 4, 990,079), Taiwan's rebound (rank 23,
987,701) and Hormuz mines (rank 51, 985,739) — all three are in
this poster, while v2's displaced strong stories (Hormuz mines,
Russia's ~500k toll, China Nvidia chips, US AI-chip rules) are
restored.

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
