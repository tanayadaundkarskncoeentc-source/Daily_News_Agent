# supabase_utils
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not set in .env")

print("🔍 Supabase URL:", SUPABASE_URL)
print("🔐 Supabase Key starts with:", SUPABASE_KEY[:30]) 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_news_to_supabase(news_data):
    print(f"🟡 Saving {len(news_data)} news items to Supabase...")

    for item in news_data:
        try:
            published_str = item.get("published", "")
            published_dt = (
                datetime.strptime(published_str, "%a, %d %b %Y")
                if published_str
                else datetime.utcnow()
            ).astimezone(pytz.utc).isoformat()

            record = {
                "title": item.get("title", ""),
                "summary": item.get("summary", ""),
                "source": item.get("source", ""),
                "link": item.get("link", ""),
                "image": item.get("image", ""),
                "published": published_dt,
                "fetched_at": datetime.utcnow().astimezone(pytz.utc).isoformat()
            }

            supabase.from_("ai_news").insert(record).execute()
            print("✅ Inserted:", record["title"])

        except Exception as e:
            print("❌ Insert error:", e)

    print("✅ All news items processed.")
