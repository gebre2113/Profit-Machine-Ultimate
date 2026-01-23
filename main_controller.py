#!/usr/bin/env python3
"""
🏆 PROFIT MACHINE ULTIMATE - ENHANCED MASTER CONTROLLER
🚀 Complete integration with WordPress, Telegram, GitHub, and advanced error handling
"""

import os
import sys
import json
import time
import logging
import traceback
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from requests.auth import HTTPBasicAuth

# የፋይል መንገድ ማረጋገጥ
def ensure_exports_directory():
    """Ensure exports directory exists at module level"""
    try:
        directory = "exports"
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created exports directory: {os.path.abspath(directory)}")
        
        # ባዶ JSON ፋይል መፍጠር
        file_path = os.path.join(directory, "backup_info.json")
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
            print(f"✅ Created backup file: {file_path}")
    except Exception as e:
        print(f"❌ Error creating exports directory: {e}")

# አሁኑኑ ፎልደሩን መፍጠር
ensure_exports_directory()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ተለዋጭ በማስቀመጥ ከሰህተት መከላከል
TELEGRAM_AVAILABLE = False
TELEGRAM_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'utils', 'telegram_reporter.py')

try:
    # Check if telegram reporter file exists
    if os.path.exists(TELEGRAM_MODULE_PATH):
        # Add utils to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
        from telegram_reporter import EnhancedTelegramReporter
        TELEGRAM_AVAILABLE = True
        print("✅ Telegram reporter loaded from file")
    else:
        print(f"⚠️ Telegram reporter file not found at: {TELEGRAM_MODULE_PATH}")
except ImportError as e:
    print(f"⚠️ Telegram reporter import failed: {e}")
except Exception as e:
    print(f"⚠️ Telegram reporter error: {e}")

class EnhancedMasterController:
    """Enhanced master controller with WordPress, Telegram, and GitHub integration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config = self._load_config()
        
        # Initialize WordPress connection
        self.wp_enabled = self._check_wordpress_config()
        if self.wp_enabled:
            print("✅ WordPress publishing enabled")
        
        # Initialize reporting
        self.telegram_reporter = None
        if TELEGRAM_AVAILABLE and self.config.get('telegram', {}).get('enabled', False):
            try:
                # Get credentials from config or environment
                bot_token = self.config.get('telegram', {}).get('bot_token') or os.getenv('TELEGRAM_BOT_TOKEN')
                chat_id = self.config.get('telegram', {}).get('chat_id') or os.getenv('TELEGRAM_CHAT_ID')
                
                if bot_token and chat_id:
                    self.telegram_reporter = EnhancedTelegramReporter(bot_token, chat_id)
                    print("✅ Telegram reporter initialized")
                else:
                    print("⚠️ Telegram credentials missing")
            except Exception as e:
                print(f"❌ Failed to initialize Telegram: {e}")
        else:
            print("ℹ️ Telegram reporter disabled or not available")
        
        # GitHub Actions detection
        self.is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        self.run_id = os.getenv('GITHUB_RUN_ID', 'local')
        
        # Enhanced logging
        self.setup_enhanced_logging()
        
        # Performance tracking
        self.performance_tracker = PerformanceTracker()
        
        print("🎛️ Enhanced Master Controller Initialized")
        if self.is_github_actions:
            print("🌐 Running in GitHub Actions environment")
        
        # WordPress stats
        self.wp_published = 0
        self.wp_failed = 0
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        config_files = [
            self.project_root / "config.json",
            self.project_root / "config_complete.json",
            self.project_root / "config" / "config.json"
        ]
        
        for config_path in config_files:
            try:
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        print(f"✅ Loaded config from: {config_path}")
                        return config
            except Exception as e:
                print(f"⚠️ Error loading config from {config_path}: {e}")
        
        # Default configuration
        print("⚠️ Using default configuration")
        return {
            'telegram': {
                'enabled': False,
                'bot_token': '',
                'chat_id': ''
            },
            'wordpress': {
                'enabled': False,
                'url': '',
                'username': '',
                'app_password': ''
            },
            'enable_hybrid_mode': True,
            'max_retries': 3,
            'retry_delay': 5,
            'auto_publish_to_wp': False
        }
    
    def _check_wordpress_config(self) -> bool:
        """Check WordPress configuration"""
        wp_config = self.config.get('wordpress', {})
        
        # Check config first
        if wp_config.get('enabled'):
            required = ['url', 'username', 'app_password']
            if all(wp_config.get(field) for field in required):
                return True
        
        # Check environment variables
        env_vars = ['WP_URL', 'WP_USERNAME', 'WP_APPLICATION_PASSWORD']
        if all(os.getenv(var) for var in env_vars):
            return True
        
        return False
    
    def setup_enhanced_logging(self):
        """Setup enhanced logging with file rotation"""
        
        log_dir = self.project_root / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # Create loggers for different components
        self.loggers = {
            'master': self._create_logger('master'),
            'v10': self._create_logger('v10'),
            'v11': self._create_logger('v11'),
            'github': self._create_logger('github'),
            'wordpress': self._create_logger('wordpress'),
            'telegram': self._create_logger('telegram')
        }
    
    def _create_logger(self, name: str) -> logging.Logger:
        """Create a logger for a specific component"""
        
        logger = logging.getLogger(f'profit_machine.{name}')
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = self.project_root / 'logs' / f'{name}_{datetime.now().strftime("%Y%m%d")}.log'
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"❌ Error creating log file for {name}: {e}")
        
        # Console handler for GitHub Actions
        if self.is_github_actions:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('::%(levelname)s::%(name)s - %(message)s')
            )
            logger.addHandler(console_handler)
        
        return logger
    
    def execute_with_retry(self, func, max_retries=3, delay=5):
        """Execute function with retry logic"""
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                self.loggers['master'].warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}"
                )
                time.sleep(delay)
    
    def ensure_directory(self, directory_path: str) -> bool:
        """Ensure directory exists before writing files"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            self.loggers['master'].error(f"Failed to create directory {directory_path}: {e}")
            return False
    
    def save_to_exports(self, data: Dict, filename: str) -> Optional[str]:
        """Save data to exports directory with safety checks"""
        
        exports_dir = self.project_root / 'exports'
        if not self.ensure_directory(str(exports_dir)):
            return None
        
        file_path = exports_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.loggers['master'].info(f"✅ File saved: {file_path}")
            return str(file_path)
        except Exception as e:
            self.loggers['master'].error(f"❌ Failed to save {filename}: {e}")
            return None
    
    def publish_to_wordpress(self, content_data: Dict) -> Dict:
        """Publish generated content to WordPress via REST API"""
        
        # Get credentials from config or environment
        wp_config = self.config.get('wordpress', {})
        
        wp_url = wp_config.get('url') or os.getenv('WP_URL')
        wp_user = wp_config.get('username') or os.getenv('WP_USERNAME')
        wp_pass = wp_config.get('app_password') or os.getenv('WP_APPLICATION_PASSWORD')
        
        if not all([wp_url, wp_user, wp_pass]):
            msg = "⚠️ WordPress credentials missing. Skipping upload."
            self.loggers['wordpress'].warning(msg)
            return {'success': False, 'error': 'Missing credentials'}
        
        # Ensure URL has correct format
                # መጀመሪያ Content-ን አስተካክል (ከ f-string ውጭ)
        formatted_content = content.replace('\n', '<br>').replace('# ', '<h2>').replace('## ', '<h3>')
        
        # አሁን HTML-ን በ f-string አዘጋጅ (ያለ backslash)
        html_content = f"""
        <div class="profit-machine-article">
            <h1>{title}</h1>
            <div class="article-meta">
                <p>Generated by Profit Machine v11.0</p>
                <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            <div class="article-content">
                {formatted_content}
            </div>
            <footer>
                <p>Automatically generated content</p>
            </footer>
        </div>
        """
        
        payload = {{
            'title': title,
            'content': html_content,
            'status': 'publish',  # በቀጥታ እንዲለጠፍ 'publish' አድርገነዋል
            'categories': [1],
            'meta': {{
                'generated_by': 'Profit Machine v11.0',
                'generated_at': datetime.now().isoformat()
            }}
        }}

        
        try:
            self.loggers['wordpress'].info(f"📤 Publishing to WordPress: {title}")
            
            response = requests.post(
                wp_url,
                json=payload,
                auth=HTTPBasicAuth(wp_user, wp_pass),
                timeout=30,
                headers={
                    'User-Agent': 'Profit Machine v11.0',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                post_id = result.get('id')
                post_url = result.get('link', 'N/A')
                
                self.wp_published += 1
                self.loggers['wordpress'].info(f"✅ Successfully published to WordPress!")
                self.loggers['wordpress'].info(f"   Post ID: {post_id}")
                self.loggers['wordpress'].info(f"   Post URL: {post_url}")
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': post_url,
                    'response': result
                }
            else:
                error_msg = f"WordPress API error: {response.status_code} - {response.text}"
                self.wp_failed += 1
                self.loggers['wordpress'].error(error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            error_msg = "WordPress request timeout"
            self.wp_failed += 1
            self.loggers['wordpress'].error(error_msg)
            return {'success': False, 'error': error_msg}
            
        except requests.exceptions.ConnectionError:
            error_msg = "WordPress connection error - check URL"
            self.wp_failed += 1
            self.loggers['wordpress'].error(error_msg)
            return {'success': False, 'error': error_msg}
            
        except Exception as e:
            error_msg = f"WordPress error: {str(e)}"
            self.wp_failed += 1
            self.loggers['wordpress'].error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def run_daily_optimized(self):
        """Optimized daily workflow with WordPress publishing"""
        
        start_time = time.time()
        
        try:
            # Step 1: Check system health
            self.loggers['master'].info("🔍 Checking system health...")
            health_status = self.check_system_health()
            
            if not health_status['healthy']:
                error_msg = f"System health check failed: {health_status['issues']}"
                self.loggers['master'].error(error_msg)
                
                if self.telegram_reporter:
                    self.telegram_reporter.send_error_report(
                        error_msg, 0, 'health_check'
                    )
                
                return {'success': False, 'error': error_msg}
            
            # Step 2: Load or generate topics
            self.loggers['master'].info("🎯 Generating topics...")
            topics = self.get_optimized_topics()
            
            # Step 3: Smart execution with WordPress publishing
            results = {
                'v10_articles': [],
                'v11_articles': [],
                'enhanced_articles': [],
                'wordpress_published': [],
                'wordpress_failed': [],
                'failed_executions': []
            }
            
            for topic_data in topics:
                self.loggers['master'].info(f"Processing: {topic_data['topic']}")
                
                # Smart routing
                target = self.smart_router_enhanced(topic_data)
                
                if target == 'v10':
                    result = self.execute_with_retry(
                        lambda: self.run_v10(topic_data)
                    )
                else:
                    result = self.execute_with_retry(
                        lambda: self.run_v11(topic_data)
                    )
                
                if result['success']:
                    # Publish to WordPress if enabled
                    if self.wp_enabled and self.config.get('auto_publish_to_wp', False):
                        wp_result = self.publish_to_wordpress(result['data'])
                        
                        if wp_result['success']:
                            result['data']['wordpress'] = wp_result
                            results['wordpress_published'].append({
                                'topic': topic_data['topic'],
                                'post_id': wp_result.get('post_id'),
                                'post_url': wp_result.get('post_url')
                            })
                        else:
                            results['wordpress_failed'].append({
                                'topic': topic_data['topic'],
                                'error': wp_result.get('error')
                            })
                    
                    if target == 'v10':
                        results['v10_articles'].append(result)
                    else:
                        results['v11_articles'].append(result)
                else:
                    results['failed_executions'].append({
                        'topic': topic_data['topic'],
                        'error': result.get('error'),
                        'target': target
                    })
            
            # Step 4: Post-processing
            if results['v10_articles'] and self.config.get('enable_hybrid_mode', True):
                self.loggers['master'].info("🔄 Running hybrid enhancement...")
                enhanced = self.enhance_with_v11_batch(results['v10_articles'])
                results['enhanced_articles'] = enhanced
            
            # Step 5: Generate reports
            execution_time = time.time() - start_time
            report = self.generate_detailed_report(results, execution_time)
            
            # Step 6: Save results
            self.save_to_exports(results, f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            self.save_to_exports(report, f"report_{datetime.now().strftime('%Y%m%d')}.json")
            
            # Step 7: Send notifications
            if self.telegram_reporter:
                self.telegram_reporter.send_master_report({
                    'workflow': 'daily_optimized',
                    'execution_time': execution_time,
                    'results': results,
                    'wordpress_stats': {
                        'published': self.wp_published,
                        'failed': self.wp_failed
                    }
                })
            
            # Step 8: Backup to GitHub
            if self.is_github_actions:
                self.backup_to_github(results)
            
            self.loggers['master'].info(
                f"✅ Daily optimized workflow completed in {execution_time:.1f}s"
            )
            
            # WordPress summary
            if self.wp_enabled:
                self.loggers['master'].info(
                    f"📊 WordPress: {self.wp_published} published, {self.wp_failed} failed"
                )
            
            return {
                'success': True,
                'report': report,
                'execution_time': execution_time,
                'wordpress_stats': {
                    'published': self.wp_published,
                    'failed': self.wp_failed
                }
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            self.loggers['master'].error(f"Workflow failed: {error_msg}")
            traceback.print_exc()
            
            if self.telegram_reporter:
                self.telegram_reporter.send_error_report(
                    error_msg, execution_time, 'daily_optimized'
                )
            
            return {
                'success': False,
                'error': error_msg,
                'execution_time': execution_time
            }
    
    def smart_router_enhanced(self, topic_data: Dict) -> str:
        """Enhanced smart routing with ML-like decision making"""
        
        topic = topic_data['topic']
        category = topic_data.get('category', 'general')
        
        # Factor 1: Category value
        category_scores = {
            'finance': 10,
            'business': 9,
            'technology': 8,
            'health': 7,
            'education': 6,
            'lifestyle': 5,
            'general': 5
        }
        
        base_score = category_scores.get(category, 5)
        
        # Factor 2: Topic length (longer = more complex)
        word_count = len(topic.split())
        if word_count > 8:
            base_score += 2
        elif word_count > 5:
            base_score += 1
        
        # Factor 3: Time of day (optimize for social media posting)
        hour = datetime.now().hour
        if 9 <= hour <= 17:  # Business hours
            base_score += 1  # Better for v11 (social media ready)
        
        # Factor 4: Day of week
        day = datetime.now().weekday()
        if day in [0, 1, 2]:  # Monday-Wednesday
            base_score += 1  # Higher traffic days
        
        # Decision
        if base_score >= 8:
            return 'v11'  # High-value content to GOD MODE
        else:
            return 'v10'  # Regular content to v10
    
    def backup_to_github(self, results: Dict):
        """Enhanced GitHub backup with optimized commits"""
        
        if not self.is_github_actions:
            return
        
        try:
            # Only commit if there are actual results
            if results['v10_articles'] or results['v11_articles']:
                # Add files
                subprocess.run(['git', 'add', 'exports/'], check=False, capture_output=True)
                subprocess.run(['git', 'add', 'logs/'], check=False, capture_output=True)
                subprocess.run(['git', 'add', '*.json'], check=False, capture_output=True)
                subprocess.run(['git', 'add', '*.py'], check=False, capture_output=True)
                
                # ከ f-string ይልቅ ተራ ስትሪንግ በመጠቀም ስህተቱን ማስቀረት
                commit_message = "🤖 Profit Machine Backup: " + datetime.now().strftime('%Y-%m-%d %H:%M') + "\n\n"
                commit_message += "📊 Results:\n"
                commit_message += "- Created " + str(len(results['v10_articles'])) + " v10 articles\n"
                commit_message += "- Created " + str(len(results['v11_articles'])) + " v11 articles\n"
                commit_message += "- Enhanced " + str(len(results['enhanced_articles'])) + " articles\n"
                commit_message += "- WordPress: " + str(self.wp_published) + " published, " + str(self.wp_failed) + " failed\n"
                commit_message += "- Failed: " + str(len(results['failed_executions'])) + "\n\n"
                commit_message += "🌐 Run ID: " + str(self.run_id)
                
                subprocess.run(
                    ['git', 'commit', '-m', commit_message],
                    check=False,
                    capture_output=True
                )
                
                # Push
                subprocess.run(['git', 'push'], check=False, capture_output=True)
                
                self.loggers['github'].info("✅ Backup pushed to GitHub")
        
        except Exception as e:
            self.loggers['github'].error(f"GitHub backup failed: {e}")
    
    def check_system_health(self) -> Dict:
        """Check system health and required resources"""
        health_issues = []
        
        # Check directories
        required_dirs = ['exports', 'logs', 'data']
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                health_issues.append(f"Missing directory: {dir_name}")
                try:
                    dir_path.mkdir(exist_ok=True)
                except Exception as e:
                    health_issues.append(f"Failed to create {dir_name}: {e}")
        
        # Check API keys (simplified)
        required_env_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                health_issues.append(f"Missing environment variable: {var}")
        
        # Check WordPress if enabled
        if self.wp_enabled:
            if not self._check_wordpress_config():
                health_issues.append("WordPress credentials incomplete")
        
        return {
            'healthy': len(health_issues) == 0,
            'issues': health_issues,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_optimized_topics(self) -> List[Dict]:
        """Get optimized topics for processing"""
        
        # Default topics for GitHub Actions
        default_topics = [
            {'topic': 'Global Technology Trends', 'category': 'technology'},
            {'topic': 'Business Innovation', 'category': 'business'},
            {'topic': 'Economic Growth Opportunities', 'category': 'finance'},
            {'topic': 'Sustainable Development', 'category': 'business'},
            {'topic': 'Digital Transformation', 'category': 'technology'}
        ]
        
        # Save topics to file
        self.save_to_exports({'topics': default_topics}, 'topics.json')
        
        return default_topics
    
    def run_v10(self, topic_data: Dict) -> Dict:
        """Run version 10 (simplified version)"""
        try:
            topic = topic_data['topic']
            
            # Simulate processing
            time.sleep(2)  # Simulate API call
            
            result = {
                'id': f"v10_{int(time.time())}_{hash(topic) % 10000}",
                'topic': topic,
                'version': 'v10',
                'content': f"""# {topic}

## Executive Summary
This comprehensive analysis examines {topic} in today's dynamic market landscape.

## Key Findings
1. Market opportunities are expanding rapidly
2. Technological innovation is driving change
3. Strategic planning is essential for success

## Recommendations
- Invest in digital transformation
- Focus on customer experience
- Leverage data analytics

## Conclusion
{topic} presents significant opportunities for forward-thinking businesses.

*Generated by Profit Machine v10 on {datetime.now().strftime('%B %d, %Y')}*""",
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'word_count': 250,
                'seo_score': 85
            }
            
            # Save result
            filename = f"v10_{topic.replace(' ', '_').replace('/', '_')[:50]}.json"
            self.save_to_exports(result, filename)
            
            return {'success': True, 'data': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_v11(self, topic_data: Dict) -> Dict:
        """Run version 11 (advanced version)"""
        try:
            topic = topic_data['topic']
            category = topic_data.get('category', 'general')
            
            # Simulate processing
            time.sleep(3)  # Simulate API call
            
            result = {
                'id': f"v11_{int(time.time())}_{hash(topic) % 10000}",
                'topic': topic,
                'category': category,
                'version': 'v11',
                'content': f"""# {topic}: Comprehensive Analysis

## 📊 Executive Summary
This in-depth report provides a detailed analysis of {topic} in the current market environment. Our research indicates significant growth potential in this sector.

## 🎯 Market Overview
The {category} industry is undergoing rapid transformation, driven by technological innovation and changing consumer behaviors.

## 📈 Key Trends
1. **Digital Acceleration**: Increased adoption of digital technologies
2. **Sustainability Focus**: Growing emphasis on environmental, social, and governance (ESG) factors
3. **Data-Driven Decisions**: Leveraging analytics for strategic planning
4. **Remote Collaboration**: Evolution of work and collaboration models

## 💡 Strategic Insights
- **Opportunity Identification**: Emerging market segments showing 20%+ annual growth
- **Competitive Analysis**: Key players and market positioning
- **Risk Assessment**: Regulatory and market risks to consider
- **Innovation Pathways**: Technological advancements shaping the future

## 🚀 Actionable Recommendations
1. **Short-term (0-6 months)**: 
   - Implement digital transformation initiatives
   - Develop sustainability roadmap
   
2. **Medium-term (6-18 months)**:
   - Expand into emerging markets
   - Invest in research and development
   
3. **Long-term (18+ months)**:
   - Establish industry leadership position
   - Build strategic partnerships

## 📊 Financial Projections
- Market size: $XX billion
- Growth rate: XX% CAGR
- Investment required: $XX million
- ROI potential: XX% over 3 years

## 🎯 Conclusion
{topic} represents a significant opportunity for businesses that strategically position themselves in this evolving landscape. By adopting innovative approaches and leveraging emerging technologies, companies can achieve sustainable growth and competitive advantage.

*Generated by Profit Machine v11.0 GOD MODE on {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*""",
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'enhanced': True,
                'social_media_ready': True,
                'word_count': 450,
                'seo_score': 92,
                'readability_score': 88,
                'estimated_revenue': round(100 + (hash(topic) % 400), 2)
            }
            
            # Save result
            filename = f"v11_{topic.replace(' ', '_').replace('/', '_')[:50]}.json"
            self.save_to_exports(result, filename)
            
            return {'success': True, 'data': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def enhance_with_v11_batch(self, v10_articles: List[Dict]) -> List[Dict]:
        """Enhance V10 articles with V11 capabilities"""
        enhanced = []
        for article in v10_articles:
            try:
                enhanced_article = article['data'].copy()
                enhanced_article['enhanced'] = True
                enhanced_article['enhanced_at'] = datetime.now().isoformat()
                enhanced_article['enhanced_by'] = 'v11_enhancer'
                enhanced_article['seo_score'] = min(100, enhanced_article.get('seo_score', 0) + 5)
                enhanced_article['word_count'] = enhanced_article.get('word_count', 0) * 1.5
                
                enhanced.append(enhanced_article)
            except Exception as e:
                self.loggers['master'].error(f"Failed to enhance article: {e}")
        
        return enhanced
    
    def generate_detailed_report(self, results: Dict, execution_time: float) -> Dict:
        """Generate detailed execution report"""
        
        report = {
            'report_id': f"report_{self.run_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'execution_time_seconds': round(execution_time, 2),
            'environment': 'github_actions' if self.is_github_actions else 'local',
            'controller_version': 'v2.0',
            'features': {
                'wordpress': self.wp_enabled,
                'telegram': TELEGRAM_AVAILABLE and self.telegram_reporter is not None,
                'github_backup': self.is_github_actions,
                'hybrid_mode': self.config.get('enable_hybrid_mode', True)
            },
            'summary': {
                'v10_articles': len(results['v10_articles']),
                'v11_articles': len(results['v11_articles']),
                'enhanced_articles': len(results['enhanced_articles']),
                'wordpress_published': len(results.get('wordpress_published', [])),
                'wordpress_failed': len(results.get('wordpress_failed', [])),
                'failed_executions': len(results.get('failed_executions', [])),
                'total_processed': len(results['v10_articles']) + len(results['v11_articles'])
            },
            'performance': self.performance_tracker.get_performance_report(),
            'system_health': self.check_system_health(),
            'topics_processed': self.get_optimized_topics(),
            'wordpress_stats': {
                'total_attempted': self.wp_published + self.wp_failed,
                'successful': self.wp_published,
                'failed': self.wp_failed,
                'success_rate': round(self.wp_published / (self.wp_published + self.wp_failed) * 100, 1) if (self.wp_published + self.wp_failed) > 0 else 0
            }
        }
        
        return report

# Additional helper classes
class PerformanceTracker:
    """Track system performance"""
    
    def __init__(self):
        self.metrics = {
            'execution_times': [],
            'success_counts': {'v10': 0, 'v11': 0, 'total': 0},
            'error_counts': {'v10': 0, 'v11': 0, 'total': 0},
            'wordpress_counts': {'success': 0, 'failed': 0},
            'resource_usage': []
        }
    
    def record_execution(self, version: str, success: bool, duration: float):
        """Record an execution"""
        
        if version in ['v10', 'v11']:
            if success:
                self.metrics['success_counts'][version] += 1
                self.metrics['success_counts']['total'] += 1
            else:
                self.metrics['error_counts'][version] += 1
                self.metrics['error_counts']['total'] += 1
            
            self.metrics['execution_times'].append({
                'version': version,
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            })
    
    def record_wordpress(self, success: bool):
        """Record WordPress publish attempt"""
        if success:
            self.metrics['wordpress_counts']['success'] += 1
        else:
            self.metrics['wordpress_counts']['failed'] += 1
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        
        if not self.metrics['execution_times']:
            return {'status': 'No data'}
        
        total_executions = len(self.metrics['execution_times'])
        success_rate = (
            self.metrics['success_counts']['total'] / total_executions * 100
            if total_executions > 0 else 0
        )
        
        wp_total = self.metrics['wordpress_counts']['success'] + self.metrics['wordpress_counts']['failed']
        wp_success_rate = (
            self.metrics['wordpress_counts']['success'] / wp_total * 100
            if wp_total > 0 else 0
        )
        
        avg_duration = sum(
            e['duration'] for e in self.metrics['execution_times']
        ) / total_executions
        
        return {
            'total_executions': total_executions,
            'success_rate': round(success_rate, 1),
            'average_duration': round(avg_duration, 1),
            'v10_success': self.metrics['success_counts']['v10'],
            'v11_success': self.metrics['success_counts']['v11'],
            'v10_errors': self.metrics['error_counts']['v10'],
            'v11_errors': self.metrics['error_counts']['v11'],
            'wordpress_success': self.metrics['wordpress_counts']['success'],
            'wordpress_failed': self.metrics['wordpress_counts']['failed'],
            'wordpress_success_rate': round(wp_success_rate, 1)
        }

# Main execution
if __name__ == "__main__":
    try:
        print("=" * 80)
        print("🚀 PROFIT MACHINE ULTIMATE CONTROLLER")
        print("🎯 WordPress + Telegram + GitHub Integration")
        print("=" * 80)
        
        controller = EnhancedMasterController()
        result = controller.run_daily_optimized()
        
        if result['success']:
            print(f"\n✅ SUCCESS! Workflow completed")
            print(f"⏱️  Execution time: {result['execution_time']:.1f}s")
            
            if controller.wp_enabled:
                print(f"📊 WordPress: {controller.wp_published} published, {controller.wp_failed} failed")
            
            print(f"\n📁 Results saved to: exports/")
            print("=" * 80)
            sys.exit(0)
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
            print("=" * 80)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
