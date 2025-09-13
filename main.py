from fastapi import FastAPI
from news_fetching import fetch_ai_news
from supabase_utils import save_news_to_supabase
from email_utils import send_email
import uvicorn
import os
import schedule
import threading
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ AI News Update Service is Live!"}

@app.post("/run-news-update")
def run_news_agent():
    """
    Endpoint to trigger the AI news fetch, filter, save, and email process.
    """
    print("🚀 Triggered news fetch process...")
    ai_news = fetch_ai_news()

    if not ai_news:
        print("⚠️ No relevant AI news found today.")
        return {"status": "No AI news found."}

    print(f"✅ {len(ai_news)} AI news items found.")
    save_news_to_supabase(ai_news)
    send_email(ai_news)

    print("🎉 News processing complete.")
    return {"status": "AI news processed and sent successfully."}

# ✅ Scheduler job
def job():
    print("🟢 Running daily news agent...")
    ai_news = fetch_ai_news()
    if ai_news:
        save_news_to_supabase(ai_news)
        send_email(ai_news)
    else:
        print("⚠️ No AI news found today.")
    print("✅ Daily news job finished.")

# ✅ Scheduler runner in background thread
def run_scheduler():
    schedule.every().day.at("06:50").do(job)  # Change to your desired time (24-hour format, IST)  1:30 UTC = 7:00 AM
    while True:
        schedule.run_pending()
        time.sleep(60)



if __name__ == "__main__":
    # Start scheduler thread when app starts
    threading.Thread(target=run_scheduler, daemon=True).start()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)


# # main.py
# import json
# from news_fetching import fetch_ai_news
# from supabase_utils import save_news_to_supabase
# from email_utils import send_email

# if __name__ == "__main__":
#     news = fetch_ai_news()

#     with open("news.json", "w", encoding="utf-8") as f:
#         json.dump(news, f, ensure_ascii=False, indent=2)
#     print(f"✅ Saved {len(news)} news items to news.json")

#     save_news_to_supabase(news)
#     send_email(news)
