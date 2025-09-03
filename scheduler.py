# # scheduler.py
# import schedule
# import time
# from main import fetch_and_process_news  # ✅ Your news agent logic here

# def run_daily_news_agent():
#     print("🟢 Starting daily news agent...")
#     fetch_and_process_news()
#     print("✅ News agent finished.")

# # ⏰ Schedule it to run once every day at 8:00 AM (adjust if needed)
# schedule.every().day.at("8:00").do(run_daily_news_agent)

# print("⏳ Scheduler started... Waiting to run daily task.")
# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check every 60 seconds
