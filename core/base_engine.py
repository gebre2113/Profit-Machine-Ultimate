import os
import sys
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import APIClient
from utils.data_processor import DataProcessor
from templates.version_templates import get_template_for_version

class UnifiedProfitEngine:
    """የሶስቱ ስሪቶችን በአንድ ስርዓት የሚያስተዳድር ማህበረሰብ እንጂን"""
    
    def __init__(self, version: str = "v9", config_path: str = "../master_config.json"):
        """
        ማህበረሰብ እንጂን የመጀመሪያ አደረጃጀት
        
        Args:
            version (str): የሚጠቀምበት ስሪት (v9, v10, v11)
            config_path (str): የቅንብር ፋይል መንገድ
        """
        self.version = version.lower()
        self.validate_version()
        
        # መሰረታዊ ቅንብሮች
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config = self.load_config(config_path)
        self.setup_logging()
        
        # የስሪት የተለየ ቅንብሮች
        self.version_config = self.config.get("version_configs", {}).get(self.version, {})
        self.output_dir = os.path.join(self.base_dir, self.version.upper())
        
        # የአገልግሎት ማህተምዎች
        self.templates = get_template_for_version(self.version)
        
        # ማስኬያዎች መጀመር
        self.api_client = APIClient(self.version, self.config)
        self.data_processor = DataProcessor(self.version)
        
        self.logger.info(f"🚀 {self.version.upper()} እንጂን ተጀምሯል")
    
    def validate_version(self):
        """የሚፈቀደውን ስሪት ያረጋግጣል"""
        valid_versions = ["v9", "v10", "v11"]
        if self.version not in valid_versions:
            raise ValueError(f"❌ ያልተረጋገጠ ስሪት: {self.version}. ተፈቅደው ያሉ: {valid_versions}")
    
    def load_config(self, config_path: str) -> Dict:
        """ቅንብር ፋይል ያነባል"""
        try:
            full_path = os.path.join(self.base_dir, config_path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    config = json.load(f)
                return config
            else:
                # መሰረታዊ ቅንብር ይፍጠር
                return self.create_default_config()
        except Exception as e:
            self.logger.error(f"ቅንብር ማንበብ አልተቻለም: {e}")
            return {}
    
    def create_default_config(self) -> Dict:
        """መሰረታዊ ቅንብር ይፈጥራል"""
        return {
            "version_configs": {
                "v9": {
                    "content_style": "simple",
                    "research_depth": "basic",
                    "output_format": "text",
                    "image_style": "illustrative"
                },
                "v10": {
                    "content_style": "enhanced",
                    "research_depth": "intermediate", 
                    "output_format": "html",
                    "image_style": "infographic"
                },
                "v11": {
                    "content_style": "enterprise",
                    "research_depth": "advanced",
                    "output_format": "markdown",
                    "image_style": "professional"
                }
            },
            "api_settings": {
                "timeout": 30,
                "retry_attempts": 3
            }
        }
    
    def setup_logging(self):
        """ለስሪቱ ምዝገባ ያዘጋጃል"""
        log_dir = os.path.join(self.base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{self.version}_engine.log")
        
        self.logger = logging.getLogger(f"ProfitEngine_{self.version}")
        self.logger.setLevel(logging.INFO)
        
        # ፋይል ሃንድለር
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # ኮንሶል ሃንድለር
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def process_topic(self, topic: str, country: str = "ET") -> Dict:
        """
        ዋናውን የስራ ሂደት ያስፈጽማል
        
        Args:
            topic (str): የሚተነትነው ርዕሰ ጉዳይ
            country (str): ሀገር (ምርጫ)
            
        Returns:
            Dict: የሂደቱ ውጤቶች
        """
        self.logger.info(f"📋 ሂደት የጀመረ ለ: {topic}")
        
        results = {
            "version": self.version,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress",
            "outputs": {}
        }
        
        try:
            # 1. ዳሰሳ
            research_data = self.gather_research(topic, country)
            results["research"] = research_data
            
            # 2. ይዘት ማመንጨት
            content = self.generate_content(topic, research_data)
            results["outputs"]["content"] = content
            
            # 3. ምስል ማመንጨት
            if self.version_config.get("image_style") != "none":
                image_url = self.generate_image(topic, research_data)
                results["outputs"]["image_url"] = image_url
            
            # 4. ለስሪት የተለየ ስራ
            if self.version == "v10":
                results["outputs"]["html_report"] = self.create_html_report(topic, content, research_data)
            elif self.version == "v11":
                results["outputs"]["strategy_doc"] = self.create_strategy_document(topic, content, research_data)
            
            # 5. ውጤቶችን ማስቀመጥ
            saved_files = self.save_outputs(topic, results["outputs"])
            results["saved_files"] = saved_files
            
            results["status"] = "completed"
            self.logger.info(f"✅ ሂደቱ ተጠናቋል ለ: {topic}")
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            self.logger.error(f"❌ ሂደቱ አልተሳካም: {e}")
        
        return results
    
    def gather_research(self, topic: str, country: str) -> Dict:
        """ለርዕሰ ጉዳዩ ዳሰሳ ያከናውናል"""
        self.logger.info(f"🔍 ዳሰሳ እየተካሄደ ነው: {topic}")
        
        research = {
            "news": [],
            "market_data": [],
            "trends": []
        }
        
        # የዜና ዳሰሳ
        try:
            news_results = self.api_client.fetch_news(topic, country)
            research["news"] = news_results[:5]  # ከ5 ዜናዎች በላይ አይውሰድ
        except Exception as e:
            self.logger.warning(f"የዜና ዳሰሳ አልተሳካም: {e}")
        
        # የገበያ መረጃ (ለ v10 እና v11)
        if self.version in ["v10", "v11"]:
            try:
                market_data = self.api_client.fetch_market_data(topic)
                research["market_data"] = market_data
            except Exception as e:
                self.logger.warning(f"የገበያ መረጃ አልተገኘም: {e}")
        
        # የተለያዩ መረጃዎችን ማስኬድ
        research = self.data_processor.process_research(research)
        
        return research
    
    def generate_content(self, topic: str, research_data: Dict) -> str:
        """ከጥናት መረጃ በመነሳት ይዘት ይፈጥራል"""
        self.logger.info(f"✍️ ይዘት እየተፈጠረ ነው: {topic}")
        
        template = self.templates["content"]
        
        # የጥናት መረጃን በማስኬድ ማቅረብ
        processed_research = self.data_processor.format_for_content(research_data)
        
        # የአይ ኤስ ጥያቄ መፍጠር
        prompt = template.format(
            topic=topic,
            research=processed_research,
            style=self.version_config.get("content_style", "standard")
        )
        
        # ይዘት ማመንጨት
        try:
            content = self.api_client.generate_ai_content(prompt)
            return content
        except Exception as e:
            self.logger.error(f"ይዘት ማመንጨት አልተቻለም: {e}")
            return self.templates["fallback_content"].format(topic=topic)
    
    def generate_image(self, topic: str, research_data: Dict) -> str:
        """ምስል የሚያመነጭ አገልግሎት ይጠቅማል"""
        self.logger.info(f"🎨 ምስል እየተፈጠረ ነው: {topic}")
        
        image_style = self.version_config.get("image_style", "illustrative")
        
        # ለስሪት የተለየ የምስል ማብራሪያ
        style_prompts = {
            "v9": "ቀላል ምስል",
            "v10": "ዝርዝር ማስተዋወቂያ",
            "v11": "የልምድ ምስል"
        }
        
        image_prompt = f"{topic} - {style_prompts.get(self.version, '')}"
        
        try:
            image_url = self.api_client.generate_image(image_prompt)
            return image_url
        except Exception as e:
            self.logger.warning(f"ምስል ማመንጨት አልተቻለም: {e}")
            # መረጃዊ ምስል ማጣቀሻ
            return f"https://via.placeholder.com/1200x600/4A90E2/FFFFFF?text={topic.replace(' ', '+')}"
    
    def create_html_report(self, topic: str, content: str, research_data: Dict) -> str:
        """ለ v10 ልዩ የ HTML ሪፖርት"""
        template = self.templates.get("html_template", "")
        
        html_content = template.format(
            title=topic,
            content=content,
            research_summary=str(len(research_data.get("news", []))),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        return html_content
    
    def create_strategy_document(self, topic: str, content: str, research_data: Dict) -> str:
        """ለ v11 የቢዝነስ ስትራቴጂ ሰነድ"""
        template = self.templates.get("strategy_template", "")
        
        strategy_doc = template.format(
            topic=topic,
            content=content,
            market_analysis=json.dumps(research_data.get("market_data", {}), indent=2),
            generated_date=datetime.now().strftime("%B %d, %Y")
        )
        
        return strategy_doc
    
    def save_outputs(self, topic: str, outputs: Dict) -> List[str]:
        """ሁሉንም ውጤቶች ይቀምጣል"""
        saved_files = []
        
        # የውጤት ፎልደር እንዳለ ያረጋግጡ
        os.makedirs(self.output_dir, exist_ok=True)
        
        base_filename = topic.lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for output_type, content in outputs.items():
            if output_type == "image_url":
                continue  # የምስል ዩአርኤል ብቻ መቀመጥ የለበትም
            
            # በፋይል አይነት ስም ይወስኑ
            if output_type == "html_report":
                filename = f"{base_filename}_report_{timestamp}.html"
            elif output_type == "strategy_doc":
                filename = f"{base_filename}_strategy_{timestamp}.md"
            else:
                filename = f"{base_filename}_{output_type}_{timestamp}.txt"
            
            filepath = os.path.join(self.output_dir, filename)
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(str(content))
                
                saved_files.append(filepath)
                self.logger.info(f"💾 ፋይል ተቀምጧል: {filename}")
            except Exception as e:
                self.logger.error(f"ፋይል ማስቀመጥ አልተቻለም {filename}: {e}")
        
        return saved_files
    
    def batch_process(self, topics: List[str], country: str = "ET") -> Dict:
        """
        ብዙ ርዕሰ ጉዳዮችን በቡድን ያካሂዳል
        
        Args:
            topics (List[str]): የሚተነትኑ ርዕሰ ጉዳዮች
            country (str): ሀገር
            
        Returns:
            Dict: የሁሉም ሂደቶች ውጤቶች
        """
        self.logger.info(f"📦 የቡድን ሂደት የጀመረ ለ {len(topics)} ርዕሰ ጉዳዮች")
        
        batch_results = {
            "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "version": self.version,
            "total_topics": len(topics),
            "processed": 0,
            "failed": 0,
            "results": []
        }
        
        for topic in topics:
            try:
                result = self.process_topic(topic, country)
                batch_results["results"].append(result)
                
                if result["status"] == "completed":
                    batch_results["processed"] += 1
                else:
                    batch_results["failed"] += 1
                    
            except Exception as e:
                self.logger.error(f"በቡድን ሂደት ላይ ስህተት ለ {topic}: {e}")
                batch_results["failed"] += 1
        
        # የቡድን ማጠቃለያ ማስቀመጥ
        summary_file = os.path.join(self.output_dir, f"batch_summary_{batch_results['batch_id']}.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📊 ቡድን ሂደት ተጠናቋል: {batch_results['processed']} ተሳክተዋል, {batch_results['failed']} አልተሳኩም")
        
        return batch_results
