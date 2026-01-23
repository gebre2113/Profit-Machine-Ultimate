#!/usr/bin/env python3
"""
Telegram Reporter - የቴሌግራም ማሳወቂያ እና ሪፖርት ሞጁል
ለ Profit Machine Enterprise ስርዓት የሚጠቅም
"""

import os
import sys
import json
import requests
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import time
import base64
from io import BytesIO

class TelegramReporter:
    """የቴሌግራም ማሳወቂያ እና ሪፖርት አገልግሎት"""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        ቴሌግራም ሪፖርተር መጀመሪያ አደረጃጀት
        
        Args:
            bot_token (str): የቴሌግራም ቦት ቶከን
            chat_id (str): የቻት መለያ
        """
        # ከአካባቢ ተለዋዋጮች ወይም ቀጥተኛ ማስገባት ማንበብ
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        
        # የኤፒአይ መሰረታዊ ዩአርኤል
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # ማስተዳደር
        self.logger = self._setup_logger()
        
        # ስታቲስቲክስ
        self.stats = {
            'messages_sent': 0,
            'errors': 0,
            'last_sent': None,
            'total_characters': 0
        }
        
        # የመላኪያ ክልል (rate limit)
        self.rate_limit_delay = 1  # ሰከንድ
        self.last_send_time = 0
        
        if not self.bot_token or not self.chat_id:
            self.logger.warning("የቴሌግራም ቁልፎች አልተገኙም. ቴሌግራም ማሳወቂያ አይሰራም.")
    
    def _setup_logger(self) -> logging.Logger:
        """ሎገር ያዘጋጃል"""
        logger = logging.getLogger("TelegramReporter")
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def _check_credentials(self) -> bool:
        """የቴሌግራም ምስክር ነክ ውሂቦችን ያረጋግጣል"""
        if not self.bot_token or not self.chat_id:
            self.logger.error("የቴሌግራም ቦት ቶከን ወይም ቻት መለያ አልተገኘም")
            return False
        
        # ቦቱ እንዳለ ማረጋገጥ
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    self.logger.info(f"ቴሌግራም ቦት ተረጋግጧል: @{data['result']['username']}")
                    return True
                else:
                    self.logger.error(f"ቴሌግራም ቦት ማረጋገጫ አልተቻለም: {data.get('description')}")
                    return False
            else:
                self.logger.error(f"የቴሌግራም ኤፒአይ ስህተት: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"የቴሌግራም ቦት ማረጋገጫ አልተቻለም: {e}")
            return False
    
    def _rate_limit(self):
        """የመላኪያ ክልልን ይቆጣጠራል"""
        current_time = time.time()
        time_since_last = current_time - self.last_send_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_send_time = time.time()
    
    def send_message(self, 
                    text: str, 
                    parse_mode: str = 'Markdown',
                    disable_web_page_preview: bool = True,
                    silent: bool = False) -> Dict:
        """
        ቀላል መልዕክት ይልካል
        
        Args:
            text (str): የሚላክ ጽሁፍ
            parse_mode (str): የጽሁፍ ቅርፅ (Markdown, HTML, ወይም None)
            disable_web_page_preview (bool): የድረ-ገጽ ቅድመ እይታ መደበቅ
            silent (bool): ሳይድ ማሳወቂያ
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        if not self._check_credentials():
            return {'ok': False, 'error': 'Credentials missing'}
        
        self._rate_limit()
        
        # የጽሁፍ ርዝመትን መገደብ (Telegram ገደብ 4096 ቁምፊዎች)
        if len(text) > 4000:
            text = text[:4000] + "...\n\n[ጽሁፉ ተቆርጧል]"
        
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': silent
        }
        
        if parse_mode:
            payload['parse_mode'] = parse_mode
        
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=30
            )
            
            result = response.json()
            
            if result.get('ok'):
                self.stats['messages_sent'] += 1
                self.stats['total_characters'] += len(text)
                self.stats['last_sent'] = datetime.now().isoformat()
                self.logger.info(f"መልዕክት ተልኳል: {len(text)} ቁምፊዎች")
            else:
                self.stats['errors'] += 1
                self.logger.error(f"መልዕክት መላክ አልተቻለም: {result.get('description')}")
            
            return result
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"መልዕክት መላክ ላይ ስህተት: {e}")
            return {'ok': False, 'error': str(e)}
    
    def send_document(self, 
                     document_path: str,
                     caption: str = "",
                     filename: str = None) -> Dict:
        """
        ፋይል ይልካል
        
        Args:
            document_path (str): የፋይሉ መንገድ
            caption (str): የፋይሉ መግለጫ
            filename (str): የፋይሉ ስም (ምርጫ)
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        if not self._check_credentials():
            return {'ok': False, 'error': 'Credentials missing'}
        
        if not os.path.exists(document_path):
            self.logger.error(f"ፋይል አልተገኘም: {document_path}")
            return {'ok': False, 'error': 'File not found'}
        
        self._rate_limit()
        
        if not filename:
            filename = os.path.basename(document_path)
        
        try:
            with open(document_path, 'rb') as file:
                files = {
                    'document': (filename, file)
                }
                
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption[:1024]  # Telegram caption limit
                }
                
                response = requests.post(
                    f"{self.base_url}/sendDocument",
                    data=data,
                    files=files,
                    timeout=60
                )
                
                result = response.json()
                
                if result.get('ok'):
                    self.stats['messages_sent'] += 1
                    self.logger.info(f"ፋይል ተልኳል: {filename}")
                else:
                    self.stats['errors'] += 1
                    self.logger.error(f"ፋይል መላክ አልተቻለም: {result.get('description')}")
                
                return result
                
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"ፋይል መላክ ላይ ስህተት: {e}")
            return {'ok': False, 'error': str(e)}
    
    def send_photo(self, 
                  photo_url: str,
                  caption: str = "",
                  filename: str = "image.jpg") -> Dict:
        """
        ምስል ይልካል
        
        Args:
            photo_url (str): የምስሉ ዩአርኤል
            caption (str): የምስሉ መግለጫ
            filename (str): የምስሉ ስም
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        if not self._check_credentials():
            return {'ok': False, 'error': 'Credentials missing'}
        
        self._rate_limit()
        
        try:
            # ምስሉን ከዩአርኤል መውሰድ
            response = requests.get(photo_url, timeout=30)
            
            if response.status_code != 200:
                self.logger.error(f"ምስል ማውሰድ አልተቻለም: {photo_url}")
                return {'ok': False, 'error': 'Failed to download image'}
            
            # ምስሉን እንደ ፋይል መላክ
            files = {
                'photo': (filename, BytesIO(response.content))
            }
            
            data = {
                'chat_id': self.chat_id,
                'caption': caption[:1024]
            }
            
            response = requests.post(
                f"{self.base_url}/sendPhoto",
                data=data,
                files=files,
                timeout=60
            )
            
            result = response.json()
            
            if result.get('ok'):
                self.stats['messages_sent'] += 1
                self.logger.info(f"ምስል ተልኳል: {filename}")
            else:
                self.stats['errors'] += 1
                self.logger.error(f"ምስል መላክ አልተቻለም: {result.get('description')}")
            
            return result
            
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"ምስል መላክ ላይ ስህተት: {e}")
            return {'ok': False, 'error': str(e)}
    
    def send_run_report(self, 
                       run_data: Dict,
                       include_stats: bool = True,
                       include_files: bool = False) -> List[Dict]:
        """
        የስራ ሪፖርት ይልካል
        
        Args:
            run_data (Dict): የስራ መረጃ
            include_stats (bool): ስታቲስቲክስ አካታ
            include_files (bool): ፋይሎችን አካታ
            
        Returns:
            List[Dict]: የሁሉም የተላኩ መልዕክቶች ውጤቶች
        """
        messages = []
        
        # 1. የመጀመሪያ መልዕክት - ማጠቃለያ
        summary_text = self._format_run_summary(run_data)
        result = self.send_message(summary_text, parse_mode='Markdown')
        messages.append(result)
        
        # 2. ዝርዝር መረጃ (ከፈለግክ)
        if include_stats and run_data.get('statistics'):
            stats_text = self._format_statistics(run_data.get('statistics', {}))
            result = self.send_message(stats_text, parse_mode='Markdown')
            messages.append(result)
        
        # 3. ፋይሎች (ከፈለግክ)
        if include_files and run_data.get('output_files'):
            for file_path in run_data.get('output_files', []):
                if os.path.exists(file_path):
                    result = self.send_document(file_path, "የስራ ውጤት")
                    messages.append(result)
                    time.sleep(0.5)  # ትንሽ ጊዜ ማጥፋት
        
        return messages
    
    def _format_run_summary(self, run_data: Dict) -> str:
        """የስራ ማጠቃለያን በቴሌግራም ቅርጽ ያዘጋጃል"""
        version = run_data.get('version', 'Unknown')
        topic = run_data.get('topic', 'Unknown')
        success = run_data.get('success', False)
        error = run_data.get('error')
        execution_time = run_data.get('execution_time', 0)
        timestamp = run_data.get('timestamp', datetime.now().isoformat())
        
        # የኢሞጂ መምረጫ
        status_emoji = "✅" if success else "❌"
        
        # የቀን ቅርጸት
        try:
            date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
        except:
            formatted_date = timestamp
        
        # Markdown ጽሁፍ መፍጠር
        text = f"""
🤖 *Profit Machine {version.upper()} Run Report*
{status_emoji} *Status:* {'Success' if success else 'Failed'}
📅 *Date:* {formatted_date}
⏱️ *Duration:* {execution_time:.2f} seconds

📝 *Topic:* {topic}

"""
        
        if not success and error:
            text += f"""
⚠️ *Error Details:*
`{error[:500]}{'...' if len(error) > 500 else ''}`
"""
        
        # የውጤት መረጃ
        if run_data.get('outputs'):
            text += "\n📊 *Outputs Generated:*\n"
            outputs = run_data.get('outputs', {})
            
            if outputs.get('content'):
                content_preview = outputs['content'][:100] + "..." if len(outputs['content']) > 100 else outputs['content']
                text += f"• Content: {len(outputs['content'])} characters\n"
            
            if outputs.get('image_url'):
                text += f"• Image: ✅ Generated\n"
            
            if outputs.get('saved_file', {}).get('path'):
                text += f"• File: `{outputs['saved_file']['path']}`\n"
        
        text += f"\n🔗 *System ID:* `{run_data.get('run_id', 'N/A')}`"
        
        return text
    
    def _format_statistics(self, stats: Dict) -> str:
        """ስታቲስቲክስን በቴሌግራም ቅርጽ ያዘጋጃል"""
        text = """
📈 *System Statistics*

*API Usage:*
• API Calls: {api_calls}
• Articles Fetched: {articles_fetched}
• Content Generated: {content_generated}
• Images Created: {images_created}
• Errors: {errors}

*Performance:*
• Cache Size: {cache_size}
• Last Updated: {last_updated}
""".format(
            api_calls=stats.get('api_calls', 0),
            articles_fetched=stats.get('articles_fetched', 0),
            content_generated=stats.get('content_generated', 0),
            images_created=stats.get('images_created', 0),
            errors=stats.get('errors', 0),
            cache_size=stats.get('cache_size', 0),
            last_updated=stats.get('timestamp', 'N/A')
        )
        
        return text
    
    def send_daily_summary(self, daily_data: Dict) -> Dict:
        """
        ዕለታዊ ማጠቃለያ ይልካል
        
        Args:
            daily_data (Dict): የቀኑ መረጃ
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        date = daily_data.get('date', datetime.now().strftime("%Y-%m-%d"))
        total_runs = daily_data.get('total_runs', 0)
        successful = daily_data.get('successful', 0)
        failed = daily_data.get('failed', 0)
        topics = daily_data.get('topics', [])
        
        success_rate = (successful / total_runs * 100) if total_runs > 0 else 0
        
        text = f"""
📊 *Daily Summary - {date}*

*Overview:*
• Total Runs: {total_runs}
• Successful: {successful}
• Failed: {failed}
• Success Rate: {success_rate:.1f}%

*Topics Processed:*
"""
        
        for i, topic in enumerate(topics[:10], 1):  # ከ10 በላይ አይውሰድ
            text += f"{i}. {topic}\n"
        
        if len(topics) > 10:
            text += f"... and {len(topics) - 10} more\n"
        
        # ምክር ወይም ምልከታ
        if success_rate >= 80:
            text += "\n✅ *Excellent performance today!*"
        elif success_rate >= 50:
            text += "\n⚠️ *Moderate performance. Check logs for errors.*"
        else:
            text += "\n❌ *Low success rate. System needs attention.*"
        
        return self.send_message(text, parse_mode='Markdown')
    
    def send_error_alert(self, 
                        error_message: str,
                        context: str = "",
                        severity: str = "error") -> Dict:
        """
        ስህተት ማስታወቂያ ይልካል
        
        Args:
            error_message (str): የስህተት መልእክት
            context (str): ተጨማሪ አውድ
            severity (str): አስቸኳይነት ደረጃ (error, warning, info)
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        emoji_map = {
            'error': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        emoji = emoji_map.get(severity, '⚠️')
        
        text = f"""
{emoji} *System Alert - {severity.upper()}*

*Error Message:*
`{error_message[:1000]}{'...' if len(error_message) > 1000 else ''}`

"""
        
        if context:
            text += f"*Context:* {context}\n"
        
        text += f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(text, parse_mode='Markdown')
    
    def send_system_status(self, system_info: Dict) -> Dict:
        """
        የስርዓት ሁኔታ ይልካል
        
        Args:
            system_info (Dict): የስርዓት መረጃ
            
        Returns:
            Dict: የኤፒአይ ምላሽ
        """
        text = f"""
🖥️ *System Status Report*

*Basic Info:*
• System: {system_info.get('system_name', 'Profit Machine')}
• Version: {system_info.get('version', 'Unknown')}
• Uptime: {system_info.get('uptime', 'N/A')}

*Resources:*
• CPU Usage: {system_info.get('cpu_usage', 'N/A')}
• Memory Usage: {system_info.get('memory_usage', 'N/A')}
• Disk Space: {system_info.get('disk_space', 'N/A')}

*API Status:*
• GROQ API: {'✅' if system_info.get('groq_status') else '❌'}
• News API: {'✅' if system_info.get('news_status') else '❌'}
• Telegram Bot: {'✅' if system_info.get('telegram_status') else '❌'}

*Recent Activity:*
• Messages Sent: {self.stats['messages_sent']}
• Errors: {self.stats['errors']}
• Last Sent: {self.stats['last_sent'] or 'Never'}

*Recommendations:*
"""
        
        # ምክር መጨመር
        if system_info.get('groq_status') and system_info.get('news_status'):
            text += "✅ All systems operational. Ready for production.\n"
        else:
            text += "⚠️ Some APIs are unavailable. Check API keys.\n"
        
        if self.stats['errors'] > 10:
            text += "❌ High error rate detected. Review system logs.\n"
        
        text += f"\n*Report Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(text, parse_mode='Markdown')
    
    def batch_send_files(self, 
                        file_list: List[Dict],
                        batch_size: int = 5) -> List[Dict]:
        """
        ብዙ ፋይሎችን በቡድን ይልካል
        
        Args:
            file_list (List[Dict]): የፋይሎች ዝርዝር
            batch_size (int): በአንድ ጊዜ የሚላኩ ፋይሎች ብዛት
            
        Returns:
            List[Dict]: የሁሉም ውጤቶች
        """
        results = []
        
        self.logger.info(f"ማስላክ በመደብ ላይ: {len(file_list)} ፋይሎች")
        
        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i + batch_size]
            self.logger.info(f"ቡድን {i//batch_size + 1} እየተላከ ነው: {len(batch)} ፋይሎች")
            
            for file_info in batch:
                file_path = file_info.get('path')
                caption = file_info.get('caption', '')
                
                if os.path.exists(file_path):
                    result = self.send_document(file_path, caption)
                    results.append(result)
                    
                    # በመካከል ጊዜ ማጥፋት
                    time.sleep(0.3)
                else:
                    self.logger.warning(f"ፋይል አልተገኘም: {file_path}")
                    results.append({'ok': False, 'error': 'File not found'})
        
        return results
    
    def get_statistics(self) -> Dict:
        """የቴሌግራም ሪፖርተር ስታቲስቲክስ ይመልሳል"""
        return {
            'telegram_stats': self.stats,
            'credentials_available': bool(self.bot_token and self.chat_id),
            'last_check': datetime.now().isoformat()
        }
    
    def test_connection(self) -> bool:
        """የቴሌግራም ግንኙነትን ይሞክራል"""
        return self._check_credentials()

# ለቀላል መጠቀም የሚረዳ አገልግሎት ተግባር
def get_telegram_reporter() -> TelegramReporter:
    """
    ቴሌግራም ሪፖርተር አገልግሎት ይመልሳል
    
    Returns:
        TelegramReporter: የቴሌግራም ሪፖርተር አገልግሎት
    """
    return TelegramReporter()

def send_telegram_notification(message: str, 
                              bot_token: str = None, 
                              chat_id: str = None) -> Dict:
    """
    ፈጣን የቴሌግራም ማሳወቂያ ይልካል
    
    Args:
        message (str): የሚላክ መልዕክት
        bot_token (str): የቦት ቶከን
        chat_id (str): የቻት መለያ
        
    Returns:
        Dict: የኤፒአይ ምላሽ
    """
    reporter = TelegramReporter(bot_token, chat_id)
    return reporter.send_message(message)

# ሙከራ ኮድ
if __name__ == "__main__":
    print("🔧 ቴሌግራም ሪፖርተር ሙከራ")
    print("="*50)
    
    # ቴሌግራም ሪፖርተር መፍጠር
    reporter = TelegramReporter()
    
    # ግንኙነት ማረጋገጫ
    if reporter.test_connection():
        print("✅ ቴሌግራም ግንኙነት ተረጋግጧል")
        
        # የሙከራ መልዕክት መላክ
        test_message = """
🤖 *Profit Machine Telegram Reporter Test*

በተሳካ ሁኔታ አገናኝተናል!

*System Info:*
• Time: {time}
• Python: {python_version}
• Module: telegram_reporter.py

*Next Steps:*
1. Integrate with Master Controller
2. Configure notifications
3. Set up daily reports

በደህና መጡ ወደ Profit Machine Enterprise! 🚀
""".format(
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            python_version=sys.version.split()[0]
        )
        
        result = reporter.send_message(test_message, parse_mode='Markdown')
        
        if result.get('ok'):
            print("✅ የሙከራ መልዕክት ተልኳል")
        else:
            print(f"❌ መልዕክት መላክ አልተቻለም: {result.get('description')}")
        
        # ስታቲስቲክስ ማሳየት
        stats = reporter.get_statistics()
        print(f"\n📊 ስታቲስቲክስ:")
        print(f"  መልዕክቶች ተልከዋል: {stats['telegram_stats']['messages_sent']}")
        print(f"  ስህተቶች: {stats['telegram_stats']['errors']}")
        
    else:
        print("❌ ቴሌግራም ግንኙነት አልተሳካም")
        print("የቴሌግራም ቁልፎችን አረጋግጠው።")
        print("TELEGRAM_BOT_TOKEN እና TELEGRAM_CHAT_ID በአካባቢ ተለዋዋጮች ውስጥ መኖር አለባቸው።")
