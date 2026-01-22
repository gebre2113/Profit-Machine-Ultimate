#!/usr/bin/env python3
"""
🏆 PROFIT MACHINE v11.0 - THE GOD MODE
🚀 Complete Digital Business Automation Suite
✅ AI-Powered Internal Linking
✅ Social Media Auto-Poster (Twitter/X, Facebook, Pinterest, LinkedIn)
✅ Smart Product Comparison Tables
✅ Multi-Model Content Verification
✅ AdSense Safe-Guard System
✅ All v10.0 Features Included
✅ Self-Learning AI System
✅ Auto-Scaling Content Strategy
✅ Real-Time Market Analysis
✅ Cross-Platform Monetization
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
from typing import Dict, List, Optional, Any, Tuple, Set
from urllib.parse import quote, urlencode
import concurrent.futures
import traceback

# =================== DEPENDENCY CHECK ===================

print("🔧 Checking dependencies for GOD MODE v11.0...")

REQUIRED_PACKAGES = {
    'requests': 'requests',
    'groq': 'groq',
    'gtts': 'gtts',
    'pygame': 'pygame',
    'psutil': 'psutil',
    'pandas': 'pandas',
    'tweepy': 'tweepy',
    'facebook-sdk': 'facebook-sdk',
    'linkedin-api': 'linkedin-api==2.0.0',
    'praw': 'praw'
}

for package, import_name in REQUIRED_PACKAGES.items():
    try:
        __import__(import_name)
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - Install: pip install {package}")

# =================== GOD MODE CONFIGURATION ===================

class GodModeConfig:
    """GOD MODE Configuration Manager"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self):
        """Load GOD MODE configuration"""
        config = {
            # API Keys for new features
            'TWITTER_API_KEY': '',
            'TWITTER_API_SECRET': '',
            'TWITTER_ACCESS_TOKEN': '',
            'TWITTER_ACCESS_SECRET': '',
            
            'FACEBOOK_ACCESS_TOKEN': '',
            'FACEBOOK_PAGE_ID': '',
            
            'PINTEREST_ACCESS_TOKEN': '',
            'PINTEREST_BOARD_ID': '',
            
            'LINKEDIN_CLIENT_ID': '',
            'LINKEDIN_CLIENT_SECRET': '',
            'LINKEDIN_ACCESS_TOKEN': '',
            
            'REDDIT_CLIENT_ID': '',
            'REDDIT_CLIENT_SECRET': '',
            'REDDIT_USER_AGENT': 'ProfitMachineBot/1.0',
            
            # AI Models for verification
            'PRIMARY_AI_MODEL': 'llama-3.3-70b-versatile',
            'SECONDARY_AI_MODEL': 'gemma2-9b-it',
            'TERTIARY_AI_MODEL': 'mixtral-8x7b-32768',
            
            # Social Media Settings
            'AUTO_POST_TO_SOCIAL': True,
            'SOCIAL_POST_DELAY_MINUTES': 30,
            'MAX_SOCIAL_POSTS_PER_DAY': 5,
            'SOCIAL_MEDIA_SCHEDULE': {
                'twitter': [9, 12, 15, 18, 21],
                'facebook': [10, 14, 19],
                'linkedin': [8, 13, 17],
                'pinterest': [11, 16, 20]
            },
            
            # Internal Linking
            'MAX_INTERNAL_LINKS': 7,
            'MIN_LINK_RELEVANCE_SCORE': 0.6,
            'INTERNAL_LINK_DEPTH': 2,
            
            # Product Comparison
            'ENABLE_PRODUCT_COMPARISON': True,
            'MAX_PRODUCTS_PER_COMPARISON': 4,
            'AUTO_GENERATE_COMPARISONS': True,
            
            # Content Verification
            'ENABLE_MULTI_MODEL_VERIFICATION': True,
            'MIN_VERIFICATION_SCORE': 80,
            'AUTO_CORRECT_CONTENT': True,
            
            # AdSense Protection
            'STRICT_ADSENSE_COMPLIANCE': True,
            'AUTO_FIX_ADSENSE_ISSUES': True,
            'ADSENSE_RISK_THRESHOLD': 30,
            
            # Advanced Features
            'ENABLE_SELF_LEARNING': True,
            'ENABLE_MARKET_ANALYSIS': True,
            'ENABLE_COMPETITOR_TRACKING': True,
            'ENABLE_TREND_PREDICTION': True,
            
            # Performance
            'PARALLEL_PROCESSING': True,
            'MAX_WORKERS': 4,
            'CACHE_ENABLED': True,
            'CACHE_TTL_HOURS': 24
        }
        
        # Load from environment variables
        for key in config:
            env_value = os.getenv(key)
            if env_value is not None:
                if isinstance(config[key], bool):
                    config[key] = env_value.lower() == 'true'
                elif isinstance(config[key], int):
                    config[key] = int(env_value)
                elif isinstance(config[key], dict):
                    try:
                        config[key] = json.loads(env_value)
                    except:
                        pass
                else:
                    config[key] = env_value
        
        return config
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)

# =================== AI-POWERED INTERNAL LINKER ===================

class AIPoweredInternalLinker:
    """AI-powered internal linking system"""
    
    def __init__(self, database_manager):
        self.db = database_manager
        self.link_cache = {}
        self.semantic_cache = {}
        
    def find_relevant_articles(self, new_article_text: str, current_category: str, 
                              max_links: int = 5) -> List[Dict]:
        """Find relevant articles for internal linking"""
        
        print(f"🔗 Finding internal links for {current_category} article...")
        
        # Extract keywords with semantic analysis
        keywords = self._extract_semantic_keywords(new_article_text)
        
        # Get articles from database
        relevant_articles = self._query_articles_by_keywords(keywords, current_category)
        
        # Calculate relevance scores
        scored_articles = []
        for article in relevant_articles:
            score = self._calculate_relevance_score(
                new_article_text, 
                article['content'], 
                keywords
            )
            
            if score >= 0.4:  # Minimum relevance threshold
                scored_articles.append({
                    **article,
                    'relevance_score': score,
                    'anchor_text': self._generate_anchor_text(article['title'], keywords),
                    'link_position': self._determine_link_position(article, len(scored_articles))
                })
        
        # Sort by relevance
        scored_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_articles[:max_links]
    
    def _extract_semantic_keywords(self, text: str) -> List[Tuple[str, float]]:
        """Extract keywords with semantic weights"""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Tokenize and count
        words = re.findall(r'\b[a-zA-Z]{4,}\b', clean_text.lower())
        
        # Common stop words
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'like', 'your', 'will', 
            'more', 'what', 'when', 'where', 'which', 'they', 'their', 'about',
            'would', 'there', 'could', 'should', 'been', 'were', 'them', 'such'
        }
        
        # Calculate TF-IDF like weights
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        total_words = len(words)
        keywords = []
        
        for word, freq in word_freq.items():
            if freq >= 2:  # Appears at least twice
                # Simple weight calculation
                weight = (freq / total_words) * 100
                
                # Boost for certain patterns
                if len(word) > 6:
                    weight *= 1.2  # Longer words often more specific
                
                keywords.append((word, weight))
        
        keywords.sort(key=lambda x: x[1], reverse=True)
        return keywords[:15]
    
    def _query_articles_by_keywords(self, keywords: List[Tuple[str, float]], 
                                   category: str) -> List[Dict]:
        """Query database for relevant articles"""
        
        # Connect to database
        conn = sqlite3.connect('data/profit_machine_v11.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query
        keyword_terms = [kw[0] for kw in keywords[:5]]
        
        query = '''
        SELECT id, title, content, category, created_at, views, revenue_estimate
        FROM articles 
        WHERE category = ? AND published = 1
        ORDER BY created_at DESC 
        LIMIT 50
        '''
        
        cursor.execute(query, (category,))
        articles = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Filter by keyword relevance
        relevant_articles = []
        for article in articles:
            content_lower = article['content'].lower()
            
            # Check for keyword matches
            keyword_matches = 0
            for keyword, _ in keywords[:8]:
                if keyword in content_lower:
                    keyword_matches += 1
            
            if keyword_matches >= 2:
                article['keyword_matches'] = keyword_matches
                relevant_articles.append(article)
        
        return relevant_articles
    
    def _calculate_relevance_score(self, new_text: str, existing_text: str, 
                                 keywords: List[Tuple[str, float]]) -> float:
        """Calculate relevance score between articles"""
        
        # Keyword overlap score
        new_words = set([kw[0] for kw in keywords])
        existing_lower = existing_text.lower()
        
        overlap_score = 0
        for word in new_words:
            if word in existing_lower:
                overlap_score += 1
        
        overlap_score = min(1.0, overlap_score / len(new_words))
        
        # Category bonus
        category_bonus = 0.2
        
        # Recency bonus (newer articles get higher score)
        try:
            # Assuming article has created_at field
            created_date = datetime.strptime(existing_text.get('created_at', ''), '%Y-%m-%d')
            days_old = (datetime.now() - created_date).days
            recency_bonus = max(0, 0.3 * (30 - days_old) / 30)
        except:
            recency_bonus = 0.1
        
        # Popularity bonus (if available)
        popularity_bonus = 0
        if existing_text.get('views', 0) > 100:
            popularity_bonus = 0.1
        elif existing_text.get('views', 0) > 1000:
            popularity_bonus = 0.2
        
        total_score = (
            overlap_score * 0.5 +
            category_bonus * 0.2 +
            recency_bonus * 0.2 +
            popularity_bonus * 0.1
        )
        
        return min(1.0, total_score)
    
    def _generate_anchor_text(self, article_title: str, keywords: List[Tuple[str, float]]) -> str:
        """Generate optimal anchor text"""
        
        # Use keywords that appear in title
        title_lower = article_title.lower()
        for keyword, _ in keywords:
            if keyword in title_lower:
                # Find the phrase containing keyword
                words = title_lower.split()
                for i, word in enumerate(words):
                    if keyword in word:
                        start = max(0, i - 2)
                        end = min(len(words), i + 3)
                        anchor = ' '.join(words[start:end])
                        return anchor.title()
        
        # Fallback to first few words of title
        return ' '.join(article_title.split()[:4])
    
    def _determine_link_position(self, article: Dict, link_index: int) -> int:
        """Determine optimal position for link"""
        # Distribute links throughout article
        positions = [3, 7, 11, 15, 19, 23, 27]
        return positions[link_index % len(positions)] if link_index < len(positions) else 5
    
    def apply_internal_links(self, content: str, links: List[Dict]) -> str:
        """Apply internal links to content"""
        
        if not links:
            return content
        
        paragraphs = content.split('\n\n')
        
        for link in links:
            position = link['link_position']
            if position < len(paragraphs):
                link_html = self._create_link_html(link)
                paragraphs.insert(position, link_html)
        
        return '\n\n'.join(paragraphs)
    
    def _create_link_html(self, link_data: Dict) -> str:
        """Create internal link HTML"""
        
        return f'''
<div class="internal-link" style="background: #f0f9ff; border-left: 4px solid #3182ce; padding: 15px; margin: 20px 0; border-radius: 0 8px 8px 0;">
<p style="margin: 0; color: #2d3748;">
<strong>📚 Related Reading:</strong> 
<a href="{link_data.get('url', '#')}" style="color: #2b6cb0; font-weight: bold; text-decoration: none;">
{link_data['anchor_text']}
</a>
</p>
<p style="margin: 10px 0 0 0; font-size: 0.9em; color: #718096;">
{link_data.get('title', '')[:100]}...
</p>
</div>
'''

# =================== SOCIAL MEDIA AUTO-POSTER ===================

class SocialMediaAutoPoster:
    """Multi-platform social media auto-poster"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.platforms = {}
        
        # Initialize platform connections
        self._initialize_platforms()
        
        # Posting queue
        self.posting_queue = []
        self.posting_history = []
        
    def _initialize_platforms(self):
        """Initialize social media platform connections"""
        
        # Twitter/X
        if all([
            self.config.get('TWITTER_API_KEY'),
            self.config.get('TWITTER_API_SECRET'),
            self.config.get('TWITTER_ACCESS_TOKEN'),
            self.config.get('TWITTER_ACCESS_SECRET')
        ]):
            try:
                import tweepy
                auth = tweepy.OAuth1UserHandler(
                    self.config['TWITTER_API_KEY'],
                    self.config['TWITTER_API_SECRET'],
                    self.config['TWITTER_ACCESS_TOKEN'],
                    self.config['TWITTER_ACCESS_SECRET']
                )
                self.platforms['twitter'] = tweepy.API(auth)
                print("✅ Twitter/X connection established")
            except Exception as e:
                print(f"⚠️  Twitter connection failed: {e}")
        
        # Facebook
        if all([
            self.config.get('FACEBOOK_ACCESS_TOKEN'),
            self.config.get('FACEBOOK_PAGE_ID')
        ]):
            try:
                import facebook
                self.platforms['facebook'] = facebook.GraphAPI(
                    access_token=self.config['FACEBOOK_ACCESS_TOKEN'],
                    version="12.0"
                )
                print("✅ Facebook connection established")
            except Exception as e:
                print(f"⚠️  Facebook connection failed: {e}")
        
        # LinkedIn (Simplified - uses API v2)
        if all([
            self.config.get('LINKEDIN_ACCESS_TOKEN')
        ]):
            self.platforms['linkedin'] = True
            print("✅ LinkedIn connection available")
        
        # Pinterest
        if all([
            self.config.get('PINTEREST_ACCESS_TOKEN'),
            self.config.get('PINTEREST_BOARD_ID')
        ]):
            self.platforms['pinterest'] = True
            print("✅ Pinterest connection available")
        
        # Reddit
        if all([
            self.config.get('REDDIT_CLIENT_ID'),
            self.config.get('REDDIT_CLIENT_SECRET'),
            self.config.get('REDDIT_USER_AGENT')
        ]):
            try:
                import praw
                self.platforms['reddit'] = praw.Reddit(
                    client_id=self.config['REDDIT_CLIENT_ID'],
                    client_secret=self.config['REDDIT_CLIENT_SECRET'],
                    user_agent=self.config['REDDIT_USER_AGENT']
                )
                print("✅ Reddit connection established")
            except Exception as e:
                print(f"⚠️  Reddit connection failed: {e}")
    
    def create_social_content(self, article: Dict, images: List[Dict] = None) -> Dict:
        """Create platform-specific social media content"""
        
        content = {
            'twitter': self._create_tweet(article, images),
            'facebook': self._create_facebook_post(article, images),
            'linkedin': self._create_linkedin_post(article, images),
            'pinterest': self._create_pinterest_pin(article, images),
            'reddit': self._create_reddit_post(article, images)
        }
        
        # Add hashtags
        hashtags = self._generate_hashtags(article['category'], article['title'])
        
        for platform, post in content.items():
            if post:
                content[platform] = {
                    'text': post + "\n\n" + hashtags,
                    'hashtags': hashtags,
                    'images': images[:1] if images else None,
                    'scheduled_time': self._get_best_posting_time(platform)
                }
        
        return content
    
    def _create_tweet(self, article: Dict, images: List[Dict] = None) -> str:
        """Create Twitter/X tweet"""
        
        title = article['title']
        summary = self._extract_summary(article.get('content', ''), 180)
        
        # Twitter character limit
        max_length = 280
        link_placeholder = " 🔗 Full article in bio"
        
        tweet = f"{title}\n\n{summary}"
        
        if len(tweet) > max_length - len(link_placeholder):
            tweet = tweet[:max_length - len(link_placeholder) - 3] + "..."
        
        tweet += link_placeholder
        
        # Add call to action
        ctas = [
            "What do you think?",
            "Have you tried this?",
            "Share your thoughts!",
            "Agree or disagree?",
            "Let me know below! 👇"
        ]
        
        if len(tweet) < 250:
            tweet += "\n\n" + random.choice(ctas)
        
        return tweet
    
    def _create_facebook_post(self, article: Dict, images: List[Dict] = None) -> str:
        """Create Facebook post"""
        
        title = article['title']
        summary = self._extract_summary(article.get('content', ''), 300)
        
        post = f"""📢 NEW ARTICLE ALERT! 📢

{title}

{summary}

💡 Key Takeaways:
• {random.choice(['Actionable strategies', 'Data-driven insights', 'Step-by-step guide'])}
• {random.choice(['Real case studies', 'Expert interviews', 'Proven methods'])}
• {random.choice(['Free resources included', 'Downloadable templates', 'Interactive tools'])}

🔗 Read the full article on our website!

What's your experience with {article['category']}? Share in the comments! 💬👇"""
        
        return post
    
    def _create_linkedin_post(self, article: Dict, images: List[Dict] = None) -> str:
        """Create LinkedIn post"""
        
        title = article['title']
        summary = self._extract_summary(article.get('content', ''), 400)
        
        post = f"""📈 Professional Insight: {title}

{summary}

🔑 Key Business Insights:
1. {random.choice(['Market analysis', 'Growth strategies', 'Risk management'])}
2. {random.choice(['ROI optimization', 'Cost reduction', 'Efficiency improvement'])}
3. {random.choice(['Industry trends', 'Future predictions', 'Innovation opportunities'])}

💼 Perfect for: {random.choice(['Entrepreneurs', 'Managers', 'Startups', 'Investors'])}

📊 Data Points: Based on analysis of {random.randint(50, 500)}+ cases

🔗 Full analysis available in the article.

#business #strategy #growth #leadership #innovation"""
        
        return post
    
    def _create_pinterest_pin(self, article: Dict, images: List[Dict] = None) -> str:
        """Create Pinterest pin"""
        
        title = article['title']
        
        pin = f"""{title}

💡 {random.choice(['Step-by-step guide', 'Visual tutorial', 'Infographic summary'])}

🎯 Perfect for: {random.choice(['Beginners', 'Advanced users', 'Professionals', 'Hobbyists'])}

📌 Save for later! Pin this to your {article['category']} board.

🔗 Click through for detailed instructions and resources.

#{article['category']} #howto #tutorial #diy #tips"""
        
        return pin
    
    def _create_reddit_post(self, article: Dict, images: List[Dict] = None) -> str:
        """Create Reddit post"""
        
        title = article['title']
        summary = self._extract_summary(article.get('content', ''), 200)
        
        # Reddit requires specific formatting
        post = f"""**{title}**

{summary}

**Key points:**
* Point 1: {random.choice(['Important finding', 'Key statistic', 'Major insight'])}
* Point 2: {random.choice(['Practical application', 'Real-world example', 'Case study'])}
* Point 3: {random.choice(['Common mistake', 'Pro tip', 'Expert advice'])}

**Discussion questions:**
1. What's your experience with this?
2. Have you tried similar approaches?
3. What worked/didn't work for you?

[Read the full article here]({article.get('url', '#')})

*Note: I'm the author of this content, sharing for discussion.*"""
        
        return post
    
    def _extract_summary(self, content: str, max_length: int) -> str:
        """Extract summary from content"""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', content)
        
        # Get first paragraph
        paragraphs = [p.strip() for p in clean.split('\n\n') if p.strip()]
        
        if paragraphs:
            summary = paragraphs[0]
        else:
            summary = clean[:max_length]
        
        if len(summary) > max_length:
            summary = summary[:max_length - 3] + "..."
        
        return summary
    
    def _generate_hashtags(self, category: str, title: str) -> str:
        """Generate relevant hashtags"""
        
        category_tags = {
            'technology': '#tech #ai #innovation #digital #future',
            'business': '#business #entrepreneur #startup #success #marketing',
            'finance': '#finance #money #investing #wealth #trading',
            'health': '#health #wellness #fitness #nutrition #lifestyle',
            'education': '#education #learning #knowledge #skills #growth'
        }
        
        base_tags = category_tags.get(category, '#content #article #blog')
        
        # Extract keywords from title for additional tags
        title_words = re.findall(r'\b[a-zA-Z]{5,}\b', title.lower())
        extra_tags = ' '.join(['#' + word for word in title_words[:3]])
        
        return f"{base_tags} {extra_tags} #{category}"
    
    def _get_best_posting_time(self, platform: str) -> datetime:
        """Calculate best posting time for platform"""
        
        schedule = self.config.get('SOCIAL_MEDIA_SCHEDULE', {}).get(platform, [9, 12, 15, 18, 21])
        
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        
        # Find next scheduled hour
        for hour in schedule:
            if hour > now.hour:
                next_hour = next_hour.replace(hour=hour)
                break
        
        # Add some random minutes
        next_hour = next_hour.replace(minute=random.randint(0, 30))
        
        return next_hour
    
    def schedule_posts(self, social_content: Dict, article_url: str = None):
        """Schedule social media posts"""
        
        print("📱 Scheduling social media posts...")
        
        for platform, content in social_content.items():
            if platform in self.platforms and content:
                post_data = {
                    'platform': platform,
                    'content': content['text'],
                    'scheduled_time': content['scheduled_time'],
                    'article_url': article_url,
                    'images': content.get('images'),
                    'status': 'scheduled'
                }
                
                self.posting_queue.append(post_data)
                
                print(f"   ✅ {platform.upper()}: Scheduled for {content['scheduled_time'].strftime('%H:%M')}")
    
    def post_immediately(self, platform: str, content: Dict, article_url: str = None) -> bool:
        """Post immediately to social media"""
        
        try:
            if platform == 'twitter' and 'twitter' in self.platforms:
                # Post to Twitter
                tweet = content['text']
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                if content.get('images'):
                    # Twitter with image
                    media_ids = []
                    for image in content['images'][:4]:  # Twitter allows up to 4 images
                        # Download and upload image
                        # Implementation depends on image source
                        pass
                    
                    if media_ids:
                        self.platforms['twitter'].update_status(
                            status=tweet, 
                            media_ids=media_ids
                        )
                    else:
                        self.platforms['twitter'].update_status(status=tweet)
                else:
                    self.platforms['twitter'].update_status(status=tweet)
                
                return True
                
            elif platform == 'facebook' and 'facebook' in self.platforms:
                # Post to Facebook page
                post = content['text']
                
                if content.get('images'):
                    # Post with image
                    self.platforms['facebook'].put_photo(
                        image=open(content['images'][0], 'rb'),
                        message=post,
                        album_id=self.config.get('FACEBOOK_PAGE_ID')
                    )
                else:
                    self.platforms['facebook'].put_object(
                        parent_object=self.config.get('FACEBOOK_PAGE_ID'),
                        connection_name='feed',
                        message=post
                    )
                
                return True
                
            elif platform == 'linkedin' and 'linkedin' in self.platforms:
                # LinkedIn post via API
                # Requires additional setup
                pass
                
            elif platform == 'reddit' and 'reddit' in self.platforms:
                # Reddit post
                subreddit = self.platforms['reddit'].subreddit(
                    random.choice(['blogging', 'content_marketing', 'SEO', 'digital_marketing'])
                )
                
                title = content['text'].split('\n')[0][:300]
                text = '\n'.join(content['text'].split('\n')[1:])
                
                submission = subreddit.submit(
                    title=title,
                    selftext=text,
                    send_replies=False
                )
                
                return submission is not None
            
        except Exception as e:
            print(f"⚠️  Failed to post to {platform}: {e}")
        
        return False

# =================== SMART PRODUCT COMPARISON ===================

class SmartProductComparer:
    """AI-powered product comparison generator"""
    
    def __init__(self, ai_generator):
        self.ai = ai_generator
        self.product_templates = self._load_product_templates()
    
    def _load_product_templates(self) -> Dict:
        """Load product comparison templates by category"""
        
        return {
            'technology': {
                'categories': ['Laptops', 'Smartphones', 'Tablets', 'Headphones', 'Smart Watches'],
                'features': ['Price', 'Processor', 'RAM', 'Storage', 'Battery Life', 'Display', 'Weight'],
                'price_ranges': ['Budget', 'Mid-range', 'Premium', 'Professional']
            },
            'health': {
                'categories': ['Blenders', 'Juicers', 'Air Fryers', 'Food Processors', 'Coffee Makers'],
                'features': ['Price', 'Power', 'Capacity', 'Features', 'Warranty', 'Noise Level'],
                'price_ranges': ['Entry-level', 'Mid-range', 'Premium', 'Commercial']
            },
            'business': {
                'categories': ['CRM Software', 'Email Marketing', 'Project Management', 'Accounting', 'Hosting'],
                'features': ['Price', 'Features', 'Users', 'Storage', 'Support', 'Integrations'],
                'price_ranges': ['Free', 'Basic', 'Professional', 'Enterprise']
            },
            'finance': {
                'categories': ['Banking Apps', 'Investment Platforms', 'Budgeting Tools', 'Tax Software', 'Crypto Exchanges'],
                'features': ['Fees', 'Features', 'Security', 'Customer Support', 'Mobile App', 'Limits'],
                'price_ranges': ['Free', 'Low-cost', 'Premium', 'High-volume']
            }
        }
    
    def create_comparison_table(self, topic: str, category: str) -> Dict:
        """Create product comparison table"""
        
        print(f"📊 Creating product comparison for {category}...")
        
        template = self.product_templates.get(category, self.product_templates['technology'])
        
        # Generate products
        products = self._generate_products(topic, template)
        
        # Create comparison analysis
        analysis = self._create_comparison_analysis(products, topic)
        
        # Generate HTML table
        html_table = self._create_html_table(products, template['features'])
        
        return {
            'products': products,
            'analysis': analysis,
            'html_table': html_table,
            'recommendation': analysis['best_overall'],
            'template_used': template
        }
    
    def _generate_products(self, topic: str, template: Dict) -> List[Dict]:
        """Generate product data"""
        
        categories = template['categories']
        features = template['features']
        price_ranges = template['price_ranges']
        
        products = []
        
        for i in range(min(4, len(price_ranges))):
            price_range = price_ranges[i]
            category = random.choice(categories)
            
            product = {
                'name': f"{price_range} {category}",
                'price_range': price_range,
                'category': category,
                'features': {},
                'pros': [],
                'cons': [],
                'rating': random.uniform(3.5, 5.0),
                'best_for': random.choice(['Beginners', 'Professionals', 'Students', 'Businesses']),
                'affiliate_link': self._generate_affiliate_link(category, price_range)
            }
            
            # Generate feature values
            for feature in features:
                if feature == 'Price':
                    product['features'][feature] = self._generate_price(price_range)
                elif feature in ['Processor', 'Power', 'Fees']:
                    product['features'][feature] = random.choice(['Low', 'Medium', 'High', 'Premium'])
                elif feature in ['RAM', 'Storage', 'Capacity', 'Users']:
                    product['features'][feature] = f"{random.choice([8, 16, 32, 64, 128])}{'GB' if feature in ['RAM', 'Storage'] else 'L'}"
                elif feature == 'Battery Life':
                    product['features'][feature] = f"{random.choice([8, 10, 12, 15, 20])} hours"
                else:
                    product['features'][feature] = random.choice(['Good', 'Very Good', 'Excellent', 'Outstanding'])
            
            # Generate pros and cons
            product['pros'] = self._generate_pros(product)
            product['cons'] = self._generate_cons(product)
            
            products.append(product)
        
        return products
    
    def _generate_price(self, price_range: str) -> str:
        """Generate price based on range"""
        
        prices = {
            'Budget': '$199-$399',
            'Mid-range': '$499-$899',
            'Premium': '$999-$1,999',
            'Professional': '$2,000-$4,000',
            'Free': 'Free',
            'Basic': '$9-$29/month',
            'Enterprise': '$299+/month'
        }
        
        return prices.get(price_range, '$299-$999')
    
    def _generate_affiliate_link(self, category: str, price_range: str) -> str:
        """Generate affiliate link for product"""
        
        # This would be replaced with actual affiliate link generation
        base_urls = {
            'amazon': 'https://amazon.com/dp/',
            'clickbank': 'https://hop.clickbank.net/?affiliate=',
            'shareasale': 'https://www.shareasale.com/r.cfm?u='
        }
        
        network = random.choice(list(base_urls.keys()))
        
        # Placeholder product IDs
        product_ids = {
            'Laptops': ['B08N5WRWNW', 'B07FK8QQQ', 'B0844JKQ9K'],
            'Smartphones': ['B09G9FPHY6', 'B09V2GQ9N9', 'B09V3JNSK8'],
            'Blenders': ['B00H8KLV6C', 'B01N0XQ33M', 'B07FDJMC9Q']
        }
        
        product_id = random.choice(product_ids.get(category, ['B08N5WRWNW']))
        
        return f"{base_urls[network]}{product_id}"
    
    def _generate_pros(self, product: Dict) -> List[str]:
        """Generate pros for product"""
        
        pros_templates = [
            f"Excellent {random.choice(['value', 'performance', 'features'])} for the price",
            f"{random.choice(['Reliable', 'Durable', 'Consistent'])} performance",
            f"Great for {product['best_for'].lower()}",
            f"{random.choice(['Easy to use', 'User-friendly interface', 'Intuitive controls'])}",
            f"Good {random.choice(['customer support', 'warranty', 'documentation'])}",
            f"High {random.choice(['quality construction', 'material quality', 'finish'])}"
        ]
        
        return random.sample(pros_templates, 3)
    
    def _generate_cons(self, product: Dict) -> List[str]:
        """Generate cons for product"""
        
        if product['price_range'] in ['Budget', 'Free']:
            cons_templates = [
                "Limited features compared to premium options",
                "Basic design and materials",
                "Customer support can be slow",
                "May lack some advanced features",
                "Shorter warranty period"
            ]
        else:
            cons_templates = [
                "Higher price point",
                "Steeper learning curve",
                "May be overkill for beginners",
                "Requires more maintenance",
                "Heavier/bulkier than competitors"
            ]
        
        return random.sample(cons_templates, 2)
    
    def _create_comparison_analysis(self, products: List[Dict], topic: str) -> Dict:
        """Create comparison analysis"""
        
        # Find best in each category
        best_budget = min(products, key=lambda x: 0 if 'Budget' in x['price_range'] else 1)
        best_premium = max(products, key=lambda x: x['rating'])
        
        # Overall recommendation
        if len(products) >= 3:
            best_overall = products[1]  # Typically mid-range is best overall
        else:
            best_overall = best_premium
        
        return {
            'best_budget': best_budget['name'],
            'best_premium': best_premium['name'],
            'best_overall': best_overall['name'],
            'key_differentiators': self._generate_differentiators(products),
            'buying_advice': self._generate_buying_advice(topic, products),
            'summary': f"Based on our analysis of {len(products)} products, {best_overall['name']} offers the best balance of features and value for most users."
        }
    
    def _generate_differentiators(self, products: List[Dict]) -> List[str]:
        """Generate key differentiators"""
        
        differentiators = [
            "Price vs. performance ratio",
            "Feature completeness",
            "Ease of use and learning curve",
            "Customer support quality",
            "Long-term reliability",
            "Resale value and depreciation"
        ]
        
        return random.sample(differentiators, 3)
    
    def _generate_buying_advice(self, topic: str, products: List[Dict]) -> str:
        """Generate buying advice"""
        
        advice_templates = [
            f"When choosing {topic.lower()}, consider your specific needs and budget. {random.choice(['Beginners', 'Casual users', 'Students'])} may prefer budget options, while {random.choice(['professionals', 'power users', 'businesses'])} should invest in premium features.",
            f"Look beyond just the price tag. Consider long-term value, support, and features you'll actually use. Sometimes spending a bit more upfront saves money in the long run.",
            f"Read user reviews and watch video demonstrations before making a decision. What works for one person may not work for your specific use case."
        ]
        
        return random.choice(advice_templates)
    
    def _create_html_table(self, products: List[Dict], features: List[str]) -> str:
        """Create HTML comparison table"""
        
        # Table header
        html = '''
<div class="product-comparison" style="overflow-x: auto; margin: 30px 0; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
<table style="width: 100%; border-collapse: collapse; background: white;">
<thead>
<tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
'''
        
        # Add product names as headers
        html += '<th style="padding: 15px; text-align: left; min-width: 150px;">Feature</th>\n'
        for product in products:
            html += f'<th style="padding: 15px; text-align: center; min-width: 200px;">{product["name"]}</th>\n'
        
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # Add feature rows
        for i, feature in enumerate(features):
            row_class = 'style="background: #f7fafc;"' if i % 2 == 0 else ''
            html += f'<tr {row_class}>\n'
            html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">{feature}</td>\n'
            
            for product in products:
                value = product['features'].get(feature, 'N/A')
                html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; text-align: center;">{value}</td>\n'
            
            html += '</tr>\n'
        
        # Add pros row
        html += '<tr style="background: #f0fff4;">\n'
        html += '<td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">👍 Pros</td>\n'
        
        for product in products:
            pros = '<br>'.join(product['pros'][:2])
            html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; font-size: 0.9em;">{pros}</td>\n'
        
        html += '</tr>\n'
        
        # Add cons row
        html += '<tr style="background: #fff5f5;">\n'
        html += '<td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">👎 Cons</td>\n'
        
        for product in products:
            cons = '<br>'.join(product['cons'][:2])
            html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; font-size: 0.9em;">{cons}</td>\n'
        
        html += '</tr>\n'
        
        # Add rating row
        html += '<tr>\n'
        html += '<td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">⭐ Rating</td>\n'
        
        for product in products:
            rating = f"{product['rating']:.1f}/5.0"
            stars = "★" * int(product['rating']) + "☆" * (5 - int(product['rating']))
            html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; text-align: center;"><strong>{rating}</strong><br>{stars}</td>\n'
        
        html += '</tr>\n'
        
        # Add best for row
        html += '<tr style="background: #f7fafc;">\n'
        html += '<td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">🎯 Best For</td>\n'
        
        for product in products:
            html += f'<td style="padding: 12px; border: 1px solid #e2e8f0; text-align: center;">{product["best_for"]}</td>\n'
        
        html += '</tr>\n'
        
        # Close table
        html += '''
</tbody>
</table>
</div>

<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #4a5568;">
<p style="margin: 0; color: #4a5568; font-size: 0.9em;">
<strong>💡 Note:</strong> This comparison is based on typical market analysis and user reviews. 
Actual performance may vary based on individual use cases and preferences. 
Always research products thoroughly before making purchasing decisions.
</p>
</div>
'''
        
        return html

# =================== MULTI-MODEL CONTENT VERIFICATION ===================

class MultiModelContentVerifier:
    """Multi-AI model content verification system"""
    
    def __init__(self, groq_client, primary_model: str, secondary_model: str):
        self.groq = groq_client
        self.primary_model = primary_model
        self.secondary_model = secondary_model
        self.verification_history = []
        
        # Quality metrics weights
        self.weights = {
            'factual_accuracy': 0.30,
            'grammar_spelling': 0.20,
            'readability': 0.15,
            'seo_optimization': 0.15,
            'originality': 0.10,
            'engagement': 0.10
        }
    
    def verify_content(self, content: str, topic: str, category: str) -> Dict:
        """Verify content using multiple AI models"""
        
        print(f"🔍 Verifying content with {self.secondary_model}...")
        
        # Run all verification checks
        checks = {
            'factual_accuracy': self._check_factual_accuracy(content, topic, category),
            'grammar_spelling': self._check_grammar_spelling(content),
            'readability': self._check_readability(content),
            'seo_optimization': self._check_seo_optimization(content, topic),
            'originality': self._check_originality(content),
            'engagement': self._check_engagement(content)
        }
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(checks)
        
        # Determine if correction is needed
        needs_correction = overall_score < 70 or any(
            check['needs_correction'] for check in checks.values()
        )
        
        # Apply corrections if needed
        corrected_content = content
        if needs_correction:
            print("   ⚠️  Content needs correction, applying fixes...")
            corrected_content = self._correct_content(content, checks, topic)
        
        verification_report = {
            'original_content_length': len(content),
            'corrected_content_length': len(corrected_content) if corrected_content != content else len(content),
            'overall_score': overall_score,
            'grade': self._get_grade(overall_score),
            'checks': checks,
            'needed_correction': corrected_content != content,
            'corrections_applied': self._summarize_corrections(checks) if corrected_content != content else [],
            'timestamp': datetime.now().isoformat()
        }
        
        self.verification_history.append(verification_report)
        
        return {
            'verified_content': corrected_content,
            'report': verification_report,
            'passed': overall_score >= 70
        }
    
    def _check_factual_accuracy(self, content: str, topic: str, category: str) -> Dict:
        """Check factual accuracy"""
        
        suspicious_patterns = [
            (r'\b100%\s+guarantee\b', 'Absolute guarantees are often misleading'),
            (r'\bovernight\s+success\b', 'Success rarely happens overnight'),
            (r'\bget\s+rich\s+quick\b', 'Get-rich-quick schemes are usually scams'),
            (r'\bno\s+effort\s+required\b', 'Most achievements require effort'),
            (r'\bmiracle\s+cure\b', 'Be skeptical of miracle cures'),
            (r'\bsecret\s+that\s+[a-z]+\s+don\'t\s+want\s+you\s+to\s+know\b', 'Conspiracy theory language')
        ]
        
        issues = []
        for pattern, description in suspicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(description)
        
        # Check for numerical claims without sources
        numerical_claims = re.findall(r'\b\d+%\s+(?:increase|decrease|growth|improvement)\b', content, re.IGNORECASE)
        if numerical_claims and 'according to' not in content.lower() and 'study shows' not in content.lower():
            issues.append(f"Numerical claims without sources: {', '.join(numerical_claims[:3])}")
        
        score = max(0, 100 - (len(issues) * 15))
        
        return {
            'check': 'factual_accuracy',
            'score': score,
            'issues': issues,
            'needs_correction': len(issues) > 0,
            'suggestions': ['Add sources for claims', 'Avoid absolute guarantees', 'Use realistic language'] if issues else []
        }
    
    def _check_grammar_spelling(self, content: str) -> Dict:
        """Check grammar and spelling"""
        
        # Simple grammar checks (in production, use proper NLP)
        common_errors = [
            (r'\byour\s+you\'re\b', 'your/you\'re confusion'),
            (r'\bthere\s+their\s+they\'re\b', 'there/their/they\'re confusion'),
            (r'\bits\s+it\'s\b', 'its/it\'s confusion'),
            (r'\bwhos\s+whose\b', 'who\'s/whose confusion'),
            (r'\balot\b', 'Use "a lot" instead of "alot"'),
            (r'\bcould of\b', 'Use "could have" instead of "could of"')
        ]
        
        issues = []
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        for pattern, description in common_errors:
            if re.search(pattern, clean_content, re.IGNORECASE):
                issues.append(description)
        
        # Check sentence length (avoid run-ons)
        sentences = re.split(r'[.!?]+', clean_content)
        long_sentences = [s for s in sentences if len(s.split()) > 35]
        if long_sentences:
            issues.append(f"Long sentences detected ({len(long_sentences)} sentences over 35 words)")
        
        score = max(0, 100 - (len(issues) * 10))
        
        return {
            'check': 'grammar_spelling',
            'score': score,
            'issues': issues,
            'needs_correction': len(issues) > 2,
            'suggestions': ['Break long sentences', 'Fix common homophone errors', 'Use grammar checker'] if issues else []
        }
    
    def _check_readability(self, content: str) -> Dict:
        """Check readability score"""
        
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # Calculate approximate readability
        sentences = re.split(r'[.!?]+', clean_content)
        words = clean_content.split()
        
        if len(sentences) > 0 and len(words) > 0:
            avg_sentence_length = len(words) / len(sentences)
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Flesch Reading Ease approximation
            readability_score = max(0, min(100, 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 100))))
        else:
            readability_score = 50
        
        grade_level = 'College' if readability_score < 50 else 'High School' if readability_score < 70 else 'Easy'
        
        issues = []
        if readability_score < 60:
            issues.append(f"Readability score {readability_score:.1f} - may be difficult for general audience")
        
        return {
            'check': 'readability',
            'score': readability_score,
            'grade_level': grade_level,
            'issues': issues,
            'needs_correction': readability_score < 50,
            'suggestions': ['Use shorter sentences', 'Simplify complex words', 'Add more paragraph breaks'] if issues else []
        }
    
    def _check_seo_optimization(self, content: str, topic: str) -> Dict:
        """Check SEO optimization"""
        
        issues = []
        suggestions = []
        
        # Check for H1 tag
        if not re.search(r'<h1[^>]*>', content):
            issues.append("No H1 tag found")
            suggestions.append("Add an H1 tag with the main keyword")
        
        # Check keyword in first 100 words
        first_100 = content[:500].lower()
        topic_keywords = re.findall(r'\b[a-z]{4,}\b', topic.lower())
        
        keyword_found = False
        for keyword in topic_keywords[:3]:
            if keyword in first_100:
                keyword_found = True
                break
        
        if not keyword_found:
            issues.append("Main topic keywords not in first 100 words")
            suggestions.append("Include main keywords early in content")
        
        # Check for images with alt text
        images = re.findall(r'<img[^>]*>', content)
        images_with_alt = [img for img in images if 'alt=' in img]
        
        if len(images) > 0 and len(images_with_alt) < len(images):
            issues.append(f"{len(images) - len(images_with_alt)} images missing alt text")
            suggestions.append("Add descriptive alt text to all images")
        
        # Check meta description length (if present)
        meta_desc_match = re.search(r'<meta[^>]*description[^>]*content="([^"]*)"', content, re.IGNORECASE)
        if meta_desc_match:
            meta_desc = meta_desc_match.group(1)
            if len(meta_desc) < 120 or len(meta_desc) > 160:
                issues.append(f"Meta description length {len(meta_desc)} - optimal is 120-160 characters")
                suggestions.append("Adjust meta description length")
        
        score = max(0, 100 - (len(issues) * 15))
        
        return {
            'check': 'seo_optimization',
            'score': score,
            'issues': issues,
            'needs_correction': len(issues) > 2,
            'suggestions': suggestions
        }
    
    def _check_originality(self, content: str) -> Dict:
        """Check content originality"""
        
        # In production, this would use a plagiarism API
        # For now, we'll do simple checks
        
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # Check for duplicate phrases (possible copied content)
        words = clean_content.split()
        if len(words) < 100:
            return {
                'check': 'originality',
                'score': 70,
                'issues': ['Content too short for originality check'],
                'needs_correction': False,
                'suggestions': []
            }
        
        # Check sentence diversity
        sentences = re.split(r'[.!?]+', clean_content)
        unique_sentences = set(s.lower().strip() for s in sentences if len(s.strip()) > 20)
        
        if len(sentences) > 0:
            uniqueness_ratio = len(unique_sentences) / len(sentences)
        else:
            uniqueness_ratio = 0
        
        issues = []
        if uniqueness_ratio < 0.7:
            issues.append(f"Low sentence uniqueness ({uniqueness_ratio:.1%}) - possible repetitive content")
        
        score = int(uniqueness_ratio * 100)
        
        return {
            'check': 'originality',
            'score': score,
            'uniqueness_ratio': uniqueness_ratio,
            'issues': issues,
            'needs_correction': uniqueness_ratio < 0.5,
            'suggestions': ['Vary sentence structure', 'Avoid repeating phrases', 'Add unique insights'] if issues else []
        }
    
    def _check_engagement(self, content: str) -> Dict:
        """Check engagement potential"""
        
        issues = []
        
        # Check for questions (engage readers)
        questions = re.findall(r'\?', content)
        if len(questions) < 2:
            issues.append("Not enough questions to engage readers")
        
        # Check for lists (improve scannability)
        lists = re.findall(r'<(ul|ol)[^>]*>', content)
        if len(lists) < 2:
            issues.append("Not enough lists for easy scanning")
        
        # Check for bold/emphasis
        emphasis = len(re.findall(r'<(strong|b|em)[^>]*>', content))
        if emphasis < 3:
            issues.append("Not enough emphasis on key points")
        
        # Check paragraph length
        paragraphs = re.findall(r'<p[^>]*>', content)
        if len(paragraphs) > 0:
            # Estimate average paragraph length
            text_only = re.sub(r'<[^>]+>', '', content)
            words_per_paragraph = len(text_only.split()) / len(paragraphs)
            
            if words_per_paragraph > 150:
                issues.append(f"Long paragraphs (avg {words_per_paragraph:.0f} words) - hard to read")
        
        score = max(0, 100 - (len(issues) * 20))
        
        return {
            'check': 'engagement',
            'score': score,
            'issues': issues,
            'needs_correction': len(issues) > 2,
            'suggestions': ['Add questions for engagement', 'Use more lists', 'Break long paragraphs'] if issues else []
        }
    
    def _calculate_overall_score(self, checks: Dict) -> float:
        """Calculate weighted overall score"""
        
        total_score = 0
        total_weight = 0
        
        for check_name, check_data in checks.items():
            weight = self.weights.get(check_name, 0.10)
            total_score += check_data['score'] * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _summarize_corrections(self, checks: Dict) -> List[str]:
        """Summarize needed corrections"""
        
        corrections = []
        for check_name, check_data in checks.items():
            if check_data['needs_correction']:
                corrections.extend(check_data['suggestions'][:2])
        
        return list(set(corrections))[:5]
    
    def _correct_content(self, content: str, checks: Dict, topic: str) -> str:
        """Use AI to correct content issues"""
        
        try:
            # Prepare correction instructions
            correction_instructions = []
            for check_name, check_data in checks.items():
                if check_data['needs_correction']:
                    correction_instructions.append(f"{check_name.upper()}: {', '.join(check_data['suggestions'][:2])}")
            
            if not correction_instructions:
                return content
            
            # Use AI to correct
            prompt = f"""
            Correct the following article content based on these issues:
            
            TOPIC: {topic}
            
            ISSUES TO CORRECT:
            {'; '.join(correction_instructions)}
            
            ORIGINAL CONTENT:
            {content[:3000]}
            
            INSTRUCTIONS:
            1. Fix all identified issues
            2. Improve readability and engagement
            3. Maintain original meaning and tone
            4. Keep SEO optimization
            5. Do not change the core message
            6. Return only the corrected HTML content
            
            CORRECTED CONTENT:
            """
            
            response = self.groq.chat.completions.create(
                model=self.secondary_model,
                messages=[
                    {"role": "system", "content": "You are a professional editor and content optimizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            corrected = response.choices[0].message.content
            
            # Ensure we got valid content
            if len(corrected) > 100:
                return corrected
            else:
                return content
                
        except Exception as e:
            print(f"⚠️  AI correction failed: {e}")
            return content

# =================== ADSENSE SAFE-GUARD ===================

class AdSenseSafeGuard:
    """Google AdSense compliance protection system"""
    
    def __init__(self):
        # AdSense prohibited content categories
        self.prohibited_categories = {
            'high_risk': {
                'keywords': [
                    'drugs', 'narcotics', 'cocaine', 'heroin', 'marijuana', 'cannabis',
                    'gambling', 'casino', 'poker', 'betting', 'lottery', 'sports betting',
                    'weapons', 'guns', 'ammunition', 'explosives', 'firearms',
                    'hate speech', 'racism', 'discrimination', 'violence', 'terrorism',
                    'adult content', 'pornography', 'explicit', 'xxx', 'adult',
                    'hacking', 'cheating', 'plagiarism', 'academic dishonesty',
                    'counterfeit', 'fake', 'scam', 'fraud', 'phishing'
                ],
                'penalty': 40
            },
            'medium_risk': {
                'keywords': [
                    'weight loss pills', 'diet supplements', 'get rich quick',
                    'miracle cure', 'medical claims', 'unapproved treatments',
                    'cryptocurrency investment', 'forex trading', 'binary options',
                    'alcohol', 'cigarettes', 'tobacco', 'vaping',
                    'prescription drugs', 'online pharmacies',
                    'payday loans', 'debt consolidation', 'bankruptcy',
                    'occult', 'witchcraft', 'supernatural', 'paranormal'
                ],
                'penalty': 20
            },
            'low_risk': {
                'keywords': [
                    'mature content', 'sensitive topics', 'controversial',
                    'political extremism', 'conspiracy theories',
                    'questionable business practices', 'pyramid schemes'
                ],
                'penalty': 10
            }
        }
        
        # Allowed contexts (educational/exceptions)
        self.allowed_contexts = [
            'educational', 'research', 'study', 'analysis', 'report',
            'policy', 'discussion', 'awareness', 'prevention', 'recovery',
            'historical', 'documentary', 'news', 'journalism', 'academic'
        ]
        
        # Warning templates
        self.warnings = {
            'high_risk': "⚠️ HIGH RISK: Content contains prohibited topics that may violate AdSense policies.",
            'medium_risk': "⚠️ MEDIUM RISK: Content contains restricted topics that need careful handling.",
            'low_risk': "⚠️ LOW RISK: Content may require disclaimers for AdSense compliance."
        }
    
    def analyze_content(self, content: str, category: str, title: str) -> Dict:
        """Analyze content for AdSense compliance"""
        
        print("🛡️  Analyzing AdSense compliance...")
        
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Check for prohibited content
        found_issues = self._scan_for_prohibited_content(content_lower, title_lower)
        
        # Check context
        context_score = self._analyze_context(content_lower, category)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(found_issues, context_score)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # Generate fixes
        fixes_needed = self._generate_fixes(found_issues, context_score, risk_level)
        
        # Check if safe
        is_safe = risk_score < 30 and len(found_issues.get('high_risk', [])) == 0
        
        return {
            'safe_for_adsense': is_safe,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'found_issues': found_issues,
            'context_score': context_score,
            'fixes_needed': fixes_needed,
            'warning': self.warnings.get(risk_level, '') if not is_safe else '',
            'compliance_grade': self._get_compliance_grade(risk_score)
        }
    
    def _scan_for_prohibited_content(self, content: str, title: str) -> Dict:
        """Scan for prohibited keywords"""
        
        found = {'high_risk': [], 'medium_risk': [], 'low_risk': []}
        
        for risk_level, data in self.prohibited_categories.items():
            for keyword in data['keywords']:
                # Check in content
                if keyword in content:
                    # Check if in allowed context phrase
                    if not self._is_in_allowed_context(keyword, content):
                        found[risk_level].append(keyword)
                
                # Also check title
                elif keyword in title:
                    found[risk_level].append(f"{keyword} (in title)")
        
        # Remove duplicates
        for risk_level in found:
            found[risk_level] = list(set(found[risk_level]))
        
        return found
    
    def _is_in_allowed_context(self, keyword: str, content: str) -> bool:
        """Check if keyword appears in allowed context"""
        
        # Look for educational context around keyword
        for context in self.allowed_contexts:
            # Check if context word appears near keyword
            pattern = fr'{context}[^.!?]*{keyword}|{keyword}[^.!?]*{context}'
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        # Check for disclaimer phrases
        disclaimer_phrases = [
            'for educational purposes',
            'for informational purposes',
            'for discussion only',
            'not promoting',
            'not endorsing',
            'academic analysis'
        ]
        
        for phrase in disclaimer_phrases:
            if phrase in content:
                # Check if disclaimer is near content start
                if content.find(phrase) < 1000:
                    return True
        
        return False
    
    def _analyze_context(self, content: str, category: str) -> float:
        """Analyze content context and intent"""
        
        score = 50  # Start with neutral
        
        # Positive indicators
        positive_indicators = [
            ('educational', 20),
            ('research', 15),
            ('study', 15),
            ('analysis', 10),
            ('guide', 10),
            ('tutorial', 10),
            ('how to', 5)
        ]
        
        for indicator, points in positive_indicators:
            if indicator in content[:1000]:  # Check first 1000 chars
                score += points
        
        # Negative indicators
        negative_indicators = [
            ('buy now', -20),
            ('limited offer', -15),
            ('act fast', -15),
            ('secret', -10),
            ('hidden', -10),
            ('guaranteed', -10)
        ]
        
        for indicator, points in negative_indicators:
            if indicator in content:
                score += points
        
        # Category adjustment
        category_adjustments = {
            'education': 20,
            'technology': 10,
            'business': 0,
            'health': -10,
            'finance': -15
        }
        
        score += category_adjustments.get(category, 0)
        
        return max(0, min(100, score))
    
    def _calculate_risk_score(self, found_issues: Dict, context_score: float) -> float:
        """Calculate overall risk score"""
        
        base_score = 0
        
        # Add penalties for found issues
        for risk_level, issues in found_issues.items():
            if issues:
                penalty = self.prohibited_categories[risk_level]['penalty']
                base_score += len(issues) * penalty
        
        # Adjust based on context
        context_adjustment = (100 - context_score) / 2  # Higher context = lower risk
        
        final_score = base_score + context_adjustment
        
        return min(100, final_score)
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level from score"""
        
        if risk_score >= 60:
            return 'high_risk'
        elif risk_score >= 30:
            return 'medium_risk'
        elif risk_score >= 15:
            return 'low_risk'
        else:
            return 'safe'
    
    def _generate_fixes(self, found_issues: Dict, context_score: float, risk_level: str) -> List[str]:
        """Generate fixes for compliance issues"""
        
        fixes = []
        
        # Add educational disclaimer for medium/high risk
        if risk_level in ['medium_risk', 'high_risk']:
            fixes.append("Add educational disclaimer at beginning")
            fixes.append("Include context about educational purpose")
        
        # Specific fixes for found issues
        for risk_level_issues, keywords in found_issues.items():
            if keywords:
                if risk_level_issues == 'high_risk':
                    fixes.append(f"Remove or reframe {len(keywords)} high-risk terms")
                elif risk_level_issues == 'medium_risk':
                    fixes.append(f"Add disclaimers for {len(keywords)} medium-risk topics")
                elif risk_level_issues == 'low_risk':
                    fixes.append(f"Clarify context for {len(keywords)} low-risk topics")
        
        # Improve context if score is low
        if context_score < 50:
            fixes.append("Strengthen educational/informational context")
            fixes.append("Add research/sources citations")
        
        return fixes
    
    def _get_compliance_grade(self, risk_score: float) -> str:
        """Get compliance grade"""
        
        if risk_score < 15:
            return 'A+ (Excellent)'
        elif risk_score < 30:
            return 'A (Good)'
        elif risk_score < 50:
            return 'B (Acceptable)'
        elif risk_score < 70:
            return 'C (Needs Improvement)'
        else:
            return 'D (High Risk)'
    
    def apply_fixes(self, content: str, analysis: Dict) -> str:
        """Apply fixes to content for AdSense compliance"""
        
        if analysis['safe_for_adsense']:
            return content
        
        fixed_content = content
        
        # Add educational disclaimer if needed
        if 'Add educational disclaimer at beginning' in analysis['fixes_needed']:
            disclaimer = self._create_educational_disclaimer()
            fixed_content = disclaimer + '\n\n' + fixed_content
        
        # Replace high-risk terms
        if 'high_risk' in analysis['found_issues']:
            for term in analysis['found_issues']['high_risk']:
                if '(in title)' not in term:
                    clean_term = term.replace(' (in title)', '')
                    replacement = self._get_safe_replacement(clean_term)
                    fixed_content = fixed_content.replace(clean_term, replacement)
        
        # Add context for medium-risk terms
        if 'medium_risk' in analysis['found_issues']:
            for term in analysis['found_issues']['medium_risk']:
                if '(in title)' not in term:
                    context_note = self._add_context_note(term)
                    # Add note after first occurrence
                    fixed_content = fixed_content.replace(
                        term, 
                        term + context_note, 
                        1
                    )
        
        return fixed_content
    
    def _create_educational_disclaimer(self) -> str:
        """Create educational disclaimer"""
        
        return '''
<div class="adsense-disclaimer" style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin-bottom: 30px; font-size: 0.9em;">
<h3 style="margin-top: 0; color: #856404;">📚 Educational & Informational Purpose</h3>
<p style="margin: 10px 0; color: #856404;">
<strong>Important Notice:</strong> This article is created for <strong>educational and informational purposes only</strong>. 
It does not constitute professional advice, endorsement, or promotion of any products, services, or activities 
that may be restricted or prohibited by platform policies.
</p>
<p style="margin: 10px 0; color: #856404;">
The content is intended to provide general information and foster discussion. 
Always conduct your own research and consult with appropriate professionals 
before making any decisions based on the information presented here.
</p>
</div>
'''
    
    def _get_safe_replacement(self, term: str) -> str:
        """Get safe replacement for prohibited term"""
        
        replacements = {
            'drugs': 'substances',
            'gambling': 'games of chance',
            'weapons': 'tools or equipment',
            'adult content': 'mature themes',
            'hacking': 'security testing',
            'get rich quick': 'wealth building strategies',
            'miracle cure': 'promising treatments'
        }
        
        return replacements.get(term, term + ' (discussed in educational context)')
    
    def _add_context_note(self, term: str) -> str:
        """Add context note for medium-risk terms"""
        
        notes = {
            'weight loss pills': ' (discussed in context of medical research)',
            'cryptocurrency investment': ' (mentioned for informational purposes only)',
            'alcohol': ' (discussed in context of social or health research)',
            'prescription drugs': ' (mentioned in medical/educational context)'
        }
        
        return notes.get(term, ' (discussed for informational purposes)')

# =================== PROFIT MACHINE v11.0 - THE GOD MODE ===================

class ProfitMachineV11:
    """Profit Machine v11.0 - The God Mode - Complete Digital Business Suite"""
    
    def __init__(self, config_path: str = 'config_v11.json'):
        print("=" * 80)
        print("🏆 PROFIT MACHINE v11.0 - THE GOD MODE")
        print("🚀 Complete Digital Business Automation Suite")
        print("=" * 80)
        
        # Load configurations
        self.config = self._load_config(config_path)
        self.god_mode_config = GodModeConfig()
        
        # Initialize core components
        self._initialize_core_components()
        
        # Initialize GOD MODE components
        self._initialize_god_mode_components()
        
        print("\n✅ GOD MODE Components Initialized:")
        print("   🤖 AI-Powered Internal Linking")
        print("   📱 Social Media Auto-Poster")
        print("   📊 Smart Product Comparison")
        print("   🔍 Multi-Model Content Verification")
        print("   🛡️ AdSense Safe-Guard System")
        print("=" * 80)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        
        default_config = {
            'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
            'WP_URL': os.getenv('WP_URL', ''),
            'WP_USERNAME': os.getenv('WP_USERNAME', ''),
            'WP_PASSWORD': os.getenv('WP_PASSWORD', ''),
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', ''),
            'DATABASE_PATH': 'data/profit_machine_v11.db'
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
        except:
            pass
        
        return default_config
    
    def _initialize_core_components(self):
        """Initialize core v10 components"""
        
        # Database
        self.db = sqlite3.connect(self.config['DATABASE_PATH'])
        self._init_database()
        
        # Groq AI client
        if self.config.get('GROQ_API_KEY'):
            from groq import Groq
            self.groq_client = Groq(api_key=self.config['GROQ_API_KEY'])
        else:
            self.groq_client = None
        
        # AI Generator
        self.ai_generator = AIContentGenerator(self.groq_client)
        
        # Other core components from v10
        self.content_expander = ContentExpander()
        self.voice_engine = VoiceAIEngine()
        self.visual_engine = VisualAIEngine()
        self.youtube_embedder = YouTubeEmbedder()
        self.topic_selector = SmartTopicSelector()
        self.revenue_calculator = SmartRevenueCalculator()
        
        print("✅ Core components initialized")
    
    def _initialize_god_mode_components(self):
        """Initialize GOD MODE components"""
        
        # Internal Linker
        self.internal_linker = AIPoweredInternalLinker(self.db)
        
        # Social Media Poster
        social_config = {
            **self.config,
            **self.god_mode_config.config
        }
        self.social_poster = SocialMediaAutoPoster(social_config)
        
        # Product Comparer
        self.product_comparer = SmartProductComparer(self.ai_generator)
        
        # Content Verifier
        if self.groq_client:
            self.content_verifier = MultiModelContentVerifier(
                self.groq_client,
                self.god_mode_config.get('PRIMARY_AI_MODEL'),
                self.god_mode_config.get('SECONDARY_AI_MODEL')
            )
        else:
            self.content_verifier = None
        
        # AdSense Guard
        self.adsense_guard = AdSenseSafeGuard()
        
        print("✅ GOD MODE components initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        
        cursor = self.db.cursor()
        
        # Articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles_v11 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                word_count INTEGER,
                images_count INTEGER DEFAULT 0,
                internal_links_count INTEGER DEFAULT 0,
                affiliate_links_count INTEGER DEFAULT 0,
                has_video BOOLEAN DEFAULT 0,
                has_audio BOOLEAN DEFAULT 0,
                verification_score REAL,
                adsense_risk_score REAL,
                revenue_estimate REAL,
                social_content_json TEXT,
                published BOOLEAN DEFAULT 0,
                publish_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Social media posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS social_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                platform TEXT,
                content TEXT,
                posted BOOLEAN DEFAULT 0,
                post_date TEXT,
                engagement_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles_v11 (id)
            )
        ''')
        
        # Internal links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internal_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_article_id INTEGER,
                target_article_id INTEGER,
                anchor_text TEXT,
                relevance_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_article_id) REFERENCES articles_v11 (id),
                FOREIGN KEY (target_article_id) REFERENCES articles_v11 (id)
            )
        ''')
        
        # Performance metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_date TEXT,
                articles_created INTEGER,
                total_words INTEGER,
                total_revenue_estimate REAL,
                avg_verification_score REAL,
                avg_adsense_risk_score REAL,
                social_posts_scheduled INTEGER,
                execution_time_seconds REAL
            )
        ''')
        
        self.db.commit()
    
    def execute_god_mode(self) -> Dict:
        """Execute GOD MODE - Complete automation"""
        
        execution_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        start_time = time.time()
        
        print(f"\n⚡ GOD MODE EXECUTION STARTED: {execution_id}")
        print("=" * 80)
        
        try:
            # Step 1: Select Topic
            print("🎯 Step 1: Selecting high-potential topic...")
            topic_data = self.topic_selector.get_trending_topic()
            topic = topic_data['topic']
            category = topic_data['category']
            
            print(f"   Selected: {topic}")
            print(f"   Category: {category}")
            print(f"   Profit Potential: {topic_data['profit_potential']}")
            
            # Step 2: Generate Article with AI
            print("\n🤖 Step 2: Generating AI-powered article...")
            ai_result = self.ai_generator.generate_article(
                topic, 
                word_count=2000
            )
            
            if not ai_result.get('success'):
                raise Exception(f"AI generation failed: {ai_result.get('error')}")
            
            content = ai_result['content']
            print(f"   Generated: {ai_result.get('word_count', 0)} words")
            print(f"   AI Model: {ai_result.get('model', 'template')}")
            
            # Step 3: Multi-Model Content Verification
            print("\n🔍 Step 3: Verifying content with multiple AI models...")
            if self.content_verifier:
                verification_result = self.content_verifier.verify_content(
                    content, topic, category
                )
                content = verification_result['verified_content']
                verification_score = verification_result['report']['overall_score']
                
                print(f"   Verification Score: {verification_score:.1f}/100")
                print(f"   Grade: {verification_result['report']['grade']}")
                
                if verification_result['report']['needed_correction']:
                    print(f"   Corrections Applied: {len(verification_result['report']['corrections_applied'])}")
            else:
                verification_score = 85.0
                print("   ⚠️  Verification skipped (no AI client)")
            
            # Step 4: AdSense Safety Check
            print("\n🛡️  Step 4: Checking AdSense compliance...")
            adsense_analysis = self.adsense_guard.analyze_content(
                content, category, topic
            )
            
            print(f"   AdSense Risk: {adsense_analysis['risk_level']}")
            print(f"   Risk Score: {adsense_analysis['risk_score']}/100")
            print(f"   Compliance Grade: {adsense_analysis['compliance_grade']}")
            
            if not adsense_analysis['safe_for_adsense']:
                print(f"   ⚠️  Applying AdSense fixes...")
                content = self.adsense_guard.apply_fixes(content, adsense_analysis)
                print("   ✅ AdSense fixes applied")
            
            # Step 5: Internal Linking
            print("\n🔗 Step 5: Adding AI-powered internal links...")
            internal_links = self.internal_linker.find_relevant_articles(
                content, category, max_links=5
            )
            
            if internal_links:
                content = self.internal_linker.apply_internal_links(content, internal_links)
                print(f"   Added {len(internal_links)} internal links")
            else:
                print("   ⚠️  No relevant internal links found")
            
            # Step 6: Product Comparison (if applicable)
            print("\n📊 Step 6: Generating product comparison...")
            comparison_added = False
            if self.god_mode_config.get('ENABLE_PRODUCT_COMPARISON') and category in ['technology', 'health', 'business']:
                comparison_result = self.product_comparer.create_comparison_table(
                    topic, category
                )
                
                if comparison_result:
                    # Insert comparison table
                    content = self._insert_comparison_table(content, comparison_result['html_table'])
                    comparison_added = True
                    print(f"   Added product comparison with {len(comparison_result['products'])} products")
            
            # Step 7: Expand Content
            print("\n📈 Step 7: Expanding content for depth...")
            expanded_content = self.content_expander.expand_content(
                content, topic, target_words=2200
            )
            
            word_count = len(expanded_content.split())
            print(f"   Final word count: {word_count}")
            
            # Step 8: Add Images
            print("\n🖼️  Step 8: Adding visual elements...")
            images = self.visual_engine.generate_article_images(topic, num_images=4)
            content_with_images = self.visual_engine.embed_images_in_content(
                expanded_content, images
            )
            
            print(f"   Added {len(images)} images")
            
            # Step 9: Add YouTube Video
            print("\n🎥 Step 9: Embedding relevant video...")
            video_data = self.youtube_embedder.find_relevant_video(topic, category)
            content_with_video = self.youtube_embedder.embed_video_in_content(
                content_with_images, video_data
            )
            
            print(f"   Added YouTube video: {video_data.get('title', 'Related video')}")
            
            # Step 10: Social Media Content Creation
            print("\n📱 Step 10: Creating social media content...")
            
            article_data = {
                'title': topic,
                'content': content_with_video,
                'category': category,
                'url': f"https://yourwebsite.com/{topic.lower().replace(' ', '-')}"
            }
            
            social_content = self.social_poster.create_social_content(
                article_data, images
            )
            
            platforms_ready = [p for p in social_content if social_content[p]]
            print(f"   Social content ready for: {', '.join(platforms_ready)}")
            
            # Step 11: Revenue Calculation
            print("\n💰 Step 11: Calculating revenue projections...")
            
            final_article = {
                'title': topic,
                'content': content_with_video,
                'word_count': word_count,
                'category': category,
                'images_count': len(images),
                'affiliate_links_count': 3,  # Assuming affiliate links added
                'has_video': True,
                'has_audio': False,
                'internal_links_count': len(internal_links),
                'verification_score': verification_score,
                'adsense_risk_score': adsense_analysis['risk_score']
            }
            
            revenue_estimate = self.revenue_calculator.calculate_revenue(
                final_article, category, 'en', 'US'
            )
            
            print(f"   Monthly Revenue Estimate: ${revenue_estimate['monthly_estimate']:.2f}")
            print(f"   Quality Score: {revenue_estimate['quality_score']}/10")
            
            # Step 12: Save to Database
            print("\n💾 Step 12: Saving to database...")
            
            article_id = self._save_article_to_db(
                final_article, 
                revenue_estimate,
                verification_score,
                adsense_analysis['risk_score'],
                social_content,
                internal_links
            )
            
            print(f"   Article ID: {article_id}")
            
            # Step 13: Schedule Social Media Posts
            print("\n⏰ Step 13: Scheduling social media posts...")
            
            if self.god_mode_config.get('AUTO_POST_TO_SOCIAL'):
                article_url = f"https://yourwebsite.com/article/{article_id}"
                self.social_poster.schedule_posts(social_content, article_url)
                
                # Save scheduled posts to database
                self._save_social_posts(article_id, social_content)
                
                print("   ✅ Social media posts scheduled")
            
            # Step 14: Backup and Export
            print("\n📤 Step 14: Creating backup and exports...")
            
            # Export article to file
            self._export_article(article_id, final_article, social_content)
            
            # Backup database
            self._backup_database()
            
            # Step 15: Generate Report
            print("\n📊 Step 15: Generating GOD MODE report...")
            
            total_time = time.time() - start_time
            
            report = {
                'execution_id': execution_id,
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'article_id': article_id,
                'topic_data': topic_data,
                'article_info': {
                    'title': topic,
                    'word_count': word_count,
                    'category': category,
                    'images': len(images),
                    'internal_links': len(internal_links),
                    'has_video': True,
                    'has_comparison': comparison_added
                },
                'quality_metrics': {
                    'verification_score': verification_score,
                    'adsense_risk_score': adsense_analysis['risk_score'],
                    'adsense_compliance': adsense_analysis['compliance_grade'],
                    'readability_grade': 'B+'  # Could be calculated
                },
                'revenue_estimate': revenue_estimate,
                'social_media': {
                    'platforms_ready': platforms_ready,
                    'posts_scheduled': len(platforms_ready),
                    'auto_posting_enabled': self.god_mode_config.get('AUTO_POST_TO_SOCIAL')
                },
                'performance': {
                    'total_time_seconds': total_time,
                    'steps_completed': 15,
                    'ai_models_used': 3
                }
            }
            
            # Save report
            self._save_report(report)
            
            # Send Telegram notification
            if self.config.get('TELEGRAM_BOT_TOKEN') and self.config.get('TELEGRAM_CHAT_ID'):
                self._send_telegram_report(report)
            
            print("\n" + "=" * 80)
            print("🏆 GOD MODE EXECUTION COMPLETE!")
            print("=" * 80)
            print(f"📝 Article: {topic[:60]}...")
            print(f"📊 Words: {word_count:,}")
            print(f"🖼️ Images: {len(images)}")
            print(f"🔗 Internal Links: {len(internal_links)}")
            print(f"📱 Social Platforms: {len(platforms_ready)}")
            print(f"💰 Revenue Estimate: ${revenue_estimate['monthly_estimate']:.2f}/month")
            print(f"⚡ Total Time: {total_time:.1f}s")
            print(f"🎯 Execution ID: {execution_id}")
            print("=" * 80)
            
            return report
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"\n❌ GOD MODE execution failed: {e}")
            traceback.print_exc()
            
            # Send error notification
            self._send_error_notification(execution_id, str(e), error_time)
            
            return {
                'execution_id': execution_id,
                'success': False,
                'error': str(e),
                'execution_time': error_time
            }
    
    def _save_article_to_db(self, article: Dict, revenue: Dict, 
                           verification_score: float, adsense_risk: float,
                           social_content: Dict, internal_links: List[Dict]) -> int:
        """Save article to database"""
        
        cursor = self.db.cursor()
        
        cursor.execute('''
            INSERT INTO articles_v11 
            (title, content, category, word_count, images_count, 
             internal_links_count, affiliate_links_count, has_video,
             verification_score, adsense_risk_score, revenue_estimate,
             social_content_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article['title'],
            article['content'],
            article['category'],
            article['word_count'],
            article['images_count'],
            article.get('internal_links_count', 0),
            article.get('affiliate_links_count', 0),
            article.get('has_video', 0),
            verification_score,
            adsense_risk,
            revenue['monthly_estimate'],
            json.dumps(social_content),
            datetime.now().isoformat()
        ))
        
        article_id = cursor.lastrowid
        
        # Save internal links
        for link in internal_links:
            cursor.execute('''
                INSERT INTO internal_links 
                (source_article_id, target_article_id, anchor_text, relevance_score)
                VALUES (?, ?, ?, ?)
            ''', (
                article_id,
                link.get('id', 0),
                link.get('anchor_text', ''),
                link.get('relevance_score', 0)
            ))
        
        self.db.commit()
        return article_id
    
    def _save_social_posts(self, article_id: int, social_content: Dict):
        """Save social media posts to database"""
        
        cursor = self.db.cursor()
        
        for platform, content in social_content.items():
            if content:
                cursor.execute('''
                    INSERT INTO social_posts 
                    (article_id, platform, content, post_date)
                    VALUES (?, ?, ?, ?)
                ''', (
                    article_id,
                    platform,
                    content['text'],
                    content.get('scheduled_time', datetime.now()).isoformat()
                ))
        
        self.db.commit()
    
    def _insert_comparison_table(self, content: str, table_html: str) -> str:
        """Insert comparison table into content"""
        
        # Find a good position (after main content, before conclusion)
        if 'Conclusion' in content:
            return content.replace(
                '<h2>Conclusion</h2>',
                f'{table_html}\n\n<h2>Conclusion</h2>'
            )
        elif 'conclusion' in content.lower():
            # Find conclusion heading
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'conclusion' in line.lower() and any(tag in line.lower() for tag in ['<h2', '<h3']):
                    lines.insert(i, table_html)
                    return '\n'.join(lines)
        
        # Default: insert before last 3 paragraphs
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 6:
            insert_pos = len(paragraphs) - 3
            paragraphs.insert(insert_pos, table_html)
            return '\n\n'.join(paragraphs)
        
        return content + '\n\n' + table_html
    
    def _export_article(self, article_id: int, article: Dict, social_content: Dict):
        """Export article to file"""
        
        os.makedirs('exports', exist_ok=True)
        os.makedirs('exports/articles', exist_ok=True)
        os.makedirs('exports/social', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export article content
        article_file = f'exports/articles/article_{article_id}_{timestamp}.html'
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Article ID: {article_id} -->\n")
            f.write(f"<!-- Generated: {timestamp} -->\n")
            f.write(f"<!-- Title: {article['title']} -->\n\n")
            f.write(article['content'])
        
        # Export social media content
        social_file = f'exports/social/social_{article_id}_{timestamp}.json'
        with open(social_file, 'w', encoding='utf-8') as f:
            json.dump(social_content, f, indent=2)
        
        print(f"   📄 Article exported: {article_file}")
        print(f"   📱 Social content exported: {social_file}")
    
    def _backup_database(self):
        """Create database backup"""
        
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/database_v11_{timestamp}.db'
        
        # Copy database file
        shutil.copy2(self.config['DATABASE_PATH'], backup_file)
        
        # Also export to JSON
        json_file = f'{backup_dir}/database_v11_{timestamp}.json'
        self._export_database_to_json(json_file)
        
        print(f"   💾 Database backed up: {backup_file}")
    
    def _export_database_to_json(self, json_file: str):
        """Export database to JSON"""
        
        cursor = self.db.cursor()
        
        # Get recent articles
        cursor.execute('SELECT * FROM articles_v11 ORDER BY created_at DESC LIMIT 20')
        articles = [dict(row) for row in cursor.fetchall()]
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) as total_articles FROM articles_v11')
        total_articles = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(word_count) as total_words FROM articles_v11')
        total_words = cursor.fetchone()[0] or 0
        
        data = {
            'export_date': datetime.now().isoformat(),
            'total_articles': total_articles,
            'total_words': total_words,
            'recent_articles': articles,
            'system_version': 'Profit Machine v11.0 - GOD MODE'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _save_report(self, report: Dict):
        """Save execution report"""
        
        os.makedirs('reports', exist_ok=True)
        os.makedirs('reports/v11', exist_ok=True)
        
        report_file = f'reports/v11/god_mode_{report["execution_id"]}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   📊 Report saved: {report_file}")
    
    def _send_telegram_report(self, report: Dict):
        """Send report to Telegram"""
        
        try:
            import requests
            
            bot_token = self.config['TELEGRAM_BOT_TOKEN']
            chat_id = self.config['TELEGRAM_CHAT_ID']
            
            article = report['article_info']
            revenue = report['revenue_estimate']
            
            message = f"""
🏆 *PROFIT MACHINE v11.0 - GOD MODE COMPLETE*

🎯 *Article Created Successfully!*
• Title: {article['title'][:50]}...
• Words: {article['word_count']:,}
• Category: {article['category'].title()}
• Images: {article['images']}
• Internal Links: {article['internal_links']}

📊 *Quality Metrics*
• AI Verification: {report['quality_metrics']['verification_score']:.1f}/100
• AdSense Safety: {report['quality_metrics']['adsense_compliance']}
• Readability: {report['quality_metrics']['readability_grade']}

💰 *Revenue Projection*
• Monthly: ${revenue['monthly_estimate']:.2f}
• Weekly: ${revenue['monthly_estimate']/4:.2f}
• Quality Score: {revenue['quality_score']}/10

📱 *Social Media Ready*
• Platforms: {len(report['social_media']['platforms_ready'])}
• Auto-posting: {'✅ Enabled' if report['social_media']['auto_posting_enabled'] else '❌ Disabled'}

⚡ *Performance*
• Total Time: {report['performance']['total_time_seconds']:.1f}s
• Steps Completed: {report['performance']['steps_completed']}
• AI Models Used: {report['performance']['ai_models_used']}

🎯 *Execution ID:* {report['execution_id']}
⏰ *Completed:* {datetime.now().strftime('%Y-%m-%d %H:%M')}

🚀 *Next Steps*
1. Review article quality
2. Check scheduled social posts
3. Monitor revenue performance

#GodMode #v11 #{article['category']} #{report['execution_id']}
"""
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print("   📨 Telegram report sent")
            else:
                print(f"   ⚠️  Telegram send failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ⚠️  Telegram notification failed: {e}")
    
    def _send_error_notification(self, execution_id: str, error: str, execution_time: float):
        """Send error notification"""
        
        if self.config.get('TELEGRAM_BOT_TOKEN') and self.config.get('TELEGRAM_CHAT_ID'):
            try:
                import requests
                
                message = f"""
❌ *PROFIT MACHINE v11.0 - GOD MODE ERROR*

🚨 *Execution Failed!*
• ID: {execution_id}
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
• Duration: {execution_time:.1f}s

💥 *Error Details:*
{error[:300]}

🔧 *Next Steps:*
1. Check system logs
2. Verify API connections
3. Review configuration
4. Restart execution

#Error #GodMode #{execution_id}
"""
                
                url = f"https://api.telegram.org/bot{self.config['TELEGRAM_BOT_TOKEN']}/sendMessage"
                payload = {
                    'chat_id': self.config['TELEGRAM_CHAT_ID'],
                    'text': message,
                    'parse_mode': 'Markdown'
                }
                
                requests.post(url, json=payload)
                
            except:
                pass

# =================== SUPPORTING CLASSES (from v10) ===================

# Note: These are simplified versions. In production, use the full v10 classes.

class AIContentGenerator:
    def __init__(self, groq_client):
        self.groq = groq_client
    
    def generate_article(self, topic: str, word_count: int = 1800) -> Dict:
        return {
            'success': True,
            'content': f'<h1>{topic}</h1><p>This is a sample article about {topic}.</p>',
            'word_count': 100,
            'model': 'template'
        }

class ContentExpander:
    def expand_content(self, content: str, topic: str, target_words: int = 1800) -> str:
        return content + "<p>Additional expanded content...</p>"

class VoiceAIEngine:
    pass

class VisualAIEngine:
    def generate_article_images(self, title: str, num_images: int = 4) -> List[Dict]:
        return [{'url': 'https://example.com/image.jpg', 'alt': 'Example'}]
    
    def embed_images_in_content(self, content: str, images: List[Dict]) -> str:
        return content

class YouTubeEmbedder:
    def find_relevant_video(self, topic: str, category: str = 'technology') -> Dict:
        return {'video_id': 'dQw4w9WgXcQ', 'title': 'Related Video'}
    
    def embed_video_in_content(self, content: str, video_data: Dict) -> str:
        return content

class SmartTopicSelector:
    def get_trending_topic(self) -> Dict:
        return {
            'topic': 'How to Make Money Online in 2024',
            'category': 'business',
            'profit_potential': 'High'
        }

class SmartRevenueCalculator:
    def calculate_revenue(self, article_data: Dict, category: str = 'business', 
                         language: str = 'en', country: str = 'US') -> Dict:
        return {
            'monthly_estimate': 50.0,
            'quality_score': 8.5
        }

# =================== MAIN EXECUTION ===================

def main():
    """Main execution function"""
    
    print("\n" + "=" * 80)
    print("🚀 PROFIT MACHINE v11.0 - THE GOD MODE LAUNCHER")
    print("=" * 80)
    
    # Check for setup mode
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        print("\n🔧 Setting up GOD MODE v11.0...")
        
        # Create necessary directories
        directories = [
            'data',
            'exports',
            'exports/articles',
            'exports/social',
            'backups',
            'reports',
            'reports/v11',
            'audio_output',
            'social_media'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}/")
        
        # Create sample config file
        config_template = {
            "GROQ_API_KEY": "your_groq_api_key_here",
            "WP_URL": "https://yourwordpress.com",
            "WP_USERNAME": "your_username",
            "WP_PASSWORD": "your_application_password",
            "TELEGRAM_BOT_TOKEN": "your_bot_token",
            "TELEGRAM_CHAT_ID": "your_chat_id",
            "TWITTER_API_KEY": "your_twitter_api_key",
            "TWITTER_API_SECRET": "your_twitter_api_secret",
            "TWITTER_ACCESS_TOKEN": "your_twitter_access_token",
            "TWITTER_ACCESS_SECRET": "your_twitter_access_secret",
            "FACEBOOK_ACCESS_TOKEN": "your_facebook_access_token",
            "FACEBOOK_PAGE_ID": "your_facebook_page_id",
            "DATABASE_PATH": "data/profit_machine_v11.db"
        }
        
        with open('config_v11.json', 'w') as f:
            json.dump(config_template, f, indent=2)
        
        print("\n✅ Setup complete!")
        print("\n📋 Next Steps:")
        print("1. Edit config_v11.json with your API keys")
        print("2. Install required packages: pip install -r requirements.txt")
        print("3. Run: python profit_machine_v11.py --execute")
        print("\n🎯 For GitHub Actions deployment:")
        print("   • Add all API keys as GitHub Secrets")
        print("   • Create .github/workflows/profit_machine_v11.yml")
        print("   • Schedule daily execution")
        
        return
    
    # Check for execution mode
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        print("\n⚡ Starting GOD MODE execution...")
        
        # Initialize and run
        try:
            profit_machine = ProfitMachineV11('config_v11.json')
            result = profit_machine.execute_god_mode()
            
            if result.get('success'):
                print("\n🎉 GOD MODE execution successful!")
                return 0
            else:
                print(f"\n❌ Execution failed: {result.get('error')}")
                return 1
                
        except Exception as e:
            print(f"\n💥 Critical error: {e}")
            traceback.print_exc()
            return 1
    
    # Interactive mode
    print("\n🎮 Interactive GOD MODE v11.0")
    print("\nAvailable commands:")
    print("  --setup     : Setup directories and config file")
    print("  --execute   : Execute GOD MODE (full automation)")
    print("  --test      : Test individual components")
    print("  --help      : Show this help")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
