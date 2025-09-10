#!/usr/bin/env python3
"""
Script to read contact messages from the portfolio database
"""

import os
import sqlite3
from datetime import datetime

def read_messages():
    """Read and display all contact messages from SQLite database"""
    db_path = os.path.join("instance", "portfolio.db")
    
    if not os.path.exists(db_path):
        print("📭 No database found. Run your portfolio first to create the database.")
        return
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query messages table
        cursor.execute("""
            SELECT name, email, message, created_at 
            FROM messages 
            ORDER BY created_at DESC
        """)
        
        messages = cursor.fetchall()
        
        if not messages:
            print("📭 No messages found in the database.")
            return
        
        print(f"📬 Found {len(messages)} message(s):\n")
        print("=" * 80)
        
        for i, (name, email, message, created_at) in enumerate(messages, 1):
            # Parse datetime string
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            print(f"\n📧 Message #{i}")
            print(f"👤 From: {name}")
            print(f"📧 Email: {email}")
            print(f"📅 Date: {dt.strftime('%B %d, %Y at %I:%M %p')}")
            print(f"💬 Message:")
            print(f"   {message}")
            print("-" * 80)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    read_messages()
