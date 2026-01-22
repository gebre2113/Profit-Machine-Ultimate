"""
የተሻሻለ የአንድነት እንጂን - ከአዲሶቹ utils ሞጁሎች ጋር የተዋሃደ
"""

import os
import sys
import json
from typing import Dict, List, Optional
from datetime import datetime

# የወላጅ ፎልደር መጨመር ለኢምፖርቶች
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ከአዲሶቹ utils ሞጁሎች ኢምፖርት
from utils import get_logger, get_file_manager, get_validator
from utils.logger import ProfitLogger
from utils.file_manager import FileManager
from utils.validators import Validators

# ሌሎች ኢምፖርቶች
from templates.version_templates import get_template_for_version

class EnhancedUnifiedEngine:
    """የተሻሻለ የአንድነት እንጂን - ከአዲስ አገልግሎቶች ጋር"""
    
    def __init__(self, version: str = "v9", config_path: str = "../master_config.json"):
        """
        የተሻሻለ እንጂን አደረጃጀት
        
        Args:
            version (str): የሚጠቀምበት ስሪት
            config_path (str): የቅንብር ፋይል መንገድ
        """
        # መጀመሪያ ማረጋገጫዎች
        self.validator = get_validator(version)
        is_valid, message = self.validator.validate_version(version)
        
        if not is_valid:
            raise ValueError(f"ስሪት ማረጋገጫ አልተቻለም: {message}")
        
        self.version = version.lower()
        
        # መሰረታዊ ቅንብሮች
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # አገልግሎቶችን መጀመር
        self.logger = get_logger(version)
        self.file_manager = get_file_manager(version)
        
        # ቅንብር መጫን
        self.config = self._load_config(config_path)
        
        # የስሪት የተለየ ቅንብሮች
        self.version_config = self.config.get("version_configs", {}).get(self.version, {})
        
        # አብነቶች
        self.templates = get_template_for_version(self.version)
        
        # የ API ክላስ ኢምፖርት (ከቀድሞ ኮድ)
        from utils.api_client import APIClient
        self.api_client = APIClient(self.version, self.config)
        
        self.logger.info(f"🚀 {self.version.upper()} እንጂን ተጀምሯል")
    
    def _load_config(self, config_path: str) -> Dict:
        """ቅንብር ፋይል ያነባል"""
        try:
            full_path = os.path.join(self.base_dir, config_path)
            
            # የፋይል መንገድ ማረጋገጫ
            is_valid, message = self.validator.validate_file_path(full_path, check_exists=True)
            
            if is_valid:
                with open(full_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # የቅንብር ማረጋገጫ
                is_config_valid, message, validated_config = self.validator.validate_config(config)
                
                if is_config_valid:
                    self.logger.info("✅ ቅንብር ተጭኗል እና ተረጋግጧል")
                    return validated_config
                else:
                    self.logger.warning(f"ቅንብር ማረጋገጫ አልተቻለም: {message}")
                    return config
            else:
                self.logger.warning(f"የቅንብር ፋይል ማረጋገጫ አልተቻለም: {message}")
                return self._create_default_config()
                
        except Exception as e:
            self.logger.error(f"ቅንብር ማንበብ አልተቻለም: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """መሰረታዊ ቅንብር ይፈጥራል"""
        self.logger.info("መሰረታዊ ቅንብር እየተፈጠረ ነው...")
        
        return {
            "version_configs": {
                "v9": {
                    "content_style": "simple",
                    "research_depth": "basic",
                    "output_format": "text",
                    "image_style": "illustrative",
                    "max_research_items": 5
                },
                "v10": {
                    "content_style": "enhanced",
                    "research_depth": "intermediate",
                    "output_format": "html",
                    "image_style": "infographic",
                    "max_research_items": 10
                },
                "v11": {
                    "content_style": "enterprise",
                    "research_depth": "advanced",
                    "output_format": "markdown",
                    "image_style": "professional",
                    "max_research_items": 20
                }
            },
            "api_settings": {
                "timeout": 30,
                "retry_attempts": 3,
                "cache_enabled": True
            },
            "system_settings": {
                "auto_backup": True,
                "cleanup_days": 7,
                "max_file_size": "10MB"
            }
        }
    
    def process_topic(self, topic: str, country: str = "ET") -> Dict:
        """
        የሂደቱን ዋና ክፍል ያስፈጽማል
        
        Args:
            topic (str): የሚተነትነው ርዕሰ ጉዳይ
            country (str): ሀገር
            
        Returns:
            Dict: የሂደቱ ውጤቶች
        """
        # የግብዓት ማረጋገጫ
        topic_valid, topic_message = self.validator.validate_topic(topic)
        country_valid, country_message = self.validator.validate_country(country)
        
        if not topic_valid:
            return {
                "status": "failed",
                "error": f"ርዕሰ ጉዳይ ማረጋገጫ አልተቻለም: {topic_message}"
            }
        
        if not country_valid:
            self.logger.warning(f"ሀገር ማረጋገጫ አልተቻለም: {country_message}")
            # ሀገሩ ባይረጋገጥም ሊቀጥል ይችላል
        
        self.logger.log_operation("ሂደት መጀመር", "started", f"ርዕሰ ጉዳይ: {topic}")
        
        results = {
            "version": self.version,
            "topic": topic,
            "country": country,
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress",
            "validation": {
                "topic": topic_valid,
                "country": country_valid
            },
            "outputs": {},
            "file_paths": []
        }
        
        try:
            # 1. ዳሰሳ
            self.logger.log_operation("ዳሰሳ", "started")
            research_data = self.gather_research(topic, country)
            results["research"] = research_data
            self.logger.log_operation("ዳሰሳ", "completed", f"{len(research_data.get('news', []))} ዜናዎች")
            
            # 2. ይዘት ማመንጨት
            self.logger.log_operation("ይዘት ማመንጨት", "started")
            content = self.generate_content(topic, research_data)
            results["outputs"]["content"] = content
            self.logger.log_operation("ይዘት ማመንጨት", "completed", f"{len(content)} ቁምፊዎች")
            
            # 3. ምስል ማመንጨት
            if self.version_config.get("image_style") != "none":
                self.logger.log_operation("ምስል ማመንጨት", "started")
                image_url = self.generate_image(topic, research_data)
                results["outputs"]["image_url"] = image_url
                self.logger.log_operation("ምስል ማመንጨት", "completed")
            
            # 4. ለስሪት የተለየ ስራ
            if self.version == "v10":
                self.logger.log_operation("HTML ሪፖርት", "started")
                results["outputs"]["html_report"] = self.create_html_report(topic, content, research_data)
                self.logger.log_operation("HTML ሪፖርት", "completed")
            elif self.version == "v11":
                self.logger.log_operation("የቢዝነስ ስትራቴጂ", "started")
                results["outputs"]["strategy_doc"] = self.create_strategy_document(topic, content, research_data)
                self.logger.log_operation("የቢዝነስ ስትራቴጂ", "completed")
            
            # 5. ውጤቶችን ማስቀመጥ
            self.logger.log_operation("ፋይል ማስቀመጥ", "started")
            saved_files = self.save_outputs(topic, results["outputs"])
            results["file_paths"] = saved_files
            self.logger.log_operation("ፋይል ማስቀመጥ", "completed", f"{len(saved_files)} ፋይሎች")
            
            results["status"] = "completed"
            self.logger.log_operation("ሙሉ ሂደት", "completed")
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            self.logger.log_operation("ሂደት", "failed", str(e))
        
        return results
    
    # ... (ሌሎች ዘዴዎች ከቀድሞ ኮድ ጋር ተመሳሳይ ናቸው)
    
    def save_outputs(self, topic: str, outputs: Dict) -> List[str]:
        """ሁሉንም ውጤቶች ይቀምጣል"""
        saved_files = []
        
        for output_type, content in outputs.items():
            if output_type == "image_url":
                continue
            
            # የፋይል ስም መወሰን
            if output_type == "html_report":
                filename = f"{topic}_report"
                subfolder = "reports"
            elif output_type == "strategy_doc":
                filename = f"{topic}_strategy"
                subfolder = "strategies"
            elif output_type == "content":
                filename = f"{topic}_content"
                subfolder = "contents"
            else:
                filename = f"{topic}_{output_type}"
                subfolder = "other"
            
            try:
                filepath = self.file_manager.save_content(filename, str(content), subfolder)
                saved_files.append(filepath)
            except Exception as e:
                self.logger.error(f"ውጤት ማስቀመጥ አልተቻለም {output_type}: {e}")
        
        # የቡድን ማጠቃለያ ማስቀመጥ
        if saved_files:
            summary = {
                "topic": topic,
                "version": self.version,
                "files": saved_files,
                "generated_at": datetime.now().isoformat()
            }
            
            try:
                summary_file = self.file_manager.save_json(f"{topic}_summary", summary, "summaries")
                saved_files.append(summary_file)
            except Exception as e:
                self.logger.error(f"ማጠቃለያ ማስቀመጥ አልተቻለም: {e}")
        
        return saved_files
    
    def batch_process(self, topics: List[str], country: str = "ET") -> Dict:
        """
        ብዙ ርዕሰ ጉዳዮችን በቡድን ያካሂዳል
        """
        # የቡድን ግብዓት ማረጋገጫ
        is_valid, message, valid_topics = self.validator.validate_batch_input(topics)
        
        if not is_valid:
            self.logger.error(f"የቡድን ግብዓት ማረጋገጫ አልተቻለም: {message}")
            return {
                "status": "failed",
                "error": message,
                "valid_topics": valid_topics
            }
        
        self.logger.info(f"📦 የቡድን ሂደት እየተካሄደ ነው ለ {len(valid_topics)} ርዕሰ ጉዳዮች")
        
        batch_results = {
            "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "version": self.version,
            "total_topics": len(valid_topics),
            "processed": 0,
            "failed": 0,
            "results": []
        }
        
        for index, topic in enumerate(valid_topics, 1):
            self.logger.info(f"📝 እየሰራሁ ነው ({index}/{len(valid_topics)}): {topic}")
            
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
            
            # በመካከል አጥጋቢ ጊዜ ማስቀመጥ
            if index % 5 == 0:
                self.file_manager.backup_files(f"batch_backup_{index}")
        
        # የቡድን ማጠቃለያ ማስቀመጥ
        summary_file = self.file_manager.save_json(
            f"batch_summary_{batch_results['batch_id']}",
            batch_results,
            "batch_summaries"
        )
        
        self.logger.info(f"📊 ቡድን ሂደት ተጠናቋል: {batch_results['processed']} ተሳክተዋል, {batch_results['failed']} አልተሳኩም")
        
        return batch_results
