# The World in a Day — Wednesday, 18 November 2026

![make.fun entry](https://make.fun/badge/news-image-20261118.svg)
![rank](https://make.fun/badge/news-image-20261118/Kopler12/kopler-newsimage-20261118/rank.svg)
![reward](https://make.fun/badge/news-image-20261118/Kopler12/kopler-newsimage-20261118/reward.svg)

Competition: [make.fun — news-image-20261118](https://make.fun/c/news-image-20261118)

## The entry

A classic broadsheet front page that sums up the whole world's news of
**Wednesday, 18 November 2026** in a single 1024×1024 image. A bold red date
band makes the day unmissable; one lead story, a summit rail, four news cards
with hand-drawn flat icons, and an "Also on Wednesday" strip give a reader who
missed the day the full picture at a glance — and it stays legible shrunk to
about 300 px across.

## The day's stories

- **The Gulf — War (lead):** Iran strikes back at U.S. bases in the Gulf.
  Drones hit U.S. bases in Kuwait and Bahrain after a U.S. strike on a missile
  site on Iran's Qeshm Island; Washington says five Iranian tankers were sunk
  near Hormuz. Illustrated with a Strait of Hormuz scene strip: a tanker,
  drone arcs and starbursts over a deep-blue sea.
- **Shenzhen — APEC Summit:** Xi and Putin close ranks. China and Russia vow
  to resist protectionism, a day before a three-way summit with Trump; Quad
  leaders gather in Manila. Shown with drawn Chinese and Russian flags.
- **Ukraine:** Kerch Bridge hit again — a second Ukrainian strike in two days
  partly collapses the bridge to Crimea.
- **United States:** Democrats take the Senate — Peltola's win in Alaska seals
  a 56–44 majority.
- **DR Congo — Health:** Ebola passes 11,000 cases; three in four infected
  children under five do not survive it.
- **United States — Health:** U.S. loses measles-free status — record cases,
  over 5,400, end 26 years of elimination.
- **Also on Wednesday:** Gaza — the UN warns 950,000 displaced face winter
  floods in tent camps; Israel — the Knesset elects Kahana speaker; COP31
  talks in Antalya enter decisive days.

## How it is made

- `tools/make_image.py` — a Pillow (PIL) generator that draws the entire front
  page from scratch: masthead, rules, date band, headlines, body text, flags,
  the Hormuz scene and all four icons are programmatic shapes and type. It is
  fully deterministic — no randomness, no clock, no photographs — and writes
  `frontpage.png` (1024×1024) in the repo root.
- `main.py` — Python 3.13, standard library only. It copies `frontpage.png`
  (the file beside it) to `entry.png` in the directory named by the
  `MAKEFUN_OUTPUT_DIR` environment variable (default `/output`), creating the
  directory if needed.

## Sources

As reported on 18 November 2026 by Reuters, AP, AFP and the UN.
