import sqlite3
import hashlib
import logging
import os
from datetime import datetime

logger = logging.getLogger("OmniCrawler.Storage")

def get_db_path():
    """Returns path to the current monthly SQLite database."""
    month_str = datetime.now().strftime("%Y-%m")
    db_dir = os.path.join("data", "db")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, f"{month_str}.sqlite")

def init_db(conn):
    """Initializes the database schema if not exists."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hot_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            hot_score TEXT,
            item_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform_hash ON hot_records (platform, item_hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON hot_records (created_at)')
    conn.commit()

def get_item_hash(platform, title, url):
    """Generate a unique hash for platform+title+url."""
    content = f"{platform}|{title}|{url}".encode('utf-8')
    return hashlib.md5(content).hexdigest()

def save_platform_data(platform, data):
    """
    Saves each item to SQLite with per-item de-duplication.
    Only saves if the item is new or the hot_score has changed since the last check.
    """
    db_path = get_db_path()
    new_records_count = 0
    
    try:
        with sqlite3.connect(db_path) as conn:
            init_db(conn)
            cursor = conn.cursor()
            
            for item in data:
                title = item.get('title', '')
                url = item.get('url', '')
                score = str(item.get('hot_score', 'N/A'))
                item_hash = get_item_hash(platform, title, url)
                
                # Check the latest record for this specific item on this platform
                cursor.execute('''
                    SELECT hot_score FROM hot_records 
                    WHERE platform = ? AND item_hash = ? 
                    ORDER BY created_at DESC LIMIT 1
                ''', (platform, item_hash))
                
                last_record = cursor.fetchone()
                
                # Skip if the exact same item and score already exists in the last capture
                if last_record and str(last_record[0]) == score:
                    continue
                
                # Insert new record
                cursor.execute('''
                    INSERT INTO hot_records (platform, title, url, hot_score, item_hash)
                    VALUES (?, ?, ?, ?, ?)
                ''', (platform, title, url, score, item_hash))
                new_records_count += 1
                
            conn.commit()
            
        if new_records_count > 0:
            logger.info(f"Saved {new_records_count} new/updated items for {platform} to {db_path}")
        else:
            logger.info(f"No changes detected for {platform}. Database untouched.")
            
        return new_records_count > 0
    except Exception as e:
        logger.error(f"SQLite Error for {platform}: {e}")
        return False
