"""
EnhancedMasterController - Main Orchestrator for Content Generation System
Manages workflow, logging, and export coordination.
"""

import os
import sys
import json
import time
import schedule
import threading
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import setup_logging
from utils.telegram_reporter import send_telegram_message
from utils.config_manager import ConfigManager


class EnhancedMasterController:
    """Main controller for orchestration with enhanced features."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize with configuration."""
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        
        # Setup directories
        self.base_dir = Path(__file__).parent.parent
        self.exports_dir = self.base_dir / "exports"
        self.exports_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.loggers = self._setup_loggers()
        
        # Track execution
        self.execution_count = 0
        self.max_executions = self.config.get("max_executions", 5)
        
        self.loggers['master'].info("🚀 EnhancedMasterController Initialized")
        
    def _setup_loggers(self) -> Dict[str, Any]:
        """Setup multiple loggers for different components."""
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        return {
            'master': setup_logging('master', log_dir / 'master.log'),
            'generation': setup_logging('generation', log_dir / 'generation.log'),
            'export': setup_logging('export', log_dir / 'export.log'),
            'wordpress': setup_logging('wordpress', log_dir / 'wordpress.log')
        }
    
    def log_system_info(self):
        """Log system and environment information."""
        logger = self.loggers['master']
        logger.info("=" * 50)
        logger.info(f"System Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Python Version: {sys.version}")
        logger.info(f"Project Root: {self.base_dir}")
        logger.info(f"Exports Directory: {self.exports_dir}")
        logger.info(f"Max Executions: {self.max_executions}")
        logger.info("=" * 50)
    
    def run_v11(self):
        """Execute the v11 content generation pipeline."""
        self.execution_count += 1
        logger = self.loggers['master']
        
        logger.info(f"🔄 Execution #{self.execution_count} started")
        
        try:
            # Step 1: Run data collection
            logger.info("Step 1: Running data collection...")
            collection_result = self._run_module("data_collection.py")
            
            if not collection_result:
                logger.error("Data collection failed")
                return False
            
            # Step 2: Run content generation
            logger.info("Step 2: Running content generation...")
            generation_result = self._run_module("content_generation.py")
            
            if not generation_result:
                logger.error("Content generation failed")
                return False
            
            # Step 3: Process and export content
            logger.info("Step 3: Processing and exporting content...")
            export_result = self._process_exports()
            
            if export_result:
                logger.info(f"✅ Execution #{self.execution_count} completed successfully")
                
                # Send to WordPress if configured
                if export_result.get('content_data'):
                    self.publish_to_wordpress(export_result['content_data'])
                    
                # Send Telegram notification
                self._send_notification(
                    f"✅ Execution #{self.execution_count} completed\n"
                    f"Topic: {export_result.get('topic', 'Unknown')}\n"
                    f"Files: {len(export_result.get('files', []))}"
                )
                
                return True
            else:
                logger.error(f"❌ Execution #{self.execution_count} failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Critical error in execution #{self.execution_count}: {str(e)}", exc_info=True)
            return False
    
    def _run_module(self, module_name: str) -> bool:
        """Execute a Python module as subprocess."""
        module_path = self.base_dir / "modules" / module_name
        
        if not module_path.exists():
            self.loggers['master'].error(f"Module not found: {module_path}")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, str(module_path)],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                self.loggers['master'].info(f"✅ {module_name} executed successfully")
                return True
            else:
                self.loggers['master'].error(
                    f"❌ {module_name} failed with exit code {result.returncode}\n"
                    f"STDERR: {result.stderr[:500]}"
                )
                return False
                
        except subprocess.TimeoutExpired:
            self.loggers['master'].error(f"❌ {module_name} timed out after 5 minutes")
            return False
        except Exception as e:
            self.loggers['master'].error(f"❌ Error running {module_name}: {str(e)}")
            return False
    
    def _process_exports(self) -> Optional[Dict]:
        """Process generated content and prepare for export."""
        logger = self.loggers['export']
        
        try:
            # Look for generated content files
            content_files = list(self.exports_dir.glob("*_generated_*.json"))
            
            if not content_files:
                logger.warning("No generated content files found")
                return None
            
            results = {
                'files': [],
                'content_data': None,
                'topic': ''
            }
            
            for file_path in content_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_data = json.load(f)
                    
                    # Store for WordPress publishing
                    if results['content_data'] is None:
                        results['content_data'] = content_data
                        results['topic'] = content_data.get('topic', 'Unknown Topic')
                    
                    # Convert to other formats
                    self._create_html_version(content_data, file_path)
                    self._create_markdown_version(content_data, file_path)
                    
                    results['files'].append(str(file_path))
                    logger.info(f"📦 Processed: {file_path.name}")
                    
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in export processing: {str(e)}", exc_info=True)
            return None
    
    def _create_html_version(self, content_data: Dict, original_path: Path):
        """Create HTML version of content."""
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content_data.get('topic', 'Generated Content')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        p {{ margin-bottom: 15px; }}
        .meta {{ color: #777; font-size: 0.9em; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>{content_data.get('topic', 'Generated Content')}</h1>
    
    <div class="meta">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Execution:</strong> #{self.execution_count}</p>
    </div>
    
    <div class="content">
"""
            
            if 'sections' in content_data:
                for section in content_data['sections']:
                    html_content += f'<div class="section">\n'
                    html_content += f'<h2>{section.get("title", "")}</h2>\n'
                    html_content += f'<p>{section.get("content", "").replace(chr(10), "<br>")}</p>\n'
                    html_content += '</div>\n'
            
            html_content += """
    </div>
</body>
</html>
"""
            
            html_path = original_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            self.loggers['export'].info(f"📄 Created HTML: {html_path.name}")
            
        except Exception as e:
            self.loggers['export'].error(f"Error creating HTML: {str(e)}")
    
    def _create_markdown_version(self, content_data: Dict, original_path: Path):
        """Create Markdown version of content."""
        try:
            markdown = f"# {content_data.get('topic', 'Generated Content')}\n\n"
            markdown += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            markdown += f"*Execution: #{self.execution_count}*\n\n"
            
            if 'sections' in content_data:
                for section in content_data['sections']:
                    markdown += f"## {section.get('title', '')}\n\n"
                    markdown += f"{section.get('content', '')}\n\n"
            
            md_path = original_path.with_suffix('.md')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
            self.loggers['export'].info(f"📝 Created Markdown: {md_path.name}")
            
        except Exception as e:
            self.loggers['export'].error(f"Error creating Markdown: {str(e)}")
    
    def publish_to_wordpress(self, content_data: Dict) -> bool:
        """Publish generated content to WordPress via REST API"""
        import requests
        from requests.auth import HTTPBasicAuth

        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_APPLICATION_PASSWORD')

        if not all([wp_url, wp_user, wp_pass]):
            self.loggers['master'].warning("⚠️ WordPress credentials missing. Skipping upload.")
            return False

        payload = {
            'title': content_data['topic'],
            'content': content_data['content'],
            'status': 'publish',  # Can change to 'draft' for testing
            'categories': [1],     # Category ID
        }

        try:
            response = requests.post(
                wp_url,
                json=payload,
                auth=HTTPBasicAuth(wp_user, wp_pass),
                timeout=30
            )
            if response.status_code == 201:
                self.loggers['master'].info(f"✅ Successfully published to WordPress: {content_data['topic']}")
                self.loggers['wordpress'].info(f"Published: {content_data['topic']} - Post ID: {response.json().get('id')}")
                return True
            else:
                self.loggers['master'].error(f"❌ WP Upload failed: {response.status_code} - {response.text}")
                self.loggers['wordpress'].error(f"Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.loggers['master'].error(f"❌ WP Error: {e}")
            self.loggers['wordpress'].error(f"Exception: {str(e)}")
            return False
    
    def _send_notification(self, message: str):
        """Send notification via Telegram."""
        try:
            # Check if Telegram is enabled in config
            telegram_config = self.config.get('telegram', {})
            if not telegram_config.get('enabled', False):
                self.loggers['master'].debug("Telegram notifications disabled")
                return
            
            send_telegram_message(
                message,
                telegram_config.get('bot_token'),
                telegram_config.get('chat_id')
            )
            self.loggers['master'].info("📱 Telegram notification sent")
            
        except Exception as e:
            self.loggers['master'].warning(f"Failed to send Telegram notification: {str(e)}")
    
    def run_scheduled(self, interval_minutes: int = 60):
        """Run the controller on a scheduled basis."""
        logger = self.loggers['master']
        
        logger.info(f"⏰ Starting scheduled execution every {interval_minutes} minutes")
        self.log_system_info()
        
        # Run immediately on start
        self.run_v11()
        
        # Schedule subsequent runs
        schedule.every(interval_minutes).minutes.do(self.run_v11)
        
        # Keep running
        try:
            while self.execution_count < self.max_executions:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Scheduled execution stopped by user")
        except Exception as e:
            logger.error(f"❌ Scheduler error: {str(e)}", exc_info=True)
    
    def run_once(self):
        """Run the controller once."""
        self.log_system_info()
        return self.run_v11()


def main():
    """Main entry point."""
    controller = EnhancedMasterController()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheduled":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            controller.run_scheduled(interval)
        elif sys.argv[1] == "--once":
            controller.run_once()
        else:
            print("Usage: python main_controller.py [--scheduled [minutes] | --once]")
            print("Default: runs once")
            controller.run_once()
    else:
        controller.run_once()


if __name__ == "__main__":
    main()
