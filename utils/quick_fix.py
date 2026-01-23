"""
Quick fix script for GitHub Actions issues
Run this script to fix common workflow problems
"""

import os
import json
import sys
from pathlib import Path

def fix_workflow_issues():
    """Fix common GitHub Actions workflow issues"""
    
    fixes = []
    
    # 1. Fix exports directory
    exports_dir = Path("exports")
    if not exports_dir.exists():
        exports_dir.mkdir(parents=True, exist_ok=True)
        (exports_dir / "daily").mkdir(exist_ok=True)
        (exports_dir / "weekly").mkdir(exist_ok=True)
        (exports_dir / "monthly").mkdir(exist_ok=True)
        (exports_dir / "temp").mkdir(exist_ok=True)
        fixes.append("Created exports directory structure")
    
    # 2. Fix backup_info.json
    backup_info_path = exports_dir / "backup_info.json"
    if not backup_info_path.exists():
        backup_info = {
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
        with open(backup_info_path, 'w') as f:
            json.dump(backup_info, f, indent=2)
        fixes.append("Created backup_info.json")
    
    # 3. Create other necessary directories
    directories = ["results", "logs", "cache"]
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            fixes.append(f"Created {directory} directory")
    
    # 4. Check workflow files
    workflow_dir = Path(".github/workflows")
    if workflow_dir.exists():
        for workflow_file in workflow_dir.glob("*.yml"):
            with open(workflow_file, 'r') as f:
                content = f.read()
            
            # Check for deprecated actions
            if "actions/upload-artifact@v3" in content:
                fixes.append(f"⚠️ Found deprecated v3 in {workflow_file.name} - Update to v4")
            if "actions/checkout@v3" in content:
                fixes.append(f"⚠️ Found deprecated v3 in {workflow_file.name} - Update to v4")
    
    return fixes

if __name__ == "__main__":
    print("🔧 Fixing GitHub Actions workflow issues...")
    print("=" * 50)
    
    fixes = fix_workflow_issues()
    
    if fixes:
        print("✅ Fixed the following issues:")
        for fix in fixes:
            print(f"  • {fix}")
    else:
        print("✅ No issues found!")
    
    print("\n📁 Current directory structure:")
    os.system("find exports/ results/ logs/ -type d | sort")
    
    print("\n🚀 To run the workflow manually:")
    print("1. Go to GitHub Actions tab")
    print("2. Click 'Run Profit Machine Ultimate'")
    print("3. Select region and click 'Run workflow'")
