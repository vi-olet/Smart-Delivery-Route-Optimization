# Smart Delivery Route Optimization

A beginner-friendly project to optimize delivery routes in Northern California using a Python geospatial pipeline, .NET Web API, SQLite database, and ArcGIS Maps SDK frontend.

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