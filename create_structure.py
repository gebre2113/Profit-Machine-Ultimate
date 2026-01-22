import os
import json
from pathlib import Path
import shutil

def create_complete_structure():
    """Profit Machine Ultimate የተሟላ መዋቅር ፍጠር"""
    
    project_root = Path(__file__).parent
    
    # ዋና የሆኑ ዳይሬክቶሪዎች
    directories = [
        'core',
        'v10',
        'v11',
        'utils',
        'data',
        'exports/v10',
        'exports/v11',
        'logs',
        'backups',
        'v10_original',
        'v11_original',
        '.github/workflows',
        'reports',
        'social_media',
        'audio_output',
        'templates'
    ]
    
    print("🏗️  Profit Machine Ultimate መዋቅር እየፈጠረ...")
    
    # ለማስቀረት የሚገባው የድህረ-ገጽ ምልክቶች ስርዓት
    protected_items = {
        '.github',
        '.git',
        'README.md',
        'requirements.txt',
        '.gitignore',
        'master_config.json',
        '.env.example'
    }
    
    # ዳይሬክቶሪዎችን ፍጠር (ፋይሎችን ከሌለ ወይም ፋይል ከሆነ ሰርድ)
    for directory in directories:
        dir_path = project_root / directory
        
        # የድህረ-ገጽ ስርዓትን አትንካ
        if any(protected in str(dir_path) for protected in protected_items):
            continue
            
        # ከሆነ ፋይል፣ ሰርድዎ
        if dir_path.exists() and dir_path.is_file():
            print(f"⚠️  ፋይል ተገኝቷል፣ እየተሰረዘ...: {directory}")
            dir_path.unlink()
        
        # ዳይሬክቶሪውን ፍጠር
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ ተፈጥሯል: {directory}/")
        except FileExistsError as e:
            print(f"⚠️  ዳይሬክቶሪ ቀድሞ ይገኛል: {directory}")
        
        # ለፓይዘን ፓኬጆች __init__.py ጨምር
        if directory in ['core', 'v10', 'v11', 'utils']:
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                init_file.touch()
    
    # ዋና የሆኑ ፋይሎችን ፍጠር (ካልተገኙ ብቻ)
    essential_files = {
        'README.md': """# 🏆 Profit Machine Ultimate
ሙሉ በሙሉ አውቶማቲክ የዲጂታል ቢዝነስ ስርአት

## ባህሪያት
✅ v10 - የይዘት ፋብሪካ
✅ v11 - GOD MODE (የጥራት ቁጥጥር እና ግብይት)
✅ Master Controller (ማርት ሩቲንግ)
✅ GitHub Actions (24/7 አውቶማቲክ)
✅ Telegram ማሳወቂያዎች
✅ የውሂብ ጎታ ቆጣቢነት

## ፈጣን መክፈቻ
1. ይህንን repository ይቅዱ
2. ይህን ያሂዱ: `python main_controller.py --setup`
3. API keys ወደ .env ፋይል ይጨምሩ
4. በአካባቢው ይሞክሩ: `python main_controller.py --workflow daily`
5. ለ24/7 አውቶማቲክ ወደ GitHub ይግቡ

## አዋቅር
`.env.example` ወደ `.env` ይቅዱ እና API keys ያክሉ።

## ድጋፍ
ለችግሮች፣ GitHub repository ይመልከቱ።
""",
        
        '.env.example': """# Profit Machine Ultimate - አካባቢ ተለዋዋጮች

# የኮር APIs
GROQ_API_KEY=your_groq_api_key_here
WP_URL=https://yourwordpress.com
WP_USERNAME=your_username
WP_PASSWORD=your_application_password

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# ማህበራዊ ሚዲያ (አማራጭ)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

FACEBOOK_ACCESS_TOKEN=your_facebook_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# አፊሊዬት ኔትዎርኮች (በGitHub Secrets ውስጥ ያከማቹ)
AMAZON_AFFILIATE_ID=your_amazon_id
CLICKBANK_AFFILIATE_ID=your_clickbank_id
SHAREASALE_AFFILIATE_ID=your_shareasale_id

# የስርአት ማስተካከያዎች
MASTER_MODE=auto
HYBRID_STRATEGY=quality_first
V10_DAILY_LIMIT=2
V11_DAILY_LIMIT=1
""",
        
        'requirements.txt': """# Profit Machine Ultimate ጥገኛዎች

# ኮር
requests==2.31.0
groq==0.3.0
python-dotenv==1.0.0
schedule==1.2.0

# የይዘት ማመንጨት
gtts==2.3.2
pygame==2.5.1

# የውሂብ ማስናድ
pandas==2.1.4
numpy==1.24.3

# ማህበራዊ ሚዲያ (አማራጭ)
tweepy==4.14.0
facebook-sdk==4.0.0
praw==7.7.1

# የስርአት ምርታማነት
psutil==5.9.6

# የድር ጣውላ ስክራፕ
beautifulsoup4==4.12.2
lxml==4.9.3

# የውሂብ ጎታ
sqlite3

# መገልጃዎች
python-dateutil==2.8.2
tqdm==4.66.1
""",
        
        '.gitignore': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Database
*.db
*.db-journal
*.sqlite
*.sqlite3

# Backups
backups/
*.backup

# System files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Environment Variables
.env
.env.local
secrets/
config_*.json

# Exports (can be large)
exports/
!exports/README.md

# Audio files
audio_output/*.mp3

# Social media exports
social_media/
""",
        
        'master_config.json': json.dumps({
            "mode": "auto",
            "hybrid_strategy": "quality_first",
            "v10_settings": {
                "enabled": True,
                "daily_limit": 2,
                "target_word_count": 1800,
                "auto_publish": False,
                "enable_affiliate": True
            },
            "v11_settings": {
                "enabled": True,
                "daily_limit": 1,
                "enable_adsense_protection": True,
                "enable_social_posting": True,
                "enable_verification": True,
                "enable_internal_linking": True
            },
            "routing_rules": {
                "new_topic": "v10",
                "enhancement": "v11",
                "high_value_topic": "v11",
                "quick_content": "v10"
            },
            "scheduling": {
                "v10_schedule": [9, 14, 19],
                "v11_schedule": [10, 16],
                "max_daily_executions": 5
            },
            "notifications": {
                "telegram_enabled": True,
                "error_alerts": True,
                "daily_reports": True,
                "revenue_alerts": True
            }
        }, indent=2),
        
        'data/README.md': """# Data Directory

ይህ ዳይሬክቶሪ የሚያከማቸው:
- የውሂብ ጎታ ፋይሎች (.db)
- JSON የተላኩ ፋይሎች
- የፈጠራ ምደባዎች
- የሥራ ታሪክ

እነዚህን ፋይሎች አትሰርዙ! አስፈላጊ የሥራ ውሂብ ይዘውታል።
""",
        
        'exports/README.md': """# Exports Directory

ከProfit Machine የተላኩ አውቶማቲክ የተላኩ ፋይሎች:
- v10/ - የይዘት ፋብሪካ የተላኩ ፋይሎች
- v11/ - GOD MODE የተሻሻሉ የተላኩ ፋይሎች
- የውሂብ ጎታ የተጠበቁ ፋይሎች
- ማህበራዊ ሚዲያ ይዘቶች

እነዚህ ፋይሎች በራስ-ሰር ይፈጠራሉ እና ወደ GitHub ይጠበቃሉ።
"""
    }
    
    # ፋይሎችን ፍጠር (ካልተገኙ ብቻ)
    for filename, content in essential_files.items():
        file_path = project_root / filename
        
        # ፋይሉ ከሌለ ብቻ ፍጠር
        if not file_path.exists():
            file_path.write_text(content)
            print(f"✅ ተፈጥሯል: {filename}")
        else:
            print(f"⚠️  ቀድሞ ይገኛል: {filename}")
    
    # ለመዋቅር ባዶ የፓይዘን ፋይሎችን ፍጠር
    empty_py_files = [
        'core/base_engine.py',
        'utils/file_manager.py',
        'utils/logger.py',
        'utils/validators.py',
        'templates/article_template.html'
    ]
    
    for filepath in empty_py_files:
        file_path = project_root / filepath
        
        # የፋይል ዳይሬክቶሪ ካልተገኘ ፍጠር
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # ፋይሉ ከሌለ ብቻ ፍጠር
        if not file_path.exists():
            file_path.touch()
            print(f"✅ ተፈጥሯል: {filepath}")
        else:
            print(f"⚠️  ቀድሞ ይገኛል: {filepath}")
    
    print("\n🎉 የፕሮጀክቱ መዋቅር በተሳካ ሁኔታ ተፈጥሯል!")
    print("\n📋 ቀጣይ እርምጃዎች:")
    print("1. የv10 ኮድዎን ወደ v10_original/ ዳይሬክቶሪ ይቅዱ")
    print("2. የv11 ኮድዎን ወደ v11_original/ ዳይሬክቶሪ ይቅዱ")
    print("3. .env.example ወደ .env ይቅዱ እና API keys ያክሉ")
    print("4. ይህን ያሂዱ: python main_controller.py --setup")
    print("5. ይሞክሩ: python main_controller.py --workflow daily")
    
    # ለGitHub Actions የተለየ ምክር
    print("\n🔧 ለGitHub Actions:")
    print("1. ይህንን ይጫኑ: pip install -r requirements.txt")
    print("2. የሚፈልጉትን API keys እንደ GitHub Secrets ያከማቹ")
    print("3. .github/workflows/ ውስጥ የስራ ፍሰት ፋይሎችን ይጨምሩ")

def clean_and_create():
    """ነገሮችን አጽድቆ እንደገና መዋቅሩን ፍጠር"""
    project_root = Path(__file__).parent
    
    # ለማስቀረት የሚገባው የድህረ-ገጽ ምልክቶች
    protected_items = ['.git', '.github', 'README.md', 'LICENSE']
    
    print("🧹 የድህረ-ገጽ ስርዓቱን ሳይጎዳ አጽዳቂ...")
    
    # የተፈጠሩትን ዳይሬክቶሪዎች ሰርድ (ጥበቃ ያለውን ሳይጎዳ)
    items_to_remove = [
        'core', 'v10', 'v11', 'utils', 'data', 'exports',
        'logs', 'backups', 'v10_original', 'v11_original',
        'reports', 'social_media', 'audio_output', 'templates'
    ]
    
    for item in items_to_remove:
        item_path = project_root / item
        
        # ጥበቃ ያለውን አትንኩ
        if any(protected in str(item_path) for protected in protected_items):
            continue
            
        if item_path.exists():
            if item_path.is_file():
                item_path.unlink()
                print(f"🗑️  ፋይል ተሰረዘ: {item}")
            elif item_path.is_dir():
                shutil.rmtree(item_path)
                print(f"🗑️  ዳይሬክቶሪ ተሰረዘ: {item}")
    
    print("\n🔧 አዲስ መዋቅር እየፈጠረ...")
    create_complete_structure()

if __name__ == "__main__":
    # የአጽዳቂ ሞድን ለመጠቀም፡-
    # clean_and_create()
    
    # ለመደበኛ አጠቃቀም፡-
    create_complete_structure()
