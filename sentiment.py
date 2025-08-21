import google.generativeai as genai
import json
import os
from datetime import datetime


genai.configure(api_key="AIzaSyCDQQCXvTUIxNGthhdlBwCuK-AGrmHG33Y")  


SCRAPER_FOLDER = "scraperoutput"      # folder where your scraper saves daily JSON files
OUTPUT_FOLDER = "sentiment_analysis"    # folder to save daily Notepad files


os.makedirs(OUTPUT_FOLDER, exist_ok=True)


today_str = datetime.now().strftime("%Y-%m-%d")
INPUT_FILE = os.path.join(SCRAPER_FOLDER, f"{today_str}.json")


if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"No scraper file found for today: {INPUT_FILE}")



with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

model = genai.GenerativeModel("gemini-2.0-flash")


def analyze_sentiment(text):
    prompt = f"""
    Classify the following article content as Positive, Neutral, or Negative in one word
    
    Content: {text}
    
    Respond with only one word: Positive, Neutral, or Negative.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Unknown"


output_file = os.path.join(OUTPUT_FOLDER, f"sentiment_{today_str}.txt")

with open(output_file, "a", encoding="utf-8") as f:  # 'a' = append
    for i, article in enumerate(articles, start=1):
        sentiment = analyze_sentiment(article.get("content", ""))
        article["sentiment"] = sentiment
        f.write(f"Article {i}\n")
        f.write(f"Title: {article.get('title','N/A')}\n")
        f.write(f"URL: {article.get('url','N/A')}\n")
        f.write(f"Content: {article.get('content','N/A')}\n")
        f.write(f"Sentiment: {sentiment}\n")
        f.write("\n" + "-"*50 + "\n\n")
        print(f"Processed Article {i}")

print(f"\nSentiment analysis complete. Daily file updated: '{output_file}'")