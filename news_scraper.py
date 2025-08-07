import os
import json
import time
from datetime import datetime
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from newspaper import Article
from newspaper.article import ArticleException

def decode_url(url):
    # Use googlenewsdecoder to get real article url behind Google News redirect
    result = new_decoderv1(url, interval=0.5)
    if result.get("status"):
        return result["decoded_url"]
    else:
        return None

def main():
    # Set up GNews to get news in English, US, max 50 articles
    google_news = GNews(language='en', country='US', max_results=50)

    print("Fetching candidate articles...")
    candidates = google_news.get_top_news()
    print(f"Candidate articles retrieved: {len(candidates)}")

    articles = []  # List to store all valid article data
    skipped = 0
    added = 0

    # Folder named with today's date in YYYY-MM-DD format
    date_folder = datetime.now().strftime('%Y-%m-%d')
    base_folder = "scraperoutput"
    os.makedirs(os.path.join(base_folder, date_folder), exist_ok=True)

    for item in candidates:
        if added >= 15:
            break  # Stop after 15 articles

        print(f"Original Google News URL: {item['url']}")
        real_url = decode_url(item['url'])
        if not real_url:
            print("Skipping article: Could not decode URL")
            skipped += 1
            continue

        print(f"Decoded URL: {real_url}")

        try:
            article = Article(real_url)
            article.download()
            article.parse()
        except ArticleException as e:
            print(f"Skipping article due to download/parse error: {e}")
            skipped += 1
            continue

        article_data = {
            "title": article.title or "No title",
            "published_date": item.get('published date', 'No date'),
            "publisher": item.get('publisher', 'Unknown publisher'),
            "url": real_url,
            "content": article.text or "No content"
        }

        articles.append(article_data)
        added += 1
        print(f"Added article: {article_data['title']}")

        # Small delay to be polite to servers and avoid throttling
        time.sleep(0.5)

    # Save all articles into one JSON file
    output_path = os.path.join(base_folder, date_folder, f"{date_folder}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\nTotal candidate articles: {len(candidates)}")
    print(f"Total articles skipped: {skipped}")
    print(f"Total articles added: {added}")

if __name__ == "__main__":
    main()
