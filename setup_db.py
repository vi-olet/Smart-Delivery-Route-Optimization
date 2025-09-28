import sqlite3
import geopandas as gpd

conn = sqlite3.connect('delivery.db')
gdf = gpd.read_file('routes.geojson')
# Convert geometry to text (lon, lat) for simplicity
gdf['lon'] = gdf.geometry.x
gdf['lat'] = gdf.geometry.y
gdf[['name', 'demand', 'lon', 'lat']].to_sql('routes', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
print("DB created: delivery.db")