## 🌍 Glacier Area Change Simulation using Shapefiles

This Python project models glacier retreat by applying area reduction percentages to glacier geometries across climate scenarios and years.

### 📌 Use Case

Designed for research or policy analysis where glacier change must be visualized spatially under SSP climate scenarios. Ideal for projects with pre-processed glacier shapefiles and estimated area change data.

---

## 🧮 Model Features

- Loads glacier geometries via `GeoPandas`
- Applies area reduction using iterative negative buffering
- Supports multiple scenarios (`ssp245`, `ssp585`) and years (`2024`, `2050`, `2075`, `2100`)
- Accelerates multi-glacier processing with `ThreadPoolExecutor`
- Outputs adjusted shapefiles per scenario-year
- Logs actual vs target area reductions

---

## 🖼️ Glacier Area Change Visualization

This new module creates an animated representation of glacier retreat using SSP scenario overlays. It's based on custom DEM styling and progressive rendering of hydrologic features.

### ✨ Visualization Features

- **GIF Animation** with temporal layers from 2024 to 2100
- **DEM Terrain Styling** with a custom color map
- **Karnali River Flow Animation** in progressive blue tones
- **Frame-rich Rendering** (`fps=60`, 100 frames per scene)
- **Scenario Comparison** in a single loop: `ssp245` vs `ssp585`

### ▶️ How to Run

```bash
python animation_area_change.py
```

Update the following paths inside the script:
- `input_directory`: Folder with glacier shapefiles (`glaciers_[scenario]_[year].shp`)
- `dem_path`: DEM raster (`.tif`)
- `river_path`: Karnali River shapefile (`.shp`)
- `output_animation`: Path to save the output GIF

---

### 📷 Sample Output

<p align="center">
  <img src="docs/glacier_animation_sample.gif" alt="Glacier Animation" width="600"/>
</p>

---

## ✍️ Author

Developed by **Siddhant Baral**

---

