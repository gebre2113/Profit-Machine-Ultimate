import os
import requests
import logging
import json
from urllib.parse import quote
from datetime import datetime

# Logging setup for tracking across all versions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("ProfitEngine")

class BaseProfitEngine:
    def __init__(self, config_path='master_config.json'):
        """
        ሶስቱንም ስሪቶች (v9, v10, v11) የሚያስተሳስር ማዕከላዊ ሞተር።
        """
        self.config = self._load_config(config_path)
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.news_key = os.getenv('NEWS_API_KEY')
        
        # API Endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def _load_config(self, path):
        """ከ master_config.json መረጃዎችን ያነባል"""
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Config ማምጣት አልተቻለም: {e}")
            return {}

    def fetch_research_data(self, topic, country='US'):
        """
        ለ v9 ዜና፣ ለ v11 ደግሞ የገበያ ዳሰሳ ያቀርባል።
        """
        logger.info(f"🔎 ምርምር እየተካሄደ ነው: {topic} in {country}")
        if not self.news_key:
            return "No real-time data available (Key missing)."

        try:
            url = f"https://newsapi.org/v2/everything?q={quote(topic)}&apiKey={self.news_key}"
            response = requests.get(url, timeout=10).json()
            articles = response.get('articles', [])[:3]
            return [f"{a['title']} - {a['source']['name']}" for a in articles]
        except Exception as e:
            logger.error(f"Research error: {e}")
            return []

    def generate_ai_content(self, topic, context_data, mode='standard'):
        """
        ለ v9 ቀላል ጽሁፍ፣ ለ v11 ደግሞ ውስብስብ የቢዝነስ ስትራቴጂ ይፈጥራል።
        mode: 'standard' (v9/v10), 'enterprise' (v11)
        """
        if not self.groq_key:
            return "Error: Missing GROQ_API_KEY"

        # ለ v11 የተለየና ጠንከር ያለ መመሪያ (Prompt)
        if mode == 'enterprise':
            system_prompt = "You are an Enterprise Business Strategist for V11."
            user_prompt = f"Create a high-level business strategy for {topic} using data: {context_data}. Include ROI analysis."
        else:
            system_prompt = "You are a Content Creator for V9/V10."
            user_prompt = f"Write an engaging article about {topic} based on: {context_data}."

        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        try:
            res = requests.post(self.groq_url, headers=headers, json=payload, timeout=30).json()
            return res['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"AI Generation error: {e}")
            return "AI content generation failed."

    def generate_image_url(self, topic):
        """ሶስቱም ስሪቶች የሚጠቀሙበት ነፃ የምስል ማመንጫ"""
        logger.info(f"🎨 ምስል እየተፈጠረ ነው ለ: {topic}")
        seed = datetime.now().microsecond
        return f"https://image.pollinations.ai/prompt/{quote(topic)}?width=1080&height=720&nologo=true&seed={seed}"

    def save_output(self, version_folder, filename, data):
        """
        ውጤቱን በሚመለከተው ፎልደር (V9, v10, ወይም v11) ውስጥ ያስቀምጣል።
        """
        path = os.path.join(version_folder, filename)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)
            logger.info(f"✅ ፋይል ተቀምጧል: {path}")
            return True
        except Exception as e:
            logger.error(f"ፋይል ማስቀመጥ አልተቻለም: {e}")
            return False
