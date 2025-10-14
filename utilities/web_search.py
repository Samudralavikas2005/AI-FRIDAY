# utilities/web_search.py
import webbrowser
import wikipedia
import re

class WebSearch:
    def __init__(self):
        pass
    
    def google_search(self, query):
        if not query or len(query) < 2:
            return "Please specify what you want to search for."
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for: {query}"
    
    def wikipedia_search(self, topic):
        if not topic or len(topic) < 2:
            return "Please specify what you want to know about."
        try:
            info = wikipedia.summary(topic, sentences=2)
            return info
        except:
            return f"Sorry, I couldn't find Wikipedia information about {topic}."
    
    def open_website(self, url_name):
        websites = {
            "youtube": "https://youtube.com",
            "instagram": "https://instagram.com", 
            "github": "https://github.com",
            "linkedin": "https://linkedin.com",
            "chat gpt": "https://chatgpt.com/",
            "gmail": "https://mail.google.com/mail/",
            "whatsapp": "https://web.whatsapp.com/",
            "aums": "https://aumscn.amrita.edu/cas/login?service=https%3A%2F%2Faumscn.amrita.edu%2Faums%2FJsp%2FCore_Common%2Findex.jsp"
        }
        
        if url_name in websites:
            webbrowser.open(websites[url_name])
            return f"Opening {url_name.title()}"
        return "Website not found in my database"
    
    def extract_search_query(self, text):
        query = None
        if "search for" in text:
            query = text.split("search for")[1].strip()
        elif "search" in text:
            query = text.split("search")[1].strip()
        elif "google" in text:
            query = text.split("google")[1].strip()
        return query
    
    def extract_topic_from_text(self, text):
        topic = None
        if "tell me about" in text:
            topic = text.split("tell me about")[1].strip()
        elif "information about" in text:
            topic = text.split("information about")[1].strip()
        elif "wikipedia" in text:
            topic = text.split("wikipedia")[1].strip()
        return topic
