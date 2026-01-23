"""
Enterprise Backup Manager - Handles data backup and export operations
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import boto3
from google.cloud import storage
import zipfile
import hashlib
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

class BackupManager:
    """Manages backup and export operations for enterprise system"""
    
    def __init__(self, config_path: str = "exports/backup_info.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # Ensure exports directory exists
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.exports_dir / "daily").mkdir(exist_ok=True)
        (self.exports_dir / "weekly").mkdir(exist_ok=True)
        (self.exports_dir / "monthly").mkdir(exist_ok=True)
        (self.exports_dir / "temp").mkdir(exist_ok=True)
        
        # Initialize cloud clients if configured
        self.s3_client = None
        self.gcs_client = None
        self._init_cloud_clients()
    
    def _load_config(self) -> Dict:
        """Load backup configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config
            default_config = {
                "backup_info": {
                    "version": "2.0.0",
                    "last_backup": None,
                    "backup_schedule": "daily",
                    "retention_days": 30,
                    "storage_locations": ["local"],
                    "compression_enabled": True,
                    "encryption_enabled": False
                }
            }
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def _init_cloud_clients(self):
        """Initialize cloud storage clients"""
        try:
            if os.getenv('AWS_ACCESS_KEY_ID'):
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')
                )
                logger.info("S3 client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize S3 client: {e}")
        
        try:
            if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                self.gcs_client = storage.Client()
                logger.info("GCS client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize GCS client: {e}")
    
    def backup_results(self, results: Dict, backup_type: str = "daily") -> str:
        """
        Backup results with encryption and compression
        
        Args:
            results: Results to backup
            backup_type: Type of backup (daily, weekly, monthly)
        
        Returns:
            Path to backup file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{backup_type}_{timestamp}"
            
            # Create backup directory
            backup_dir = self.exports_dir / backup_type
            backup_dir.mkdir(exist_ok=True)
            
            # Save results as JSON
            json_path = backup_dir / f"{backup_filename}.json"
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Compress if enabled
            if self.config['backup_info']['compression_enabled']:
                zip_path = backup_dir / f"{backup_filename}.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(json_path, arcname=f"{backup_filename}.json")
                
                # Remove original JSON file
                os.remove(json_path)
                backup_path = zip_path
            else:
                backup_path = json_path
            
            # Encrypt if enabled
            if self.config['backup_info']['encryption_enabled']:
                backup_path = self._encrypt_file(backup_path)
            
            # Upload to cloud storage
            self._upload_to_cloud(backup_path, backup_type)
            
            # Update config
            self.config['backup_info']['last_backup'] = timestamp
            self._save_config()
            
            # Cleanup old backups
            self._cleanup_old_backups(backup_type)
            
            logger.info(f"Backup completed: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
    
    def _encrypt_file(self, file_path: Path) -> Path:
        """Encrypt backup file"""
        # Generate or load encryption key
        key_path = self.exports_dir / ".encryption_key"
        if key_path.exists():
            with open(key_path, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
        
        # Encrypt file
        fernet = Fernet(key)
        with open(file_path, 'rb') as f:
            original_data = f.read()
        
        encrypted_data = fernet.encrypt(original_data)
        
        encrypted_path = file_path.with_suffix('.encrypted')
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Remove original file
        os.remove(file_path)
        
        return encrypted_path
    
    def _upload_to_cloud(self, file_path: Path, backup_type: str):
        """Upload backup to cloud storage"""
        timestamp = datetime.now().strftime("%Y/%m/%d")
        
        # Upload to S3
        if self.s3_client and 's3' in self.config['backup_info']['storage_locations']:
            try:
                s3_key = f"backups/{backup_type}/{timestamp}/{file_path.name}"
                self.s3_client.upload_file(
                    str(file_path),
                    os.getenv('S3_BACKUP_BUCKET', 'profit-machine-backups'),
                    s3_key
                )
                logger.info(f"Uploaded to S3: {s3_key}")
            except Exception as e:
                logger.error(f"S3 upload failed: {e}")
        
        # Upload to GCS
        if self.gcs_client and 'gcs' in self.config['backup_info']['storage_locations']:
            try:
                bucket_name = os.getenv('GCS_BACKUP_BUCKET', 'profit-machine-backups')
                bucket = self.gcs_client.bucket(bucket_name)
                blob = bucket.blob(f"backups/{backup_type}/{timestamp}/{file_path.name}")
                blob.upload_from_filename(str(file_path))
                logger.info(f"Uploaded to GCS: {blob.name}")
            except Exception as e:
                logger.error(f"GCS upload failed: {e}")
    
    def _cleanup_old_backups(self, backup_type: str):
        """Remove old backups based on retention policy"""
        retention_days = self.config['backup_info']['retention_days']
        backup_dir = self.exports_dir / backup_type
        
        if not backup_dir.exists():
            return
        
        cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 3600)
        
        for file_path in backup_dir.iterdir():
            if file_path.stat().st_mtime < cutoff_date:
                try:
                    file_path.unlink()
                    logger.info(f"Removed old backup: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to remove old backup {file_path}: {e}")
    
    def _save_config(self):
        """Save updated configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_backup_status(self) -> Dict:
        """Get backup status and statistics"""
        status = {
            "last_backup": self.config['backup_info']['last_backup'],
            "total_backups": 0,
            "backup_sizes": {},
            "storage_usage": {}
        }
        
        for backup_type in ["daily", "weekly", "monthly"]:
            backup_dir = self.exports_dir / backup_type
            if backup_dir.exists():
                backups = list(backup_dir.iterdir())
                status["total_backups"] += len(backups)
                status["backup_sizes"][backup_type] = {
                    "count": len(backups),
                    "total_size_mb": sum(f.stat().st_size for f in backups) / (1024 * 1024)
                }
        
        return status
