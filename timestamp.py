from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime

app = FastAPI()

class DateRange(BaseModel):
    start_datetime: datetime
    end_datetime: datetime

def get_db_connection():
    return psycopg2.connect(
        dbname="db_db",
        user="db_user",
        password="db_password",
        host="localhost",
        port="5432"
    )

@app.post("/latest_values")
async def get_latest_values(date_range: DateRange):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT m.node_id, n.node_name, m.timestamp_measured, m.value
    FROM Measures m
    JOIN GridNode n ON m.node_id = n.node_id
    WHERE m.timestamp_measured BETWEEN %s AND %s
    AND m.timestamp_collected = (
        SELECT MAX(timestamp_collected)
        FROM Measures m2
        WHERE m2.node_id = m.node_id
        AND m2.timestamp_measured = m.timestamp_measured
    )
    ORDER BY m.node_id, m.timestamp_measured
    """
    cursor.execute(query, (date_range.start_datetime, date_range.end_datetime))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {"node_id": row[0], "node_name": row[1], "timestamp": row[2], "value": row[3]}
        for row in results
    ]
