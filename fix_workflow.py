"""
Fix for GitHub Actions workflow - Creates necessary directories and files
"""

import os
import json
from pathlib import Path

def setup_exports_directory():
    """Setup exports directory structure"""
    
    # Create main directories
    directories = [
        "exports",
        "exports/daily",
        "exports/weekly",
        "exports/monthly",
        "exports/temp",
        "results",
        "logs",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True, parents=True)
        print(f"Created directory: {directory}")
    
    # Create backup_info.json
    backup_info = {
        "backup_info": {
            "version": "2.0.0",
            "last_backup": None,
            "backup_schedule": "daily",
            "retention_days": 30,
            "storage_locations": ["local"],
            "compression_enabled": True,
            "encryption_enabled": False
        },
        "export_formats": {
            "pdf": {
                "enabled": True,
                "template": "professional",
                "watermark": True
            },
            "excel": {
                "enabled": True,
                "include_charts": True,
                "auto_format": True
            },
            "json": {
                "enabled": True,
                "pretty_print": True,
                "include_metadata": True
            }
        },
        "notification_settings": {
            "on_success": True,
            "on_failure": True,
            "channels": ["slack", "email", "telegram"],
            "recipients": ["devops@company.com", "alerts@company.com"]
        }
    }
    
    with open("exports/backup_info.json", "w") as f:
        json.dump(backup_info, f, indent=2)
    
    print("Created exports/backup_info.json")
    
    # Create .gitkeep files in empty directories
    for directory in directories:
        gitkeep_path = Path(directory) / ".gitkeep"
        if not list(Path(directory).iterdir()):
            gitkeep_path.touch()
    
    return True

if __name__ == "__main__":
    print("Setting up exports directory structure...")
    success = setup_exports_directory()
    if success:
        print("✓ Setup completed successfully")
    else:
        print("✗ Setup failed")
        exit(1)
