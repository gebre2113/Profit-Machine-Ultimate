"""
Core/base_engine.py - የሶስቱ ስሪቶች ማዕከላዊ ሞተር (Universal Engine)
ለ V9 (ቀላል ስራ)፣ v10 (ኦቶሜሽን) እና v11 (ላቀ ቢዝነስ ትንተና) የሚሰራ
"""

import os
import sys
import requests
import logging
import json
from urllib.parse import quote
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import hashlib
import time

# Logging setup for tracking across all versions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('profit_engine.log'),
        logging.StreamHandler()
    ]
)

class BaseProfitEngine:
    """ሶስቱንም ስሪቶች (v9, v10, v11) የሚያስተሳስር ማዕከላዊ ሞተር"""
    
    # Version-specific constants
    VERSION_CONFIG = {
        'v9': {
            'mode': 'standard',
            'research_level': 'basic',
            'content_type': 'article',
            'image_style': 'simple',
            'max_articles': 3,
            'timeout': 15
        },
        'v10': {
            'mode': 'enhanced',
            'research_level': 'intermediate',
            'content_type': 'enhanced_article',
            'image_style': 'infographic',
            'max_articles': 5,
            'timeout': 20
        },
        'v11': {
            'mode': 'enterprise',
            'research_level': 'advanced',
            'content_type': 'business_strategy',
            'image_style': 'professional',
            'max_articles': 8,
            'timeout': 30
        }
    }
    
    def __init__(self, version: str = 'v9', config_path: str = 'master_config.json'):
        """
        ማዕከላዊ ሞተር መጀመሪያ አደረጃጀት
        
        Args:
            version (str): የሚጠቀምበት ስሪት (v9, v10, v11)
            config_path (str): የቅንብር ፋይል መንገድ
        """
        self.version = self._validate_version(version)
        self.logger = logging.getLogger(f"ProfitEngine_{self.version.upper()}")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Load API keys
        self._load_api_keys()
        
        # Set version-specific configuration
        self.version_config = self.VERSION_CONFIG.get(self.version, self.VERSION_CONFIG['v9'])
        
        # API Endpoints
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.news_url = "https://newsapi.org/v2/everything"
        
        # Cache for API responses
        self.cache = {}
        
        # Statistics tracking
        self.stats = {
            'api_calls': 0,
            'articles_fetched': 0,
            'content_generated': 0,
            'images_created': 0,
            'errors': 0
        }
        
        self.logger.info(f"🚀 {self.version.upper()} ሞተር ተጀምሯል")
    
    def _validate_version(self, version: str) -> str:
        """የስሪት ስምን ያረጋግጣል"""
        valid_versions = ['v9', 'v10', 'v11']
        version_lower = version.lower()
        
        if version_lower not in valid_versions:
            self.logger.warning(f"ያልተረጋገጠ ስሪት: {version}. የሚፈቀደው v9, v10, v11 ብቻ ነው")
            return 'v9'
        
        return version_lower
    
    def _load_config(self, path: str) -> Dict:
        """ከ master_config.json መረጃዎችን ያነባል"""
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"✅ ቅንብር ተጭኗል ከ: {path}")
                
                # Merge version-specific config
                if self.version in config.get('version_overrides', {}):
                    config.update(config['version_overrides'][self.version])
                
                return config
            else:
                self.logger.warning(f"ቅንብር ፋይል አልተገኘም: {path}")
                return self._create_default_config()
        except Exception as e:
            self.logger.error(f"Config ማምጣት አልተቻለም: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """መሰረታዊ ቅንብር ይፈጥራል"""
        return {
            'api_settings': {
                'max_retries': 3,
                'cache_duration': 3600,  # 1 hour
                'rate_limit_delay': 1
            },
            'content_settings': {
                'max_length': 2000,
                'min_length': 300,
                'language': 'amharic'
            },
            'version_overrides': {
                'v9': {'simple_mode': True},
                'v10': {'automation': True},
                'v11': {'enterprise_features': True}
            }
        }
    
    def _load_api_keys(self):
        """ከአካባቢ ተለዋዋጮች ኤፒአይ ቁልፎችን ያነባል"""
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.news_key = os.getenv('NEWS_API_KEY')
        self.serper_key = os.getenv('SERPER_API_KEY')  # ለ v10/v11 ተጨማሪ ዳሰሳ
        
        # Validate API keys
        if not self.groq_key:
            self.logger.warning("GROQ_API_KEY አልተገኘም. የአይ አይ ይዘት ማመንጨት አይሰራም")
        
        if not self.news_key:
            self.logger.warning("NEWS_API_KEY አልተገኘም. የዜና ዳሰሳ አይሰራም")
    
    def _get_cache_key(self, func_name: str, *args) -> str:
        """ለካሽ የተለየ ቁልፍ ይፈጥራል"""
        key_string = f"{func_name}_{self.version}_{'_'.join(str(arg) for arg in args)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[Any]:
        """ካሽ ውስጥ ያለውን ውጤት ያወጣል"""
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if datetime.now() < cache_entry['expires']:
                self.logger.debug(f"ካሽ ውጤት ተገኘ: {cache_key}")
                return cache_entry['data']
            else:
                # ያለፈ ካሽ ማጥፋት
                del self.cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, data: Any, duration: int = 3600):
        """ውጤትን በካሽ ውስጥ ያስቀምጣል"""
        expires = datetime.now() + timedelta(seconds=duration)
        self.cache[cache_key] = {
            'data': data,
            'expires': expires,
            'created': datetime.now()
        }
        self.logger.debug(f"ውጤት በካሽ ተቀምጧል: {cache_key}")
    
    def fetch_research_data(self, topic: str, country: str = 'US') -> Dict[str, List]:
        """
        የተዋሃደ ዳሰሳ ዘዴ - ለሶስቱም ስሪቶች
        
        Args:
            topic (str): የሚፈለገው ርዕሰ ጉዳይ
            country (str): ሀገር (ምርጫ)
            
        Returns:
            Dict: የዳሰሳ ውጤቶች በተለያዩ ክፍሎች
        """
        cache_key = self._get_cache_key('research', topic, country)
        cached_result = self._check_cache(cache_key)
        
        if cached_result:
            return cached_result
        
        self.logger.info(f"🔎 ምርምር እየተካሄደ ነው: {topic} in {country}")
        self.stats['api_calls'] += 1
        
        research_data = {
            'news': [],
            'market_data': [],
            'trends': [],
            'statistics': {}
        }
        
        # 1. News API Research (ለሶስቱም ስሪቶች)
        if self.news_key:
            try:
                url = f"{self.news_url}?q={quote(topic)}&apiKey={self.news_key}&pageSize=10"
                response = requests.get(url, timeout=self.version_config['timeout'])
                
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    max_articles = self.version_config['max_articles']
                    
                    for article in articles[:max_articles]:
                        research_data['news'].append({
                            'title': article.get('title', 'No title'),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'description': article.get('description', '')[:200],
                            'url': article.get('url', ''),
                            'date': article.get('publishedAt', ''),
                            'relevance_score': self._calculate_relevance(topic, article.get('title', ''))
                        })
                    
                    self.stats['articles_fetched'] += len(research_data['news'])
                    self.logger.info(f"📰 {len(research_data['news'])} ዜናዎች ተገኝተዋል")
                else:
                    self.logger.warning(f"የዜና ኤፒአይ ስህተት: {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"Research error: {e}")
                self.stats['errors'] += 1
        
        # 2. Additional market research for v10 and v11
        if self.version in ['v10', 'v11']:
            research_data.update(self._fetch_market_data(topic, country))
        
        # 3. Version-specific enhancements
        if self.version == 'v11':
            research_data['statistics'] = self._generate_statistics(research_data)
        
        # Cache the results
        self._save_to_cache(cache_key, research_data, duration=7200)  # 2 hours
        
        return research_data
    
    def _fetch_market_data(self, topic: str, country: str) -> Dict:
        """የገበያ መረጃ ያገኛል (ለ v10/v11)"""
        market_data = {
            'market_size': 'በግምት',
            'growth_rate': 'በግምት',
            'competitors': [],
            'opportunities': []
        }
        
        # ይህን ክፍል በእውነተኛ የገበያ ዳታ ኤፒአይ መሙላት ይቻላል
        if self.serper_key:
            try:
                # Serper API for market data (example)
                serper_url = "https://google.serper.dev/search"
                headers = {'X-API-KEY': self.serper_key}
                payload = {
                    "q": f"{topic} market size {country} 2024",
                    "num": 5
                }
                
                response = requests.post(serper_url, json=payload, headers=headers, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    # Process market data here
                    pass
                    
            except Exception as e:
                self.logger.debug(f"Market data fetch failed: {e}")
        
        return market_data
    
    def _calculate_relevance(self, topic: str, text: str) -> float:
        """የጽሁፍ ግንኙነት ደረጃ ያሰላል"""
        topic_words = set(topic.lower().split())
        text_words = set(text.lower().split())
        
        if not topic_words or not text_words:
            return 0.0
        
        intersection = topic_words.intersection(text_words)
        return len(intersection) / len(topic_words)
    
    def _generate_statistics(self, research_data: Dict) -> Dict:
        """ስታቲስቲክስ ይፈጥራል (ለ v11)"""
        stats = {
            'total_sources': len(research_data.get('news', [])),
            'avg_relevance': 0,
            'date_range': '',
            'source_diversity': 0
        }
        
        if research_data.get('news'):
            relevance_scores = [item.get('relevance_score', 0) for item in research_data['news']]
            stats['avg_relevance'] = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
            
            sources = set(item.get('source', '') for item in research_data['news'])
            stats['source_diversity'] = len(sources)
        
        return stats
    
    def generate_ai_content(self, topic: str, context_data: Dict, mode: str = None) -> str:
        """
        የአይ አይ ይዘት ይፈጥራል - ለሶስቱም ስሪቶች
        
        Args:
            topic (str): የሚፈለገው ርዕሰ ጉዳይ
            context_data (Dict): የዳሰሳ መረጃ
            mode (str): የማመንጨት ሁነታ (standard/enterprise)
            
        Returns:
            str: የተመነጨው ይዘት
        """
        if not self.groq_key:
            return "ስህተት: GROQ_API_KEY አልተገኘም"
        
        # Determine mode based on version if not specified
        if mode is None:
            mode = 'enterprise' if self.version == 'v11' else 'standard'
        
        cache_key = self._get_cache_key('ai_content', topic, mode, str(context_data)[:100])
        cached_result = self._check_cache(cache_key)
        
        if cached_result:
            return cached_result
        
        self.logger.info(f"🤖 AI ይዘት እየተፈጠረ ነው ለ: {topic} (ሁነታ: {mode})")
        self.stats['api_calls'] += 1
        
        # Prepare prompts based on version and mode
        system_prompt, user_prompt = self._prepare_prompts(topic, context_data, mode)
        
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        
        # Model selection based on version
        model_mapping = {
            'v9': 'llama3-8b-8192',
            'v10': 'mixtral-8x7b-32768',
            'v11': 'llama3-70b-8192'
        }
        
        payload = {
            "model": model_mapping.get(self.version, 'llama3-8b-8192'),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7 if self.version == 'v9' else 0.5,
            "max_tokens": 1024 if self.version == 'v9' else 2048 if self.version == 'v10' else 4096
        }
        
        try:
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Post-process content based on version
                content = self._post_process_content(content, mode)
                
                self.stats['content_generated'] += 1
                self.logger.info(f"✅ AI ይዘት ተፈጥሯል ({len(content)} ቁምፊዎች)")
                
                # Cache the result
                self._save_to_cache(cache_key, content, duration=10800)  # 3 hours
                
                return content
            else:
                error_msg = f"API ስህተት: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                self.stats['errors'] += 1
                return error_msg
                
        except Exception as e:
            error_msg = f"AI ማመንጨት ላይ ስህተት: {e}"
            self.logger.error(error_msg)
            self.stats['errors'] += 1
            return error_msg
    
    def _prepare_prompts(self, topic: str, context_data: Dict, mode: str) -> tuple:
        """ለተለያዩ ሁነታዎች የሚሆን ፕሮምፕት ያዘጋጃል"""
        
        if mode == 'enterprise':
            system_prompt = """አንተ የኢንተርፕራይዝ ደረጃ የቢዝነስ ስትራቴጂስት ነህ። 
            ለከፍተኛ አስተዳዳሪዎች የሚሆን ዝርዝር የቢዝነስ ስትራቴጂ ፍጠር።
            የሚከተሉትን አካትፍ:
            1. የፈጣን ማጠቃለያ
            2. የገበያ ትንተና
            3. SWOT ትንተና
            4. ROI ፕሮጀክሽን
            5. የግብዓት እቅድ"""
            
            user_prompt = f"""ለ'{topic}' የኢንተርፕራይዝ ደረጃ የቢዝነስ ስትራቴጂ ፍጠር።

የዳሰሳ መረጃዎች:
{json.dumps(context_data, indent=2, ensure_ascii=False)[:2000]}

የቢዝነስ ስትራቴጂው ዝርዝር፣ በውሂብ የተደገፈ እና ለመተግበር አግባብ ያለው መሆን አለበት።"""
        
        elif mode == 'enhanced':
            system_prompt = """አንተ የቢዝነስ ትንተና ሊቅ ነህ።
            የተሻሻለ የቢዝነስ ጽሁፍ ፍጠር ከጥልቀት ያለው ትንተና ጋር።
            አስፈላጊ የቢዝነስ ሃሳቦችን አካትፍ።"""
            
            user_prompt = f"""ስለ '{topic}' ዝርዝር የቢዝነስ ትንተና ጽሁፍ ፍጠር።

የዳሰሳ መረጃ:
{json.dumps(context_data.get('news', []), indent=2, ensure_ascii=False)[:1500]}

ጽሁፉ ለንግድ ሰዎች አገልግሎት የሚያቀርብ እና አግባብ ያሉ ሃሳቦችን መያዝ አለበት።"""
        
        else:  # standard mode
            system_prompt = """አንተ ብሩህ እና ማንበብ ቀላል የሆኑ ጽሁፎችን የምትጽፍ የዜና ጸሐፊ ነህ።
            በአዲስ አበባ ላይ ያለ የቢዝነስ ሰው ለሚያነብ አይነት ግልጽ እና አስተማሪ ጽሁፎችን ፍጠር።"""
            
            user_prompt = f"""ስለ '{topic}' ቀላል እና ለሁሉም የሚታወቅ ጽሁፍ ፍጠር።

የዜና መረጃ:
{json.dumps([{'title': item.get('title', ''), 'source': item.get('source', '')} 
             for item in context_data.get('news', [])[:3]], indent=2, ensure_ascii=False)}

ጽሁፉ አጭር፣ ግልጽ እና አስደሳች መሆን አለበት።"""
        
        return system_prompt, user_prompt
    
    def _post_process_content(self, content: str, mode: str) -> str:
        """የተመነጨውን ይዘት በስሪት መሠረት ያስተካክላል"""
        
        # Add headers based on version
        if mode == 'enterprise':
            header = f"# የቢዝነስ ስትራቴጂ ሰነድ\n## ቀን: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            footer = "\n\n---\n*ይህ ሰነድ በ ProfitEngine V11 ተፈጥሯል*"
            content = header + content + footer
            
        elif mode == 'enhanced':
            header = f"## የቢዝነስ ትንተና: {datetime.now().strftime('%B %d, %Y')}\n\n"
            content = header + content
            
        # Add Amharic formatting if needed
        if self.config.get('content_settings', {}).get('language') == 'amharic':
            # Ensure proper Amharic formatting
            content = content.replace('?', '፧').replace('!', '፥')
        
        return content
    
    def generate_image_url(self, topic: str, style: str = None) -> str:
        """
        ምስል የሚያመነጭ አገልግሎት ይጠቅማል
        
        Args:
            topic (str): የሚፈለገው ርዕሰ ጉዳይ
            style (str): የምስል ዘይቤ (ምርጫ)
            
        Returns:
            str: የምስሉ URL
        """
        if style is None:
            style = self.version_config['image_style']
        
        self.logger.info(f"🎨 ምስል እየተፈጠረ ነው ለ: {topic} (ዘይቤ: {style})")
        self.stats['images_created'] += 1
        
        # Prepare image prompt based on version and style
        image_prompts = {
            'simple': f"simple illustration of {topic}, clean, minimal",
            'infographic': f"business infographic about {topic}, data visualization, professional",
            'professional': f"enterprise business concept for {topic}, executive style, high quality"
        }
        
        prompt = image_prompts.get(style, topic)
        
        # Add version-specific enhancements
        if self.version == 'v11':
            prompt = f"professional business strategy diagram: {prompt}"
        
        # Generate unique seed
        seed = datetime.now().microsecond + hash(topic) % 1000000
        
        # Use multiple image service options for fallback
        image_services = [
            f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1200&height=800&nologo=true&seed={seed}",
            f"https://api.placeholder.ai/v1/image?text={quote(prompt[:50])}&width=1200&height=800",
            f"https://dummyimage.com/1200x800/3498db/ffffff&text={quote(prompt[:30])}"
        ]
        
        return image_services[0]  # Return primary service
    
    def save_output(self, filename: str, data: str, version_folder: str = None) -> Dict:
        """
        ውጤቱን በሚመለከተው ፎልደር ውስጥ ያስቀምጣል
        
        Args:
            filename (str): የፋይሉ ስም
            data (str): የሚቀመጠ ውሂብ
            version_folder (str): የስሪቱ ፎልደር (ምርጫ)
            
        Returns:
            Dict: የማስቀመጢያ ውጤት
        """
        if version_folder is None:
            version_folder = self.version.upper()
        
        # Create version folder if it doesn't exist
        os.makedirs(version_folder, exist_ok=True)
        
        # Clean filename
        safe_filename = self._clean_filename(filename)
        
        # Add timestamp and extension
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{safe_filename}_{timestamp}.txt"
        
        path = os.path.join(version_folder, final_filename)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)
            
            self.logger.info(f"✅ ፋይል ተቀምጧል: {path}")
            
            return {
                'success': True,
                'path': path,
                'filename': final_filename,
                'size': len(data),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"ፋይል ማስቀመጥ አልተቻለም: {e}")
            self.stats['errors'] += 1
            
            return {
                'success': False,
                'error': str(e),
                'path': path
            }
    
    def save_json_output(self, filename: str, data: Dict, version_folder: str = None) -> Dict:
        """
        JSON ውሂብን ያስቀምጣል
        
        Args:
            filename (str): የፋይሉ ስም
            data (Dict): የሚቀመጥ JSON ውሂብ
            version_folder (str): የስሪቱ ፎልደር (ምርጫ)
            
        Returns:
            Dict: የማስቀመጢያ ውጤት
        """
        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            return self.save_output(filename, json_data, version_folder)
        except Exception as e:
            self.logger.error(f"JSON ማስቀመጥ አልተቻለም: {e}")
            return {'success': False, 'error': str(e)}
    
    def _clean_filename(self, filename: str) -> str:
        """ፋይል ስምን ለማጽዳት ይጠቅማል"""
        # Remove invalid characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Trim and limit length
        filename = filename.strip()
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename
    
    def run_complete_pipeline(self, topic: str, country: str = 'US') -> Dict:
        """
        ሙሉውን የስራ ሂደት ያስፈጽማል
        
        Args:
            topic (str): የሚተነትነው ርዕሰ ጉዳይ
            country (str): ሀገር
            
        Returns:
            Dict: የሙሉው ሂደት ውጤት
        """
        self.logger.info(f"🚀 የሙሉ ፋይል ሂደት ጀመረ ለ: {topic}")
        
        start_time = time.time()
        
        result = {
            'version': self.version,
            'topic': topic,
            'country': country,
            'timestamp': datetime.now().isoformat(),
            'pipeline_steps': {},
            'outputs': {},
            'statistics': self.stats.copy()
        }
        
        try:
            # Step 1: Research
            result['pipeline_steps']['research'] = 'started'
            research_data = self.fetch_research_data(topic, country)
            result['pipeline_steps']['research'] = 'completed'
            result['research_summary'] = {
                'news_count': len(research_data.get('news', [])),
                'market_data': len(research_data.get('market_data', [])),
                'trends': len(research_data.get('trends', []))
            }
            
            # Step 2: Content Generation
            result['pipeline_steps']['content_generation'] = 'started'
            mode = 'enterprise' if self.version == 'v11' else 'enhanced' if self.version == 'v10' else 'standard'
            content = self.generate_ai_content(topic, research_data, mode)
            result['pipeline_steps']['content_generation'] = 'completed'
            result['outputs']['content'] = content[:500] + "..." if len(content) > 500 else content
            
            # Step 3: Image Generation
            result['pipeline_steps']['image_generation'] = 'started'
            image_url = self.generate_image_url(topic)
            result['pipeline_steps']['image_generation'] = 'completed'
            result['outputs']['image_url'] = image_url
            
            # Step 4: Save Content
            result['pipeline_steps']['saving'] = 'started'
            save_result = self.save_output(topic, content)
            result['pipeline_steps']['saving'] = 'completed'
            result['outputs']['saved_file'] = save_result
            
            # Step 5: Save Research Data (for v10 and v11)
            if self.version in ['v10', 'v11']:
                research_save = self.save_json_output(f"{topic}_research", research_data)
                result['outputs']['research_file'] = research_save
            
            # Step 6: Generate report for v11
            if self.version == 'v11':
                report = self._generate_comprehensive_report(topic, content, research_data, image_url)
                report_save = self.save_output(f"{topic}_comprehensive_report", report)
                result['outputs']['comprehensive_report'] = report_save
            
            result['pipeline_steps']['overall'] = 'completed'
            result['success'] = True
            
            elapsed_time = time.time() - start_time
            result['execution_time'] = f"{elapsed_time:.2f} ሰከንድ"
            
            self.logger.info(f"✅ ፋይል ሂደቱ ተጠናቋል በ {elapsed_time:.2f} ሰከንድ")
            
        except Exception as e:
            result['pipeline_steps']['overall'] = 'failed'
            result['success'] = False
            result['error'] = str(e)
            self.logger.error(f"❌ ፋይል ሂደቱ አልተሳካም: {e}")
        
        return result
    
    def _generate_comprehensive_report(self, topic: str, content: str, research_data: Dict, image_url: str) -> str:
        """ለ v11 ዝርዝር ሪፖርት ይፈጥራል"""
        report = f"""# የቢዝነስ ስትራቴጂ ሪፖርት
## ርዕሰ ጉዳይ: {topic}
## የተፈጠረበት ቀን: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## ስሪት: {self.version.upper()}

---

## 1. የጥናት ማጠቃለያ
- ጠቅላላ የዜና ምንጮች: {len(research_data.get('news', []))}
- የገበያ መረጃዎች: {len(research_data.get('market_data', []))}
- የግንዛቤ ደረጃ: {research_data.get('statistics', {}).get('avg_relevance', 0):.2f}

---

## 2. የቢዝነስ ስትራቴጂ
{content}

---

## 3. የምስል ማጣቀሻ
![Business Strategy]({image_url})

---

## 4. የስርዓት ስታቲስቲክስ
- የኤፒአይ ጥሪዎች: {self.stats['api_calls']}
- የተገኙ ዜናዎች: {self.stats['articles_fetched']}
- የተፈጠሩ የይዘት ቁምፊዎች: {self.stats['content_generated']}
- ስህተቶች: {self.stats['errors']}

---

*ይህ ሪፖርት በ ProfitEngine V11 ተፈጥሯል*
"""
        return report
    
    def get_statistics(self) -> Dict:
        """የአሁኑን ስታቲስቲክስ ያሳያል"""
        return {
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'statistics': self.stats,
            'cache_size': len(self.cache),
            'config_version': self.config.get('version', '1.0')
        }
    
    def clear_cache(self):
        """ካሽ ያጽዳል"""
        self.cache.clear()
        self.logger.info("✅ ካሽ ተጽድቋል")

# Utility function for easy import
def create_engine(version: str = 'v9', config_path: str = 'master_config.json') -> BaseProfitEngine:
    """
    ሞተር ለመፍጠር ቀላል ተግባር
    
    Args:
        version (str): የሚፈልጉት ስሪት
        config_path (str): የቅንብር ፋይል መንገድ
        
    Returns:
        BaseProfitEngine: የተፈጠረ ሞተር
    """
    return BaseProfitEngine(version=version, config_path=config_path)

# Example usage
if __name__ == "__main__":
    # Test the engine
    engine = BaseProfitEngine(version='v11')
    
    # Run complete pipeline
    result = engine.run_complete_pipeline("የኢትዮጵያ የቴክ ኢንዱስትሪ", country="ET")
    
    print(f"ስሪት: {result['version']}")
    print(f"ርዕሰ ጉዳይ: {result['topic']}")
    print(f"ሁኔታ: {'✅ ተሳክቷል' if result.get('success') else '❌ አልተሳካም'}")
    print(f"ሰዓት: {result.get('execution_time', 'N/A')}")
    print(f"የዜናዎች ብዛት: {result.get('research_summary', {}).get('news_count', 0)}")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\n📊 ስታቲስቲክስ:")
    print(f"  የኤፒአይ ጥሪዎች: {stats['statistics']['api_calls']}")
    print(f"  የተፈጠሩ ይዘቶች: {stats['statistics']['content_generated']}")
