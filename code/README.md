# Sonic City Portrait

An interactive soundscape map of London, built with crowd-sourced noise
measurement data from [NoiseCapture / Noise-Planet](https://noise-planet.org).

**Live site:** *(GitHub Pages link — add once deployed)*  
**Portfolio PDF:** *(add link once submitted)*

---

## Data

`data/london_noise.csv` — 17,661 noise measurement areas across all 32 London
boroughs, extracted from the NoiseCapture United Kingdom dataset (ODbL licence).

Columns: `borough`, `lat`, `lon`, `laeq`, `la50`, `measure_count`,
`first_measure`, `last_measure`

---

## Running locally

Requires the **Live Server** extension in VSCode (or any local HTTP server).
Opening `index.html` directly via `file://` will not work — the CSV fetch
requires a server context.

1. Open the project folder in VSCode
2. Right-click `index.html` → **Open with Live Server**
3. The map opens at `http://127.0.0.1:5500`

---

## Project structure

```
sonic-city/
├── data/
│   └── london_noise.csv      Cleaned NoiseCapture data (London boroughs only)
├── charts/                   Exploratory charts from explore.py
├── index.html                Main map visualisation
├── explore.py                Data exploration script (produces charts/)
└── README.md
```

---

## Development stages

| Step | What was built |
|------|---------------|
| 1    | All data points rendering on a basic Leaflet map |
| …    | *(updated as development continues)* |

---

## Data source & licence

NoiseCapture dataset © Noise-Planet contributors, distributed under the
[Open Database Licence (ODbL)](https://opendatacommons.org/licenses/odbl/).
