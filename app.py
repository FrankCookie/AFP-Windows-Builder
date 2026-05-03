#!/usr/bin/env python3
"""
AFP 运动康复 AI 分析系统集成版 v12.0
集成 Flask Web 应用与运动康复 AI 分析系统
"""

from flask import Flask, request, render_template_string, jsonify, send_file
import subprocess
import os
import json
import time
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULTS_FOLDER = BASE_DIR / "results"
EXE_PATH = Path("/Users/frankcookie/Documents/DataTool/AFP/运动康复AI分析系统_v12.0_集成增强版.exe")

# 创建必要文件夹
UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

# AFP 工业风 HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFP 运动康复 AI 分析系统 v12.0</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #090909;
            color: #FFFFFF;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* 金属网格背景 */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(91, 200, 245, 0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(91, 200, 245, 0.08) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }
        
        .container {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* 顶部发光条 */
        .header-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #5BC8F5, #8ED4FF, #5BC8F5);
            z-index: 1000;
        }
        
        /* 主标题区域 */
        .hero {
            text-align: center;
            padding: 60px 20px 40px;
            border-bottom: 1px solid rgba(91, 200, 245, 0.2);
            margin-bottom: 40px;
        }
        
        .hero h1 {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #5BC8F5, #8ED4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        
        .hero .subtitle {
            font-size: 18px;
            color: #8ED4FF;
            opacity: 0.8;
        }
        
        /* 上传区域 */
        .upload-section {
            background: linear-gradient(135deg, rgba(9, 9, 9, 0.95), rgba(20, 20, 30, 0.95));
            border: 1px solid rgba(91, 200, 245, 0.3);
            border-radius: 8px;
            padding: 40px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .upload-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #5BC8F5, transparent);
        }
        
        .upload-area {
            border: 2px dashed rgba(91, 200, 245, 0.4);
            border-radius: 8px;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .upload-area:hover {
            border-color: #5BC8F5;
            background: rgba(91, 200, 245, 0.05);
        }
        
        .upload-area.drag-over {
            border-color: #5BC8F5;
            background: rgba(91, 200, 245, 0.1);
        }
        
        .upload-icon {
            font-size: 64px;
            margin-bottom: 20px;
            opacity: 0.6;
        }
        
        .upload-text {
            font-size: 18px;
            color: #8ED4FF;
            margin-bottom: 10px;
        }
        
        .upload-hint {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.5);
        }
        
        input[type="file"] {
            display: none;
        }
        
        /* 分析按钮 */
        .analyze-btn {
            background: linear-gradient(135deg, #5BC8F5, #8ED4FF);
            color: #090909;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: 700;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 20px;
            clip-path: polygon(10px 0%, 100% 0%, calc(100% - 10px) 100%, 0% 100%);
            transition: all 0.3s;
        }
        
        .analyze-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(91, 200, 245, 0.4);
        }
        
        .analyze-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* 加载动画 */
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 3px solid rgba(91, 200, 245, 0.2);
            border-top: 3px solid #5BC8F5;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* 结果展示 */
        .result-section {
            display: none;
            background: linear-gradient(135deg, rgba(9, 9, 9, 0.95), rgba(20, 20, 30, 0.95));
            border: 1px solid rgba(91, 200, 245, 0.3);
            border-radius: 8px;
            padding: 40px;
            margin-top: 30px;
        }
        
        .result-section.active {
            display: block;
        }
        
        .result-title {
            font-size: 28px;
            font-weight: 700;
            color: #5BC8F5;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(91, 200, 245, 0.2);
        }
        
        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .result-card {
            background: rgba(91, 200, 245, 0.05);
            border: 1px solid rgba(91, 200, 245, 0.2);
            border-radius: 8px;
            padding: 20px;
        }
        
        .result-card h3 {
            font-size: 14px;
            color: #8ED4FF;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .result-card .value {
            font-size: 32px;
            font-weight: 900;
            color: #5BC8F5;
        }
        
        .result-card .unit {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.6);
            margin-left: 5px;
        }
        
        /* AFP 建议 */
        .afp-advice {
            background: rgba(91, 200, 245, 0.08);
            border-left: 3px solid #5BC8F5;
            padding: 20px;
            margin-top: 30px;
            border-radius: 4px;
        }
        
        .afp-advice h3 {
            font-size: 18px;
            color: #5BC8F5;
            margin-bottom: 15px;
        }
        
        .afp-advice ul {
            list-style: none;
            padding-left: 0;
        }
        
        .afp-advice li {
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .afp-advice li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #5BC8F5;
            font-weight: 700;
        }
        
        /* 错误信息 */
        .error-message {
            background: rgba(220, 53, 69, 0.1);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            color: #dc3545;
        }
        
        /* 底部信息 */
        .footer {
            text-align: center;
            padding: 40px 20px;
            color: rgba(255, 255, 255, 0.4);
            font-size: 14px;
            border-top: 1px solid rgba(91, 200, 245, 0.2);
            margin-top: 60px;
        }
        
        .file-info {
            background: rgba(91, 200, 245, 0.05);
            border: 1px solid rgba(91, 200, 245, 0.2);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            display: none;
        }
        
        .file-info.active {
            display: block;
        }
        
        .file-info p {
            margin: 5px 0;
            color: rgba(255, 255, 255, 0.7);
        }
    </style>
</head>
<body>
    <div class="header-bar"></div>
    
    <div class="container">
        <div class="hero">
            <h1>AFP 运动康复 AI 分析系统</h1>
            <p class="subtitle">实用功能性物理 · 第一性功能训练体系 | v12.0 集成增强版</p>
        </div>
        
        <div class="upload-section">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📹</div>
                <div class="upload-text">拖拽视频文件到此处，或点击上传</div>
                <div class="upload-hint">支持 MP4、MOV、AVI 格式，最大 500MB</div>
                <input type="file" id="fileInput" accept="video/*">
            </div>
            
            <div class="file-info" id="fileInfo">
                <p>已选择文件: <strong id="fileName"></strong></p>
                <p>文件大小: <strong id="fileSize"></strong></p>
            </div>
            
            <div style="text-align: center;">
                <button class="analyze-btn" id="analyzeBtn" disabled>开始 AI 分析</button>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="color: #5BC8F5; font-size: 18px;">AI 正在分析视频中...</p>
            <p style="color: rgba(255, 255, 255, 0.5); margin-top: 10px;">请稍候，正在进行运动康复分析</p>
        </div>
        
        <div class="result-section" id="resultSection">
            <h2 class="result-title">📊 分析结果</h2>
            
            <div class="result-grid" id="resultGrid">
                <!-- 动态填充 -->
            </div>
            
            <div class="afp-advice" id="afpAdvice">
                <!-- 动态填充 -->
            </div>
        </div>
        
        <div class="error-message" id="errorMessage" style="display: none;">
            <!-- 错误信息 -->
        </div>
        
        <div class="footer">
            <p>AFP 训练体系 · 实用功能性物理 · 第一性功能训练</p>
            <p style="margin-top: 10px; opacity: 0.6;">Powered by AI Analysis System v12.0</p>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const loading = document.getElementById('loading');
        const resultSection = document.getElementById('resultSection');
        const resultGrid = document.getElementById('resultGrid');
        const afpAdvice = document.getElementById('afpAdvice');
        const errorMessage = document.getElementById('errorMessage');
        
        let selectedFile = null;
        
        // 点击上传区域
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // 文件选择
        fileInput.addEventListener('change', (e) => {
            handleFile(e.target.files[0]);
        });
        
        // 拖拽上传
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            handleFile(e.dataTransfer.files[0]);
        });
        
        function handleFile(file) {
            if (!file) return;
            
            const validTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo'];
            if (!validTypes.includes(file.type) && !file.name.match(/\.(mp4|mov|avi)$/i)) {
                showError('请上传视频文件（MP4、MOV、AVI 格式）');
                return;
            }
            
            if (file.size > 500 * 1024 * 1024) {
                showError('文件大小不能超过 500MB');
                return;
            }
            
            selectedFile = file;
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.classList.add('active');
            analyzeBtn.disabled = false;
            
            hideError();
            resultSection.classList.remove('active');
        }
        
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
            if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
            return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
        }
        
        // 开始分析
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('video', selectedFile);
            
            loading.classList.add('active');
            resultSection.classList.remove('active');
            hideError();
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                loading.classList.remove('active');
                
                if (result.success) {
                    displayResult(result);
                } else {
                    showError(result.error || '分析失败，请重试');
                }
            } catch (error) {
                loading.classList.remove('active');
                showError('网络错误: ' + error.message);
            }
        });
        
        function displayResult(result) {
            resultGrid.innerHTML = '';
            
            // 填充结果卡片
            if (result.data) {
                Object.entries(result.data).forEach(([key, value]) => {
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.innerHTML = `
                        <h3>${key}</h3>
                        <span class="value">${value}</span>
                    `;
                    resultGrid.appendChild(card);
                });
            }
            
            // AFP 建议
            if (result.advice) {
                afpAdvice.innerHTML = `
                    <h3>💡 AFP 训练建议</h3>
                    <ul>
                        ${result.advice.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                `;
            }
            
            resultSection.classList.add('active');
        }
        
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        }
        
        function hideError() {
            errorMessage.style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析视频"""
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': '没有上传视频'})
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'})
    
    # 保存上传的文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)
    
    try:
        # 调用 AI 分析系统
        result = call_ai_system(filepath)
        
        return jsonify({
            'success': True,
            'data': result.get('data', {}),
            'advice': result.get('advice', []),
            'raw_output': result.get('raw', '')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    finally:
        # 清理上传的文件（可选）
        # filepath.unlink(missing_ok=True)
        pass

def call_ai_system(video_path):
    """
    调用运动康复 AI 分析系统
    根据实际 .exe 文件的接口调整此函数
    """
    if not EXE_PATH.exists():
        # 模拟结果（用于测试）
        return generate_mock_result(video_path)
    
    try:
        # 方法1: 直接调用（如果 exe 支持命令行参数）
        # result = subprocess.run(
        #     [str(EXE_PATH), str(video_path)],
        #     capture_output=True,
        #     text=True,
        #     timeout=300
        # )
        
        # 方法2: 通过 Wine 调用（macOS/Linux）
        result = subprocess.run(
            ['wine', str(EXE_PATH), str(video_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 解析输出
        output = result.stdout or result.stderr or ""
        
        # TODO: 根据实际输出格式解析
        # 这里假设输出是 JSON 格式
        try:
            data = json.loads(output)
            return data
        except:
            # 如果不是 JSON，返回原始输出
            return {
                'data': {
                    '分析结果': '已完成',
                    '输出': output[:500]
                },
                'advice': [
                    '建议根据分析结果调整训练计划',
                    '重点关注动作模式的对称性',
                    '加强弱侧肌群的功能性训练'
                ],
                'raw': output
            }
        
    except subprocess.TimeoutExpired:
        raise Exception('分析超时（>5分钟），请检查视频长度或分辨率')
    except FileNotFoundError as e:
        if 'wine' in str(e):
            raise Exception('Wine 未安装，请先安装: brew install --cask wine')
        raise Exception(f'无法执行分析程序: {e}')
    except Exception as e:
        raise Exception(f'调用 AI 分析系统失败: {e}')

def generate_mock_result(video_path):
    """生成模拟结果（用于测试）"""
    return {
        'data': {
            '动作质量评分': '78/100',
            '对称性指数': '0.72',
            '稳定性评级': 'B+',
            '功能动作模式': '3/5'
        },
        'advice': [
            '右侧髋关节稳定性需加强，建议增加单腿支撑训练',
            '上肢对称性良好，可维持当前训练强度',
            '核心控制能力中等，建议加入动态稳定性训练',
            '整体功能动作模式有提升空间，建议系统性训练'
        ],
        'raw': '模拟分析结果（实际部署时请安装 Wine 并放置 .exe 文件）'
    }

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'exe_exists': EXE_PATH.exists(),
        'wine_available': check_wine()
    })

def check_wine():
    """检查 Wine 是否可用"""
    try:
        result = subprocess.run(['which', 'wine'], capture_output=True)
        return result.returncode == 0
    except:
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("AFP 运动康复 AI 分析系统 v12.0")
    print("=" * 60)
    print(f"工作目录: {BASE_DIR}")
    print(f"EXE 路径: {EXE_PATH}")
    print(f"EXE 存在: {EXE_PATH.exists()}")
    print(f"Wine 可用: {check_wine()}")
    print("=" * 60)
    print("访问地址:")
    print("  📱 本地: http://127.0.0.1:5000")
    print("  🌐 局域网: http://" + get_local_ip() + ":5000")
    print("=" * 60)
    print("提示:")
    if not EXE_PATH.exists():
        print(f"  ⚠️  请将 .exe 文件放到: {EXE_PATH}")
    if not check_wine():
        print("  ⚠️  macOS 用户请安装 Wine: brew install --cask wine")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

def get_local_ip():
    """获取局域网 IP"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"
