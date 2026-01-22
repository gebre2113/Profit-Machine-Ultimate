"""
የፋይል ስራዎችን ለማስተዳደር የሚረዳ አገልግሎት
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import logging

class FileManager:
    """የተለያዩ ፋይሎችን ለማስተዳደር የሚረዳ አገልግሎት"""
    
    def __init__(self, version: str = "v9"):
        """
        የፋይል ማኔጅር አደረጃጀት
        
        Args:
            version (str): የሚሰራበት ስሪት
        """
        self.version = version
        self.base_dir = self._get_base_directory()
        self.setup_directories()
        self.logger = logging.getLogger(f"FileManager_{version}")
    
    def _get_base_directory(self) -> str:
        """የመሰረት ፎልደር ያገኛል"""
        import sys
        
        if getattr(sys, 'frozen', False):
            # ከተጠናከረ ፕሮግራም ከሆነ
            base_dir = os.path.dirname(sys.executable)
        else:
            # ከፓይቶን ስክሪፕት ከሆነ
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        return base_dir
    
    def setup_directories(self):
        """ሁሉንም አስፈላጊ ፎልደሮች ያፈጥራል"""
        directories = [
            self.version.upper(),  # ለስሪቱ የውጤት ፎልደር
            os.path.join("data", "processed"),
            os.path.join("data", "raw"),
            os.path.join("data", "exports"),
            "temp",
            "backup"
        ]
        
        for directory in directories:
            full_path = os.path.join(self.base_dir, directory)
            os.makedirs(full_path, exist_ok=True)
    
    def save_content(self, filename: str, content: str, subfolder: Optional[str] = None) -> str:
        """
        ይዘት ወደ ፋይል ይቀምጣል
        
        Args:
            filename (str): የፋይል ስም
            content (str): የሚቀመጠ ይዘት
            subfolder (str, optional): የተወሰነ ንዑስ ፎልደር
            
        Returns:
            str: የተሰራው ፋይል መንገድ
        """
        try:
            # የፋይል ስም ማጽዳት
            clean_filename = self._clean_filename(filename)
            
            # የፋይል ስምን ሙሉ ማድረግ
            full_filename = self._generate_filename(clean_filename)
            
            # የፋይል መንገድ መወሰን
            if subfolder:
                file_dir = os.path.join(self.base_dir, self.version.upper(), subfolder)
            else:
                file_dir = os.path.join(self.base_dir, self.version.upper())
            
            os.makedirs(file_dir, exist_ok=True)
            
            filepath = os.path.join(file_dir, full_filename)
            
            # ፋይል መፍጠር
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"ፋይል ተቀምጧል: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"ፋይል ማስቀመጥ አልተቻለም: {e}")
            raise
    
    def save_json(self, filename: str, data: Dict, subfolder: Optional[str] = None) -> str:
        """
        JSON መረጃ ወደ ፋይል ይቀምጣል
        
        Args:
            filename (str): የፋይል ስም
            data (Dict): የሚቀመጠ JSON መረጃ
            subfolder (str, optional): የተወሰነ ንዑስ ፎልደር
            
        Returns:
            str: የተሰራው ፋይል መንገድ
        """
        try:
            json_content = json.dumps(data, indent=2, ensure_ascii=False)
            return self.save_content(filename, json_content, subfolder)
        except Exception as e:
            self.logger.error(f"JSON መቀመጥ አልተቻለም: {e}")
            raise
    
    def read_file(self, filepath: str) -> str:
        """
        ፋይል ያነባል
        
        Args:
            filepath (str): የፋይሉ መንገድ
            
        Returns:
            str: የፋይሉ ይዘት
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"ፋይል ማንበብ አልተቻለም: {e}")
            raise
    
    def read_json(self, filepath: str) -> Dict:
        """
        JSON ፋይል ያነባል
        
        Args:
            filepath (str): የፋይሉ መንገድ
            
        Returns:
            Dict: የ JSON መረጃ
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"JSON ፋይል ማንበብ አልተቻለም: {e}")
            raise
    
    def list_files(self, subfolder: Optional[str] = None, extension: Optional[str] = None) -> List[str]:
        """
        የተወሰነ ፎልደር ውስጥ ያሉ ፋይሎችን ይዘረዝራል
        
        Args:
            subfolder (str, optional): ንዑስ ፎልደር
            extension (str, optional): የፋይል ማያያዣ
            
        Returns:
            List[str]: የፋይሎች ዝርዝር
        """
        try:
            if subfolder:
                folder_path = os.path.join(self.base_dir, self.version.upper(), subfolder)
            else:
                folder_path = os.path.join(self.base_dir, self.version.upper())
            
            if not os.path.exists(folder_path):
                return []
            
            files = []
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    if extension:
                        if item.endswith(extension):
                            files.append(item_path)
                    else:
                        files.append(item_path)
            
            return files
            
        except Exception as e:
            self.logger.error(f"ፋይሎችን ማውጣት አልተቻለም: {e}")
            return []
    
    def delete_file(self, filepath: str):
        """
        ፋይል ያጥፋል
        
        Args:
            filepath (str): የፋይሉ መንገድ
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(f"ፋይል ተሰርዟል: {filepath}")
        except Exception as e:
            self.logger.error(f"ፋይል መሰረዝ አልተቻለም: {e}")
    
    def cleanup_old_files(self, days: int = 7, subfolder: Optional[str] = None):
        """
        የቆዩ ፋይሎችን ያጥፋል
        
        Args:
            days (int): የተፈቀደው የቀን ብዛት
            subfolder (str, optional): ንዑስ ፎልደር
        """
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            files = self.list_files(subfolder)
            
            deleted_count = 0
            for filepath in files:
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_time < cutoff_date:
                    self.delete_file(filepath)
                    deleted_count += 1
            
            self.logger.info(f"{deleted_count} የቆዩ ፋይሎች ተሰርዘዋል")
            
        except Exception as e:
            self.logger.error(f"ንቁ ፋይሎችን ማጽዳት አልተቻለም: {e}")
    
    def _clean_filename(self, filename: str) -> str:
        """ፋይል ስምን ለማጽዳት ይጠቅማል"""
        # የማይፈቀዱ ቁምፊዎችን መለወጥ
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        clean_name = filename
        
        for char in invalid_chars:
            clean_name = clean_name.replace(char, '_')
        
        # ማለፊያ ቦታዎችን ማጥፋት
        clean_name = clean_name.strip()
        
        # ርዝመትን መገደብ
        if len(clean_name) > 200:
            clean_name = clean_name[:200]
        
        return clean_name
    
    def _generate_filename(self, base_name: str) -> str:
        """ለፋይል ስም ተስማሚ ስም ይፈጥራል"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # የፋይል ማያያዣ መጨመር
        if '.' not in base_name:
            base_name = f"{base_name}_{timestamp}.txt"
        else:
            # የቀድሞ ማያያዣ መጠበቅ
            name_parts = base_name.rsplit('.', 1)
            base_name = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
        
        return base_name
    
    def backup_files(self, backup_name: str = None):
        """
        ፋይሎችን የአጠቃቀም ጊዜ ይጠብቃል
        
        Args:
            backup_name (str): የአጠቃቀም ጊዜ ስም
        """
        try:
            if not backup_name:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            source_dir = os.path.join(self.base_dir, self.version.upper())
            backup_dir = os.path.join(self.base_dir, "backup", backup_name)
            
            if os.path.exists(source_dir):
                shutil.copytree(source_dir, backup_dir)
                self.logger.info(f"አጠቃቀም ጊዜ ተሰርቷል: {backup_dir}")
                return backup_dir
            else:
                self.logger.warning("ለአጠቃቀም ጊዜ ምንም ፋይሎች አልተገኙም")
                return None
                
        except Exception as e:
            self.logger.error(f"አጠቃቀም ጊዜ ማድረግ አልተቻለም: {e}")
            return None

# ለቀላል መጠቀም የሚረዳ አገልግሎት ተግባር
def get_file_manager(version: str = "v9") -> FileManager:
    """
    የፋይል ማኔጅር አገልግሎት ይመልሳል
    
    Args:
        version (str): የሚሰራበት ስሪት
        
    Returns:
        FileManager: የፋይል ማኔጅር አገልግሎት
    """
    return FileManager(version)
