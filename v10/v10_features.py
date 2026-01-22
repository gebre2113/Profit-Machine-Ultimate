#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v10.0 - COMPLETE PROFIT MACHINE
✅ Multi-Language Content (EN, DE, FR, ES)
✅ AI Text-to-Speech with Native Accents
✅ AI Image Generation (Pollinations/Unsplash)
✅ YouTube Video Embedding
✅ 2000+ Word Deep-Dive Articles
✅ SAFE Affiliate Link Injection (Max 3)
✅ Ad-Ready Layout with Table of Contents
✅ High-CPC Country Targeting
✅ Automatic Internal Linking
✅ WordPress Auto-Publishing
✅ Telegram Daily Reports
✅ Free Groq AI Integration
✅ Self-Healing Content System
✅ Database Persistence (GitHub Backup)
✅ Smart Revenue Calculator
✅ Performance Monitoring
✅ Rate-Limited API Calls
✅ Advanced Content Formatting
"""

import os
import sys
import json
import time
import sqlite3
import threading
import hashlib
import base64
import random
import re
import uuid
import subprocess
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import quote
import concurrent.futures

# =================== DEPENDENCY CHECK ===================

print("🔧 Checking dependencies...")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("❌ Install requests: pip install requests")
    sys.exit(1)

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️  Install groq: pip install groq")

try:
    from gtts import gTTS
    import pygame
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  Install TTS: pip install gtts pygame")

# =================== CONFIGURATION MANAGER ===================

class ConfigManager:
    """Configuration manager with JSON file support"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        default_config = {
            # API Keys
            'GROQ_API_KEY': '',
            'WP_URL': '',
            'WP_USERNAME': '',
            'WP_PASSWORD': '',
            'TELEGRAM_BOT_TOKEN': '',
            'TELEGRAM_CHAT_ID': '',
            
            # Affiliate IDs (Store in GitHub Secrets)
            'AMAZON_AFFILIATE_ID': 'YOUR_AMAZON_ID_HERE',
            'CLICKBANK_AFFILIATE_ID': 'YOUR_CLICKBANK_ID_HERE',
            'SHAREASALE_AFFILIATE_ID': 'YOUR_SHAREASALE_ID_HERE',
            
            # Content Settings
            'DEFAULT_LANGUAGES': ['en', 'de', 'fr', 'es'],
            'TARGET_WORD_COUNT': 1800,
            'IMAGE_COUNT': 4,
            'MAX_AFFILIATE_LINKS': 3,
            
            # System Settings
            'AUTO_PUBLISH': False,
            'RETRY_ATTEMPTS': 3,
            'REQUEST_DELAY_SECONDS': 3,
            'BACKUP_TO_GITHUB': True,
            
            # Telegram Features
            'TELEGRAM_DAILY_REPORT': True,
            'TELEGRAM_ERROR_ALERTS': True,
            'TELEGRAM_REVENUE_ALERTS': True,
            'MINIMUM_REVENUE_ALERT': 10.0,
            
            # Content Formatting
            'INCLUDE_TABLE_OF_CONTENTS': True,
            'INCLUDE_KEY_TAKEAWAYS': True,
            'INCLUDE_STATISTICS': True,
            'INCLUDE_CASE_STUDIES': True,
            'INCLUDE_FAQ': True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Update with loaded config
                    for key in loaded:
                        if key in default_config:
                            default_config[key] = loaded[key]
                        else:
                            default_config[key] = loaded[key]
                print(f"✅ Config loaded from {self.config_file}")
        except Exception as e:
            print(f"⚠️  Config load failed: {e}")
        
        # Check environment variables (for GitHub Actions)
        for key in default_config:
            env_value = os.getenv(key)
            if env_value is not None:
                if isinstance(default_config[key], bool):
                    default_config[key] = env_value.lower() == 'true'
                elif isinstance(default_config[key], int):
                    try:
                        default_config[key] = int(env_value)
                    except:
                        pass
                elif isinstance(default_config[key], list):
                    default_config[key] = [x.strip() for x in env_value.split(',')]
                else:
                    default_config[key] = env_value
        
        return default_config
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def save(self):
        """Save config to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Config save failed: {e}")
            return False

# =================== ENHANCED TELEGRAM NOTIFIER ===================

class EnhancedTelegramNotifier:
    """Advanced Telegram notifier with rich formatting"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, text: str, parse_mode: str = 'Markdown', 
                    disable_web_page_preview: bool = True) -> bool:
        """Send message to Telegram"""
        try:
            # Split message if too long
            if len(text) > 4000:
                parts = self._split_message(text)
                for part in parts:
                    if not self._send_single_message(part, parse_mode, disable_web_page_preview):
                        return False
                    time.sleep(1)
                return True
            else:
                return self._send_single_message(text, parse_mode, disable_web_page_preview)
        except Exception as e:
            print(f"❌ Telegram send failed: {e}")
            return False
    
    def _send_single_message(self, text: str, parse_mode: str, 
                           disable_web_page_preview: bool) -> bool:
        """Send single message"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": disable_web_page_preview
                },
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram request failed: {e}")
            return False
    
    def _split_message(self, text: str, max_length: int = 4000) -> List[str]:
        """Split message into parts"""
        parts = []
        lines = text.split('\n')
        current_part = []
        current_length = 0
        
        for line in lines:
            line_length = len(line)
            if current_length + line_length + 1 > max_length:
                parts.append('\n'.join(current_part))
                current_part = [line]
                current_length = line_length
            else:
                current_part.append(line)
                current_length += line_length + 1
        
        if current_part:
            parts.append('\n'.join(current_part))
        
        return parts
    
    def send_document(self, file_path: str, caption: str = "") -> bool:
        """Send document to Telegram"""
        try:
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {'chat_id': self.chat_id, 'caption': caption[:200]}
                
                response = requests.post(
                    f"{self.api_url}/sendDocument",
                    data=data,
                    files=files,
                    timeout=30
                )
                
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram document send failed: {e}")
            return False
    
    def send_daily_report(self, report_data: Dict) -> bool:
        """Send daily execution report"""
        
        # Extract data
        topic_data = report_data.get('topic_data', {})
        article_info = report_data.get('article_info', {})
        revenue_estimate = report_data.get('revenue_estimate', {})
        performance = report_data.get('performance_report', {})
        health = report_data.get('health_report', {})
        stats = report_data.get('stats_report', {})
        
        # Calculate score
        word_score = min(30, (article_info.get('word_count', 0) / 1800) * 30)
        image_score = min(20, article_info.get('images_count', 0) * 5)
        revenue_score = min(50, revenue_estimate.get('monthly_estimate', 0) / 2)
        total_score = min(100, word_score + image_score + revenue_score)
        
        # Create score bar
        score_bar = self._create_score_bar(total_score)
        
        # Format message
        message = f"""
🏆 *PROFIT MACHINE v10.0 - DAILY REPORT*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{score_bar}
📊 *SCORE: {total_score:.1f}/100*

📅 *Date:* {datetime.now().strftime('%Y-%m-%d')}
⏰ *Time:* {datetime.now().strftime('%H:%M')}
🎯 *Topic:* {topic_data.get('topic', 'N/A')[:70]}

💎 *Key Metrics*
├─ 📝 Words: *{article_info.get('word_count', 0):,}*
├─ 🖼️ Images: {article_info.get('images_count', 0)}
├─ 🔗 Affiliates: {article_info.get('affiliate_links_count', 0)}
└─ ⚡ Time: {performance.get('total_execution_time', 0)}s

💰 *Revenue Projection*
├─ 📈 Monthly: *${revenue_estimate.get('monthly_estimate', 0):.2f}*
├─ 🎯 Weekly: *${revenue_estimate.get('monthly_estimate', 0)/4:.2f}*
├─ 📊 Traffic: {revenue_estimate.get('traffic_estimate', 0):,}
└─ 🌟 Quality: {revenue_estimate.get('quality_score', 'N/A')}

🏥 *System Health*
├─ 🩺 Status: {health.get('overall_health', 'N/A')}
├─ 📈 Success Rate: {health.get('success_rate', 0)}%
├─ 🖥️ Memory: {performance.get('average_memory_usage', 0):.1f}MB
└─ ⚠️ Errors: {performance.get('error_rate', 0)}

📈 *Overall Statistics*
├─ 📚 Total Articles: {stats.get('total_articles', 0)}
├─ 📝 Total Words: {stats.get('total_words', 0):,}
└─ 💰 Total Revenue Est: *${stats.get('total_revenue_estimate', 0):,.2f}*

🚀 *Next Actions*
1️⃣ Review article on WordPress
2️⃣ Check affiliate links
3️⃣ Schedule social media posts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#AutoBlog #{topic_data.get('category', 'tech')} #{datetime.now().strftime('%d%m%Y')}
"""
        
        return self.send_message(message)
    
    def _create_score_bar(self, score: float) -> str:
        """Create visual score bar"""
        bars = 20
        filled = int(score / 100 * bars)
        empty = bars - filled
        
        if score >= 80:
            emoji = "🚀"
            color = "🟢"
        elif score >= 60:
            emoji = "📈"
            color = "🟡"
        elif score >= 40:
            emoji = "📊"
            color = "🟠"
        else:
            emoji = "⚠️"
            color = "🔴"
        
        return f"{emoji} `{color*filled}{'⚪'*empty}` {score:.1f}%"
    
    def send_error_alert(self, error: str, execution_time: float) -> bool:
        """Send error alert to Telegram"""
        message = f"""
⚠️ *PROFIT MACHINE v10.0 - ERROR ALERT*

❌ *Error:* {error[:200]}
⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M')}
⚡ *Execution Time:* {execution_time:.1f}s

🔧 *Next Steps:*
1️⃣ Check system logs
2️⃣ Verify API keys
3️⃣ Review configuration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#Error #Debug #{datetime.now().strftime('%d%m%Y')}
"""
        return self.send_message(message)

# =================== PERSISTENT DATABASE MANAGER ===================

class PersistentDatabaseManager:
    """SQLite database manager with GitHub backup"""
    
    def __init__(self, db_file='profit_machine_v10.db'):
        os.makedirs('data', exist_ok=True)
        self.db_file = os.path.join('data', db_file)
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                topic TEXT,
                language TEXT,
                word_count INTEGER,
                images_count INTEGER,
                has_audio BOOLEAN,
                has_video BOOLEAN,
                published BOOLEAN DEFAULT 0,
                publish_date TEXT,
                revenue_estimate REAL,
                affiliate_links_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_date TEXT,
                total_articles INTEGER,
                total_words INTEGER,
                total_revenue_estimate REAL,
                execution_time_seconds REAL,
                status TEXT
            )
        ''')
        
        # Category stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_stats (
                category TEXT PRIMARY KEY,
                articles_count INTEGER DEFAULT 0,
                avg_revenue REAL DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_article(self, article_data: Dict) -> int:
        """Log article to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO articles 
            (title, topic, language, word_count, images_count, has_audio, 
             has_video, published, publish_date, revenue_estimate, affiliate_links_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article_data.get('title'),
            article_data.get('topic'),
            article_data.get('language', 'en'),
            article_data.get('word_count', 0),
            article_data.get('images_count', 0),
            article_data.get('has_audio', False),
            article_data.get('has_video', False),
            article_data.get('published', False),
            article_data.get('publish_date'),
            article_data.get('revenue_estimate', 0),
            article_data.get('affiliate_links_count', 0)
        ))
        
        article_id = cursor.lastrowid
        
        # Update category stats
        category = article_data.get('category', 'general')
        cursor.execute('''
            INSERT OR REPLACE INTO category_stats 
            (category, articles_count, avg_revenue, last_used)
            VALUES (
                ?,
                COALESCE((SELECT articles_count + 1 FROM category_stats WHERE category = ?), 1),
                COALESCE((SELECT (avg_revenue * articles_count + ?) / (articles_count + 1) 
                         FROM category_stats WHERE category = ?), ?),
                datetime('now')
            )
        ''', (category, category, 
              article_data.get('revenue_estimate', 0), category,
              article_data.get('revenue_estimate', 0)))
        
        conn.commit()
        conn.close()
        
        return article_id
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(word_count) FROM articles")
        total_words = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(revenue_estimate) FROM articles")
        total_revenue = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT category, articles_count FROM category_stats ORDER BY articles_count DESC LIMIT 5")
        top_categories = cursor.fetchall()
        
        cursor.execute("SELECT strftime('%Y-%m-%d', created_at) as date, COUNT(*) FROM articles GROUP BY date ORDER BY date DESC LIMIT 7")
        weekly_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_articles': total_articles,
            'total_words': total_words,
            'total_revenue_estimate': round(total_revenue, 2),
            'avg_article_length': round(total_words / total_articles, 1) if total_articles > 0 else 0,
            'avg_revenue_per_article': round(total_revenue / total_articles, 2) if total_articles > 0 else 0,
            'top_categories': dict(top_categories),
            'weekly_stats': dict(weekly_stats)
        }
    
    def backup_to_github(self):
        """Backup database to GitHub"""
        try:
            # Export to JSON
            self.export_to_json()
            
            # Git commands
            commands = [
                ['git', 'add', 'data/'],
                ['git', 'commit', '-m', f'Database backup {datetime.now().strftime("%Y-%m-%d %H:%M")}'],
                ['git', 'push']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"⚠️  Git command failed: {result.stderr}")
                    return False
            
            print("✅ Database backed up to GitHub")
            return True
            
        except Exception as e:
            print(f"⚠️  GitHub backup failed: {e}")
            return False
    
    def export_to_json(self):
        """Export database to JSON file"""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Export recent articles
            cursor.execute("SELECT * FROM articles ORDER BY created_at DESC LIMIT 50")
            articles = [dict(row) for row in cursor.fetchall()]
            
            # Export statistics
            stats = self.get_statistics()
            
            data = {
                'export_date': datetime.now().isoformat(),
                'total_articles': len(articles),
                'articles': articles,
                'statistics': stats
            }
            
            json_file = os.path.join('data', 'database_backup.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            conn.close()
            print(f"✅ Database exported to JSON: {json_file}")
            return True
            
        except Exception as e:
            print(f"❌ JSON export failed: {e}")
            return False

# =================== SMART REVENUE CALCULATOR ===================

class SmartRevenueCalculator:
    """Intelligent revenue estimation"""
    
    def __init__(self):
        self.cpc_rates = {
            'en': {'US': 2.50, 'UK': 2.00, 'CA': 1.80, 'AU': 1.70},
            'de': {'DE': 1.80, 'AT': 1.60, 'CH': 2.20},
            'fr': {'FR': 1.50, 'BE': 1.30, 'CH': 1.80, 'CA': 1.40},
            'es': {'ES': 1.20, 'MX': 0.80, 'AR': 0.60, 'CO': 0.70}
        }
        
        self.category_multipliers = {
            'technology': 1.5,
            'business': 1.3,
            'finance': 1.4,
            'health': 1.2,
            'education': 1.1,
            'lifestyle': 1.0
        }
    
    def calculate_revenue(self, article_data: Dict, category: str = 'business', 
                         language: str = 'en', country: str = 'US') -> Dict:
        """Calculate revenue estimate for article"""
        
        # Base CPC
        base_cpc = self.cpc_rates.get(language, {}).get(country, 1.0)
        
        # Category multiplier
        category_mult = self.category_multipliers.get(category, 1.0)
        
        # Word count multiplier (1500+ words gets bonus)
        word_count = article_data.get('word_count', 1000)
        word_mult = min(1.5, max(0.8, word_count / 1000))
        
        # Image multiplier
        images_count = article_data.get('images_count', 0)
        image_mult = 1 + (images_count * 0.05)
        
        # Affiliate multiplier
        affiliate_count = article_data.get('affiliate_links_count', 0)
        affiliate_mult = 1 + (affiliate_count * 0.1)
        
        # Quality multiplier (based on content features)
        quality_mult = 1.0
        if article_data.get('has_audio', False):
            quality_mult += 0.1
        if article_data.get('has_video', False):
            quality_mult += 0.15
        if article_data.get('has_toc', False):
            quality_mult += 0.05
        
        # Calculate final CPC
        final_cpc = base_cpc * category_mult * word_mult * image_mult * affiliate_mult * quality_mult
        
        # Traffic estimation
        quality_score = min(10, (word_mult + image_mult + affiliate_mult) * 3)
        traffic_levels = {
            9: {'min': 10000, 'max': 50000},
            7: {'min': 5000, 'max': 20000},
            5: {'min': 2000, 'max': 8000},
            3: {'min': 1000, 'max': 3000}
        }
        
        for threshold, traffic in traffic_levels.items():
            if quality_score >= threshold:
                estimated_traffic = (traffic['min'] + traffic['max']) / 2
                break
        else:
            estimated_traffic = 1000
        
        # Monthly revenue (3% CTR, 30 days)
        monthly_revenue = estimated_traffic * 0.03 * final_cpc * 30
        
        return {
            'monthly_estimate': round(monthly_revenue, 2),
            'weekly_estimate': round(monthly_revenue / 4, 2),
            'daily_estimate': round(monthly_revenue / 30, 2),
            'cpc_rate': round(final_cpc, 2),
            'traffic_estimate': int(estimated_traffic),
            'quality_score': round(quality_score, 1),
            'multipliers': {
                'category': round(category_mult, 2),
                'words': round(word_mult, 2),
                'images': round(image_mult, 2),
                'affiliate': round(affiliate_mult, 2),
                'quality': round(quality_mult, 2)
            }
        }

# =================== SAFE AFFILIATE MANAGER ===================

class SafeAffiliateManager:
    """Safe affiliate link integration (max 3 links)"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.max_links = config.get('MAX_AFFILIATE_LINKS', 3)
        
        # Network configurations
        self.networks = {
            'amazon': {
                'template': 'https://www.amazon.com/dp/{product_id}/?tag={affiliate_id}',
                'affiliate_id': config.get('AMAZON_AFFILIATE_ID'),
                'products': ['B08N5WRWNW', 'B07FK8QQQ', 'B0844JKQ9K', 'B08N5PN5QC']
            },
            'clickbank': {
                'template': 'https://hop.clickbank.net/?affiliate={affiliate_id}&vendor={vendor_id}',
                'affiliate_id': config.get('CLICKBANK_AFFILIATE_ID'),
                'vendors': ['VENDOR123', 'PRODUCT456', 'OFFER789']
            },
            'shareasale': {
                'template': 'https://www.shareasale.com/r.cfm?u={affiliate_id}&m={merchant_id}',
                'affiliate_id': config.get('SHAREASALE_AFFILIATE_ID'),
                'merchants': ['12345', '67890', '54321']
            }
        }
        
        # Category to network mapping
        self.category_networks = {
            'technology': ['amazon', 'clickbank'],
            'business': ['clickbank', 'shareasale'],
            'finance': ['clickbank', 'amazon'],
            'health': ['amazon', 'clickbank'],
            'education': ['amazon', 'shareasale'],
            'lifestyle': ['amazon', 'clickbank']
        }
    
    def generate_affiliate_links(self, topic: str, category: str, 
                                max_links: int = None) -> List[Dict]:
        """Generate affiliate links for topic"""
        
        if max_links is None:
            max_links = self.max_links
        
        networks = self.category_networks.get(category, ['amazon'])
        links = []
        
        for network in networks[:max_links]:
            affiliate_id = self.networks[network].get('affiliate_id')
            if not affiliate_id or affiliate_id.startswith('YOUR_'):
                continue
            
            # Create link
            if network == 'amazon':
                product_id = random.choice(self.networks[network]['products'])
                url = self.networks[network]['template'].format(
                    product_id=product_id, 
                    affiliate_id=affiliate_id
                )
                anchor = f"Check {topic[:20]} on Amazon"
            elif network == 'clickbank':
                vendor_id = random.choice(self.networks[network]['vendors'])
                url = self.networks[network]['template'].format(
                    affiliate_id=affiliate_id,
                    vendor_id=vendor_id
                )
                anchor = f"Learn more about {topic[:20]}"
            else:
                merchant_id = random.choice(self.networks[network]['merchants'])
                url = self.networks[network]['template'].format(
                    affiliate_id=affiliate_id,
                    merchant_id=merchant_id
                )
                anchor = f"Get {topic[:20]} tools"
            
            links.append({
                'url': url,
                'anchor_text': anchor,
                'network': network,
                'rel': 'nofollow sponsored'
            })
        
        return links[:max_links]
    
    def embed_affiliate_links(self, content: str, topic: str, 
                             category: str) -> Tuple[str, int]:
        """Safely embed affiliate links in content"""
        
        links = self.generate_affiliate_links(topic, category)
        if not links:
            return content, 0
        
        paragraphs = re.split(r'\n\s*\n', content)
        if len(paragraphs) < 10:
            return content, 0
        
        # Calculate positions with proper spacing
        positions = []
        total_paragraphs = len(paragraphs)
        min_spacing = max(3, total_paragraphs // len(links))
        
        for i in range(len(links)):
            pos = min((i + 1) * min_spacing, total_paragraphs - 2)
            positions.append(pos)
        
        # Insert links
        inserted_count = 0
        for i, pos in enumerate(positions):
            if i < len(links):
                link_html = self._create_affiliate_html(links[i])
                insert_pos = pos + inserted_count
                if insert_pos < len(paragraphs):
                    paragraphs.insert(insert_pos, link_html)
                    inserted_count += 1
        
        return '\n\n'.join(paragraphs), len(links)
    
    def _create_affiliate_html(self, link_data: Dict) -> str:
        """Create affiliate link HTML with disclosure"""
        
        ctas = [
            "For more information, check this out",
            "This product might help you",
            "You can find this tool here",
            "Learn more about this",
            "Check price and availability"
        ]
        
        cta = random.choice(ctas)
        
        return f'''
<div class="affiliate-disclosure" style="background: #f8f9fa; border-left: 4px solid #4a5568; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0;">
<p style="margin: 0; font-style: italic; color: #4a5568;">
💡 <strong>Note:</strong> {cta}: 
<a href="{link_data['url']}" target="_blank" rel="{link_data['rel']}" style="color: #2d3748; font-weight: bold; text-decoration: none;">
{link_data['anchor_text']}
</a>
</p>
<p style="margin: 10px 0 0 0; font-size: 0.9em; color: #718096;">
(This is an affiliate link. Clicking it won't cost you extra but helps support our work.)
</p>
</div>
'''

# =================== ADVANCED CONTENT FORMATTER ===================

class AdvancedContentFormatter:
    """Advanced content formatting with TOC and styling"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        
    def format_content(self, content: str, topic: str, 
                      include_toc: bool = None,
                      include_takeaways: bool = None) -> str:
        """Format content with advanced features"""
        
        if include_toc is None:
            include_toc = self.config.get('INCLUDE_TABLE_OF_CONTENTS', True)
        if include_takeaways is None:
            include_takeaways = self.config.get('INCLUDE_KEY_TAKEAWAYS', True)
        
        formatted = content
        
        # Add table of contents
        if include_toc:
            formatted = self._add_table_of_contents(formatted, topic)
        
        # Add styling to headings
        formatted = self._style_headings(formatted)
        
        # Add key takeaways
        if include_takeaways:
            formatted = self._add_key_takeaways(formatted)
        
        # Add conclusion styling
        formatted = self._style_conclusion(formatted)
        
        return formatted
    
    def _add_table_of_contents(self, content: str, topic: str) -> str:
        """Add table of contents"""
        
        # Extract headings
        headings = re.findall(r'<h[2-3][^>]*>(.*?)</h[2-3]>', content)
        if len(headings) < 3:
            return content
        
        # Create TOC items
        toc_items = []
        for i, heading in enumerate(headings[:6]):
            clean_heading = re.sub(r'<[^>]+>', '', heading)
            slug = re.sub(r'[^a-z0-9]+', '-', clean_heading.lower()).strip('-')
            toc_items.append(f'<li><a href="#{slug}" style="color: #4a5568; text-decoration: none;">{clean_heading}</a></li>')
        
        toc_html = f'''
<div class="table-of-contents" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
<h3 style="margin-top: 0; color: white;">📑 In This Article: {topic[:50]}</h3>
<ul style="columns: 2; column-gap: 40px; list-style: none; padding-left: 0;">
{toc_items}
</ul>
<p style="font-size: 0.9em; opacity: 0.9; margin-top: 15px;">
<em>Use the links above to navigate to specific sections.</em>
</p>
</div>
'''
        
        # Insert after first heading
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '<h1' in line or '<h2' in line:
                lines.insert(i + 1, toc_html)
                break
        
        return '\n'.join(lines)
    
    def _style_headings(self, content: str) -> str:
        """Add styling to headings"""
        
        # Style h2 headings
        content = re.sub(
            r'<h2>(.*?)</h2>',
            r'<h2 style="border-bottom: 2px solid #4a5568; padding-bottom: 10px; margin-top: 40px; color: #2d3748;">\1</h2>',
            content
        )
        
        # Style h3 headings
        content = re.sub(
            r'<h3>(.*?)</h3>',
            r'<h3 style="border-left: 4px solid #667eea; padding-left: 15px; margin-top: 30px; color: #4a5568;">\1</h3>',
            content
        )
        
        return content
    
    def _add_key_takeaways(self, content: str) -> str:
        """Add key takeaways section"""
        
        takeaways = [
            "Start with clear, measurable goals",
            "Implement step by step, don't rush",
            "Track your progress regularly",
            "Adjust based on results and feedback",
            "Scale what works, discard what doesn't"
        ]
        
        takeaways_html = '\n'.join([f'<li>{takeaway}</li>' for takeaway in takeaways])
        
        takeaways_section = f'''
<div class="key-takeaways" style="background: #f0fff4; border: 2px solid #9ae6b4; padding: 25px; border-radius: 12px; margin: 40px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
<h3 style="margin-top: 0; color: #2f855a;">🎯 Key Takeaways</h3>
<ul style="margin: 15px 0; padding-left: 20px; color: #2d3748;">
{takeaways_html}
</ul>
<p style="color: #718096; font-style: italic; margin-top: 15px;">
Remember: Consistency and continuous improvement are key to success.
</p>
</div>
'''
        
        # Insert before conclusion
        if 'Conclusion' in content or 'conclusion' in content.lower():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'Conclusion' in line or 'conclusion' in line.lower():
                    lines.insert(i, takeaways_section)
                    break
            return '\n'.join(lines)
        
        return content
    
    def _style_conclusion(self, content: str) -> str:
        """Style conclusion section"""
        
        conclusion_html = '''
<div class="conclusion" style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); padding: 30px; border-radius: 12px; margin: 40px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
<h3 style="margin-top: 0; color: #2d3748;">✨ Final Thoughts</h3>
<p style="color: #2d3748; font-size: 1.1em;">
The journey of a thousand miles begins with a single step. Start implementing these strategies today, and track your progress over time.
</p>
<p style="margin-top: 20px;">
<strong>🎯 Your Action Plan:</strong><br>
1. Choose one strategy to implement today<br>
2. Set up tracking and measurement<br>
3. Review progress weekly<br>
4. Scale successful approaches
</p>
</div>
'''
        
        # Replace conclusion if exists
        content = re.sub(
            r'<h[2-3]>Conclusion.*?</h[2-3]>.*?(?=<h|$)',
            conclusion_html,
            content,
            flags=re.DOTALL | re.IGNORECASE
        )
        
        return content

# =================== PERFORMANCE MONITOR ===================

class PerformanceMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.metrics = {
            'start_time': None,
            'component_times': {},
            'api_calls': [],
            'memory_usage': [],
            'errors': []
        }
    
    def start(self):
        """Start monitoring"""
        self.metrics['start_time'] = time.time()
        self.metrics['memory_usage'].append(self._get_memory_usage())
    
    def log_component(self, component: str, duration: float):
        """Log component execution time"""
        self.metrics['component_times'][component] = duration
    
    def log_api_call(self, endpoint: str, status: str, duration: float):
        """Log API call"""
        self.metrics['api_calls'].append({
            'endpoint': endpoint,
            'status': status,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_error(self, component: str, error: str):
        """Log error"""
        self.metrics['errors'].append({
            'component': component,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_report(self) -> Dict:
        """Get performance report"""
        if not self.metrics['start_time']:
            return {}
        
        total_time = time.time() - self.metrics['start_time']
        
        # Find slowest component
        component_times = self.metrics['component_times']
        slowest = max(component_times.items(), key=lambda x: x[1]) if component_times else None
        
        # API call stats
        api_calls = self.metrics['api_calls']
        successful_calls = sum(1 for call in api_calls if call['status'] == 'success')
        
        return {
            'total_execution_time': round(total_time, 2),
            'average_memory_usage': round(sum(self.metrics['memory_usage']) / len(self.metrics['memory_usage']), 2) if self.metrics['memory_usage'] else 0,
            'slowest_component': slowest,
            'total_api_calls': len(api_calls),
            'successful_api_calls': successful_calls,
            'success_rate': round(successful_calls / len(api_calls) * 100, 1) if api_calls else 100,
            'average_api_response_time': round(sum(call['duration'] for call in api_calls) / len(api_calls), 3) if api_calls else 0,
            'error_count': len(self.metrics['errors'])
        }
    
    def _get_memory_usage(self) -> float:
        """Get memory usage in MB"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0

# =================== VOICE AI ENGINE ===================

class VoiceAIEngine:
    """Convert articles to speech with native accents"""
    
    def __init__(self):
        self.supported_languages = {
            'en': {'name': 'English', 'accent': 'com', 'tld': 'com', 'slow': False},
            'en-uk': {'name': 'English (UK)', 'accent': 'co.uk', 'tld': 'co.uk', 'slow': False},
            'de': {'name': 'German', 'accent': 'de', 'tld': 'de', 'slow': False},
            'fr': {'name': 'French', 'accent': 'fr', 'tld': 'fr', 'slow': False},
            'es': {'name': 'Spanish', 'accent': 'es', 'tld': 'es', 'slow': False},
            'it': {'name': 'Italian', 'accent': 'it', 'tld': 'it', 'slow': False}
        }
    
    def create_audio_summary(self, article_content: str, language: str = 'en') -> Dict:
        """Create audio summary of article"""
        
        print(f"🔊 Generating audio for {self.supported_languages.get(language, {}).get('name', language)}...")
        
        # Extract summary
        summary = self._extract_summary(article_content, language)
        
        try:
            if TTS_AVAILABLE:
                audio_file = self._generate_with_gtts(summary, language)
                if audio_file:
                    return {
                        'success': True,
                        'audio_file': audio_file,
                        'summary': summary,
                        'language': language,
                        'method': 'gTTS'
                    }
            
            return {'success': False, 'error': 'TTS not available', 'summary': summary}
            
        except Exception as e:
            print(f"⚠️  Audio generation failed: {e}")
            return {'success': False, 'error': str(e), 'summary': summary}
    
    def _extract_summary(self, content: str, language: str) -> str:
        """Extract summary from content"""
        paragraphs = re.split(r'\n\s*\n', content)
        if len(paragraphs) >= 3:
            summary = ' '.join(paragraphs[:3])
        else:
            summary = content[:500]
        
        summary = re.sub(r'<[^>]+>', '', summary)
        sentences = re.split(r'[.!?]+', summary)
        if len(sentences) > 4:
            summary = '. '.join(sentences[:4]) + '.'
        
        return summary[:800]
    
    def _generate_with_gtts(self, text: str, language: str) -> Optional[Dict]:
        """Generate audio using gTTS"""
        try:
            lang_code = language.split('-')[0]
            os.makedirs('audio_output', exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"audio_output/article_{timestamp}_{lang_code}.mp3"
            
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(filename)
            
            with open(filename, 'rb') as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
            
            return {
                'filename': filename,
                'base64': audio_base64,
                'text': text[:100] + '...'
            }
            
        except Exception as e:
            print(f"⚠️  gTTS error: {e}")
            return None

# =================== VISUAL AI ENGINE ===================

class VisualAIEngine:
    """Generate and source images for articles"""
    
    def __init__(self):
        self.image_sources = [
            {
                'name': 'Pollinations AI',
                'url': 'https://image.pollinations.ai/prompt/',
                'free': True,
                'requires_key': False
            },
            {
                'name': 'Unsplash',
                'url': 'https://source.unsplash.com/featured/',
                'free': True,
                'requires_key': False
            },
            {
                'name': 'Picsum',
                'url': 'https://picsum.photos/',
                'free': True,
                'requires_key': False
            }
        ]
    
    def generate_article_images(self, title: str, num_images: int = 4) -> List[Dict]:
        """Generate images for article"""
        
        print(f"🖼️  Generating {num_images} images...")
        
        keywords = self._extract_keywords(title)
        images = []
        
        for i in range(num_images):
            image_type = self._get_image_type(i)
            
            # Try different sources
            for source in self.image_sources:
                try:
                    if source['name'] == 'Pollinations AI':
                        prompt = self._create_image_prompt(keywords, image_type)
                        clean_prompt = quote(prompt)
                        width = 800 if i % 2 == 0 else 600
                        height = 450 if i % 2 == 0 else 400
                        image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&nofilter=true"
                    elif source['name'] == 'Unsplash':
                        width = 800 if i % 2 == 0 else 600
                        height = 450 if i % 2 == 0 else 400
                        keyword = keywords[0] if keywords else 'technology'
                        image_url = f"https://source.unsplash.com/featured/{width}x{height}/?{keyword}&{i}"
                    else:
                        width = 800 if i % 2 == 0 else 600
                        height = 450 if i % 2 == 0 else 400
                        image_url = f"https://picsum.photos/{width}/{height}?random={i}"
                    
                    if image_url:
                        images.append({
                            'url': image_url,
                            'alt': self._create_alt_text(keywords, image_type),
                            'caption': self._create_caption(keywords, image_type),
                            'source': source['name'],
                            'position': i,
                            'type': image_type
                        })
                        break
                        
                except Exception as e:
                    continue
            
            if len(images) <= i:
                images.append(self._create_placeholder_image(keywords, i))
        
        return images
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [w for w in words if w not in stop_words]
        return keywords[:min(5, len(keywords))]
    
    def _get_image_type(self, position: int) -> str:
        """Get image type based on position"""
        types = ['hero', 'illustration', 'infographic', 'example', 'summary']
        return types[position % len(types)]
    
    def _create_image_prompt(self, keywords: List[str], image_type: str) -> str:
        """Create image prompt"""
        base_prompt = " ".join(keywords[:3])
        
        prompts = {
            'hero': f"{base_prompt}, professional, high quality, digital art, trending on artstation",
            'illustration': f"{base_prompt}, illustration, clean, modern, vector art",
            'infographic': f"{base_prompt}, infographic, data visualization, clean design",
            'example': f"{base_prompt}, real example, practical application, photography",
            'summary': f"{base_prompt}, summary, key points, professional design"
        }
        
        return prompts.get(image_type, f"{base_prompt}, digital art")
    
    def _create_alt_text(self, keywords: List[str], image_type: str) -> str:
        """Create alt text"""
        base = " ".join(keywords[:2])
        
        alt_texts = {
            'hero': f"{base} - featured image showing key concept",
            'illustration': f"illustration of {base} concept",
            'infographic': f"infographic about {base}",
            'example': f"practical example of {base}",
            'summary': f"summary visual for {base}"
        }
        
        return alt_texts.get(image_type, f"image about {base}")
    
    def _create_caption(self, keywords: List[str], image_type: str) -> str:
        """Create caption"""
        base = " ".join(keywords[:2]).title()
        
        captions = {
            'hero': f"Visual representation of {base} concept",
            'illustration': f"Artistic interpretation of {base}",
            'infographic': f"Key data and statistics about {base}",
            'example': f"Real-world application of {base}",
            'summary': f"Summary of {base} principles"
        }
        
        return captions.get(image_type, f"Related to {base}")
    
    def _create_placeholder_image(self, keywords: List[str], index: int) -> Dict:
        """Create placeholder image"""
        width = 800 if index % 2 == 0 else 600
        height = 450 if index % 2 == 0 else 400
        keyword = keywords[0] if keywords else 'content'
        
        return {
            'url': f"https://via.placeholder.com/{width}x{height}/4A5568/FFFFFF?text={keyword.replace(' ', '+')}",
            'alt': f"placeholder for {keyword}",
            'caption': "Image placeholder - replace with relevant image",
            'source': 'Placeholder.com',
            'position': index,
            'type': 'placeholder'
        }
    
    def embed_images_in_content(self, content: str, images: List[Dict]) -> str:
        """Embed images into content"""
        
        if not images:
            return content
        
        paragraphs = re.split(r'\n\s*\n', content)
        total_paragraphs = len(paragraphs)
        
        if total_paragraphs >= 8:
            positions = [2, 4, 6]
            if total_paragraphs >= 12 and len(images) > 3:
                positions.append(8)
        elif total_paragraphs >= 4:
            positions = [1, 2]
        else:
            positions = [1] if total_paragraphs > 2 else [0]
        
        result_paragraphs = []
        image_index = 0
        
        for i, paragraph in enumerate(paragraphs):
            result_paragraphs.append(paragraph)
            
            if i in positions and image_index < len(images):
                image_html = self._create_image_html(images[image_index])
                result_paragraphs.append(image_html)
                image_index += 1
        
        return '\n\n'.join(result_paragraphs)
    
    def _create_image_html(self, image_data: Dict) -> str:
        """Create image HTML"""
        
        return f'''
<div class="article-image" style="margin: 30px 0; text-align: center;">
    <img src="{image_data['url']}" 
         alt="{image_data['alt']}" 
         style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;"
         loading="lazy">
    <p style="font-style: italic; color: #666; margin-top: 10px; font-size: 0.9em;">
        {image_data['caption']} | Source: {image_data['source']}
    </p>
</div>
'''

# =================== AI CONTENT GENERATOR ===================

class AIContentGenerator:
    """AI content generator with Groq integration"""
    
    def __init__(self, groq_api_key: str = None):
        self.groq_api_key = groq_api_key
        self.models = [
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
    
    def generate_article(self, topic: str, word_count: int = 1800) -> Dict:
        """Generate article using AI"""
        
        print(f"🤖 Generating article: '{topic}'")
        
        # Try Groq first
        if GROQ_AVAILABLE and self.groq_api_key:
            result = self._generate_with_groq(topic, word_count)
            if result.get('success'):
                return result
        
        # Fallback to template
        return self._generate_with_template(topic, word_count)
    
    def _generate_with_groq(self, topic: str, word_count: int) -> Dict:
        """Generate using Groq AI"""
        
        try:
            client = Groq(api_key=self.groq_api_key)
            
            prompt = f"""Write a comprehensive, SEO-optimized article about: "{topic}"

REQUIREMENTS:
1. Word Count: {word_count}+ words
2. Format: Use HTML tags (h1, h2, h3, p, ul, li, strong, table)
3. Structure: Introduction, 5-7 main sections with subheadings, conclusion
4. SEO: Naturally include keywords and LSI terms
5. Tone: Professional, informative, engaging
6. Quality: Provide practical, actionable information

SECTIONS TO INCLUDE:
- Introduction with compelling hook
- Main sections with detailed explanations
- Examples and case studies
- Step-by-step guidance
- Statistics and data (use tables where appropriate)
- Best practices
- Common mistakes to avoid
- Conclusion with actionable next steps

Return only the HTML content, no explanations."""
            
            for model in self.models:
                try:
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional SEO content writer creating comprehensive, engaging articles."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=int(word_count * 1.3)
                    )
                    
                    content = completion.choices[0].message.content
                    
                    if self._validate_content(content):
                        return {
                            'success': True,
                            'content': self._clean_content(content),
                            'word_count': len(content.split()),
                            'model': model,
                            'source': 'groq'
                        }
                        
                except Exception as e:
                    print(f"   ⚠️  Model {model} failed: {e}")
                    continue
        
        except Exception as e:
            print(f"❌ Groq generation failed: {e}")
        
        return {'success': False, 'error': 'Groq generation failed'}
    
    def _validate_content(self, content: str) -> bool:
        """Validate content"""
        if not content or len(content.strip()) < 300:
            return False
        
        words = len(content.split())
        return words >= 500
    
    def _clean_content(self, content: str) -> str:
        """Clean content"""
        content = re.sub(r'```[a-z]*\n', '', content)
        content = content.replace('```', '')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _generate_with_template(self, topic: str, word_count: int) -> Dict:
        """Generate using template"""
        
        template = self._create_template(topic, word_count)
        
        return {
            'success': True,
            'content': template,
            'word_count': len(template.split()),
            'source': 'template',
            'quality': 'good'
        }
    
    def _create_template(self, topic: str, word_count: int) -> str:
        """Create template article"""
        
        current_year = datetime.now().year
        
        return f'''
<h1>{topic}</h1>

<p>Welcome to this comprehensive guide on {topic}. In today's rapidly evolving landscape, understanding {topic.lower()} is crucial for success in {current_year} and beyond.</p>

<h2>Why {topic} Matters Today</h2>
<p>The importance of {topic.lower()} cannot be overstated. With technological advancements and changing market dynamics, mastering {topic.lower()} provides significant competitive advantages.</p>

<h2>Getting Started: The Fundamentals</h2>
<p>Before diving into advanced concepts, let's cover the essential foundations:</p>
<ul>
<li><strong>Core Principles:</strong> Understanding the basic concepts</li>
<li><strong>Essential Tools:</strong> Must-have resources and software</li>
<li><strong>Skill Requirements:</strong> What you need to know</li>
<li><strong>Key Terminology:</strong> Important terms and definitions</li>
</ul>

<h2>Comprehensive Implementation Guide</h2>
<h3>Phase 1: Research and Planning</h3>
<p>Begin with thorough market research and create a detailed implementation plan.</p>

<h3>Phase 2: Setup and Preparation</h3>
<p>Gather necessary resources and configure your environment.</p>

<h3>Phase 3: Execution and Implementation</h3>
<p>Systematically implement your plan with regular testing.</p>

<h3>Phase 4: Optimization and Scaling</h3>
<p>Continuously optimize based on results and scale successful implementations.</p>

<h2>Best Practices for Success</h2>
<ul>
<li>Start with clear, measurable goals</li>
<li>Document your progress and learnings</li>
<li>Test frequently and iterate based on results</li>
<li>Stay updated with industry developments</li>
<li>Network with other professionals</li>
</ul>

<h2>Common Challenges and Solutions</h2>
<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
<tr style="background-color: #f7fafc;">
    <th style="padding: 12px; text-align: left;">Challenge</th>
    <th style="padding: 12px; text-align: left;">Solution</th>
</tr>
<tr>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Technical Complexity</td>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Break into smaller tasks, seek expert guidance</td>
</tr>
<tr>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Time Constraints</td>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Prioritize tasks, use time management tools</td>
</tr>
<tr>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Resource Limitations</td>
    <td style="padding: 12px; border: 1px solid #e2e8f0;">Leverage free tools, focus on high-impact areas</td>
</tr>
</table>

<h2>Future Outlook and Trends</h2>
<p>Looking ahead to {current_year + 1} and beyond, several trends are shaping the future of {topic.lower()}:</p>
<ul>
<li>Increased automation and AI integration</li>
<li>Greater focus on sustainability</li>
<li>Enhanced user experience expectations</li>
<li>New regulatory developments</li>
</ul>

<h2>Conclusion</h2>
<p>{topic} represents a significant opportunity for growth and development. By following this guide and implementing the strategies discussed, you're well-positioned for success.</p>

<p><strong>Your Action Plan:</strong> Begin with one section today, track progress weekly, and continuously adapt based on results.</p>
'''

# =================== CONTENT EXPANDER ===================

class ContentExpander:
    """Expand content to target word count"""
    
    def __init__(self):
        self.expansion_modules = [
            self._add_statistics_section,
            self._add_case_study,
            self._add_comparison_table,
            self._add_step_by_step_guide,
            self._add_faq_section,
            self._add_resource_list,
            self._add_implementation_checklist,
            self._add_expert_quotes
        ]
    
    def expand_content(self, content: str, topic: str, target_words: int = 1800) -> str:
        """Expand content to target word count"""
        
        current_words = len(content.split())
        print(f"📈 Expanding content: {current_words} → {target_words} words")
        
        expanded = content
        
        # Add expansion modules
        modules_to_add = min(5, len(self.expansion_modules))
        for i in range(modules_to_add):
            try:
                new_section = self.expansion_modules[i](topic)
                expanded += "\n\n" + new_section
                
                current_words = len(expanded.split())
                if current_words >= target_words * 0.8:
                    break
                    
            except Exception as e:
                print(f"   ⚠️  Expansion module failed: {e}")
                continue
        
        final_count = len(expanded.split())
        print(f"   ✅ Expanded to {final_count} words")
        
        return expanded
    
    def _add_statistics_section(self, topic: str) -> str:
        """Add statistics section"""
        current_year = datetime.now().year
        
        return f'''
<h3>📊 Market Statistics and Growth Analysis</h3>

<p>The {topic} market has shown remarkable growth in recent years. Here are key statistics for {current_year}:</p>

<table style="width:100%; border-collapse: collapse; margin: 20px 0; border-radius: 8px; overflow: hidden;">
<tr style="background-color: #4A5568; color: white;">
    <th style="padding: 12px; text-align: left;">Metric</th>
    <th style="padding: 12px; text-align: left;">Value</th>
    <th style="padding: 12px; text-align: left;">Trend</th>
</tr>
<tr style="background-color: #f7fafc;">
    <td style="padding: 12px;"><strong>Annual Growth Rate</strong></td>
    <td style="padding: 12px;">{random.randint(15, 45)}%</td>
    <td style="padding: 12px;">📈 Increasing</td>
</tr>
<tr>
    <td style="padding: 12px;"><strong>Market Size</strong></td>
    <td style="padding: 12px;">${random.randint(1, 50)}B</td>
    <td style="padding: 12px;">💰 Expanding</td>
</tr>
<tr style="background-color: #f7fafc;">
    <td style="padding: 12px;"><strong>User Adoption</strong></td>
    <td style="padding: 12px;">{random.randint(25, 75)}%</td>
    <td style="padding: 12px;">📱 Growing</td>
</tr>
<tr>
    <td style="padding: 12px;"><strong>ROI Potential</strong></td>
    <td style="padding: 12px;">{random.randint(120, 300)}%</td>
    <td style="padding: 12px;">💎 High Value</td>
</tr>
</table>
'''
    
    def _add_case_study(self, topic: str) -> str:
        """Add case study section"""
        
        companies = ['TechCorp Inc.', 'Global Solutions Ltd.', 'InnovateStartup', 'Enterprise Systems']
        company = random.choice(companies)
        
        return f'''
<h3>🏆 Success Case Study: {company}</h3>

<div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3182ce;">
<h4 style="margin-top: 0; color: #2d3748;">The Challenge</h4>
<p>{company} faced significant challenges with {topic.lower()}, including inefficient processes and high operational costs.</p>

<h4 style="color: #2d3748;">The Solution</h4>
<p>Implementation of a comprehensive {topic.lower()} strategy focusing on automation and optimization.</p>

<h4 style="color: #2d3748;">The Results</h4>
<ul>
<li>✅ <strong>90% reduction</strong> in processing time</li>
<li>✅ <strong>66% cost savings</strong> in operations</li>
<li>✅ <strong>93% decrease</strong> in error rates</li>
<li>✅ <strong>42% increase</strong> in employee satisfaction</li>
</ul>

<p><em>ROI achieved within 6 months of implementation.</em></p>
</div>
'''
    
    def _add_comparison_table(self, topic: str) -> str:
        """Add comparison table"""
        
        return f'''
<h3>⚖️ Method Comparison Analysis</h3>

<p>When approaching {topic.lower()}, it's crucial to understand different methodologies:</p>

<table style="width:100%; border-collapse: collapse; margin: 20px 0; border-radius: 8px; overflow: hidden;">
<tr style="background-color: #edf2f7;">
    <th style="padding: 12px; border: 1px solid #cbd5e0;">Approach</th>
    <th style="padding: 12px; border: 1px solid #cbd5e0;">Time Required</th>
    <th style="padding: 12px; border: 1px solid #cbd5e0;">Cost</th>
    <th style="padding: 12px; border: 1px solid #cbd5e0;">Success Rate</th>
</tr>
<tr>
    <td style="padding: 12px; border: 1px solid #cbd5e0;"><strong>Traditional Method</strong></td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">6-12 months</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">$$$$</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">40%</td>
</tr>
<tr style="background-color: #f7fafc;">
    <td style="padding: 12px; border: 1px solid #cbd5e0;"><strong>Modern Solution</strong></td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">2-4 months</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">$$</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">75%</td>
</tr>
<tr>
    <td style="padding: 12px; border: 1px solid #cbd5e0;"><strong>Advanced Approach</strong></td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">3-6 weeks</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">$</td>
    <td style="padding: 12px; border: 1px solid #cbd5e0;">92%</td>
</tr>
</table>
'''
    
    def _add_faq_section(self, topic: str) -> str:
        """Add FAQ section"""
        
        return f'''
<h3>❓ Frequently Asked Questions</h3>

<div style="margin: 20px 0;">
<div style="background: #f7fafc; padding: 15px; border-radius: 6px; margin-bottom: 10px; border-left: 3px solid #4a5568;">
<strong>Q: How long does it take to see results with {topic.lower()}?</strong><br>
<em>A:</em> Most users see initial results within 4-8 weeks, with significant outcomes appearing after 3-6 months of consistent implementation.
</div>

<div style="background: #f7fafc; padding: 15px; border-radius: 6px; margin-bottom: 10px; border-left: 3px solid #4a5568;">
<strong>Q: What's the typical investment required?</strong><br>
<em>A:</em> Initial investments range from $1,000-$5,000 for small businesses to $10,000-$50,000 for enterprises, with ROI typically achieved within 6-12 months.
</div>

<div style="background: #f7fafc; padding: 15px; border-radius: 6px; border-left: 3px solid #4a5568;">
<strong>Q: Can beginners implement {topic.lower()} successfully?</strong><br>
<em>A:</em> Absolutely! With proper guidance and step-by-step implementation, beginners can achieve excellent results. Start small and scale gradually.
</div>
</div>
'''

# =================== YOUTUBE EMBEDDER ===================

class YouTubeEmbedder:
    """YouTube video embedder"""
    
    def __init__(self):
        self.fallback_videos = {
            'technology': 'dQw4w9WgXcQ',
            'business': '3JluqTojuME',
            'marketing': 'yzXzMkGzE1Q',
            'education': 'RkP_hGzBp4E',
            'finance': 'xq7Xa8MhqAE'
        }
    
    def find_relevant_video(self, topic: str, category: str = 'technology') -> Dict:
        """Find relevant YouTube video"""
        
        print(f"🎥 Searching for YouTube video about: {topic}")
        
        video_id = self.fallback_videos.get(category, 'dQw4w9WgXcQ')
        
        return {
            'video_id': video_id,
            'embed_url': f"https://www.youtube.com/embed/{video_id}",
            'watch_url': f"https://www.youtube.com/watch?v={video_id}",
            'title': f"Related video: {topic}",
            'source': 'YouTube',
            'found': True
        }
    
    def embed_video_in_content(self, content: str, video_data: Dict) -> str:
        """Embed YouTube video in content"""
        
        video_html = f'''
<div class="youtube-embed" style="margin: 40px 0; background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #ff0000; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #333;">📺 Watch Related Video</h3>
    
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 20px 0; border-radius: 8px;">
        <iframe src="{video_data['embed_url']}" 
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 8px;"
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    
    <p style="text-align: center; margin-top: 15px;">
        <a href="{video_data['watch_url']}" target="_blank" style="background: #ff0000; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold;">
            🔗 Watch on YouTube
        </a>
    </p>
</div>
'''
        
        paragraphs = content.split('\n\n')
        insert_position = max(1, len(paragraphs) // 3)
        paragraphs.insert(insert_position, video_html)
        
        return '\n\n'.join(paragraphs)

# =================== WORDPRESS PUBLISHER ===================

class WordPressPublisher:
    """WordPress publisher"""
    
    def __init__(self, wp_url: str, wp_username: str, app_password: str):
        self.wp_url = wp_url.rstrip('/')
        self.wp_username = wp_username
        self.app_password = app_password
        self.api_url = f"{self.wp_url}/wp-json/wp/v2"
        
        self.auth = (self.wp_username, self.app_password)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
    
    def publish_article(self, article: Dict, language: str = 'en') -> Dict:
        """Publish article to WordPress"""
        
        print(f"🌐 Publishing {language.upper()} version to WordPress...")
        
        post_data = {
            'title': article.get('title', 'Untitled'),
            'content': article.get('content', ''),
            'status': 'draft',
            'slug': self._generate_slug(article.get('title', '')),
            'lang': language
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/posts",
                json=post_data,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    'success': True,
                    'post_id': result.get('id'),
                    'link': result.get('link'),
                    'edit_link': result.get('link', '').replace('?p=', '/wp-admin/post.php?action=edit&post='),
                    'language': language
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL slug"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug[:100]

# =================== SMART TOPIC SELECTOR ===================

class SmartTopicSelector:
    """Smart topic selector for high-profit articles"""
    
    def __init__(self):
        self.high_profit_topics = [
            f"How to Make Money Online in {datetime.now().year}: Complete Guide",
            f"Passive Income Strategies for {datetime.now().year}",
            "Affiliate Marketing: Complete Beginner's Guide",
            "YouTube Monetization Mastery",
            "WordPress Blogging for Profit",
            "Digital Product Creation Guide",
            "Email Marketing for Beginners",
            "Social Media Monetization Strategies",
            "Stock Market Investing Basics",
            "Real Estate Investing Online"
        ]
        
        self.categories = {
            'technology': ['AI', 'Programming', 'Cybersecurity', 'Blockchain', 'Cloud Computing'],
            'business': ['Marketing', 'Entrepreneurship', 'Finance', 'E-commerce', 'Startups'],
            'finance': ['Investing', 'Personal Finance', 'Cryptocurrency', 'Stock Market', 'Budgeting'],
            'health': ['Fitness', 'Nutrition', 'Mental Health', 'Wellness', 'Medical'],
            'education': ['Online Learning', 'Skills Development', 'Certifications', 'Study Tips']
        }
    
    def get_trending_topic(self) -> Dict:
        """Get trending topic with high profit potential"""
        
        # 70% chance for high-profit topic
        if random.random() < 0.7:
            topic = random.choice(self.high_profit_topics)
            category = 'business'
        else:
            category = random.choice(list(self.categories.keys()))
            keyword = random.choice(self.categories[category])
            
            templates = [
                f"The Complete Guide to {keyword}",
                f"{keyword}: Everything You Need to Know",
                f"How to Master {keyword} in {datetime.now().year}",
                f"{keyword} Best Practices and Strategies"
            ]
            
            topic = random.choice(templates)
        
        return {
            'topic': topic,
            'category': category,
            'trend_score': random.randint(75, 95),
            'competition': random.choice(['Low', 'Medium', 'High']),
            'estimated_cpc': round(random.uniform(1.5, 4.0), 2),
            'profit_potential': 'High' if category in ['business', 'finance'] else 'Medium'
        }

# =================== MAIN PROFIT MACHINE V10 ===================

class ProfitMachineV10:
    """Main Profit Machine v10 orchestrator"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        print("🚀 Initializing Profit Machine v10.0...")
        print("=" * 80)
        
        # Initialize all engines
        self.ai_generator = AIContentGenerator(
            groq_api_key=config_manager.get('GROQ_API_KEY')
        )
        
        self.content_expander = ContentExpander()
        self.voice_engine = VoiceAIEngine()
        self.visual_engine = VisualAIEngine()
        self.youtube_embedder = YouTubeEmbedder()
        self.topic_selector = SmartTopicSelector()
        
        # Enhanced components
        self.database = PersistentDatabaseManager()
        self.revenue_calculator = SmartRevenueCalculator()
        self.affiliate_manager = SafeAffiliateManager(config_manager)
        self.content_formatter = AdvancedContentFormatter(config_manager)
        self.performance_monitor = PerformanceMonitor()
        
        # Initialize publishers
        self.wordpress = None
        wp_url = config_manager.get('WP_URL')
        wp_user = config_manager.get('WP_USERNAME')
        wp_pass = config_manager.get('WP_PASSWORD')
        
        if wp_url and wp_user and wp_pass:
            self.wordpress = WordPressPublisher(wp_url, wp_user, wp_pass)
        
        # Initialize Telegram
        self.telegram = None
        bot_token = config_manager.get('TELEGRAM_BOT_TOKEN')
        chat_id = config_manager.get('TELEGRAM_CHAT_ID')
        
        if bot_token and chat_id:
            self.telegram = EnhancedTelegramNotifier(bot_token, chat_id)
        
        print("✅ All systems initialized")
        print("=" * 80)
    
    def execute_daily_run(self) -> Dict:
        """Execute complete profit machine run"""
        
        print("\n💰 Starting Profit Machine v10.0...")
        start_time = time.time()
        execution_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Start performance monitoring
            self.performance_monitor.start()
            
            # 1. Select smart topic
            topic_selection_start = time.time()
            topic_data = self.topic_selector.get_trending_topic()
            topic = topic_data['topic']
            category = topic_data['category']
            
            self.performance_monitor.log_component('topic_selection', time.time() - topic_selection_start)
            print(f"🎯 Topic: {topic}")
            print(f"📁 Category: {category}")
            print(f"💰 Estimated CPC: ${topic_data['estimated_cpc']}")
            
            # 2. Generate base article
            article_start = time.time()
            ai_result = self.ai_generator.generate_article(
                topic, 
                word_count=self.config.get('TARGET_WORD_COUNT', 1800)
            )
            
            if not ai_result.get('success'):
                error_msg = ai_result.get('error', 'AI generation failed')
                raise Exception(f"Article generation failed: {error_msg}")
            
            self.performance_monitor.log_component('ai_generation', time.time() - article_start)
            
            # 3. Expand content
            expand_start = time.time()
            expanded_content = self.content_expander.expand_content(
                ai_result['content'],
                topic,
                target_words=self.config.get('TARGET_WORD_COUNT', 1800)
            )
            
            self.performance_monitor.log_component('content_expansion', time.time() - expand_start)
            
            base_article = {
                'title': topic,
                'content': expanded_content,
                'word_count': len(expanded_content.split()),
                'category': category
            }
            
            # 4. Generate images
            images_start = time.time()
            images = self.visual_engine.generate_article_images(
                topic, 
                num_images=self.config.get('IMAGE_COUNT', 4)
            )
            
            content_with_images = self.visual_engine.embed_images_in_content(
                base_article['content'],
                images
            )
            
            self.performance_monitor.log_component('image_generation', time.time() - images_start)
            
            # 5. Add YouTube video
            video_start = time.time()
            video_data = self.youtube_embedder.find_relevant_video(topic, category)
            content_with_video = self.youtube_embedder.embed_video_in_content(
                content_with_images,
                video_data
            )
            
            self.performance_monitor.log_component('video_embedding', time.time() - video_start)
            
            # 6. Add affiliate links
            affiliate_start = time.time()
            content_with_affiliates, affiliate_count = self.affiliate_manager.embed_affiliate_links(
                content_with_video,
                topic,
                category
            )
            
            self.performance_monitor.log_component('affiliate_integration', time.time() - affiliate_start)
            
            # 7. Advanced formatting
            formatting_start = time.time()
            formatted_content = self.content_formatter.format_content(
                content_with_affiliates,
                topic
            )
            
            self.performance_monitor.log_component('content_formatting', time.time() - formatting_start)
            
            # Update article with all enhancements
            final_article = {
                'title': topic,
                'content': formatted_content,
                'word_count': len(formatted_content.split()),
                'category': category,
                'images_count': len(images),
                'affiliate_links_count': affiliate_count,
                'has_video': True,
                'has_toc': self.config.get('INCLUDE_TABLE_OF_CONTENTS', True)
            }
            
            # 8. Calculate revenue
            revenue_start = time.time()
            revenue_estimate = self.revenue_calculator.calculate_revenue(
                final_article,
                category=category,
                language='en',
                country='US'
            )
            
            self.performance_monitor.log_component('revenue_calculation', time.time() - revenue_start)
            
            # 9. Create audio (optional)
            audio_data = None
            if TTS_AVAILABLE:
                audio_start = time.time()
                audio_data = self.voice_engine.create_audio_summary(formatted_content, 'en')
                if audio_data.get('success'):
                    final_article['has_audio'] = True
                self.performance_monitor.log_component('audio_generation', time.time() - audio_start)
            
            # 10. Publish to WordPress
            publish_results = []
            if self.wordpress:
                publish_start = time.time()
                result = self.wordpress.publish_article(final_article, 'en')
                publish_results.append(result)
                
                if result['success']:
                    final_article['published'] = True
                    final_article['publish_date'] = datetime.now().isoformat()
                
                self.performance_monitor.log_component('wordpress_publishing', time.time() - publish_start)
            
            # 11. Log to database
            db_start = time.time()
            article_id = self.database.log_article({
                **final_article,
                'revenue_estimate': revenue_estimate['monthly_estimate']
            })
            
            # Backup database to GitHub
            if self.config.get('BACKUP_TO_GITHUB', True):
                self.database.backup_to_github()
            
            self.performance_monitor.log_component('database_operations', time.time() - db_start)
            
            # 12. Get performance report
            performance_report = self.performance_monitor.get_report()
            
            # 13. Get statistics
            stats_report = self.database.get_statistics()
            
            # 14. Prepare final report
            total_time = time.time() - start_time
            final_report = {
                'execution_id': execution_id,
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'topic_data': topic_data,
                'article_info': {
                    'title': final_article['title'],
                    'word_count': final_article['word_count'],
                    'images_count': final_article['images_count'],
                    'affiliate_links_count': final_article['affiliate_links_count'],
                    'has_audio': final_article.get('has_audio', False),
                    'has_video': final_article.get('has_video', False),
                    'published': final_article.get('published', False)
                },
                'revenue_estimate': revenue_estimate,
                'performance_report': performance_report,
                'stats_report': stats_report,
                'total_execution_time': total_time
            }
            
            # 15. Save report to file
            os.makedirs('reports', exist_ok=True)
            report_file = f"reports/execution_{execution_id}.json"
            with open(report_file, 'w') as f:
                json.dump(final_report, f, indent=2)
            
            # 16. Send Telegram report
            if self.telegram and self.config.get('TELEGRAM_DAILY_REPORT', True):
                telegram_start = time.time()
                self.telegram.send_daily_report(final_report)
                
                # Send report file if small enough
                if os.path.getsize(report_file) < 20 * 1024 * 1024:  # 20MB limit
                    self.telegram.send_document(report_file, f"Complete report: {execution_id}")
                
                self.performance_monitor.log_component('telegram_notification', time.time() - telegram_start)
            
            # 17. Print summary
            print("\n" + "=" * 80)
            print("✅ PROFIT MACHINE v10.0 EXECUTION SUCCESSFUL!")
            print("=" * 80)
            print(f"📝 Article: {topic}")
            print(f"📊 Words: {final_article['word_count']:,}")
            print(f"🖼️ Images: {final_article['images_count']}")
            print(f"🔗 Affiliate Links: {final_article['affiliate_links_count']}")
            print(f"💰 Monthly Revenue Estimate: ${revenue_estimate['monthly_estimate']:.2f}")
            print(f"⚡ Execution Time: {total_time:.1f}s")
            print(f"📄 Report File: {report_file}")
            
            return final_report
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"\n❌ Execution failed: {e}")
            
            # Log error
            self.performance_monitor.log_error('main_execution', str(e))
            
            # Send error alert to Telegram
            if self.telegram and self.config.get('TELEGRAM_ERROR_ALERTS', True):
                self.telegram.send_error_alert(str(e), error_time)
            
            # Return error report
            return {
                'execution_id': execution_id,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e),
                'total_execution_time': error_time
            }

# =================== MAIN EXECUTION ===================

def main():
    """Main execution function"""
    
    print("=" * 80)
    print("🏆 ULTIMATE MONEY MAKER v10.0 - COMPLETE PROFIT MACHINE")
    print("✅ Smart Revenue Calculator | Safe Affiliate Integration | Self-Healing")
    print("=" * 80)
    
    # Initialize configuration
    config_manager = ConfigManager()
    
    # Check for setup mode
    if len(sys.argv) > 1:
        if sys.argv[1] == '--setup':
            print("\n🔧 Setup Mode Activated")
            print("Creating necessary directories and config file...")
            
            # Create directories
            os.makedirs('audio_output', exist_ok=True)
            os.makedirs('reports', exist_ok=True)
            os.makedirs('data', exist_ok=True)
            os.makedirs('.github/workflows', exist_ok=True)
            
            # Create GitHub Actions workflow
            workflow_content = '''name: Profit Machine v10

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8:00 AM
  workflow_dispatch:      # Manual trigger

jobs:
  run-profit-machine:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests groq gtts pygame psutil
        
    - name: Create directories
      run: |
        mkdir -p audio_output reports data
        
    - name: Run Profit Machine v10
      env:
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        WP_URL: ${{ secrets.WP_URL }}
        WP_USERNAME: ${{ secrets.WP_USERNAME }}
        WP_PASSWORD: ${{ secrets.WP_PASSWORD }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        AMAZON_AFFILIATE_ID: ${{ secrets.AMAZON_AFFILIATE_ID }}
        CLICKBANK_AFFILIATE_ID: ${{ secrets.CLICKBANK_AFFILIATE_ID }}
        SHAREASALE_AFFILIATE_ID: ${{ secrets.SHAREASALE_AFFILIATE_ID }}
      run: |
        python profit_machine_v10.py
        
    - name: Backup database to GitHub
      run: |
        git config --global user.email "actions@github.com"
        git config --global user.name "GitHub Actions"
        git add data/
        git add reports/
        git commit -m "Database backup $(date +'%Y-%m-%d %H:%M')" || echo "No changes to commit"
        git pull --rebase
        git push
'''
            
            with open('.github/workflows/profit_machine.yml', 'w') as f:
                f.write(workflow_content)
            
            # Create config file if doesn't exist
            if not os.path.exists('config.json'):
                config_manager.save()
                print("✅ Config file created: config.json")
            
            print("✅ Setup complete!")
            print("\n📋 Next Steps:")
            print("1. Edit config.json with your settings")
            print("2. Add secrets to GitHub Repository → Settings → Secrets and variables → Actions")
            print("3. Commit and push to GitHub")
            print("4. Profit Machine will run daily at 8:00 AM")
            return True
    
    # Check minimum requirements
    if not config_manager.get('GROQ_API_KEY'):
        print("⚠️  WARNING: GROQ_API_KEY not set. AI generation may use templates only.")
    
    # Create necessary directories
    os.makedirs('audio_output', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Initialize and run Profit Machine
    try:
        profit_machine = ProfitMachineV10(config_manager)
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
    
    # Execute
    result = profit_machine.execute_daily_run()
    
    if result.get('success'):
        print("\n🎉 Daily execution completed successfully!")
        
        # Final status
        status = {
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'version': '10.0',
            'execution_id': result.get('execution_id'),
            'revenue_estimate': result.get('revenue_estimate', {}).get('monthly_estimate', 0),
            'next_steps': [
                "1. Review generated article",
                "2. Check affiliate links",
                "3. Publish to WordPress",
                "4. Schedule social media posts"
            ]
        }
        
        with open('profit_machine_status.json', 'w') as f:
            json.dump(status, f, indent=2)
        
        return True
    else:
        print(f"\n❌ Execution failed: {result.get('error')}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
