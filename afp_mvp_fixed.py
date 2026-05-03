#!/usr/bin/env python3
"""
AFP MVP - 完整独立版
Applied Functional Physics 智能模拟演示系统
单文件运行版本 - 修复403错误
"""

from flask import Flask, render_template_string, request, redirect, url_for, send_file
import os
import random
import time
from pathlib import Path

# ==================== 配置 ====================
app = Flask(__name__)
app.secret_key = 'afp_mvp_2026'

UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 模拟数据生成 ====================
def generate_simulation_data(age, gender, height, weight):
    """根据客户信息生成个性化模拟数据"""
    random.seed(int(time.time() * 1000) % 1000000 + hash(str(age) + gender + str(height) + str(weight)))
    
    # 年龄影响：20岁=95分，60岁=75分
    if age:
        age_int = int(age)
        base_score = 95 - (age_int - 20) * (20.0 / 40.0)
        base_score = max(75, min(95, base_score))
    else:
        base_score = 85 + random.uniform(-5, 5)
    
    # 性别影响
    if gender == 'male':
        left_right_diff = random.uniform(0.10, 0.15)
    elif gender == 'female':
        left_right_diff = random.uniform(0.15, 0.20)
    else:
        left_right_diff = random.uniform(0.12, 0.18)
    
    # BMI影响
    if height and weight:
        height_m = float(height) / 100.0
        bmi = float(weight) / (height_m * height_m)
        if bmi > 25:
            joint_pressure = f"BMI {bmi:.1f}，关节压力增加"
        elif bmi > 22:
            joint_pressure = f"BMI {bmi:.1f}，关节压力适中"
        else:
            joint_pressure = f"BMI {bmi:.1f}，关节压力正常"
    else:
        joint_pressure = "请输入身高体重"
    
    # 生成评分
    score_symmetry = round(base_score + random.uniform(-5, 5), 1)
    score_force = round(base_score + random.uniform(-8, 3), 1)
    score_coordination = round(base_score + random.uniform(-10, 2), 1)
    
    # 重心偏移数据
    center_offset_data = [
        {"phase": "左单脚支撑", "value": round(random.uniform(-8, -3), 1)},
        {"phase": "右单脚支撑", "value": round(random.uniform(3, 8), 1)},
        {"phase": "双脚支撑", "value": round(random.uniform(-2, 2), 1)},
        {"phase": "左脚蹬伸", "value": round(random.uniform(-6, -2), 1)},
    ]
    
    # 对称性数据
    symmetry_data = [
        {"metric": "左-右地面反作用力比", "left": round(0.45 + random.uniform(-0.05, 0.05), 3), 
         "right": round(0.45 + random.uniform(-0.05, 0.05), 3)},
        {"metric": "左-右力矩生成比", "left": round(0.48 + random.uniform(-0.08, 0.08), 3), 
         "right": round(0.48 + random.uniform(-0.08, 0.08), 3)},
        {"metric": "左-右力链传递效率", "left": round(0.85 + random.uniform(-0.10, 0.10), 3), 
         "right": round(0.85 + random.uniform(-0.10, 0.10), 3)},
    ]
    
    # 力量输出数据
    force_data = [
        {"phase": "支撑期", "force": round(random.uniform(1.2, 2.5), 2), "efficiency": round(random.uniform(0.70, 0.95), 3)},
        {"phase": "腾空期", "force": round(random.uniform(0.3, 0.8), 2), "efficiency": round(random.uniform(0.60, 0.90), 3)},
        {"phase": "落地缓冲", "force": round(random.uniform(2.0, 3.5), 2), "efficiency": round(random.uniform(0.65, 0.88), 3)},
    ]
    
    return {
        'base_score': round(base_score, 1),
        'score_symmetry': score_symmetry,
        'score_force': score_force,
        'score_coordination': score_coordination,
        'joint_pressure': joint_pressure,
        'center_offset_data': center_offset_data,
        'symmetry_data': symmetry_data,
        'force_data': force_data,
    }

# ==================== HTML模板 ====================
INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFP | Applied Functional Physics</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 60px 20px 40px; border-bottom: 1px solid #222; margin-bottom: 40px; }
        .header h1 { font-size: 48px; font-weight: 700; color: #ffffff; letter-spacing: 2px; margin-bottom: 10px; }
        .header .subtitle { font-size: 18px; color: #888; margin-bottom: 30px; }
        .header .description { max-width: 800px; margin: 0 auto; text-align: left; background: #111; padding: 30px; border-radius: 8px; border: 1px solid #222; }
        .header .description h3 { color: #4CAF50; margin-bottom: 15px; font-size: 20px; }
        .header .description p { margin-bottom: 15px; color: #ccc; }
        .core-actions { display: flex; justify-content: center; gap: 30px; margin-top: 20px; font-size: 24px; color: #4CAF50; font-weight: 600; }
        .form-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }
        .form-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; }
        .form-card h2 { color: #4CAF50; margin-bottom: 25px; font-size: 24px; border-bottom: 2px solid #222; padding-bottom: 10px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #aaa; font-size: 14px; }
        .form-group input, .form-group select { width: 100%; padding: 12px; background: #0a0a0a; border: 1px solid #333; border-radius: 4px; color: #e0e0e0; font-size: 16px; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #4CAF50; }
        .gender-select { display: flex; gap: 15px; }
        .gender-option { flex: 1; padding: 12px; background: #0a0a0a; border: 2px solid #333; border-radius: 4px; text-align: center; cursor: pointer; transition: all 0.3s; }
        .gender-option:hover { border-color: #4CAF50; }
        .gender-option.selected { border-color: #4CAF50; background: #1a2e1a; }
        .upload-area { border: 2px dashed #333; border-radius: 8px; padding: 60px 20px; text-align: center; cursor: pointer; transition: all 0.3s; }
        .upload-area:hover { border-color: #4CAF50; background: #0f1a0f; }
        .upload-icon { font-size: 48px; margin-bottom: 20px; color: #4CAF50; }
        .upload-text { color: #888; margin-bottom: 10px; }
        .upload-hint { color: #666; font-size: 14px; }
        input[type="file"] { display: none; }
        .submit-btn { display: block; width: 100%; max-width: 400px; margin: 40px auto; padding: 18px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; transition: background 0.3s; }
        .submit-btn:hover { background: #45a049; }
        .submit-btn:disabled { background: #333; cursor: not-allowed; }
        @media (max-width: 768px) { .form-section { grid-template-columns: 1fr; } .header h1 { font-size: 36px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AFP | Applied Functional Physics</h1>
            <div class="subtitle">实用功能性物理 · 第一性功能训练体系</div>
            <div class="description">
                <h3>🧬 AFP理念</h3>
                <p><strong>Applied Functional Physics（实用功能性物理）</strong>是熊异自主研发的一套基于物理定律和人类进化原理的功能训练体系。</p>
                <p><strong>核心原理：</strong></p>
                <ul style="margin-left: 20px; margin-bottom: 15px; color: #ccc;">
                    <li>基于牛顿力学三定律分析人体运动</li>
                    <li>利用地面反作用力（GRF）作为运动起源</li>
                    <li>通过力链传递实现全身协调性</li>
                    <li>遵循人类进化形成的走、跑、跳、投掷四大核心动作模式</li>
                </ul>
                <p><strong>核心动作模式：</strong></p>
                <div class="core-actions"><span>走</span><span>·</span><span>跑</span><span>·</span><span>跳</span><span>·</span><span>投掷</span></div>
                <p style="margin-top: 20px;"><strong>评估重点：</strong></p>
                <ul style="margin-left: 20px; color: #ccc;">
                    <li>动作流畅度（Fluidity）</li>
                    <li>全身协调性（Coordination）</li>
                    <li>动态平衡（Dynamic Balance）</li>
                </ul>
                <p style="margin-top: 15px; padding: 15px; background: #1a1a1a; border-left: 4px solid #4CAF50; border-radius: 4px;">
                    <strong>⚠️ 模拟演示版说明：</strong><br>
                    本系统为MVP模拟演示版本。上传视频后，系统会根据客户信息生成个性化的模拟分析数据。<br>
                    所有数据均为智能模拟生成，用于展示AFP分析系统的界面和功能。
                </p>
            </div>
        </div>
        <form method="POST" action="/upload" enctype="multipart/form-data" id="analysisForm">
            <div class="form-section">
                <div class="form-card">
                    <h2>👤 客户信息</h2>
                    <div class="form-group">
                        <label for="age">年龄（岁）</label>
                        <input type="number" id="age" name="age" min="10" max="100" required>
                    </div>
                    <div class="form-group">
                        <label>性别</label>
                        <div class="gender-select">
                            <div class="gender-option" data-value="male" onclick="selectGender(this)">♂ 男</div>
                            <div class="gender-option" data-value="female" onclick="selectGender(this)">♀ 女</div>
                        </div>
                        <input type="hidden" id="gender" name="gender" required>
                    </div>
                    <div class="form-group">
                        <label for="height">身高（cm）</label>
                        <input type="number" id="height" name="height" min="100" max="250" required>
                    </div>
                    <div class="form-group">
                        <label for="weight">体重（kg）</label>
                        <input type="number" id="weight" name="weight" min="30" max="200" required>
                    </div>
                </div>
                <div class="form-card">
                    <h2>🎬 视频上传</h2>
                    <div class="upload-area" id="uploadArea" onclick="document.getElementById('videoFile').click()">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">点击或拖拽视频文件到此处</div>
                        <div class="upload-hint">支持 mp4, mov, avi, mkv, webm 格式</div>
                    </div>
                    <input type="file" id="videoFile" name="video" accept=".mp4,.mov,.avi,.mkv,.webm" required>
                    <div id="fileInfo" style="margin-top: 20px; padding: 15px; background: #0a0a0a; border-radius: 4px; display: none;">
                        <div style="color: #4CAF50; margin-bottom: 5px;">✓ 已选择文件</div>
                        <div style="color: #888; font-size: 14px;" id="fileName"></div>
                    </div>
                </div>
            </div>
            <button type="submit" class="submit-btn" id="submitBtn">开始分析</button>
        </form>
    </div>
    <script>
        function selectGender(element) {
            document.querySelectorAll('.gender-option').forEach(opt => opt.classList.remove('selected'));
            element.classList.add('selected');
            document.getElementById('gender').value = element.dataset.value;
        }
        document.getElementById('videoFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileName').textContent = file.name + ' (' + (file.size / 1024 / 1024).toFixed(2) + ' MB)';
            }
        });
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', function(e) { e.preventDefault(); this.classList.add('dragover'); });
        uploadArea.addEventListener('dragleave', function(e) { e.preventDefault(); this.classList.remove('dragover'); });
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('videoFile').files = files;
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileName').textContent = files[0].name + ' (' + (files[0].size / 1024 / 1024).toFixed(2) + ' MB)';
            }
        });
        document.getElementById('analysisForm').addEventListener('submit', function(e) {
            const gender = document.getElementById('gender').value;
            if (!gender) { alert('请选择性别'); e.preventDefault(); return; }
            const video = document.getElementById('videoFile').files[0];
            if (!video) { alert('请上传视频文件'); e.preventDefault(); return; }
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').textContent = '分析中...';
        });
    </script>
</body>
</html>"""

REPORT_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFP分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 30px 20px; border-bottom: 1px solid #222; margin-bottom: 30px; }
        .header h1 { font-size: 36px; color: #ffffff; margin-bottom: 10px; }
        .header .badge { display: inline-block; padding: 8px 20px; background: #ff9800; color: #000; border-radius: 20px; font-size: 14px; font-weight: 600; margin-top: 10px; }
        .client-info { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .info-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; text-align: center; }
        .info-card .label { color: #888; font-size: 14px; margin-bottom: 5px; }
        .info-card .value { color: #4CAF50; font-size: 24px; font-weight: 600; }
        .video-section { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; margin-bottom: 30px; text-align: center; }
        .video-section h2 { color: #4CAF50; margin-bottom: 20px; font-size: 20px; }
        video { max-width: 720px; width: 100%; border-radius: 8px; background: #000; }
        .scores { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
        .score-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; text-align: center; }
        .score-card .score-label { color: #888; font-size: 16px; margin-bottom: 10px; }
        .score-card .score-value { font-size: 48px; font-weight: 700; color: #4CAF50; margin-bottom: 5px; }
        .score-card .score-unit { color: #666; font-size: 14px; }
        .charts { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .chart-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; }
        .chart-card h3 { color: #4CAF50; margin-bottom: 20px; font-size: 18px; }
        .chart-container { position: relative; height: 300px; }
        .data-table { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; margin-bottom: 30px; }
        .data-table h3 { color: #4CAF50; margin-bottom: 20px; font-size: 18px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #222; }
        th { color: #888; font-weight: 600; font-size: 14px; }
        td { color: #e0e0e0; }
        .afp-guidance { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; margin-bottom: 30px; }
        .afp-guidance h3 { color: #4CAF50; margin-bottom: 20px; font-size: 20px; }
        .afp-guidance ol { margin-left: 20px; color: #ccc; }
        .afp-guidance li { margin-bottom: 15px; line-height: 1.8; }
        .back-btn { display: block; width: 100%; max-width: 400px; margin: 40px auto; padding: 18px; background: #333; color: #e0e0e0; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; text-align: center; text-decoration: none; }
        .back-btn:hover { background: #444; }
        @media (max-width: 768px) { .client-info, .scores, .charts { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AFP | 智能分析报告</h1>
            <div class="badge">⚠️ 模拟演示版 - 数据仅供展示</div>
        </div>
        <div class="client-info">
            <div class="info-card"><div class="label">年龄</div><div class="value">{{ age }}岁</div></div>
            <div class="info-card"><div class="label">性别</div><div class="value">{{ gender_text }}</div></div>
            <div class="info-card"><div class="label">身高/体重</div><div class="value">{{ height }}cm/{{ weight }}kg</div></div>
            <div class="info-card"><div class="label">关节压力</div><div class="value" style="font-size: 18px;">{{ joint_pressure }}</div></div>
        </div>
        <div class="video-section">
            <h2>🎬 分析视频</h2>
            <video controls preload="metadata">
                <source src="/video/{{ video_filename }}" type="video/mp4">
                您的浏览器不支持视频播放
            </video>
        </div>
        <div class="scores">
            <div class="score-card"><div class="score-label">动作对称性</div><div class="score-value">{{ scores.symmetry }}</div><div class="score-unit">/ 100</div></div>
            <div class="score-card"><div class="score-label">力量输出</div><div class="score-value">{{ scores.force }}</div><div class="score-unit">/ 100</div></div>
            <div class="score-card"><div class="score-label">全身协调性</div><div class="score-value">{{ scores.coordination }}</div><div class="score-unit">/ 100</div></div>
        </div>
        <div class="charts">
            <div class="chart-card"><h3>📊 能力雷达图</h3><div class="chart-container"><canvas id="radarChart"></canvas></div></div>
            <div class="chart-card"><h3>📈 重心偏移分析</h3><div class="chart-container"><canvas id="offsetChart"></canvas></div></div>
        </div>
        <div class="data-table"><h3>📐 动作对称性明细</h3><table><thead><tr><th>指标</th><th>左侧</th><th>右侧</th></tr></thead><tbody>{% for item in symmetry_data %}<tr><td>{{ item.metric }}</td><td>{{ "%.3f"|format(item.left) }}</td><td>{{ "%.3f"|format(item.right) }}</td></tr>{% endfor %}</tbody></table></div>
        <div class="data-table"><h3>💪 力量输出明细</h3><table><thead><tr><th>阶段</th><th>地面反作用力 (BW)</th><th>传递效率</th></tr></thead><tbody>{% for item in force_data %}<tr><td>{{ item.phase }}</td><td>{{ "%.2f"|format(item.force) }}</td><td>{{ "%.3f"|format(item.efficiency) }}</td></tr>{% endfor %}</tbody></table></div>
        <div class="afp-guidance">
            <h3>📐 AFP动态指导方向（物理版）</h3>
            <ol>
                <li><strong>强化力链传递效率</strong>：通过走跑跳投掷动作，提升全身力矩传递连续性，减少能量损耗</li>
                <li><strong>优化左右负载分布</strong>：通过拓扑模型调整左右侧地面反作用力平衡，重建动态力平衡</li>
                <li><strong>提升躯干枢纽效率</strong>：改善躯干作为力传递枢纽的刚度与柔度匹配，形成自适应优化系统</li>
            </ol>
            <div style="margin-top: 20px; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #4CAF50;">
                <strong>💡 核心理念：</strong>所有训练必须基于全身联动设计，不存在孤立训练。利用走跑跳投掷的进化动作模式，通过物理定律优化人体运动表现。
            </div>
        </div>
        <a href="/" class="back-btn">← 返回首页，分析新视频</a>
    </div>
    <script>
        new Chart(document.getElementById('radarChart').getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['动作对称性', '力量输出', '全身协调性', '动态平衡', '动作流畅度'],
                datasets: [{ label: '评估得分', data: [{{ scores.symmetry }}, {{ scores.force }}, {{ scores.coordination }}, {{ scores.coordination - 5 }}, {{ (scores.symmetry + scores.force + scores.coordination) / 3 }}], backgroundColor: 'rgba(76, 175, 80, 0.2)', borderColor: 'rgba(76, 175, 80, 1)', borderWidth: 2, pointBackgroundColor: 'rgba(76, 175, 80, 1)' }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { r: { beginAtZero: true, max: 100, ticks: { color: '#888', backdropColor: 'transparent' }, grid: { color: '#333' }, angleLines: { color: '#333' }, pointLabels: { color: '#ccc' } } }, plugins: { legend: { display: false } } }
        });
        new Chart(document.getElementById('offsetChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: [{% for item in center_offset_data %}'{{ item.phase }}',{% endfor %}],
                datasets: [{ label: '重心偏移 (cm)', data: [{% for item in center_offset_data %}{{ item.value }},{% endfor %}], backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(255, 206, 86, 0.6)'], borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)'], borderWidth: 1 }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { ticks: { color: '#888' }, grid: { color: '#333' } }, x: { ticks: { color: '#888' }, grid: { color: '#333' } } }, plugins: { legend: { labels: { color: '#ccc' } } } }
        });
    </script>
</body>
</html>"""

# ==================== Flask路由 ====================
@app.route('/')
def index():
    return INDEX_HTML

@app.route('/upload', methods=['POST'])
def upload():
    try:
        age = request.form.get('age', type=int)
        gender = request.form.get('gender')
        height = request.form.get('height', type=int)
        weight = request.form.get('weight', type=int)
        
        if not all([age, gender, height, weight]):
            return "错误：请填写所有客户信息", 400
        
        if 'video' not in request.files:
            return "错误：请上传视频文件", 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return "错误：请选择视频文件", 400
        
        if not allowed_file(video_file.filename):
            return "错误：不支持的文件格式", 400
        
        timestamp = int(time.time())
        video_filename = f"{timestamp}_{video_file.filename}"
        video_path = UPLOAD_FOLDER / video_filename
        video_file.save(video_path)
        
        simulation_data = generate_simulation_data(age, gender, height, weight)
        
        return render_template_string(REPORT_HTML,
            age=age,
            gender_text='男' if gender == 'male' else '女',
            height=height,
            weight=weight,
            joint_pressure=simulation_data['joint_pressure'],
            video_filename=video_filename,
            scores={
                'symmetry': simulation_data['score_symmetry'],
                'force': simulation_data['score_force'],
                'coordination': simulation_data['score_coordination'],
            },
            symmetry_data=simulation_data['symmetry_data'],
            force_data=simulation_data['force_data'],
            center_offset_data=simulation_data['center_offset_data']
        )
    except Exception as e:
        return f"处理失败: {str(e)}", 500

@app.route('/video/<filename>')
def serve_video(filename):
    video_path = UPLOAD_FOLDER / filename
    if not video_path.exists():
        return "Video not found", 404
    return send_file(video_path, mimetype='video/mp4')

# ==================== 主程序 ====================
if __name__ == '__main__':
    print("=" * 60)
    print("AFP MVP - 智能模拟演示系统（修复版）")
    print("=" * 60)
    print(f"📁 工作目录: {Path(__file__).parent}")
    print(f"📁 上传目录: {UPLOAD_FOLDER}")
    print("=" * 60)
    print("🌐 访问地址:")
    print("   http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False)
