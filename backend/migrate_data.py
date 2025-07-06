#!/usr/bin/env python3
"""
Data Migration Script: JSON to Supabase
This script migrates your existing JSON files to Supabase tables.
Run this ONCE after setting up your Supabase tables.
"""

import json
import httpx
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_API_KEY in your .env file")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

BASE_DIR = Path(__file__).parent

async def supabase_insert(table: str, data: dict):
    """Insert data into Supabase table"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=HEADERS, json=data)
            response.raise_for_status()
            print(f"✅ Inserted into {table}: {data}")
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"❌ Error inserting into {table}: {e.response.status_code} - {e.response.text}")
            print(f"   Data: {data}")
            return None

async def migrate_users():
    """Migrate users.json to users table"""
    print("\n🔄 Migrating users...")
    
    users_file = BASE_DIR / "users.json"
    if not users_file.exists():
        print("❌ users.json not found")
        return
    
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    for user_id, user_info in users_data.items():
        await supabase_insert("users", {
            "id": user_id,
            "name": user_info.get("name", ""),
            "status": user_info.get("status", "neutral")
        })
    
    print(f"✅ Migrated {len(users_data)} users")

async def migrate_ads():
    """Migrate ads.json to ads table"""
    print("\n🔄 Migrating ads...")
    
    ads_file = BASE_DIR / "ads.json"
    if not ads_file.exists():
        print("❌ ads.json not found")
        return
    
    with open(ads_file, 'r') as f:
        ads_data = json.load(f)
    
    for ad in ads_data:
        await supabase_insert("ads", {
            "title": ad.get("title", ""),
            "description": ad.get("description", ""),
            "category": ad.get("category", ""),
            "target_audience": ad.get("target_audience", "neutral"),
            "explanation": ad.get("explanation", "")
        })
    
    print(f"✅ Migrated {len(ads_data)} ads")

async def migrate_blocked_ads():
    """Migrate blocked_ads.json to blocked_ads table"""
    print("\n🔄 Migrating blocked ads...")
    
    blocked_file = BASE_DIR / "blocked_ads.json"
    if not blocked_file.exists():
        print("❌ blocked_ads.json not found")
        return
    
    with open(blocked_file, 'r') as f:
        blocked_ads = json.load(f)
    
    for ad_title in blocked_ads:
        await supabase_insert("blocked_ads", {
            "ad_title": ad_title
        })
    
    print(f"✅ Migrated {len(blocked_ads)} blocked ads")

async def migrate_user_blocked_ads():
    """Migrate user_blocked_ads.json to user_blocked_ads table"""
    print("\n🔄 Migrating user blocked ads...")
    
    user_blocked_file = BASE_DIR / "user_blocked_ads.json"
    if not user_blocked_file.exists():
        print("❌ user_blocked_ads.json not found")
        return
    
    with open(user_blocked_file, 'r') as f:
        user_blocked_data = json.load(f)
    
    count = 0
    for user_id, blocked_ads in user_blocked_data.items():
        for ad_title in blocked_ads:
            await supabase_insert("user_blocked_ads", {
                "user_id": user_id,
                "ad_title": ad_title
            })
            count += 1
    
    print(f"✅ Migrated {count} user blocked ads")

async def migrate_feedback():
    """Migrate feedback.json to feedback table"""
    print("\n🔄 Migrating feedback...")
    
    feedback_file = BASE_DIR / "feedback.json"
    if not feedback_file.exists():
        print("❌ feedback.json not found")
        return
    
    with open(feedback_file, 'r') as f:
        feedback_data = json.load(f)
    
    count = 0
    for user_id, feedback_list in feedback_data.items():
        for feedback_item in feedback_list:
            await supabase_insert("feedback", {
                "user_id": user_id,
                "ad_title": feedback_item.get("ad_title", ""),
                "feedback": feedback_item.get("feedback", ""),
                "emotion": feedback_item.get("emotion", "neutral"),
                "timestamp": feedback_item.get("timestamp", datetime.now().isoformat())
            })
            count += 1
    
    print(f"✅ Migrated {count} feedback entries")

async def migrate_user_preferences():
    """Migrate user_preferences.json to user_preferences table"""
    print("\n🔄 Migrating user preferences...")
    
    prefs_file = BASE_DIR / "user_preferences.json"
    if not prefs_file.exists():
        print("❌ user_preferences.json not found")
        return
    
    with open(prefs_file, 'r') as f:
        prefs_data = json.load(f)
    
    for user_id, preferences in prefs_data.items():
        await supabase_insert("user_preferences", {
            "user_id": user_id,
            "emotion_filter": preferences.get("emotion_filter", True),
            "personalization": preferences.get("personalization", True),
            "explanations": preferences.get("explanations", True),
            "data_collection": preferences.get("data_collection", True)
        })
    
    print(f"✅ Migrated {len(prefs_data)} user preferences")

async def main():
    """Run all migrations"""
    print("🚀 Starting data migration from JSON to Supabase...")
    print(f"📍 Base directory: {BASE_DIR}")
    print(f"🔗 Supabase URL: {SUPABASE_URL}")
    
    try:
        # Test connection first
        url = f"{SUPABASE_URL}/rest/v1/users"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
        print("✅ Supabase connection successful")
        
        # Run migrations
        await migrate_users()
        await migrate_ads()
        await migrate_blocked_ads()
        await migrate_user_blocked_ads()
        await migrate_feedback()
        await migrate_user_preferences()
        
        print("\n🎉 Migration completed successfully!")
        print("⚠️  Remember to:")
        print("   1. Backup your JSON files before deleting them")
        print("   2. Test your new Supabase-integrated backend")
        print("   3. Update your deployment with the new code")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print("Please check your Supabase credentials and table setup")

if __name__ == "__main__":
    asyncio.run(main())