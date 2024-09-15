import threading 
import time
import requests
from bs4 import BeautifulSoup
import django
django.setup()  # Ensure Django is set up before importing model

from VectorDB.VectorDB import vector_db

def scrape_news():
    from Application.models import Document
    while True:
        #Adding the news scraping logic code here
        url = "https://www.bbc.com/news"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all('article')
        
        for article in articles:
            h3_tag = article.find('h3')
            if h3_tag:  # Check if h3_tag is not None
                title = h3_tag.get_text()
                link = article.find('a')['href']
                summary = article.find('p').get_text()
                
                doc = Document.objects.create(documentName=title, doc_key=link, doc_content=summary)
            
                #adding to vector database
                vector_db.add_document(doc.documentName, doc.doc_key, summary)
        
        time.sleep(60) #scrape every 60 seconds
        
def start_news_scraper():
    try:
        thread = threading.Thread(target=scrape_news)
        thread.start()
        thread.join()  # Wait for the thread to finish
    except KeyboardInterrupt:
        print("Scraper stopped by user.")
        # Optionally, you can add logic to clean up or stop the thread if needed