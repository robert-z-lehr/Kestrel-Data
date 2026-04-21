# [Kestrel Data](https://robert-z-lehr.github.io/Kestrel-Data/)

This repository is set up to support a GitHub Pages map of Kestrel heat-stress sessions.

## Repository layout

- `index.html` — static Leaflet map for GitHub Pages
- `data/session_summary.csv` — processed session summary table
- `data/sessions.geojson` — map-ready point layer used by the page
- `scripts/build_kestrel_pages.py` — processing script
- `notebooks/kestrel_pages_export.ipynb` — notebook version of the processing workflow
- `.nojekyll` — prevents GitHub Pages from applying Jekyll processing

## WORKFLOW:

1. Put raw Kestrel CSV files into:

```text
data/raw/
```

2. Run either:

- the notebook: `notebooks/kestrel_pages_export.ipynb`, or
- the script: `python scripts/build_kestrel_pages.py`

The processing will:

1. read all Kestrel CSV files in `data/raw/`
2. extract session coordinates from the `Location coordinates` field
3. compute session summary statistics
4. write:
   - `data/session_summary.csv`
   - `data/sessions.geojson`

3. Upload to GitHub Pages

Recommended Pages setting:

- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/ (root)`

After Pages is enabled, the site should be available at:

```text
https://robert-z-lehr.github.io/Kestrel-Data/
```
