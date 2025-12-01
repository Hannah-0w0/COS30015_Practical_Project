import pandas as pd
import folium
import os

# 1. CONFIGURATION
# We look for the CSV inside the 'Results' folder
input_csv = os.path.join("CSV_Results", "trace_results.csv")
output_map = os.path.join("CSV_Results", "attacker_map.html")

# 2. LOAD DATA
try:
    df = pd.read_csv(input_csv)
except FileNotFoundError:
    print(f"Error: Could not find {input_csv}.")
    print("Did you run '1_trace_spam.py' first?")
    exit()

# 3. COORDINATES DICTIONARY (Shortcuts for main countries)
country_coords = {
    "United States": [37.0902, -95.7129],
    "China": [35.8617, 104.1954],
    "Japan": [36.2048, 138.2529],
    "Taiwan": [23.6978, 120.9605],
    "Korea": [35.9078, 127.7669],
    "Russia": [61.5240, 105.3188],
    "Germany": [51.1657, 10.4515],
    "France": [46.2276, 2.2137],
    "Canada": [56.1304, -106.3468],
    "India": [20.5937, 78.9629],
    "Argentina": [-38.4161, -63.6167],
    "Brazil": [-14.2350, -51.9253],
    "United Kingdom": [55.3781, -3.4360],
    "Italy": [41.8719, 12.5674],
    "Netherlands": [52.1326, 5.2913]
}

# 4. GENERATE MAP
m = folium.Map(location=[20, 0], zoom_start=2)

print("Generating Map...")
count = 0

# Filter out bad data
df = df[df['Country'].notna()]
df = df[df['Country'] != "Error"]
df = df[df['Country'] != "Unknown"]

for index, row in df.iterrows():
    country = row['Country']
    ip = row['Source IP']
    
    if country in country_coords:
        lat, lon = country_coords[country]
        
        # Add slight randomness so dots don't stack perfectly
        import random
        lat += random.uniform(-0.5, 0.5)
        lon += random.uniform(-0.5, 0.5)
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            popup=f"IP: {ip}\nISP: {row['ISP']}",
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(m)
        count += 1

# 5. SAVE TO RESULTS FOLDER
m.save(output_map)
print(f"Success! Map saved to: {output_map}")
print(f"Plotted {count} attackers.")