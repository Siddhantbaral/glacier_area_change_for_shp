import geopandas as gpd
import numpy as np
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def load_shapefile(shapefile_path):
    return gpd.read_file(shapefile_path)

def calculate_target_area(current_area, reduction_percentage):
    return current_area * (1 - reduction_percentage / 100)

def calculate_buffer_size(current_area, target_area):
    area_diff = current_area - target_area
    if area_diff <= 0:
        return 0
    buffer_size = 0
    step_size = 0.001  # Buffer size step in meters
    while True:
        buffered_area = (current_area - buffer_size * step_size)  # Approximation
        if buffered_area <= target_area:
            break
        buffer_size += step_size
    return buffer_size

def apply_shrink_operation(geometry, buffer_size):
    if buffer_size <= 0:
        return geometry
    return geometry.buffer(-buffer_size)

def process_glacier_row(row, target_area_km2):
    current_area_km2 = row.geometry.area / 1e6  # Convert to km²
    tolerance = 0.01  # Tolerance level in km²
    buffer_size = 0.001  # Initial buffer size in meters

    while True:
        shrunk_geom = apply_shrink_operation(row.geometry, buffer_size)
        shrunk_area_km2 = shrunk_geom.area / 1e6  # Convert to km²
        if abs(shrunk_area_km2 - target_area_km2) <= tolerance:
            break
        buffer_size += 0.001  # Increment buffer size

    if not shrunk_geom.is_valid:
        shrunk_geom = shrunk_geom.buffer(0)  # Fix invalid geometries

    return shrunk_geom

def adjust_glacier_terminus(glacier_gdf, target_areas):
    with ThreadPoolExecutor() as executor:
        target_areas_dict = dict(enumerate(target_areas))
        results = list(executor.map(lambda index: process_glacier_row(glacier_gdf.iloc[index], target_areas_dict[index]), range(len(glacier_gdf))))
    
    adjusted_gdf = glacier_gdf.copy()
    adjusted_gdf['geometry'] = results
    return adjusted_gdf

def save_shapefile(gdf, output_path):
    gdf.to_file(output_path)

def main(input_shapefile, output_dir, reduction_percentages, years, scenarios):
    glaciers = load_shapefile(input_shapefile)
    initial_areas_km2 = glaciers.geometry.area / 1e6  # Convert to km²

    for scenario in scenarios:
        for year, reduction_percentage in zip(years, reduction_percentages[scenario]):
            print(f"\nScenario: {scenario}, Year: {year}, Reduction Percentage: {reduction_percentage}")

            target_areas_km2 = [calculate_target_area(area, reduction_percentage) for area in initial_areas_km2]
            
            # Initialize progress bar
            with tqdm(total=len(glaciers), desc=f"Processing {scenario} {year}", unit='glacier') as pbar:
                adjusted_glaciers = adjust_glacier_terminus(glaciers.copy(), target_areas_km2)
                pbar.update(len(glaciers))
            
            # Calculate and print the actual reduction percentages
            actual_areas_km2 = adjusted_glaciers.geometry.area / 1e6  # Convert to km²
            actual_reduction_percentages = ((initial_areas_km2 - actual_areas_km2) / initial_areas_km2) * 100
            
            print("\nResults:")
            for i, (initial, target, actual, reduction) in enumerate(zip(initial_areas_km2, target_areas_km2, actual_areas_km2, actual_reduction_percentages)):
                print(f"Glacier {i+1}:")
                print(f"  Initial area: {initial:.6f} km²")
                print(f"  Target area: {target:.6f} km²")
                print(f"  Actual area: {actual:.6f} km²")
                print(f"  Target reduction: {reduction_percentage:.2f}%")
                print(f"  Actual reduction: {reduction:.2f}%")
                print(f"  Difference: {abs(reduction - reduction_percentage):.2f}%")
            
            output_shapefile = os.path.join(output_dir, f"glaciers_{scenario}_{year}.shp")
            save_shapefile(adjusted_glaciers, output_shapefile)
            print(f"\nSaved shapefile for {scenario} {year} at {output_shapefile}")

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

