#!/usr/bin/env python3
"""
版本管理工具
用于更新 blender_manifest.toml 中的版本号并创建 Git 标签
"""

import re
import sys
import subprocess
from pathlib import Path

def read_manifest():
    """读取 manifest 文件"""
    manifest_path = Path(__file__).parent / "blender_manifest.toml"
    if not manifest_path.exists():
        print("错误：找不到 blender_manifest.toml 文件")
        sys.exit(1)
    
    return manifest_path.read_text(encoding='utf-8')

def write_manifest(content):
    """写入 manifest 文件"""
    manifest_path = Path(__file__).parent / "blender_manifest.toml"
    manifest_path.write_text(content, encoding='utf-8')

def get_current_version():
    """获取当前版本号"""
    content = read_manifest()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None

def update_version(new_version):
    """更新版本号"""
    content = read_manifest()
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    write_manifest(updated_content)
    print(f"版本号已更新为 {new_version}")

def create_git_tag(version):
    """创建 Git 标签"""
    try:
        # 添加文件到 Git
        subprocess.run(['git', 'add', 'blender_manifest.toml'], check=True)
        subprocess.run(['git', 'commit', '-m', f'版本更新至 {version}'], check=True)
        
        # 创建标签
        subprocess.run(['git', 'tag', f'v{version}'], check=True)
        print(f"Git 标签 v{version} 已创建")
        
        # 推送到远程仓库
        response = input("是否推送到远程仓库？(y/N): ")
        if response.lower() == 'y':
            subprocess.run(['git', 'push'], check=True)
            subprocess.run(['git', 'push', '--tags'], check=True)
            print("已推送到远程仓库")
            
    except subprocess.CalledProcessError as e:
        print(f"Git 操作失败: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("用法: python update_version.py <new_version>")
        print("例如: python update_version.py 1.0.1")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # 验证版本号格式
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("错误：版本号格式应为 x.y.z（例如 1.0.1）")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"当前版本: {current_version}")
    print(f"新版本: {new_version}")
    
    # 确认更新
    response = input("确认更新版本号？(y/N): ")
    if response.lower() != 'y':
        print("取消更新")
        sys.exit(0)
    
    # 更新版本号
    update_version(new_version)
    
    # 创建 Git 标签
    response = input("是否创建 Git 标签并提交？(y/N): ")
    if response.lower() == 'y':
        create_git_tag(new_version)
    
    print("完成！")

if __name__ == "__main__":
    main()
