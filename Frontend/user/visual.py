from flask import Flask, render_template, send_file
import folium
import geopandas as gpd
import pandas as pd

app = Flask(__name__)

# Load GeoJSON
geojson_path = r"C:\Users\nethr\OneDrive\Desktop\ET\EcoTrade\Frontend\user\TN.geojson"
gdf = gpd.read_file(geojson_path)
district_field = "district"  # Ensure this matches the column in your GeoJSON

# Load CSV data
csv_path = r"C:\Users\nethr\OneDrive\Desktop\ET\EcoTrade\Frontend\user\TN.csv.csv"  # Make sure the CSV is structured correctly
df = pd.read_csv(csv_path)

# Function to generate the folium map
def generate_map(material):
    # Create base TN map
    minx, miny, maxx, maxy = gdf.total_bounds
    m = folium.Map(location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=7, tiles=None)
    folium.TileLayer("cartodbpositron", opacity=0).add_to(m)  # Transparent background
    
    # Filter dataset based on selected material
    material_data = df[df["Material"] == material]
    district_colors = {row["District"]: "red" for _, row in material_data.iterrows()}  # Customize colors
    
    # Add districts
    folium.GeoJson(
        gdf,
        name="Tamil Nadu Districts",
        style_function=lambda feature: {
            "fillColor": district_colors.get(feature["properties"][district_field], "transparent"),
            "color": "black",
            "weight": 1.5,
            "fillOpacity": 0.5 if feature["properties"][district_field] in district_colors else 0.1
        },
        tooltip=folium.GeoJsonTooltip(fields=[district_field], aliases=["District: "])
    ).add_to(m)
    
    return m

# Route to serve the base HTML page
@app.route("/")
def home():
    return render_template("T.html")  # Keep this page as is

# Route to update the map
@app.route("/update_map/<material>")
def update_map(material):
    print(f"Updating map for material: {material}")
    
    # Generate map only (not a full HTML page)
    map_obj = generate_map(material)
    map_obj.save("static/map.html")  # Save updated map

    return "Map updated", 200  # Return status only (no full HTML)

if __name__ == "__main__":
    app.run(debug=True)
