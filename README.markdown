# Smart Delivery Route Optimization

A beginner-friendly project to optimize delivery routes in Northern California using a Python geospatial pipeline, .NET Web API, SQLite database, and ArcGIS Maps SDK frontend.

It solves a **Capacitated Vehicle Routing Problem (VRP)**, adapted from the Mosel example problem `e4deliver.mos` (FICO Xpress Optimization, [link](https://www.fico.com/fico-xpress-optimization/docs/dms2023-04/examples/mosel/ApplBook/GUID-CF8BDC06-20F2-3FAA-A417-014D44B73E7C.html?scroll=e4deliver_mos)), to optimize delivery routes for a tanker truck distributing heating oil from a refinery in Sacramento to six clients in Northern California (Oakland, San Jose, San Francisco, Vallejo, Fremont, Sunnyvale). Built with a Python geospatial pipeline, .NET Web API, SQLite database, and ArcGIS Maps SDK frontend, it minimizes travel distance while respecting vehicle capacity constraints, showcasing the power of optimization in logistics.

## About the Project
This project implements a **Capacitated Vehicle Routing Problem (VRP)**, a generalization of the Traveling Salesman Problem (TSP), inspired by the `e4deliver.mos` example from FICO's Xpress Mosel Applications (March 2002, revised March 2022). It optimizes routes for a single tanker truck (capacity: 5000 units) to deliver oil to six clients with demands of 1000–2000 units (total demand: 7900 units), allowing depot returns for refills. Using **PuLP**, the Python script `optimize.py` formulates a mixed-integer linear program (MILP) with binary variables (`prec[i,j]`) for route sequencing and continuous variables (`quant[i]`) to track delivered quantities, ensuring no subtours (via Miller-Tucker-Zemlin-inspired constraints) and capacity adherence. Distances are computed from real-world coordinates (e.g., Sacramento at 38.5816, -121.4944) using Euclidean metrics scaled to kilometers. The solution (~500 km) is visualized as red markers (locations) and a blue polyline (route) on an ArcGIS map, with data stored in SQLite and served via a .NET API.

### Why VRP Matters
VRP, as exemplified in `e4deliver.mos`, is critical to global supply chains, driving efficiency for companies like Amazon or UPS, saving billions annually through reduced fuel and time costs. As an NP-hard problem, it pushes algorithmic innovation (e.g., branch-and-cut in CBC solver, used here). Economically, it optimizes resource allocation; environmentally, it cuts emissions by minimizing travel; socially, it enhances service reliability in regions like Northern California. This project adapts the Mosel formulation to a modern stack, democratizing optimization for small-scale operators to achieve enterprise-level efficiency.

## Project Structure
- `DeliveryApi/`: .NET Core Web API to serve route data.
  - `Controllers/RouteController.cs`: API endpoint for routes.
  - `Program.cs`: API entry point with CORS support.
  - `appsettings.json`, `DeliveryApi.csproj`: .NET configuration.
- `optimize.py`: Python script for TSP optimization and GeoJSON/map generation.
- `setup_db.py`: Creates SQLite database (`delivery.db`) from GeoJSON.
- `check_db.py`: Verifies database contents.
- `index.html`: ArcGIS Maps SDK frontend showing routes on a map.
- `map.html`: Folium-generated map (for quick visualization).
- `routes.geojson`: Generated route data.
- `delivery.db`: SQLite database (not tracked in Git).

## Prerequisites
- Python 3.13+ with `pulp`, `geopandas`, `folium` (`pip install pulp geopandas folium`).
- .NET 8.0 SDK (`dotnet --version`).
- VSCode with Python, .NET, and Live Server extensions.
- SQLite (`sqlite3 --version`, optional for manual DB checks).
- 
<img width="1912" height="1073" alt="map png" src="https://github.com/user-attachments/assets/f4fc241e-d165-46a8-b88a-22bed5c789ed" />

## Setup and Run
1. **Python Pipeline**:
   - In `SmartDelivery`:
     ```
     python optimize.py
     python setup_db.py
     ```
   - Generates `routes.geojson`, `map.html`, `delivery.db`.
2. **Run API**:
   - In `DeliveryApi`:
     ```
     dotnet add package Microsoft.Data.Sqlite
     dotnet add package Newtonsoft.Json
     dotnet run
     ```
   - Access `http://localhost:5225/Route` for JSON data.
3. **View Frontend**:
   - Open `index.html` via VSCode Live Server or browser.
   - Shows ArcGIS map with red markers (locations) and blue route line.

## Debugging
- Check database: `python check_db.py`.
- View API: `http://localhost:5225/Route`.
- Browser Console (F12) for map errors.

## Notes
- Built for Northern CA (Sacramento refinery, Bay Area clients).
- Optimizes routes with PuLP, respects vehicle capacity (5000 units).
- Uses SQLite for simplicity (no spatialite required).
