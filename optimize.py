import pulp
import geopandas as gpd
from shapely.geometry import Point
import folium
import sqlite3
import os

# Data: Northern CA locations (lat, lon, demand). Refinery=0.
locations = [
    (38.5816, -121.4944, 0),  # Sacramento (depot)
    (37.8044, -122.2711, 1500),  # Oakland
    (37.3382, -121.8863, 1200),  # San Jose
    (37.7749, -122.4194, 1800),  # SF
    (38.1049, -122.2708, 1000),  # Vallejo
    (37.5483, -121.9886, 2000),  # Fremont
    (37.3394, -121.8949, 1400)   # Sunnyvale
]
n = len(locations)
demands = [d for _, _, d in locations]
cap = 5000
dists = [[((locations[i][0]-locations[j][0])**2 + (locations[i][1]-locations[j][1])**2)**0.5 * 111 for j in range(n)] for i in range(n)]  # Approx km

# PuLP model
prob = pulp.LpProblem("Delivery_TSP", pulp.LpMinimize)
prec = pulp.LpVariable.dicts("prec", ((i,j) for i in range(n) for j in range(n) if i != j), cat='Binary')
quant = pulp.LpVariable.dicts("quant", range(1,n), lowBound=0)

# Objective
prob += pulp.lpSum(dists[i][j] * prec[(i,j)] for i in range(n) for j in range(n) if i != j)

# Constraints
for j in range(1,n):
    prob += pulp.lpSum(prec[(i,j)] for i in range(n) if i != j) == 1
    prob += pulp.lpSum(prec[(j,i)] for i in range(n) if i != j) == 1
for i in range(1,n):
    prob += quant[i] <= cap + (demands[i] - cap) * prec[(0,i)]
    for j in range(1,n):
        if i != j:
            prob += quant[j] >= quant[i] + demands[j] - cap + cap * prec[(i,j)] + (cap - demands[j] - demands[i]) * prec[(j,i)]
    prob += quant[i] <= cap
    prob += quant[i] >= demands[i]

prob.solve(pulp.PULP_CBC_CMD(msg=0))  # Silent solve

# Extract route (simple greedy from depot)
route = [0]
curr = 0
while len(route) < n:
    next_node = max((j for j in range(1,n) if j not in route), key=lambda j: pulp.value(prec[(curr,j)]))
    route.append(next_node)
    curr = next_node

# Geospatial: Save to GeoJSON & Folium map
gdf = gpd.GeoDataFrame({'name': [f'Loc{i}' for i in range(n)], 'demand': demands}, geometry=[Point(lon, lat) for lat, lon, _ in locations])
gdf.to_file('routes.geojson', driver='GeoJSON')

m = folium.Map(location=[38.5, -122], zoom_start=8)
for i, row in gdf.iterrows():
    folium.Marker(row.geometry.coords[0], popup=f"{row['name']} demand: {row['demand']}").add_to(m)
folium.PolyLine([(locations[i][1], locations[i][0]) for i in route], color='red').add_to(m)  # lat lon
m.save('map.html')
print("Route:", route)
print("Total dist:", pulp.value(prob.objective))