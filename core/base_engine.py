import os
import requests
import json
import logging
from urllib.parse import quote
from datetime import datetime

# የምዝግብ ማስታወሻ (Logging) አወቃቀር
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseProfitEngine:
    """
    የ PROFIT MACHINE v9 ዋና ኢንጂን።
    ይህ ክፍል መረጃን የመሰብሰብ፣ ይዘት የመፍጠር እና ምስል የማመንጨት ኃላፊነት አለበት።
    """
    
    def __init__(self, groq_api_key=None, news_api_key=None):
        # ቁልፎችን ከአካባቢ ተለዋዋጮች (Environment Variables) ወይም በቀጥታ ይቀበላል
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        self.news_api_key = news_api_key or os.getenv('NEWS_API_KEY')
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def fetch_market_insights(self, topic: str):
        """ደረጃ 1፡ ወቅታዊ መረጃዎችን ከ NewsAPI በነፃ መሰብሰብ"""
        if not self.news_api_key:
            logger.warning("NewsAPI Key አልተገኘም! ያለ ወቅታዊ መረጃ እቀጥላለሁ።")
            return []

        try:
            url = f"https://newsapi.org/v2/everything?q={quote(topic)}&sortBy=relevancy&pageSize=5&apiKey={self.news_api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                insights = [f"{a['title']}: {a['description']}" for a in articles if a['title']]
                logger.info(f"✅ {len(insights)} የገበያ መረጃዎች ተገኝተዋል።")
                return insights
            return []
        except Exception as e:
            logger.error(f"❌ መረጃ ሲፈለግ ስህተት አጋጥሟል፡ {e}")
            return []

    def generate_professional_content(self, topic: str, insights: list):
        """ደረጃ 2፡ በ Groq (Llama 3) አማካኝነት ጥራት ያለው ጽሁፍ መፍጠር"""
        if not self.groq_api_key:
            return "ስህተት፡ GROQ_API_KEY አልተገኘም።"

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        # AI ይዘቱን እንዲያዘጋጅ የሚሰጥ መመሪያ (Prompt)
        context = "\n".join(insights) if insights else "General market trends."
        prompt = f"""
        እንደ ባለሙያ ቢዝነስ ጸሐፊ በመሆን ስለ '{topic}' ጥልቅ ትንተና ጻፍ።
        የሚከተሉትን ነጥቦች ተጠቀም፦
        {context}
        
        መስፈርቶች፦
        - ርዕሱ ማራኪ ይሁን።
        - በ HTML ፎርማት (h2, p, ul, li) ተጠቀም።
        - ቢያንስ 5 ተግባራዊ ሊሆኑ የሚችሉ ምክሮችን (Actionable Steps) አካትት።
        - ቋንቋው ፕሮፌሽናል ይሁን።
        """

        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)
            result = response.json()
            content = result['choices'][0]['message']['content']
            logger.info("✅ የ AI ይዘት በስኬት ተፈጥሯል።")
            return content
        except Exception as e:
            logger.error(f"❌ ይዘት ሲፈጠር ስህተት አጋጥሟል፡ {e}")
            return "ይዘቱን መፍጠር አልተቻለም።"

    def create_visual_asset(self, topic: str):
        """ደረጃ 3፡ በ Pollinations.ai አማካኝነት ነፃ እና ጥራት ያለው ምስል ማግኘት"""
        try:
            # ምስሉን ይበልጥ ፕሮፌሽናል ለማድረግ የተጨመሩ ቁልፍ ቃላት
            enhanced_prompt = quote(f"Professional high-quality business cover for {topic}, digital art, cinematic lighting")
            image_url = f"https://image.pollinations.ai/prompt/{enhanced_prompt}?width=1280&height=720&nologo=true&seed={datetime.now().microsecond}"
            logger.info("✅ ምስል በስኬት ተዘጋጅቷል።")
            return image_url
        except Exception as e:
            logger.error(f"❌ ምስል ሲዘጋጅ ስህተት አጋጥሟል፡ {e}")
            return "https://via.placeholder.com/1280x720?text=No+Image+Available"

    def compile_report(self, topic: str):
        """ሁሉንም ክፍሎች በማቀናጀት የመጨረሻውን ውጤት ማምረት"""
        logger.info(f"🚀 የ '{topic}' ሪፖርት ዝግጅት ተጀምሯል...")
        
        insights = self.fetch_market_insights(topic)
        content = self.generate_professional_content(topic, insights)
        image_url = self.create_visual_asset(topic)
        
        final_html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd;">
            <img src="{image_url}" alt="{topic}" style="width: 100%; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: #2c3e50;">{topic}</h1>
            <div style="color: #34495e;">
                {content}
            </div>
            <hr>
            <p style="font-size: 0.8em; color: #7f8c8d;">ሪፖርቱ የተፈጠረው በ Profit Machine v9 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """
        return final_html

# ለሙከራ (በቀጥታ ፋይሉ ሲከፈት የሚሰራ)
if __name__ == "__main__":
    # እዚህ ጋር ቁልፎችህን ለሙከራ ማስገባት ትችላለህ
    engine = BaseProfitEngine()
    # result = engine.compile_report("AI in E-commerce")
    # print(result)
