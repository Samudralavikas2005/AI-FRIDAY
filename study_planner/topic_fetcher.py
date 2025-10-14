# study_planner/topic_fetcher.py
import requests
import re
from config import GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID, GEMINI_API_KEY, GEMINI_ENDPOINT

class TopicFetcher:
    def __init__(self):
        pass
    
    def get_subject_topics(self, subject_name):
        try:
            all_topics = set()
            
            # Try Google API first
            api_topics = self.get_topics_from_google_api(subject_name)
            if api_topics:
                all_topics.update(api_topics)
                print(f"✅ Google API found {len(api_topics)} topics")
            
            # Fallback to AI if API doesn't give enough results
            if len(all_topics) < 5:
                print("🔍 API didn't find enough topics, trying AI...")
                ai_topics = self.get_topics_from_ai(subject_name)
                if ai_topics:
                    all_topics.update(ai_topics)
                    print(f"✅ AI found {len(ai_topics)} additional topics")
            
            # Final fallback to generated topics
            if len(all_topics) < 3:
                print("🔍 Using generated topics as fallback...")
                generated = self.generate_topics_from_subject_name(subject_name)
                all_topics.update(generated)
            
            final_topics = self.prioritize_and_organize_topics(list(all_topics), subject_name)
            
            print(f"✅ Final topics: {len(final_topics)}")
            return final_topics
                
        except Exception as e:
            print(f"❌ Error fetching topics for {subject_name}: {e}")
            return self.generate_topics_from_subject_name(subject_name)
    
    def get_topics_from_google_api(self, subject_name):
        try:
            if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
                print("❌ Google API keys not configured")
                return []
            
            print(f"🔍 Using Google API to search: {subject_name}")
            
            search_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_API_KEY,
                'cx': GOOGLE_SEARCH_ENGINE_ID,
                'q': f"{subject_name} syllabus important topics curriculum",
                'num': 5
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            data = response.json()
            
            all_topics = set()
            
            if 'items' in data:
                for item in data['items']:
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    
                    topics_from_title = self.extract_topics_from_text(title, subject_name)
                    topics_from_snippet = self.extract_topics_from_text(snippet, subject_name)
                    
                    all_topics.update(topics_from_title)
                    all_topics.update(topics_from_snippet)
                    
                    print(f"✅ API result: {title[:50]}...")
            
            print(f"✅ Google API found {len(all_topics)} topics")
            return list(all_topics)
            
        except Exception as e:
            print(f"❌ Google API error: {e}")
            return []
    
    def get_topics_from_ai(self, subject_name):
        try:
            if not GEMINI_API_KEY:
                return []
                
            prompt = f"""List the 10 most important topics someone should study for {subject_name}. 
            Return only the topic names as a simple list, one per line."""
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 300}
            }
            url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            
            if "candidates" in data and data["candidates"]:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return self.parse_ai_response(content)
                
            return []
            
        except:
            return []
    
    def parse_ai_response(self, ai_text):
        topics = []
        lines = ai_text.split('\n')
        
        for line in lines:
            line = line.strip()
            line = re.sub(r'^[\d\-\*•\.\)\]]+\s*', '', line)
            line = re.sub(r'<[^>]+>', '', line)
            line = re.sub(r'\s+', ' ', line).strip()
            
            if line and len(line) > 5 and len(line) < 80:
                topics.append(line)
        
        return topics[:10]
    
    def extract_topics_from_text(self, text, subject_name):
        topics = set()
        
        sentences = re.split(r'[.,;•\-–]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if 10 <= len(sentence) <= 80:
                clean_sentence = self.clean_topic_text(sentence)
                if self.is_valid_educational_topic(clean_sentence, subject_name):
                    topics.add(clean_sentence)
        
        return list(topics)
    
    def clean_topic_text(self, text):
        text = re.sub(r'&[^;]+;', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'https?://[^\s]+', '', text)
        text = re.sub(r'[^\w\s\-\(\)]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        garbage_patterns = [
            r'^status:\s*\w+',
            r'free trial',
            r'results for',
            r'&quot;',
            r'^\d+\s+results',
            r'search.*query',
            r'^newnew',
            r'^preview',
        ]
        
        for pattern in garbage_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text[:60].strip()
    
    def is_valid_educational_topic(self, topic, subject_name):
        if len(topic) < 10 or len(topic) > 60:
            return False
        
        invalid_indicators = [
            'status:', 'free trial', 'results for', '&quot;', 'search', 
            'menu', 'login', 'sign', 'home', 'contact', 'privacy',
            'cookie', 'copyright', 'javascript', 'css', 'http',
            'newnew', 'preview', 'skills you', 'packt', 'educba',
            'microsoft', 'advanced java', 'intermediate javascript'
        ]
        
        topic_lower = topic.lower()
        if any(indicator in topic_lower for indicator in invalid_indicators):
            return False
        
        subject_words = subject_name.lower().split()
        has_subject_relevance = any(word in topic_lower for word in subject_words)
        
        educational_terms = [
            'introduction', 'fundamental', 'basic', 'advanced', 'concept',
            'principle', 'theory', 'method', 'technique', 'application',
            'example', 'exercise', 'problem', 'solution', 'practice',
            'programming', 'development', 'design', 'analysis', 'implementation'
        ]
        
        has_educational_content = any(term in topic_lower for term in educational_terms)
        
        return has_subject_relevance or has_educational_content
    
    def prioritize_and_organize_topics(self, topics, subject_name):
        if not topics:
            return []
        
        priority_order = [
            ('introduction', 1), ('overview', 1), ('getting started', 1),
            ('basic', 2), ('fundamental', 2), ('beginner', 2),
            ('advanced', 3), ('expert', 3), ('professional', 3)
        ]
        
        def get_topic_priority(topic):
            topic_lower = topic.lower()
            for pattern, priority in priority_order:
                if pattern in topic_lower:
                    return priority
            return 2
        
        sorted_topics = sorted(topics, key=lambda x: (get_topic_priority(x), x))
        return sorted_topics[:12]
    
    def generate_topics_from_subject_name(self, subject_name):
        words = subject_name.lower().split()
        
        if any(word in words for word in ['programming', 'code', 'software', 'computer']):
            return [f"{topic} in {subject_name}" for topic in [
                "Basic Syntax and Structure", "Data Types and Variables", "Control Flow",
                "Functions and Methods", "Object-Oriented Concepts", "Data Structures",
                "Algorithm Design", "Debugging Techniques", "Software Development", "Project Implementation"
            ]]
        elif any(word in words for word in ['math', 'calculus', 'algebra']):
            return [f"{topic} in {subject_name}" for topic in [
                "Basic Concepts and Notation", "Fundamental Operations", "Equations and Formulas",
                "Theorems and Proofs", "Problem Solving Techniques", "Advanced Applications",
                "Mathematical Modeling", "Computational Methods", "Theoretical Framework", "Practical Implementations"
            ]]
        else:
            return [f"{topic} of {subject_name}" for topic in [
                "Introduction to", "Fundamentals of", "Core Principles of", "Basic Concepts in",
                "Advanced Topics in", "Practical Applications of", "Problem Solving in",
                "Current Trends in", "Research Methods in", "Future Directions in"
            ]]
