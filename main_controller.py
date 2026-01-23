"""
🏆 PROFIT MACHINE ULTIMATE - ENHANCED MASTER CONTROLLER
🚀 Adds Telegram reporting, GitHub integration, and better error handling
"""

import os
import sys
import json
import time
import logging
import traceback
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import os

# ፋይሉ የሚቀመጥበትን መንገድ ማረጋገጥ
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

try:
    from utils.telegram_reporter import EnhancedTelegramReporter
    TELEGRAM_AVAILABLE = True
    print("✅ Telegram reporter loaded")
except ImportError:
    print("⚠️ Telegram reporter not available")

class EnhancedMasterController:
    """Enhanced master controller with Telegram and GitHub integration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config = self._load_config()
        
        # Initialize reporting
        self.telegram_reporter = None
        if TELEGRAM_AVAILABLE and self.config.get('telegram', {}).get('enabled', False):
            try:
                self.telegram_reporter = EnhancedTelegramReporter(
                    self.config['telegram']['bot_token'],
                    self.config['telegram']['chat_id']
                )
                print("✅ Telegram reporter initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Telegram: {e}")
        
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
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            config_path = self.project_root / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Default configuration
                return {
                    'telegram': {
                        'enabled': False,
                        'bot_token': '',
                        'chat_id': ''
                    },
                    'enable_hybrid_mode': True,
                    'max_retries': 3,
                    'retry_delay': 5
                }
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}
    
    def setup_enhanced_logging(self):
        """Setup enhanced logging with file rotation"""
        
        log_dir = self.project_root / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # Create loggers for different components
        self.loggers = {
            'master': self._create_logger('master'),
            'v10': self._create_logger('v10'),
            'v11': self._create_logger('v11'),
            'github': self._create_logger('github')
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
    
    def run_daily_optimized(self):
        """Optimized daily workflow for GitHub Actions"""
        
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
            
            # Step 3: Smart execution
            results = {
                'v10_articles': [],
                'v11_articles': [],
                'enhanced_articles': [],
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
                    'results': results
                })
            
            # Step 8: Backup to GitHub
            if self.is_github_actions:
                self.backup_to_github(results)
            
            self.loggers['master'].info(
                f"✅ Daily optimized workflow completed in {execution_time:.1f}s"
            )
            
            return {
                'success': True,
                'report': report,
                'execution_time': execution_time
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
                
                # Commit with meaningful message
                commit_message = f"""🤖 Profit Machine Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Created {len(results['v10_articles'])} v10 articles
Created {len(results['v11_articles'])} v11 articles
Enhanced {len(results['enhanced_articles'])} articles
Failed: {len(results['failed_executions'])}

Run ID: {self.run_id}
"""
                
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
        required_env_vars = ['GROQ_API_KEY']
        for var in required_env_vars:
            if not os.getenv(var):
                health_issues.append(f"Missing environment variable: {var}")
        
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
                'topic': topic,
                'version': 'v10',
                'content': f"Generated content about {topic} using V10 engine.",
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
            # Save result
            filename = f"v10_{topic.replace(' ', '_')}.json"
            self.save_to_exports(result, filename)
            
            return {'success': True, 'data': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_v11(self, topic_data: Dict) -> Dict:
        """Run version 11 (advanced version)"""
        try:
            topic = topic_data['topic']
            
            # Simulate processing
            time.sleep(3)  # Simulate API call
            
            result = {
                'topic': topic,
                'version': 'v11',
                'content': f"Generated advanced content about {topic} using V11 GOD MODE engine.",
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'enhanced': True,
                'social_media_ready': True
            }
            
            # Save result
            filename = f"v11_{topic.replace(' ', '_')}.json"
            self.save_to_exports(result, filename)
            
            return {'success': True, 'data': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def enhance_with_v11_batch(self, v10_articles: List[Dict]) -> List[Dict]:
        """Enhance V10 articles with V11 capabilities"""
        enhanced = []
        for article in v10_articles:
            try:
                enhanced_article = article.copy()
                enhanced_article['enhanced'] = True
                enhanced_article['enhanced_at'] = datetime.now().isoformat()
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
            'summary': {
                'v10_articles': len(results['v10_articles']),
                'v11_articles': len(results['v11_articles']),
                'enhanced_articles': len(results['enhanced_articles']),
                'failed_executions': len(results['failed_executions']),
                'total_processed': len(results['v10_articles']) + len(results['v11_articles'])
            },
            'performance': self.performance_tracker.get_performance_report(),
            'system_health': self.check_system_health(),
            'topics_processed': [topic for topic in self.get_optimized_topics()]
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
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        
        if not self.metrics['execution_times']:
            return {'status': 'No data'}
        
        total_executions = len(self.metrics['execution_times'])
        success_rate = (
            self.metrics['success_counts']['total'] / total_executions * 100
            if total_executions > 0 else 0
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
            'v11_errors': self.metrics['error_counts']['v11']
        }

# Main execution
if __name__ == "__main__":
    try:
        print("🚀 Starting Profit Machine Enhanced Controller...")
        controller = EnhancedMasterController()
        result = controller.run_daily_optimized()
        
        if result['success']:
            print(f"✅ Success! Execution time: {result['execution_time']:.1f}s")
            sys.exit(0)
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        sys.exit(1)
