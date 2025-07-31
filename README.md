# Glacier Area Change Simulation using Shapefiles

This Python script models glacier terminus retreat by applying area reduction percentages to existing glacier geometries stored in a shapefile. It supports multiple climate scenarios and future projection years.

## 📍 Use Case

Designed for research or policy analysis where glacier change must be visualized spatially under SSP climate scenarios. Ideal for projects with pre-processed glacier shapefiles and estimated area/volume change data.

## 🧰 Features

- Loads glacier geometries using `GeoPandas`
- Applies area reduction through iterative negative buffering
- Handles multiple scenarios (`ssp245`, `ssp585`) and years (`2050`, `2075`, `2100`)
- Uses `ThreadPoolExecutor` for faster multi-glacier processing
- Outputs adjusted shapefiles per scenario-year combination
- Logs actual vs target area and reduction percentages

## 📦 Requirements

```bash
pip install geopandas numpy tqdm
