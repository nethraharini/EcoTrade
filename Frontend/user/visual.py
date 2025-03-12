import folium
import geopandas as gpd

# Load GeoJSON file
geojson_path = "TN.geojson"  # Make sure this file contains only TN districts
gdf = gpd.read_file(geojson_path)

# Print available fields to verify correct district column
print(gdf.columns)

# Use the correct district name field (update if different in your file)
district_field = "district"

# Find Tamil Nadu's bounding box (so we only show TN)
minx, miny, maxx, maxy = gdf.total_bounds
m = folium.Map(location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=7, tiles=None)

# Add a white background to remove the global map
folium.TileLayer("cartodbpositron", opacity=0).add_to(m)  # Makes background empty

# Add district boundaries (Only Tamil Nadu, rest removed)
folium.GeoJson(
    gdf,
    name="Tamil Nadu Districts",
    style_function=lambda feature: {
        "fillColor": "transparent",  # Keep TN transparent
        "color": "black",  # Border color
        "weight": 1.5,  # Border thickness
        "fillOpacity": 0.1  # Slight visibility of TN area
    },
    tooltip=folium.GeoJsonTooltip(fields=[district_field], aliases=["District: "])  # Hover to show district name
).add_to(m)

# Save the map
m.save("visual.html")
print("Tamil Nadu map saved as TN_visualization.html")
