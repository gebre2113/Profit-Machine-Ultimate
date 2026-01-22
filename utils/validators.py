"""
ለተለያዩ ስሪቶች የማረጋገጫ አገልግሎቶች
"""

import os
import re
import json
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse
import logging

class Validators:
    """ለተለያዩ መረጃዎች የማረጋገጫ አገልግሎት"""
    
    def __init__(self, version: str = "v9"):
        """
        የቫሊዴተር አደረጃጀት
        
        Args:
            version (str): የሚሰራበት ስሪት
        """
        self.version = version
        self.logger = logging.getLogger(f"Validator_{version}")
    
    def validate_version(self, version: str) -> Tuple[bool, str]:
        """
        የስሪት ስምን ያረጋግጣል
        
        Args:
            version (str): የሚፈቀደው ስሪት
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        valid_versions = ["v9", "v10", "v11"]
        
        if version.lower() in valid_versions:
            return True, f"ስሪት {version} ተረጋግጧል"
        else:
            return False, f"ያልተረጋገጠ ስሪት: {version}. ተፈቅደው ያሉት: {valid_versions}"
    
    def validate_topic(self, topic: str) -> Tuple[bool, str]:
        """
        የርዕሰ ጉዳይ ስምን ያረጋግጣል
        
        Args:
            topic (str): የሚፈቀደው ርዕሰ ጉዳይ
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        if not topic or not isinstance(topic, str):
            return False, "ርዕሰ ጉዳይ ባዶ ሊሆን አይችልም"
        
        # ርዝመት ማረጋገጫ
        if len(topic) < 2:
            return False, "ርዕሰ ጉዳይ በጣም አጭር ነው (ከ2 ቁምፊዎች በላይ መሆን አለበት)"
        
        if len(topic) > 200:
            return False, "ርዕሰ ጉዳይ በጣም ረጅም ነው (ከ200 ቁምፊዎች በላይ መሆን አይፈቀድም)"
        
        # የሚፈቀዱ ቁምፊዎች ማረጋገጫ
        if re.search(r'[<>:"|?*]', topic):
            return False, "ርዕሰ ጉዳይ የማይፈቀዱ ቁምፊዎችን ይዟል"
        
        return True, "ርዕሰ ጉዳይ ተረጋግጧል"
    
    def validate_country(self, country: str) -> Tuple[bool, str]:
        """
        የሀገር ስምን ያረጋግጣል
        
        Args:
            country (str): የሚፈቀደው ሀገር ኮድ
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        # የተመቻቸ የሀገር ኮዶች
        valid_countries = ['ET', 'US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'CN', 'IN']
        
        if not country or not isinstance(country, str):
            return False, "ሀገር ባዶ ሊሆን አይችልም"
        
        country_upper = country.upper()
        
        if country_upper in valid_countries:
            return True, f"ሀገር {country_upper} ተረጋግጧል"
        else:
            # ለሌሎች ሀገራት ምርመራ
            if len(country) == 2 and country.isalpha():
                return True, f"ሀገር {country_upper} ተቀባይነት አለው"
            else:
                return False, f"ያልተረጋገጠ የሀገር ኮድ: {country}"
    
    def validate_api_key(self, key_type: str, key_value: str) -> Tuple[bool, str]:
        """
        የኤፒአይ ቁልፍን ያረጋግጣል
        
        Args:
            key_type (str): የኤፒአይ ቁልፍ አይነት
            key_value (str): የኤፒአይ ቁልፍ
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        if not key_value or not isinstance(key_value, str):
            return False, f"{key_type} ቁልፍ ባዶ ነው"
        
        # የቁልፍ ርዝመት ማረጋገጫ
        min_lengths = {
            'GROQ_API_KEY': 30,
            'NEWS_API_KEY': 30,
            'SERPER_API_KEY': 20
        }
        
        min_length = min_lengths.get(key_type, 10)
        
        if len(key_value) < min_length:
            return False, f"{key_type} ቁልፍ በጣም አጭር ነው"
        
        # መሰረታዊ ቅርፅ ማረጋገጫ
        if key_type == 'GROQ_API_KEY' and key_value.startswith('gsk_'):
            return True, "GROQ ቁልፍ ተረጋግጧል"
        elif key_type == 'NEWS_API_KEY' and len(key_value) == 32:
            return True, "የዜና ቁልፍ ተረጋግጧል"
        elif key_type == 'SERPER_API_KEY' and key_value.isalnum():
            return True, "Serper ቁልፍ ተረጋግጧል"
        else:
            # አጠቃላይ ማረጋገጫ
            return True, f"{key_type} ቁልፍ ተቀባይነት አለው"
    
    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        URLን ያረጋግጣል
        
        Args:
            url (str): የሚፈቀደው URL
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        if not url or not isinstance(url, str):
            return False, "URL ባዶ ነው"
        
        try:
            result = urlparse(url)
            
            # መሰረታዊ URL መዋቅር ማረጋገጫ
            if all([result.scheme, result.netloc]):
                return True, "URL ተረጋግጧል"
            else:
                return False, "URL ትክክለኛ መዋቅር የለውም"
                
        except Exception:
            return False, "URL ማረጋገጫ አልተቻለም"
    
    def validate_file_path(self, filepath: str, check_exists: bool = True) -> Tuple[bool, str]:
        """
        የፋይል መንገድን ያረጋግጣል
        
        Args:
            filepath (str): የፋይሉ መንገድ
            check_exists (bool): ፋይሉ እንዳለ ይፈትሽ
            
        Returns:
            Tuple[bool, str]: (ማረጋገጫ ውጤት, መልእክት)
        """
        if not filepath or not isinstance(filepath, str):
            return False, "የፋይል መንገድ ባዶ ነው"
        
        # የማይፈቀዱ ቁምፊዎች ማረጋገጫ
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in filepath:
                return False, f"የፋይል መንገድ የማይፈቀዱ ቁምፊዎችን ይዟል: {char}"
        
        # ርዝመት ማረጋገጫ
        if len(filepath) > 260:
            return False, "የፋይል መንገድ በጣም ረጅም ነው"
        
        # ፋይሉ እንዳለ ማረጋገጫ
        if check_exists and not os.path.exists(filepath):
            return False, "ፋይሉ አልተገኘም"
        
        return True, "የፋይል መንገድ ተረጋግጧል"
    
    def validate_json(self, json_string: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        JSON ገመድን ያረጋግጣል
        
        Args:
            json_string (str): የሚፈቀደው JSON ገመድ
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (ማረጋገጫ ውጤት, መልእክት, JSON መረጃ)
        """
        if not json_string or not isinstance(json_string, str):
            return False, "JSON ገመድ ባዶ ነው", None
        
        try:
            data = json.loads(json_string)
            return True, "JSON ተረጋግጧል", data
        except json.JSONDecodeError as e:
            return False, f"JSON ማረጋገጫ አልተቻለም: {e}", None
    
    def validate_batch_input(self, topics: List[str]) -> Tuple[bool, str, List[str]]:
        """
        የቡድን ግብዓትን ያረጋግጣል
        
        Args:
            topics (List[str]): የሚፈቀዱ ርዕሰ ጉዳዮች
            
        Returns:
            Tuple[bool, str, List[str]]: (ማረጋገጫ ውጤት, መልእክት, የተረጋገጡ ርዕሰ ጉዳዮች)
        """
        if not topics or not isinstance(topics, list):
            return False, "የቡድን ግብዓት ባዶ ወይም ትክክለኛ አይደለም", []
        
        if len(topics) == 0:
            return False, "የቡድን ግብዓት ባዶ ነው", []
        
        # የርዕሰ ጉዳዮች ብዛት ማረጋገጫ
        max_topics = {
            'v9': 10,
            'v10': 20,
            'v11': 50
        }
        
        max_allowed = max_topics.get(self.version, 10)
        
        if len(topics) > max_allowed:
            return False, f"የበለጠ ርዕሰ ጉዳዮች አሉ: {len(topics)} > {max_allowed}", []
        
        # እያንዳንዱን ርዕሰ ጉዳይ ማረጋገጫ
        valid_topics = []
        invalid_topics = []
        
        for topic in topics:
            is_valid, message = self.validate_topic(topic)
            if is_valid:
                valid_topics.append(topic)
            else:
                invalid_topics.append(f"{topic}: {message}")
        
        if invalid_topics:
            error_message = f"{len(invalid_topics)} ርዕሰ ጉዳዮች ልክ አልያዙም: {', '.join(invalid_topics[:3])}"
            if len(invalid_topics) > 3:
                error_message += "..."
            return False, error_message, valid_topics
        
        return True, f"ሁሉም {len(valid_topics)} ርዕሰ ጉዳዮች ተረጋግጠዋል", valid_topics
    
    def validate_config(self, config: Dict) -> Tuple[bool, str, Dict]:
        """
        የቅንብር መረጃን ያረጋግጣል
        
        Args:
            config (Dict): የሚፈቀደው ቅንብር
            
        Returns:
            Tuple[bool, str, Dict]: (ማረጋገጫ ውጤት, መልእክት, የተረጋገጠ ቅንብር)
        """
        if not config or not isinstance(config, dict):
            return False, "ቅንብር ባዶ ወይም ትክክለኛ አይደለም", {}
        
        required_keys = ['version_configs', 'api_settings']
        
        for key in required_keys:
            if key not in config:
                return False, f"ማለፊያ ቁልፍ በቅንብር ውስጥ የለም: {key}", {}
        
        # የስሪት ቅንብሮችን ማረጋገጫ
        version_configs = config.get('version_configs', {})
        
        for version in ['v9', 'v10', 'v11']:
            if version not in version_configs:
                self.logger.warning(f"ስሪት {version} በቅንብር ውስጥ የለም")
        
        return True, "ቅንብር ተረጋግጧል", config

# ለቀላል መጠቀም የሚረዳ አገልግሎት ተግባር
def get_validator(version: str = "v9") -> Validators:
    """
    የቫሊዴተር አገልግሎት ይመልሳል
    
    Args:
        version (str): የሚሰራበት ስሪት
        
    Returns:
        Validators: የቫሊዴተር አገልግሎት
    """
    return Validators(version)

# ፈጣን ማረጋገጫ ተግባራት
def quick_validate_topic(topic: str) -> bool:
    """ፈጣን ርዕሰ ጉዳይ ማረጋገጫ"""
    validator = Validators()
    is_valid, _ = validator.validate_topic(topic)
    return is_valid

def quick_validate_version(version: str) -> bool:
    """ፈጣን ስሪት ማረጋገጫ"""
    validator = Validators()
    is_valid, _ = validator.validate_version(version)
    return is_valid
