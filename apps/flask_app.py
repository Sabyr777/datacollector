import os

from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return conn

@app.route('/daily_service_purchases', methods=['GET'])
def get_daily_service_purchases():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT purchase_date, service_title, total_daily_purchase 
            FROM report_daily_service_purchases
        """)

        purchases = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(purchases)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/daily_referrals', methods=['GET'])
def get_daily_referrals():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT 
                DATE(created_at) AS referral_date, 
                COUNT(*) AS daily_referrals
            FROM invite_code_entries
            GROUP BY referral_date
            ORDER BY referral_date
        """)

        referrals = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(referrals)
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)
