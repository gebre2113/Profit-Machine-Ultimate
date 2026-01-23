#!/usr/bin/env python3
"""
📱 Telegram Reporter for Profit Machine
Sends notifications to Telegram channel
"""

import logging
import traceback
from datetime import datetime
try:
    import requests
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Requests library not available for Telegram")

class EnhancedTelegramReporter:
    """Enhanced Telegram reporter with formatted messages"""
    
    def __init__(self, bot_token: str, chat_id: str):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("requests library required for Telegram")
        
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.logger = logging.getLogger('profit_machine.telegram')
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test Telegram connection"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            if response.status_code == 200:
                self.logger.info("✅ Telegram connection successful")
                return True
            else:
                self.logger.warning(f"⚠️ Telegram connection test failed: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Telegram connection error: {e}")
            return False
    
    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """Send message to Telegram channel"""
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }
            
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info("📤 Telegram message sent")
                return True
            else:
                self.logger.error(f"❌ Telegram send failed: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Telegram error: {e}")
            return False
    
    def send_master_report(self, report_data: dict) -> bool:
        """Send master workflow report"""
        
        summary = report_data.get('results', {}).get('summary', {})
        execution_time = report_data.get('execution_time', 0)
        
        message = f"""🏆 <b>PROFIT MACHINE REPORT</b>

📅 {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

📊 <b>Summary:</b>
• V10 Articles: {summary.get('v10_articles', 0)}
• V11 Articles: {summary.get('v11_articles', 0)}
• Enhanced: {summary.get('enhanced_articles', 0)}
• Failed: {summary.get('failed_executions', 0)}

⏱️ <b>Performance:</b>
• Time: {execution_time:.1f}s
• Status: ✅ Success

🔗 <b>Environment:</b>
• GitHub Actions: {'✅ Yes' if report_data.get('environment') == 'github_actions' else '❌ No'}
• WordPress: {'✅ Enabled' if report_data.get('wordpress_stats', {}).get('published', 0) > 0 else '⚠️ Disabled'}

#ProfitMachine #Automation"""
        
        return self.send_message(message)
    
    def send_error_report(self, error_message: str, execution_time: float, context: str = "unknown") -> bool:
        """Send error report"""
        
        message = f"""🚨 <b>PROFIT MACHINE ERROR</b>

📅 {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

⚠️ <b>Context:</b> {context}

⏱️ <b>Execution Time:</b> {execution_time:.1f}s

❌ <b>Error:</b>
<code>{error_message[:1000]}</code>

🔧 <b>Action Required:</b>
Please check the logs for details.

#ProfitMachine #Error"""
        
        return self.send_message(message)
    
    def send_wordpress_report(self, stats: dict) -> bool:
        """Send WordPress publishing report"""
        
        message = f"""📤 <b>WORDPRESS PUBLISHING REPORT</b>

📅 {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

✅ <b>Published:</b> {stats.get('published', 0)}
❌ <b>Failed:</b> {stats.get('failed', 0)}
📈 <b>Success Rate:</b> {stats.get('success_rate', 0):.1f}%

🎯 <b>Status:</b> {'✅ All successful' if stats.get('failed', 0) == 0 else '⚠️ Some failures'}

#ProfitMachine #WordPress"""
        
        return self.send_message(message)
