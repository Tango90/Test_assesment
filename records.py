import psycopg2
from datetime import datetime, timedelta
import random

# Database connection
conn = psycopg2.connect(
    dbname="name_db",
    user="db_user",
    password="db_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Insert Grids
grids = ['Grid1', 'Grid2', 'Grid3']
for grid in grids:
    cursor.execute("INSERT INTO Grid (grid_name) VALUES (%s) ON CONFLICT DO NOTHING", (grid,))

# Insert Regions (3 per Grid)
regions = ['Region1', 'Region2', 'Region3']
for grid_id in range(1, 4):
    for region in regions:
        cursor.execute(
            "INSERT INTO GridRegion (region_name, grid_id) VALUES (%s, %s)",
            (f"{region}_G{grid_id}", grid_id)
        )

# Insert Nodes (3 per Region)
nodes = ['Node1', 'Node2', 'Node3']
for region_id in range(1, 10):
    for node in nodes:
        cursor.execute(
            "INSERT INTO GridNode (node_name, region_id) VALUES (%s, %s)",
            (f"{node}_R{region_id}", region_id)
        )

# Insert Measures (1 week, 3 nodes per region, 9 regions, hourly evolution)
start_date = datetime(2025, 7, 1)
for node_id in range(1, 28):  # 3 nodes * 9 regions = 27 nodes
    for day in range(7):
        for hour in range(24):
            timestamp_measured = start_date + timedelta(days=day, hours=hour)
            # Simulate evolution: 3 updates per hour at different collection times
            for i in range(3):
                timestamp_collected = timestamp_measured - timedelta(hours=12 - i)
                value = 100 + random.uniform(-5, 5)  # Random value around 100
                cursor.execute(
                    """
                    INSERT INTO Measures (node_id, timestamp_measured, timestamp_collected, value)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (node_id, timestamp_measured, timestamp_collected, value)
                )

conn.commit()
cursor.close()
conn.close()
