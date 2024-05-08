import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_data():
    # Connect to databases
    src_conn = psycopg2.connect(host=os.getenv('SOURCE_DB_HOST'), dbname=os.getenv('SOURCE_DB_NAME'), user=os.getenv('SOURCE_DB_USER'), password=os.getenv('SOURCE_DB_PASS'))
    src_cur = src_conn.cursor()

    # Extract data from source 
    src_cur.execute("""
    COPY smartphones 
    FROM 'D:/data/smartphones.csv'
    DELIMITER ','
    CSV HEADER;
    """)
    data = src_cur.fetchall()

    src_cur.close()
    src_conn.close()

    return data

from collections import defaultdict
def transform_data(data):
    brand_statistics = defaultdict(lambda: {'total_ram': 0, 'total_storage': 0, 'count': 0})
    for row in data:
        brand = row[1]
        # Update brand statistics
        brand_statistics[brand]['total_ram'] += row[3] 
        brand_statistics[brand]['total_storage'] += row[4]
        brand_statistics[brand]['count'] += 1
    
    # Calculate average RAM and storage capacity for each brand
    aggregated_data = []
    for brand, stats in brand_statistics.items():
        average_ram = stats['total_ram'] / stats['count']
        average_storage = stats['total_storage'] / stats['count']
        # Add aggregated statistics for each brand
        aggregated_data.append((brand, average_ram, average_storage))
    
    return aggregated_data

def load_data(aggregated_data):
    # Connect to target database
    tgt_conn = psycopg2.connect(host=os.getenv('TARGET_DB_HOST'), dbname=os.getenv('TARGET_DB_NAME'), user=os.getenv('TARGET_DB_USER'), password=os.getenv('TARGET_DB_PASS'))
    tgt_cur = tgt_conn.cursor()

    # Load data into target table
    target_table = """
    CREATE TABLE IF NOT EXISTS destination_table (
        smartphone_name VARCHAR(255),
        brand VARCHAR(255),
        model VARCHAR(255),
        ram_gb INT,
        storage_gb INT,
        color VARCHAR(50),
        free BOOLEAN,
        price_usd DECIMAL
    )
    """
    for row in aggregated_data:
        # Assuming target_table has same schema as source_table
        tgt_cur.execute("INSERT INTO target_table VALUES (%s)", row)

    tgt_conn.commit()

    tgt_cur.close()
    tgt_conn.close()

if __name__ == "__main__":
    data = extract_data()
    transformed_data = transform_data(data)
    load_data(transformed_data)
    