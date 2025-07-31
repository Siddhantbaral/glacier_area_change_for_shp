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
```

## 🔧 Usage

Adjust input paths and parameters in the `main()` function:
```python
# Example usage
input_shapefile = r'E:\glacier_input\glacier.shp'
output_dir = r'E:\glacier_output'
years = [2024, 2050, 2075, 2100]
reduction_percentages = {
    'ssp245': [23.26, 34.08, 52.43, 60.31],
    'ssp585': [23.08, 33.81, 58.25, 78.96]
}
scenarios = ['ssp245', 'ssp585']
main(input_shapefile, output_dir, reduction_percentages, years, scenarios)
```
## 📁 Output

Shapefiles are saved in the format: glaciers_[scenario]_[year].shp

## 🌍 Glacier Area Change Visualization

Below is a visual illustration showing the modeled terminus retreat based on area reduction:

![Glacier Change](karnali_area_change.gif)

## ✍️ Author

Developed by [Siddhant Baral](https://github.com/Siddhantbaral)

