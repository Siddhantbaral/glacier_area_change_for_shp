import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import numpy as np
from PIL import Image
import rasterio
from rasterio.plot import show
from matplotlib.collections import LineCollection
from shapely.geometry import LineString
from matplotlib.colors import LinearSegmentedColormap

def load_shapefiles(directory, scenarios, years):
    """
    Loads glacier shapefiles for each scenario and year from the directory.
    Reprojects each to EPSG:4326 if necessary.
    """
    shapefiles = {}
    for scenario in scenarios:
        shapefiles[scenario] = []
        for year in years:
            filepath = os.path.join(directory, f"glaciers_{scenario}_{year}.shp")
            if os.path.exists(filepath):
                gdf = gpd.read_file(filepath)
                # Reproject to EPSG:4326 if not already
                if gdf.crs is None or gdf.crs.to_string() != "EPSG:4326":
                    gdf = gdf.to_crs(epsg=4326)
                shapefiles[scenario].append(gdf)
                print(f"{filepath}: {gdf.shape[0]} features loaded")
            else:
                print(f"File not found: {filepath}")
                shapefiles[scenario].append(None)
    return shapefiles

def load_river_shapefile(river_path):
    """
    Loads the river shapefile and reprojects it to EPSG:4326.
    """
    river_gdf = gpd.read_file(river_path)
    if river_gdf.crs is None or river_gdf.crs.to_string() != "EPSG:4326":
        river_gdf = river_gdf.to_crs(epsg=4326)
    return river_gdf

def load_dem(dem_path):
    """
    Opens the DEM using rasterio.
    Assumes the DEM is in EPSG:4326 and warns if it's not.
    """
    src = rasterio.open(dem_path)
    if src.crs.to_string() != "EPSG:4326":
        print("Warning: DEM is not in EPSG:4326. Please reproject externally.")
    return src

def plot_glaciers(glaciers, year, scenario, ax, dem_src):
    """
    Plots the DEM in the background using a custom colormap,
    overlays glacier polygons as a solid blue fill (with no boundary stroke),
    and sets fixed axis limits based on the DEM.
    """
    # Define a custom colormap for the DEM using your chosen colors:
    # yellow, green, pink and saddlebrown.
    dem_cmap = LinearSegmentedColormap.from_list("DEM Colors", ["yellow", "green", "pink", "saddlebrown"])
    
    # Plot DEM using the custom colormap.
    show(dem_src, ax=ax, cmap=dem_cmap)
    dem_bounds = dem_src.bounds

    # Plot glacier polygons as a solid blue fill without any boundary stroke.
    if glaciers is not None and not glaciers.empty:
        glaciers.plot(ax=ax, color='blue', alpha=1.0, edgecolor='none')
    else:
        print("No glacier geometries to plot for this scenario/year.")
    
    # Fix axes based on DEM bounds.
    ax.set_xlim(dem_bounds.left, dem_bounds.right)
    ax.set_ylim(dem_bounds.bottom, dem_bounds.top)
    
    # Set axis labels with styled fonts.
    ax.set_xlabel("Longitude", fontsize=14, fontweight='bold')
    ax.set_ylabel("Latitude", fontsize=14, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=12, width=2, length=6, direction='in', pad=10)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontweight('bold')
    
    # Define legend items.
    glacier_patch = plt.Line2D([0], [0], color='blue', lw=4, label='Glacier Area')
    river_patch = plt.Line2D([0], [0], color='deepskyblue', lw=2, label='Karnali River')
    ax.legend(handles=[glacier_patch, river_patch], loc='upper right')

def animate_river(river_gdf, ax):
    """
    Sets up the river animation by extracting a LineString from the river data,
    splitting it into segments, and returning an update function to adjust segment colors.
    """
    river_line = river_gdf.geometry.iloc[0]
    if not isinstance(river_line, LineString):
        print("Error: River geometry is not a LineString")
        return None

    coords = np.array(river_line.coords)
    segments = np.concatenate([coords[:-1, None], coords[1:, None]], axis=1)
    lc = LineCollection(segments, cmap='Blues', linewidth=2)
    ax.add_collection(lc)

    def update(frame):
        n_segments = int((frame / 100) * len(segments))
        colors = np.zeros(len(segments))
        if n_segments > 0:
            colors[:n_segments] = np.linspace(0.5, 1, n_segments)
        lc.set_array(colors)
        return lc,
    
    return update

def create_animation(shapefiles, scenarios, years, output_file, dem_path, river_path):
    """
    For each scenario and year, generates a figure with the DEM, glacier data, and river.
    Captures 100 frames per scene (using the river color update) and combines them into a GIF.
    """
    dem_src = load_dem(dem_path)
    river_gdf = load_river_shapefile(river_path)
    
    images = []
    for scenario in scenarios:
        for year, glaciers in zip(years, shapefiles[scenario]):
            fig, ax = plt.subplots(figsize=(12, 12))
            plot_glaciers(glaciers, year, scenario, ax, dem_src)
            # Plot the river layer in deepskyblue.
            river_gdf.plot(ax=ax, color='deepskyblue', linewidth=2)
            
            # Use a larger title for beautiful presentation.
            title = f"Glacier Area Change - Basin Name\nScenario: {scenario.upper()}, Year: {year}"
            fig.suptitle(title, fontsize=24, fontweight='bold', y=0.87)
            
            # Adjust layout so the title does not overlap.
            plt.tight_layout(rect=[0, 0, 1, 0.92])
            
            # Set up river animation.
            update = animate_river(river_gdf, ax)
            frames = []
            for i in range(100):  # Generate 100 frames for the animation.
                update(i)
                fig.canvas.draw()
                image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                frames.append(image)
            
            images.extend(frames)
            plt.close(fig)
    
    # Resize all captured images to ensure consistent dimensions.
    max_shape = max(image.shape[:2] for image in images)
    resized_images = []
    for image in images:
        img = Image.fromarray(image)
        img = img.resize(max_shape[::-1], Image.Resampling.LANCZOS)
        resized_images.append(np.array(img))
    
    imageio.mimsave(output_file, resized_images, fps=60, loop=0)
    print(f"Animation saved to {output_file}")

if __name__ == "__main__":
    input_directory = r'C:\glacier_shp'
    output_animation = r'C:\glacier_shp\animation.gif'
    dem_path = r"C:\glacier_shp\dem.tif"
    river_path = r"C:\glacier_shp\rivers.shp"
    years = [2024, 2050, 2075, 2100]
    scenarios = ['ssp245', 'ssp585']
    
    shapefiles = load_shapefiles(input_directory, scenarios, years)
    create_animation(shapefiles, scenarios, years, output_animation, dem_path, river_path)
