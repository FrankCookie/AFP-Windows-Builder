#!/usr/bin/env python3
"""
AFP 运动康复 AI 分析系统 - 简化版
用于快速测试和部署
"""

from flask import Flask, request, jsonify
import os
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
EXE_PATH = Path("/Users/frankcookie/Documents/DataTool/AFP/运动康复AI分析系统_v12.0_集成增强版.exe")

# 创建上传文件夹
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route('/')
def index():
    """主页 - 简单的上传界面"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AFP AI 分析系统</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #090909;
                color: white;
            }
            h1 { color: #5BC8F5; }
            .upload-box {
                border: 2px dashed #5BC8F5;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                margin: 20px 0;
            }
            button {
                background: #5BC8F5;
                color: #090909;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover { background: #8ED4FF; }
            .result { 
                margin-top: 30px; 
                padding: 20px; 
                background: rgba(91, 200, 245, 0.1); 
                border-radius: 8px; 
            }
            .error { 
                margin-top: 30px; 
                padding: 20px; 
                background: rgba(220, 53, 69, 0.1); 
                border: 1px solid #dc3545; 
                border-radius: 8px; 
                color: #dc3545;
            }
        </style>
    </head>
    <body>
        <h1>🏋️ AFP 运动康复 AI 分析系统 v12.0</h1>
        <p>上传视频文件，进行 AI 运动分析</p>
        
        <div class="upload-box">
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="video" accept="video/*" required>
                <br><br>
                <button type="submit">开始分析</button>
            </form>
        </div>
        
        <div id="result"></div>
        
        <script>
            document.getElementById('uploadForm').onsubmit = async (e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const resultDiv = document.getElementById('result');
                
                resultDiv.innerHTML = '<p>⏳ 正在分析视频，请稍候...</p>';
                
                try {
                    const res = await fetch('/analyze', { method: 'POST', body: formData });
                    const data = await res.json();
                    
                    if (data.success) {
                        let html = '<div class="result"><h2>✅ 分析完成</h2>';
                        html += '<pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
                        resultDiv.innerHTML = html;
                    } else {
                        resultDiv.innerHTML = '<div class="error"><h3>❌ 错误</h3><p>' + data.error + '</p></div>';
                    }
                } catch (err) {
                    resultDiv.innerHTML = '<div class="error"><h3>❌ 网络错误</h3><p>' + err.message + '</p></div>';
                }
            };
        </script>
    </body>
    </html>
    """
    return html

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析视频"""
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': '没有上传视频'})
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    # 保存文件
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)
    
    try:
        # 检查 exe 是否存在
        if not EXE_PATH.exists():
            # 模拟结果
            return jsonify({
                'success': True,
                'mode': 'simulation',
                'message': '模拟模式：未找到 .exe 文件',
                'result': {
                    '动作质量': '78/100',
                    '对称性': '0.72',
                    '稳定性': 'B+'
                },
                'advice': [
                    '加强弱侧训练',
                    '提高动作对称性',
                    '改善核心稳定性'
                ]
            })
        
        # TODO: 实际调用 exe
        # 需要根据实际 exe 的接口来调整
        return jsonify({
            'success': True,
            'mode': 'real',
            'message': '请配置 exe 调用参数',
            'note': '请根据 .exe 的实际接口修改 call_ai_system() 函数'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        # 可选：删除上传的文件
        # filepath.unlink(missing_ok=True)
        pass

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'exe_exists': EXE_PATH.exists(),
        'upload_folder': str(UPLOAD_FOLDER)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("AFP 运动康复 AI 分析系统 v12.0")
    print("=" * 60)
    print(f"访问地址: http://127.0.0.1:5000")
    print(f"EXE 路径: {EXE_PATH}")
    print(f"EXE 存在: {EXE_PATH.exists()}")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
