#!/usr/bin/env python3
"""
🏆 PROFIT MACHINE ULTIMATE - MASTER CONTROLLER
🚀 Orchestrates v10 (Content Factory) and v11 (God Mode)
🎯 Smart Routing: New content → v10, Enhancement → v11
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/master_controller.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MasterController:
    """Master controller for Profit Machine Ultimate"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config = self._load_config()
        
        # Initialize versions
        self.v10 = None
        self.v11 = None
        
        # State management
        self.execution_history = []
        self.performance_metrics = {
            'v10_executions': 0,
            'v11_executions': 0,
            'success_rate': 0,
            'total_revenue_estimate': 0
        }
        
        logger.info("🎛️  Master Controller Initialized")
    
    def _load_config(self) -> Dict:
        """Load master configuration"""
        
        config_path = self.project_root / 'master_config.json'
        
        default_config = {
            'mode': 'auto',  # auto, v10_only, v11_only, hybrid
            'hybrid_strategy': 'quality_first',  # quality_first, speed_first, revenue_first
            'v10_settings': {
                'enabled': True,
                'daily_limit': 2,
                'target_word_count': 1800,
                'auto_publish': False
            },
            'v11_settings': {
                'enabled': True,
                'daily_limit': 1,
                'enable_adsense_protection': True,
                'enable_social_posting': True,
                'enable_verification': True
            },
            'routing_rules': {
                'new_topic': 'v10',
                'enhancement': 'v11',
                'high_value_topic': 'v11',
                'quick_content': 'v10'
            },
            'scheduling': {
                'v10_schedule': [9, 14, 19],  # Run at 9AM, 2PM, 7PM
                'v11_schedule': [10, 16],      # Run at 10AM, 4PM
                'max_daily_executions': 5
            }
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    # Deep merge
                    self._deep_merge(default_config, loaded)
        except Exception as e:
            logger.error(f"Config load error: {e}")
        
        return default_config
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Deep merge dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def initialize_versions(self):
        """Initialize both v10 and v11 engines"""
        
        try:
            # Initialize v10
            if self.config['v10_settings']['enabled']:
                logger.info("🚀 Initializing Profit Machine v10...")
                from v10.v10_engine import ProfitMachineV10
                self.v10 = ProfitMachineV10()
                logger.info("✅ v10 Initialized")
            
            # Initialize v11
            if self.config['v11_settings']['enabled']:
                logger.info("🔥 Initializing Profit Machine v11 - GOD MODE...")
                from v11.v11_engine import ProfitMachineV11
                self.v11 = ProfitMachineV11()
                logger.info("✅ v11 Initialized - GOD MODE READY")
                
        except Exception as e:
            logger.error(f"❌ Version initialization failed: {e}")
            raise
    
    def smart_router(self, task_type: str, topic: str = None, category: str = None) -> str:
        """Smart routing between v10 and v11"""
        
        routing_rules = self.config['routing_rules']
        strategy = self.config['hybrid_strategy']
        
        # Rule-based routing
        if task_type in routing_rules:
            return routing_rules[task_type]
        
        # Strategy-based routing
        if strategy == 'quality_first':
            # High-value content goes to v11
            high_value_categories = ['finance', 'business', 'technology']
            if category in high_value_categories:
                return 'v11'
            else:
                return 'v10'
        
        elif strategy == 'speed_first':
            # Quick content to v10, deep content to v11
            if len(topic.split()) <= 5:  # Short topic
                return 'v10'
            else:
                return 'v11'
        
        elif strategy == 'revenue_first':
            # Estimate revenue potential
            revenue_potential = self._estimate_revenue_potential(topic, category)
            if revenue_potential > 50:  # $50+ monthly estimate
                return 'v11'
            else:
                return 'v10'
        
        # Default
        return 'v10'
    
    def _estimate_revenue_potential(self, topic: str, category: str) -> float:
        """Estimate revenue potential for routing"""
        
        # Simple estimation based on category
        category_values = {
            'finance': 100,
            'business': 80,
            'technology': 70,
            'health': 50,
            'education': 40,
            'lifestyle': 30
        }
        
        base_value = category_values.get(category, 30)
        
        # Adjust based on topic keywords
        high_value_keywords = ['money', 'profit', 'investment', 'earn', 'make money']
        for keyword in high_value_keywords:
            if keyword in topic.lower():
                base_value *= 1.5
                break
        
        return base_value
    
    def execute_workflow(self, workflow_type: str = 'daily') -> Dict:
        """Execute complete workflow"""
        
        logger.info(f"⚡ Starting {workflow_type.upper()} workflow...")
        start_time = time.time()
        
        try:
            if not self.v10 and not self.v11:
                self.initialize_versions()
            
            results = {}
            
            if workflow_type == 'daily':
                # Daily content creation workflow
                results = self._daily_content_workflow()
            
            elif workflow_type == 'enhancement':
                # Enhance existing content
                results = self._enhancement_workflow()
            
            elif workflow_type == 'hybrid':
                # Hybrid v10 + v11 workflow
                results = self._hybrid_workflow()
            
            elif workflow_type == 'maintenance':
                # System maintenance and cleanup
                results = self._maintenance_workflow()
            
            # Update metrics
            execution_time = time.time() - start_time
            self._update_performance_metrics(results, execution_time)
            
            # Save execution history
            self._save_execution_history(results, execution_time)
            
            logger.info(f"✅ {workflow_type.upper()} workflow completed in {execution_time:.1f}s")
            
            return {
                'success': True,
                'workflow': workflow_type,
                'results': results,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _daily_content_workflow(self) -> Dict:
        """Daily content creation workflow"""
        
        results = {
            'v10_articles': [],
            'v11_articles': [],
            'enhanced_articles': [],
            'social_posts': []
        }
        
        # Get topics for the day
        topics = self._get_daily_topics()
        
        for topic_data in topics:
            topic = topic_data['topic']
            category = topic_data['category']
            
            # Smart routing
            target_version = self.smart_router('new_topic', topic, category)
            
            if target_version == 'v10' and self.v10:
                logger.info(f"🎯 Routing '{topic}' to v10")
                
                # Execute v10
                v10_result = self.v10.execute_daily_run()
                
                if v10_result.get('success'):
                    results['v10_articles'].append({
                        'topic': topic,
                        'article_id': v10_result.get('article_id'),
                        'word_count': v10_result.get('word_count', 0),
                        'revenue_estimate': v10_result.get('revenue_estimate', {}).get('monthly_estimate', 0)
                    })
                    
                    # Optional: Send v10 article to v11 for enhancement
                    if self.config['mode'] == 'hybrid':
                        enhanced = self._enhance_with_v11(v10_result)
                        if enhanced:
                            results['enhanced_articles'].append(enhanced)
            
            elif target_version == 'v11' and self.v11:
                logger.info(f"🎯 Routing '{topic}' to v11 - GOD MODE")
                
                # Execute v11 directly
                v11_result = self.v11.execute_god_mode()
                
                if v11_result.get('success'):
                    results['v11_articles'].append({
                        'topic': topic,
                        'article_id': v11_result.get('article_id'),
                        'word_count': v11_result.get('article_info', {}).get('word_count', 0),
                        'revenue_estimate': v11_result.get('revenue_estimate', {}).get('monthly_estimate', 0),
                        'verification_score': v11_result.get('quality_metrics', {}).get('verification_score', 0)
                    })
                    
                    # Track social posts
                    if v11_result.get('social_media'):
                        results['social_posts'].append({
                            'article_id': v11_result.get('article_id'),
                            'platforms': v11_result['social_media'].get('platforms_ready', [])
                        })
        
        return results
    
    def _enhance_with_v11(self, v10_result: Dict) -> Optional[Dict]:
        """Enhance v10 article with v11 God Mode"""
        
        try:
            if not self.v11:
                return None
            
            logger.info(f"🔧 Enhancing v10 article with v11 God Mode...")
            
            # Extract article data from v10 result
            article_data = {
                'title': v10_result.get('topic_data', {}).get('topic', 'Unknown'),
                'content': self._extract_v10_content(v10_result),
                'category': v10_result.get('topic_data', {}).get('category', 'general'),
                'word_count': v10_result.get('article_info', {}).get('word_count', 0),
                'images_count': v10_result.get('article_info', {}).get('images_count', 0)
            }
            
            # Use v11 to enhance
            enhanced_result = self.v11.enhance_existing_article(article_data)
            
            if enhanced_result.get('success'):
                return {
                    'original_article_id': v10_result.get('article_id'),
                    'enhanced_article_id': enhanced_result.get('article_id'),
                    'improvements': enhanced_result.get('improvements', []),
                    'quality_improvement': enhanced_result.get('quality_improvement', 0)
                }
        
        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
        
        return None
    
    def _extract_v10_content(self, v10_result: Dict) -> str:
        """Extract content from v10 result"""
        # This would read the actual article file
        # For now, return placeholder
        return f"Content for: {v10_result.get('topic_data', {}).get('topic', 'Unknown')}"
    
    def _enhancement_workflow(self) -> Dict:
        """Enhancement-only workflow"""
        
        logger.info("✨ Running enhancement workflow...")
        
        # Find low-scoring articles to enhance
        articles_to_enhance = self._find_articles_for_enhancement()
        
        results = {
            'enhanced_articles': [],
            'failed_enhancements': [],
            'quality_improvements': []
        }
        
        for article in articles_to_enhance:
            try:
                enhanced = self.v11.enhance_existing_article(article)
                if enhanced.get('success'):
                    results['enhanced_articles'].append(enhanced)
                    
                    # Calculate quality improvement
                    old_score = article.get('quality_score', 60)
                    new_score = enhanced.get('quality_score', 80)
                    improvement = new_score - old_score
                    
                    results['quality_improvements'].append({
                        'article_id': article['id'],
                        'improvement': improvement,
                        'old_score': old_score,
                        'new_score': new_score
                    })
                else:
                    results['failed_enhancements'].append({
                        'article_id': article['id'],
                        'error': enhanced.get('error')
                    })
                    
            except Exception as e:
                logger.error(f"Enhancement failed for article {article.get('id')}: {e}")
        
        return results
    
    def _hybrid_workflow(self) -> Dict:
        """Hybrid v10 + v11 workflow"""
        
        logger.info("🔄 Running hybrid workflow...")
        
        # Step 1: v10 creates raw content
        v10_results = []
        if self.v10:
            for _ in range(self.config['v10_settings']['daily_limit']):
                result = self.v10.execute_daily_run()
                if result.get('success'):
                    v10_results.append(result)
        
        # Step 2: v11 enhances and markets
        v11_results = []
        social_posts = []
        
        if self.v11:
            for v10_result in v10_results:
                # Enhance with v11
                enhanced = self._enhance_with_v11(v10_result)
                if enhanced:
                    v11_results.append(enhanced)
                
                # Create social media posts
                if self.config['v11_settings']['enable_social_posting']:
                    social_result = self._create_social_posts(v10_result)
                    social_posts.extend(social_result)
        
        return {
            'v10_articles_created': len(v10_results),
            'v11_enhancements': len(v11_results),
            'social_posts_created': len(social_posts),
            'estimated_monthly_revenue': sum(
                r.get('revenue_estimate', {}).get('monthly_estimate', 0) 
                for r in v10_results
            )
        }
    
    def _get_daily_topics(self) -> List[Dict]:
        """Get topics for the day"""
        
        # In production, this would come from a database or API
        # For now, generate sample topics
        
        import random
        
        categories = ['technology', 'business', 'finance', 'health', 'education']
        current_year = datetime.now().year
        
        topic_templates = [
            f"How to Make Money with AI in {current_year}",
            f"Passive Income Strategies for {current_year}",
            "Complete Guide to Affiliate Marketing",
            "YouTube Monetization Mastery",
            "WordPress Blogging for Profit",
            "Digital Product Creation Guide",
            "Email Marketing for Beginners",
            "Stock Market Investing Basics"
        ]
        
        topics = []
        for template in topic_templates[:3]:  # 3 topics per day
            category = random.choice(categories)
            topics.append({
                'topic': template,
                'category': category,
                'priority': random.choice(['high', 'medium', 'low']),
                'estimated_cpc': round(random.uniform(1.5, 4.0), 2)
            })
        
        return topics
    
    def _find_articles_for_enhancement(self) -> List[Dict]:
        """Find articles that need enhancement"""
        
        # This would query the database
        # For now, return sample data
        
        return [
            {
                'id': 1,
                'title': 'How to Start a Blog',
                'category': 'business',
                'quality_score': 65,
                'word_count': 1200,
                'created_at': '2024-01-15',
                'needs_enhancement': ['seo', 'internal_links', 'images']
            },
            {
                'id': 2,
                'title': 'Basic Investment Strategies',
                'category': 'finance',
                'quality_score': 58,
                'word_count': 1500,
                'created_at': '2024-01-10',
                'needs_enhancement': ['adsense_compliance', 'verification', 'product_comparison']
            }
        ]
    
    def _create_social_posts(self, article_data: Dict) -> List[Dict]:
        """Create social media posts for article"""
        
        if not self.v11:
            return []
        
        try:
            social_content = self.v11.social_poster.create_social_content(article_data)
            
            posts = []
            for platform, content in social_content.items():
                if content:
                    posts.append({
                        'platform': platform,
                        'content': content.get('text', '')[:100],
                        'scheduled_time': content.get('scheduled_time')
                    })
            
            return posts
        
        except Exception as e:
            logger.error(f"Social post creation failed: {e}")
            return []
    
    def _update_performance_metrics(self, results: Dict, execution_time: float):
        """Update performance metrics"""
        
        # Count executions
        if results.get('v10_articles'):
            self.performance_metrics['v10_executions'] += len(results['v10_articles'])
        
        if results.get('v11_articles'):
            self.performance_metrics['v11_executions'] += len(results['v11_articles'])
        
        # Calculate success rate
        total_executions = (
            self.performance_metrics['v10_executions'] + 
            self.performance_metrics['v11_executions']
        )
        
        successful_executions = (
            len(results.get('v10_articles', [])) + 
            len(results.get('v11_articles', []))
        )
        
        if total_executions > 0:
            self.performance_metrics['success_rate'] = (
                successful_executions / total_executions * 100
            )
        
        # Update revenue
        revenue = 0
        for article in results.get('v10_articles', []):
            revenue += article.get('revenue_estimate', 0)
        
        for article in results.get('v11_articles', []):
            revenue += article.get('revenue_estimate', 0)
        
        self.performance_metrics['total_revenue_estimate'] += revenue
        
        # Save metrics
        self._save_performance_metrics()
    
    def _save_performance_metrics(self):
        """Save performance metrics to file"""
        
        metrics_file = self.project_root / 'data' / 'performance_metrics.json'
        metrics_file.parent.mkdir(exist_ok=True)
        
        metrics_data = {
            **self.performance_metrics,
            'last_updated': datetime.now().isoformat(),
            'total_articles': (
                self.performance_metrics['v10_executions'] + 
                self.performance_metrics['v11_executions']
            )
        }
        
        try:
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def _save_execution_history(self, results: Dict, execution_time: float):
        """Save execution history"""
        
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'workflow_type': 'daily',
            'execution_time': execution_time,
            'results_summary': {
                'v10_articles': len(results.get('v10_articles', [])),
                'v11_articles': len(results.get('v11_articles', [])),
                'enhanced_articles': len(results.get('enhanced_articles', [])),
                'social_posts': len(results.get('social_posts', []))
            },
            'success': True
        }
        
        self.execution_history.append(history_entry)
        
        # Keep only last 100 entries
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
        
        # Save to file
        history_file = self.project_root / 'data' / 'execution_history.json'
        history_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(history_file, 'w') as f:
                json.dump(self.execution_history, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def get_system_status(self) -> Dict:
        """Get system status report"""
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'versions': {
                'v10': 'Ready' if self.v10 else 'Not Initialized',
                'v11': 'Ready' if self.v11 else 'Not Initialized'
            },
            'config': {
                'mode': self.config['mode'],
                'strategy': self.config['hybrid_strategy']
            },
            'performance': self.performance_metrics,
            'recent_executions': len(self.execution_history),
            'system_health': self._check_system_health()
        }
        
        return status
    
    def _check_system_health(self) -> Dict:
        """Check system health"""
        
        health = {
            'database': 'healthy',
            'apis': 'healthy',
            'storage': 'healthy',
            'overall': 'healthy'
        }
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            if free < 1024**3:  # Less than 1GB free
                health['storage'] = 'warning'
        except:
            health['storage'] = 'unknown'
        
        # Check recent errors
        if len(self.execution_history) > 0:
            recent_failures = sum(
                1 for entry in self.execution_history[-5:] 
                if not entry.get('success', True)
            )
            
            if recent_failures > 2:
                health['overall'] = 'degraded'
        
        return health

# Command Line Interface
def main():
    """Main CLI entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Profit Machine Ultimate - Master Controller'
    )
    
    parser.add_argument(
        '--workflow',
        type=str,
        choices=['daily', 'enhancement', 'hybrid', 'maintenance'],
        default='daily',
        help='Workflow to execute'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['auto', 'v10_only', 'v11_only', 'hybrid'],
        help='Override configuration mode'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Setup project structure'
    )
    
    args = parser.parse_args()
    
    # Setup mode
    if args.setup:
        setup_project_structure()
        return
    
    # Initialize controller
    controller = MasterController()
    
    # Status mode
    if args.status:
        status = controller.get_system_status()
        print(json.dumps(status, indent=2))
        return
    
    # Override mode if specified
    if args.mode:
        controller.config['mode'] = args.mode
        print(f"⚠️  Mode overridden to: {args.mode}")
    
    # Execute workflow
    result = controller.execute_workflow(args.workflow)
    
    # Print result
    print("\n" + "=" * 80)
    print("🏆 PROFIT MACHINE ULTIMATE - EXECUTION COMPLETE")
    print("=" * 80)
    
    if result['success']:
        results = result['results']
        
        print(f"📅 Workflow: {result['workflow'].upper()}")
        print(f"⏱️  Execution Time: {result['execution_time']:.1f}s")
        
        if 'v10_articles' in results:
            print(f"\n📝 v10 Articles Created: {len(results['v10_articles'])}")
            for article in results['v10_articles'][:3]:
                print(f"   • {article['topic'][:50]}...")
        
        if 'v11_articles' in results:
            print(f"\n🔥 v11 GOD MODE Articles: {len(results['v11_articles'])}")
            for article in results['v11_articles'][:3]:
                print(f"   • {article['topic'][:50]}...")
                print(f"     Quality Score: {article.get('verification_score', 'N/A')}")
        
        if 'enhanced_articles' in results:
            print(f"\n✨ Articles Enhanced: {len(results['enhanced_articles'])}")
        
        if 'social_posts' in results:
            print(f"\n📱 Social Posts Created: {len(results['social_posts'])}")
        
        print(f"\n💰 Estimated Monthly Revenue: ${result.get('results', {}).get('estimated_monthly_revenue', 0):.2f}")
        
    else:
        print(f"❌ Execution Failed: {result.get('error')}")
    
    print("=" * 80)

def setup_project_structure():
    """Setup project directory structure"""
    
    project_root = Path(__file__).parent
    
    directories = [
        'core',
        'v10',
        'v11',
        'utils',
        'data',
        'exports',
        'exports/v10',
        'exports/v11',
        'logs',
        'backups'
    ]
    
    files = {
        'master_config.json': {
            'mode': 'auto',
            'hybrid_strategy': 'quality_first'
        },
        '.env.example': """
# Master Configuration
MASTER_MODE=auto
MASTER_STRATEGY=quality_first

# v10 Configuration
V10_ENABLED=true
V10_DAILY_LIMIT=2

# v11 Configuration
V11_ENABLED=true
V11_DAILY_LIMIT=1
V11_ENABLE_ADSENSE=true
V11_ENABLE_SOCIAL=true

# API Keys (Add your actual keys)
GROQ_API_KEY=your_key_here
WP_URL=https://yourwordpress.com
TWITTER_API_KEY=your_key_here
FACEBOOK_ACCESS_TOKEN=your_token_here
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
"""
    }
    
    print("🔧 Setting up project structure...")
    
    # Create directories
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / '__init__.py').touch()
        print(f"✅ Created: {directory}/")
    
    # Create files
    for filename, content in files.items():
        file_path = project_root / filename
        
        if isinstance(content, dict):
            content = json.dumps(content, indent=2)
        
        file_path.write_text(content)
        print(f"✅ Created: {filename}")
    
    # Create requirements.txt
    requirements = project_root / 'requirements.txt'
    requirements.write_text("""
# Profit Machine Ultimate Dependencies
requests==2.31.0
groq==0.3.0
gtts==2.3.2
pygame==2.5.1
psutil==5.9.6
pandas==2.1.4
tweepy==4.14.0
facebook-sdk==4.0.0
praw==7.7.1
python-dotenv==1.0.0
schedule==1.2.0
""")
    print("✅ Created: requirements.txt")
    
    print("\n🎉 Project structure setup complete!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Add v10.py to v10/ directory")
    print("3. Add v11.py to v11/ directory")
    print("4. Run: python main_controller.py --setup")
    print("5. Run: python main_controller.py --status")

if __name__ == "__main__":
    main()
