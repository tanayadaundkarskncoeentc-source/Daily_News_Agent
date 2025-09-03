# news_fetching.py
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.runnables import Runnable
import os
from dotenv import load_dotenv

load_dotenv()

AI_KEYWORDS = ["artificial intelligence", "AI ", "AI:", "AI-", "AI.", "AI,"]  # Add variations to catch more matches


FEED_SOURCES = {
    "The Verge": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    # "Reddit AI": "https://www.reddit.com/r/artificial/.rss",
    # "Reddit AI News": "https://www.reddit.com/r/ainews/.rss",
    "Analytics Vidhya": "https://www.analyticsvidhya.com/blog/feed/",
    "VentureBeat": "https://venturebeat.com/category/ai/feed/",
    "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "DeepMind": "https://deepmind.com/blog/feed/basic",
    "AI Trends": "https://www.aitrends.com/feed/",
    "Wired AI": "https://www.wired.com/feed/category/artificial-intelligence/latest/rss",
    "Google Research": "https://ai.googleblog.com/feeds/posts/default",
    "AWS ML Blog": "https://aws.amazon.com/blogs/ai/feed/",
    "Meta AI": "https://rsshub.app/meta/ai",
    "Towards Data Science": "https://towardsdatascience.com/feed",
    "TLDR AI": "https://tldr.tech/newsletter/ai.rss",
    "AI Breakfast": "https://aibreakfast.substack.com/feed",
    "The Rundown AI": "https://therundown.substack.com/feed",
    "Bloomberg Tech": "https://www.bloomberg.com/feed/podcast/big-take.xml",
}

# ✅ LangChain Mistral setup
llm = ChatMistralAI(
    temperature=0.0,
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY")
)

def is_ai_related_llm(title, summary):
    prompt = ChatPromptTemplate.from_template("""
    Determine if this news is primarily about artificial intelligence. Respond only with "Yes" or "No".

    Title: {title}
    Summary: {summary}
    """)
    
    chain: Runnable = prompt | llm
    response = chain.invoke({"title": title, "summary": summary})
    return "yes" in response.content.lower()

def extract_image(entry):
    if "media_content" in entry:
        return entry["media_content"][0].get("url", "")
    if "media_thumbnail" in entry:
        return entry["media_thumbnail"][0].get("url", "")
    if "links" in entry:
        for link in entry["links"]:
            if link.get("type", "").startswith("image"):
                return link.get("href", "")
    if "summary" in entry:
        soup = BeautifulSoup(entry["summary"], "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img.get("src")
    return ""

def fetch_ai_news():
    news_items = []
    time_limit = datetime.utcnow() - timedelta(hours=24)

    for source_name, feed_url in FEED_SOURCES.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                published_parsed = entry.get("published_parsed")
                if published_parsed:
                    published_dt = datetime(*published_parsed[:6])
                    if published_dt < time_limit:
                        continue

                title = entry.get("title", "No Title")
                link = entry.get("link", "")
                raw_summary_html = entry.get("summary", "")
                summary = BeautifulSoup(raw_summary_html, "html.parser").get_text().strip()

                # ✅ First, keyword filter
                combined_text = f"{title} {summary}".lower()
                if not any(keyword.lower() in combined_text for keyword in AI_KEYWORDS):
                    continue

                # ✅ Filter using Mistral
                if not is_ai_related_llm(title, summary):
                    continue

                published = published_dt.strftime("%a, %d %b %Y")

                news_items.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "published": published,
                    "summary": summary,
                    "image": extract_image(entry)
                })
        except Exception as e:
            print(f"Error from {source_name}: {e}")

    return news_items





# #news_fetching
# import feedparser
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from email.utils import parsedate_to_datetime

# FEED_SOURCES = {
#     "The Verge": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
#     "MIT Tech Review": "https://www.technologyreview.com/feed/",
#     "Reddit AI": "https://www.reddit.com/r/artificial/.rss",
#     "Reddit AI News": "https://www.reddit.com/r/ainews/.rss",
#     "Analytics Vidhya": "https://www.analyticsvidhya.com/blog/feed/",
#     "VentureBeat": "https://venturebeat.com/category/ai/feed/",
#     "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
#     "OpenAI Blog": "https://openai.com/blog/rss.xml",
#     "DeepMind": "https://deepmind.com/blog/feed/basic",
#     "AI Trends": "https://www.aitrends.com/feed/",
#     "Wired AI": "https://www.wired.com/feed/category/artificial-intelligence/latest/rss",
#     "Google Research": "https://ai.googleblog.com/feeds/posts/default",
#     "AWS ML Blog": "https://aws.amazon.com/blogs/ai/feed/",
#     "Meta AI": "https://rsshub.app/meta/ai",
#     "Towards Data Science": "https://towardsdatascience.com/feed",
#     "TLDR AI": "https://tldr.tech/newsletter/ai.rss",
#     "AI Breakfast": "https://aibreakfast.substack.com/feed",
#     "The Rundown AI": "https://therundown.substack.com/feed",
#     "Bloomberg Tech": "https://www.bloomberg.com/feed/podcast/big-take.xml",
# }

# AI_KEYWORDS = ["artificial intelligence", "AI ", "AI:"]

# def is_ai_related(entry):
#     content = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
#     return any(keyword.lower() in content for keyword in AI_KEYWORDS)

# def extract_image(entry):
#     if "media_content" in entry:
#         return entry["media_content"][0].get("url", "")
#     if "media_thumbnail" in entry:
#         return entry["media_thumbnail"][0].get("url", "")
#     if "links" in entry:
#         for link in entry["links"]:
#             if link.get("type", "").startswith("image"):
#                 return link.get("href", "")
#     if "summary" in entry:
#         soup = BeautifulSoup(entry["summary"], "html.parser")
#         img = soup.find("img")
#         if img and img.get("src"):
#             return img.get("src")
#     return ""

# def fetch_ai_news():
#     news_items = []
#     time_limit = datetime.utcnow() - timedelta(hours=24)

#     for source_name, feed_url in FEED_SOURCES.items():
#         try:
#             feed = feedparser.parse(feed_url)
#             for entry in feed.entries:
#                 published_parsed = entry.get("published_parsed")
#                 if published_parsed:
#                     published_dt = datetime(*published_parsed[:6])
#                     if published_dt < time_limit:
#                         continue

#                 if is_ai_related(entry):
#                     title = entry.get("title", "No Title")
#                     link = entry.get("link", "")
#                     published_dt = datetime(*entry.published_parsed[:6])
#                     published = published_dt.strftime("%a, %d %b %Y")

#                     summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text().strip()
#                     if "submitted by" in summary.lower():
#                         continue

#                     news_items.append({
#                         "source": source_name,
#                         "title": title,
#                         "link": link,
#                         "published": published,
#                         "summary": summary,
#                         "image": extract_image(entry)
#                     })
#         except Exception as e:
#             print(f"Error from {source_name}: {e}")

#     return news_items
