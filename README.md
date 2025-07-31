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
input_shapefile = r'E:\UK_glacier_shp\oggm_filtered_glacier_karnali.shp'
output_dir = r'E:\UK_glacier_shp'
years = [2050, 2075, 2100]
reduction_percentages = {
    'ssp245': [13.94, 47.02, 61.50],
    'ssp585': [19.11, 57.99, 87.71]
}
scenarios = ['ssp245', 'ssp585']
main(input_shapefile, output_dir, reduction_percentages, years, scenarios)
```
## 📁 Output

Shapefiles are saved in the format: glaciers_[scenario]_[year].shp

## ✍️ Author

Developed by [Siddhant Baral](https://github.com/Siddhantbaral)

