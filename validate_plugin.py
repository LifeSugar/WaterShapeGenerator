#!/usr/bin/env python3
"""
插件验证脚本
用于验证插件结构和配置的正确性
"""

import sys
import re
from pathlib import Path

def validate_manifest():
    """验证 manifest 文件"""
    manifest_path = Path(__file__).parent / "blender_manifest.toml"
    
    if not manifest_path.exists():
        print("❌ 错误：找不到 blender_manifest.toml")
        return False
    
    try:
        content = manifest_path.read_text(encoding='utf-8')
        print("✅ manifest 文件存在")
        
        # 检查必需字段
        required_fields = {
            'schema_version': r'schema_version\s*=\s*"([^"]+)"',
            'id': r'id\s*=\s*"([^"]+)"',
            'version': r'version\s*=\s*"([^"]+)"',
            'name': r'name\s*=\s*"([^"]+)"',
            'maintainer': r'maintainer\s*=\s*"([^"]+)"',
            'type': r'type\s*=\s*"([^"]+)"'
        }
        
        for field, pattern in required_fields.items():
            match = re.search(pattern, content)
            if match:
                print(f"✅ {field}: {match.group(1)}")
            else:
                print(f"❌ 缺少必需字段: {field}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ manifest 文件读取错误: {e}")
        return False

def validate_structure():
    """验证文件结构"""
    base_path = Path(__file__).parent
    
    required_files = [
        "__init__.py",
        "blender_manifest.toml",
        "includes/__init__.py",
        "includes/operators.py",
        "includes/panels.py",
        "includes/properties.py",
    ]
    
    required_dirs = [
        "includes",
        "assets",
    ]
    
    print("\n检查文件结构:")
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ 缺少目录: {dir_path}/")
            return False
    
    return True

def validate_python_syntax():
    """验证 Python 语法"""
    import py_compile
    import tempfile
    
    base_path = Path(__file__).parent
    python_files = [
        "__init__.py",
        "includes/__init__.py",
        "includes/operators.py",
        "includes/panels.py",
        "includes/properties.py",
        "includes/resource.py",
        "includes/method.py",
        "includes/cn.py",
    ]
    
    print("\n检查 Python 语法:")
    
    for file_path in python_files:
        full_path = base_path / file_path
        if full_path.exists():
            try:
                with tempfile.NamedTemporaryFile(suffix='.pyc', delete=True) as tmp:
                    py_compile.compile(str(full_path), tmp.name, doraise=True)
                print(f"✅ {file_path}")
            except py_compile.PyCompileError as e:
                print(f"❌ {file_path}: {e}")
                return False
        else:
            print(f"⚠️  跳过不存在的文件: {file_path}")
    
    return True

def main():
    print("🔍 开始验证插件...")
    
    success = True
    
    # 验证 manifest
    if not validate_manifest():
        success = False
    
    # 验证文件结构
    if not validate_structure():
        success = False
    
    # 验证 Python 语法
    if not validate_python_syntax():
        success = False
    
    print("\n" + "="*50)
    if success:
        print("🎉 所有验证通过！插件可以打包发布。")
        return 0
    else:
        print("❌ 验证失败，请修复上述问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
