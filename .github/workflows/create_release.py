#!/usr/bin/env python3
"""
GitHub Release Creator for AFP Windows EXE
Creates a GitHub release and uploads the EXE file
"""
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

# Get environment variables
github_token = os.environ.get('GITHUB_TOKEN')
github_repo = os.environ.get('GITHUB_REPOSITORY', 'FrankCookie/AFP-Windows-Builder')
run_number = os.environ.get('GITHUB_RUN_NUMBER', '1')

if not github_token:
    print("Error: GITHUB_TOKEN not found")
    sys.exit(1)

version = f"1.0.{run_number}"
tag_name = f"v{version}"
release_name = f"AFP智能分析系统 v{version}"

# Create release
print(f"Creating release: {release_name} (tag: {tag_name})")

create_release_url = f"https://api.github.com/repos/{github_repo}/releases"

release_data = {
    "tag_name": tag_name,
    "name": release_name,
    "body": f"""AFP智能分析报告系统 Windows版本

## 下载与安装
1. 下载 AFP智能分析报告系统_Windows.zip
2. 解压到任意文件夹
3. 双击 AFP智能分析报告系统.exe 即可运行

## 系统要求
- Windows 10/11
- 无需安装Python或其他依赖

## 功能特点
- 智能分析运动员平衡能力
- 支持多种测试模式
- 生成专业分析报告
- 个性化训练建议
""",
    "draft": False,
    "prerelease": False
}

# Create release request
req = urllib.request.Request(
    create_release_url,
    data=json.dumps(release_data).encode('utf-8'),
    headers={
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        release_info = json.loads(response.read().decode('utf-8'))
        upload_url = release_info['upload_url'].replace('{?name,label}', '')
        release_id = release_info['id']
        print(f"Release created successfully! ID: {release_id}")
except urllib.error.HTTPError as e:
    print(f"Error creating release: {e.code} - {e.read().decode('utf-8')}")
    sys.exit(1)

# Upload asset
exe_path = "dist/AFP智能分析报告系统_Windows.zip"
asset_name = "AFP智能分析报告系统_Windows.zip"

print(f"Uploading {asset_name}...")

upload_url = f"{upload_url}?name={urllib.parse.quote(asset_name)}"

with open(exe_path, 'rb') as f:
    exe_data = f.read()

req = urllib.request.Request(
    upload_url,
    data=exe_data,
    headers={
        'Authorization': f'token {github_token}',
        'Content-Type': 'application/zip'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        asset_info = json.loads(response.read().decode('utf-8'))
        print(f"Asset uploaded successfully! URL: {asset_info['browser_download_url']}")
except urllib.error.HTTPError as e:
    print(f"Error uploading asset: {e.code} - {e.read().decode('utf-8')}")
    sys.exit(1)

print("\n✅ Done! Release available at:")
print(f"https://github.com/{github_repo}/releases/tag/{tag_name}")
