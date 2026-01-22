"""
የተለያዩ ስሪቶች ለምዝገባ የሚጠቅም አገልግሎት
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional

class ProfitLogger:
    """የበርካታ ስሪቶችን ለማስተናገድ የሚረዳ ሎገር"""
    
    def __init__(self, version: str = "v9"):
        """
        የሎገር አደረጃጀት
        
        Args:
            version (str): የሚሰራበት ስሪት
        """
        self.version = version
        self.logger = self.setup_logger()
    
    def setup_logger(self) -> logging.Logger:
        """ሎገርን ለስራ ዝግጁ ያደርገዋል"""
        # ሎገር ስም መፍጠር
        logger_name = f"ProfitEngine_{self.version}"
        logger = logging.getLogger(logger_name)
        
        # ሎገር ደረጃ መስጠት
        logger.setLevel(logging.INFO)
        
        # የተለያዩ ሃንድለሮች እንዳሉ ያረጋግጡ
        if not logger.handlers:
            self._add_handlers(logger)
        
        return logger
    
    def _add_handlers(self, logger: logging.Logger):
        """ሎገር ሃንድለሮችን ይጨምራል"""
        # የሎግ ፎልደር መፍጠር
        log_dir = self._ensure_log_directory()
        
        # ለእያንዳንዱ ስሪት የተለየ የሎግ ፋይል
        log_file = os.path.join(log_dir, f"{self.version}_engine.log")
        
        # ፋይል ሃንድለር
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # ኮንሶል ሃንድለር
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # ሃንድለሮችን መጨመር
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    def _ensure_log_directory(self) -> str:
        """ሎግ ፎልደር እንዳለ ያረጋግጣል"""
        # የአጭር መንገድ ማግኘት
        if getattr(sys, 'frozen', False):
            # ከተጠናከረ ፕሮግራም ከሆነ
            base_dir = os.path.dirname(sys.executable)
        else:
            # ከፓይቶን ስክሪፕት ከሆነ
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        return log_dir
    
    def info(self, message: str):
        """መረጃ ሎግ ያከናውናል"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """ማስጠንቀቂያ ሎግ ያከናውናል"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """ስህተት ሎግ ያከናውናል"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """የማረጋገጫ ሎግ ያከናውናል"""
        self.logger.debug(message)
    
    def log_operation(self, operation: str, status: str, details: Optional[str] = None):
        """የኦፔሬሽን ሎግ ያከናውናል"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] {operation} - {status}"
        
        if details:
            message += f" | {details}"
        
        if status.lower() in ['success', 'completed']:
            self.info(message)
        elif status.lower() in ['warning', 'partial']:
            self.warning(message)
        else:
            self.error(message)

# ለቀላል መጠቀም የሚረዳ አገልግሎት ተግባር
def get_logger(version: str = "v9") -> ProfitLogger:
    """
    የሎገር አገልግሎት ይመልሳል
    
    Args:
        version (str): የሚሰራበት ስሪት
        
    Returns:
        ProfitLogger: የሎገር አገልግሎት
    """
    return ProfitLogger(version)

# የማያቋርጥ አገልግሎት
global_logger = ProfitLogger("system")
