import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import logging

logger = logging.getLogger('trinetra.db')

def get_connection():
    db_url = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_qTz5RJ3ALUGy@ep-frosty-resonance-adeowc34-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to DB: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id SERIAL PRIMARY KEY,
                    scan_id VARCHAR(50) NOT NULL,
                    patient_name VARCHAR(100),
                    verdict VARCHAR(50),
                    confidence VARCHAR(20),
                    risk_level VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"DB Init error: {e}")
    finally:
        conn.close()

def get_total_scans():
    conn = get_connection()
    if not conn:
        return 0
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM scans")
            result = cur.fetchone()
            return result[0] if result else 0
    except Exception as e:
        logger.error(f"Error getting total scans: {e}")
        return 0
    finally:
        conn.close()

def save_scan(scan_id, patient_name, verdict, confidence, risk_level):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO scans (scan_id, patient_name, verdict, confidence, risk_level)
                VALUES (%s, %s, %s, %s, %s)
            """, (scan_id, patient_name, verdict, confidence, risk_level))
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving scan: {e}")
    finally:
        conn.close()

def search_scans(query=""):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if query:
                search_term = f"%{query}%"
                cur.execute("""
                    SELECT * FROM scans 
                    WHERE patient_name ILIKE %s OR scan_id ILIKE %s 
                    ORDER BY created_at DESC LIMIT 50
                """, (search_term, search_term))
            else:
                cur.execute("SELECT * FROM scans ORDER BY created_at DESC LIMIT 50")
            
            results = cur.fetchall()
            # Convert timestamp to string for JSON serialization
            for row in results:
                if row.get('created_at'):
                    row['created_at'] = row['created_at'].isoformat()
            return results
    except Exception as e:
        logger.error(f"Error searching scans: {e}")
        return []
    finally:
        conn.close()
