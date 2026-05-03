#!/usr/bin/env python3
"""
AFP 智能模拟演示系统 v1.0
单文件版本 - 深色专业风格
适配 13.6寸 MacBook Air (2560×1664)
"""

from flask import Flask, render_template_string, request, send_file
import random
import time
import json
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'mov', 'avi', 'mkv', 'webm'}

def generate_personalized_data(age, gender, height, weight):
    """根据客户信息生成个性化模拟数据"""
    random.seed(int(time.time() * 1000) % 1000000 + hash(str(age) + gender + str(height)))
    
    # 年龄影响：年龄越小分数越高
    if age <= 25:
        base_score = random.uniform(88, 95)
    elif age <= 35:
        base_score = random.uniform(82, 90)
    elif age <= 45:
        base_score = random.uniform(75, 85)
    else:
        base_score = random.uniform(68, 80)
    
    # BMI计算
    bmi = weight / ((height / 100) ** 2)
    
    # BMI影响：BMI越高，压力提示越多
    if bmi < 18.5:
        weight_status = "偏轻"
        pressure_tip = "体重偏轻，注意肌肉量不足，可能影响力量传导"
    elif bmi < 24:
        weight_status = "正常"
        pressure_tip = "体重正常，力传导效率较好"
    elif bmi < 28:
        weight_status = "偏重"
        pressure_tip = "体重偏重，关节压力较大，建议先减重再强化训练"
    else:
        weight_status = "肥胖"
        pressure_tip = "体重超标，关节负担重，优先进行低冲击的功能训练"
    
    # 性别影响
    if gender == 'male':
        force_base = random.uniform(2.5, 3.5)
        symmetry_base = random.uniform(0.70, 0.85)
    else:
        force_base = random.uniform(2.0, 3.0)
        symmetry_base = random.uniform(0.65, 0.80)
    
    # 重心偏移（年龄越大，偏移越大）
    offset_range = random.uniform(3, 5) if age < 30 else random.uniform(5, 10)
    center_offset = [
        round(random.uniform(-offset_range, -offset_range * 0.5), 1),
        round(random.uniform(-offset_range * 0.5, 0), 1),
        round(random.uniform(0, offset_range * 0.5), 1),
        round(random.uniform(offset_range * 0.5, offset_range), 1),
    ]
    
    # 对称性数据
    sym_left = [round(symmetry_base + random.uniform(-0.1, 0.05), 3) for _ in range(3)]
    sym_right = [round(symmetry_base + random.uniform(-0.05, 0.1), 3) for _ in range(3)]
    
    # 地面反作用力（GRF）波形数据
    phase_labels = ['支撑前期', '支撑早期', '支撑中期', '支撑后期', '蹬伸期', '离地期']
    grf_left_wave = [round(0.5 + random.uniform(-0.1, 0.1) + i * 0.3, 2) for i in range(6)]
    grf_right_wave = [round(0.5 + random.uniform(-0.1, 0.1) + i * 0.3, 2) for i in range(6)]
    
    # 效率波形
    eff_wave = [round(0.6 + random.uniform(-0.05, 0.08) + i * 0.02, 3) for i in range(6)]
    
    # 逐帧GRF数据
    grf_left_frames = [round(random.uniform(0.8, 1.3), 3) for _ in range(10)]
    grf_right_frames = [round(random.uniform(0.75, 1.25), 3) for _ in range(10)]
    torque_left_frames = [round(random.uniform(0.4, 1.0), 3) for _ in range(10)]
    torque_right_frames = [round(random.uniform(0.35, 0.95), 3) for _ in range(10)]
    
    # 判断差异
    grf_diff = abs(sum(grf_left_frames) / len(grf_left_frames) - sum(grf_right_frames) / len(grf_right_frames))
    grf_diff_pct = round(grf_diff * 100, 1)
    
    sym_diff = sum(abs(sym_left[i] - sym_right[i]) for i in range(3)) / 3 * 100
    
    # 评分
    score_symmetry = round(base_score + random.uniform(-8, 3), 1)
    score_force = round(base_score + random.uniform(-10, 2), 1)
    score_coordination = round(base_score + random.uniform(-12, 1), 1)
    
    # 指导方向（根据数据个性化）
    guidance = []
    if grf_diff_pct > 10:
        guidance.append("⚠️ 左右GRF差异超过10%，建议进行对称性训练，重点改善弱侧发力")
    if sym_diff > 10:
        guidance.append("⚠️ 左右对称性差异较大，推荐走跑跳投掷联动练习，减少强弱侧差异")
    if offset_range > 6:
        guidance.append("⚠️ 重心偏移较大，建议加强核心稳定性训练，改善动态平衡")
    if bmi >= 24:
        guidance.append(f"⚠️ BMI={bmi:.1f}（{weight_status}），关节压力较大，建议低冲击训练")
    if not guidance:
        guidance.append("✅ 各项指标良好，继续保持当前训练节奏，可逐步增加训练强度")
    
    guidance.append("💡 训练重点：走·跑·跳·投掷 四个基础动作模式，每周3-4次")
    
    data = {
        'bmi': round(bmi, 1),
        'weight_status': weight_status,
        'pressure_tip': pressure_tip,
        'base_score': round(base_score, 1),
        'score_symmetry': score_symmetry,
        'score_force': score_force,
        'score_coordination': score_coordination,
        'center_offset': center_offset,
        'offset_range': round(offset_range, 1),
        'sym_left': sym_left,
        'sym_right': sym_right,
        'sym_diff': round(sym_diff, 1),
        'grf_left_wave': grf_left_wave,
        'grf_right_wave': grf_right_wave,
        'eff_wave': eff_wave,
        'phase_labels': phase_labels,
        'grf_left_frames': grf_left_frames,
        'grf_right_frames': grf_right_frames,
        'torque_left_frames': torque_left_frames,
        'torque_right_frames': torque_right_frames,
        'grf_diff_pct': grf_diff_pct,
        'guidance': guidance,
    }
    
    return data

# ==================== 首页模板 ====================
INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFP | Applied Functional Physics - 智能分析报告系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            background: #0a0a0a; 
            color: #e0e0e0; 
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
        
        /* 头部 */
        .header { text-align: center; margin-bottom: 40px; padding-bottom: 30px; border-bottom: 1px solid #222; }
        .header h1 { font-size: 42px; color: #fff; margin-bottom: 8px; letter-spacing: 2px; }
        .header .subtitle { color: #888; font-size: 16px; margin-bottom: 15px; }
        .demo-badge { display: inline-block; padding: 6px 18px; background: #ff9800; color: #000; border-radius: 20px; font-size: 13px; font-weight: 600; }
        
        /* AFP 核心理念 */
        .afp-concept { 
            max-width: 900px; 
            margin: 0 auto 40px; 
            background: #111; 
            padding: 30px; 
            border-radius: 10px; 
            border-left: 4px solid #4CAF50;
        }
        .afp-concept h2 { color: #4CAF50; margin-bottom: 15px; font-size: 22px; }
        .afp-concept p { color: #ccc; margin-bottom: 12px; line-height: 1.8; }
        .afp-concept .highlight { color: #4CAF50; font-weight: 600; }
        
        /* 对比表格 */
        .comparison-section { margin-bottom: 40px; }
        .comparison-section h2 { color: #4CAF50; text-align: center; margin-bottom: 20px; font-size: 20px; }
        .comparison-table { 
            width: 100%; 
            max-width: 1000px; 
            margin: 0 auto; 
            border-collapse: collapse; 
            background: #111;
            border-radius: 8px;
            overflow: hidden;
        }
        .comparison-table th { 
            padding: 16px; 
            text-align: center; 
            font-size: 16px; 
            background: #1a1a1a;
        }
        .comparison-table th:first-child { text-align: left; color: #888; }
        .comparison-table td { 
            padding: 14px 16px; 
            color: #ccc; 
            font-size: 14px; 
            border-top: 1px solid #222;
            vertical-align: top;
        }
        .comparison-table tr:hover { background: #1a1a1a; }
        .th-negative { color: #ff5252; }
        .th-positive { color: #4CAF50; }
        
        /* 表单区域 */
        .form-section { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 30px; 
            margin-bottom: 30px;
        }
        .card { 
            background: #111; 
            border: 1px solid #222; 
            border-radius: 10px; 
            padding: 30px; 
        }
        .card h3 { color: #4CAF50; margin-bottom: 20px; font-size: 18px; }
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; margin-bottom: 8px; color: #aaa; font-size: 14px; }
        .form-group input, .form-group select { 
            width: 100%; 
            padding: 12px 14px; 
            background: #0a0a0a; 
            border: 1px solid #333; 
            border-radius: 6px; 
            color: #e0e0e0; 
            font-size: 15px; 
        }
        .form-group input:focus, .form-group select:focus { 
            outline: none; 
            border-color: #4CAF50; 
        }
        .gender-select { display: flex; gap: 12px; }
        .gender-btn { 
            flex: 1; 
            padding: 12px; 
            background: #0a0a0a; 
            border: 2px solid #333; 
            border-radius: 6px; 
            text-align: center; 
            cursor: pointer; 
            color: #e0e0e0; 
            font-size: 15px;
            transition: all 0.2s;
        }
        .gender-btn:hover { border-color: #4CAF50; }
        .gender-btn.selected { border-color: #4CAF50; background: #1a2e1a; color: #4CAF50; }
        
        /* 上传区域 */
        .upload-area { 
            border: 2px dashed #333; 
            border-radius: 10px; 
            padding: 50px 20px; 
            text-align: center; 
            cursor: pointer; 
            transition: all 0.3s;
        }
        .upload-area:hover { border-color: #4CAF50; background: #111; }
        .upload-area .icon { font-size: 48px; margin-bottom: 15px; }
        .upload-area .text { color: #aaa; margin-bottom: 8px; }
        .upload-area .hint { color: #666; font-size: 13px; }
        #fileInfo { margin-top: 15px; color: #4CAF50; font-size: 14px; display: none; }
        
        /* 提交按钮 */
        .submit-btn { 
            display: block; 
            width: 100%; 
            max-width: 400px; 
            margin: 0 auto; 
            padding: 16px; 
            background: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            font-size: 18px; 
            font-weight: 600;
            cursor: pointer; 
            transition: background 0.2s;
        }
        .submit-btn:hover { background: #45a049; }
        .submit-btn:disabled { background: #333; cursor: not-allowed; }
        
        /* 底部 */
        .footer { 
            text-align: center; 
            margin-top: 50px; 
            padding-top: 30px; 
            border-top: 1px solid #222; 
            color: #555; 
            font-size: 13px; 
        }
        
        @media (max-width: 768px) {
            .form-section { grid-template-columns: 1fr; }
            .header h1 { font-size: 32px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>AFP</h1>
            <div class="subtitle">Applied Functional Physics · 功能物理学</div>
            <div class="demo-badge">⚡ 模拟演示版</div>
        </div>
        
        <!-- AFP 核心理念 -->
        <div class="afp-concept">
            <h2>💡 AFP 核心理念</h2>
            <p>AFP（<span class="highlight">Applied Functional Physics</span>）是一种基于功能物理学原理的训练体系，通过分析人体在自然动作中的力传导效率，找出不平衡点并进行针对性改善。</p>
            <p><strong>核心原理：</strong>人体的每一个动作都是一条<span class="highlight">力传导链</span>——从脚底接触地面，经过脚踝、膝盖、髋关节、脊柱，最终传递到手或头顶。这条链条上任何一个环节出问题，都会让整个动作变得低效，甚至导致慢性疼痛。</p>
            <p><strong>训练方法：</strong>使用<span class="highlight">走、跑、跳、投掷</span>这四种人类最基础的动作模式进行训练，让身体在自然动作中自我优化，形成良性循环。</p>
        </div>
        
        <!-- 传统 vs AFP 对比 -->
        <div class="comparison-section">
            <h2>⚡ 传统训练 vs AFP功能训练</h2>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th></th>
                        <th class="th-negative">❌ 传统方法</th>
                        <th class="th-positive">✅ AFP方法</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>解决问题的方式</strong></td>
                        <td>哪里痛就治哪里（头痛医头，脚痛医脚）</td>
                        <td>平衡强弱侧，像天平一样把压力平均分担</td>
                    </tr>
                    <tr>
                        <td><strong>训练方式</strong></td>
                        <td>只练单个肌肉（孤立训练，比如只练股四头肌）</td>
                        <td>全身联动，让身体各部位一起配合发力</td>
                    </tr>
                    <tr>
                        <td><strong>动作设计</strong></td>
                        <td>使用固定模板和静态动作（照标准姿势做）</td>
                        <td>使用走、跑、跳、投掷这些自然功能动作</td>
                    </tr>
                    <tr>
                        <td><strong>评估重点</strong></td>
                        <td>只看力量大小、围度数据（表面数字）</td>
                        <td>重点看动作流畅度、协调性、力传导效率</td>
                    </tr>
                    <tr>
                        <td><strong>效果持续性</strong></td>
                        <td>短期缓解，容易反复（停训后问题回来）</td>
                        <td>长期自我优化，持续进步（身体自己学会更好工作）</td>
                    </tr>
                    <tr>
                        <td><strong>依赖程度</strong></td>
                        <td>被动治疗，依赖外部干预（医生、器械）</td>
                        <td>主动训练，让身体形成自我优化系统</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 表单 -->
        <form method="POST" action="/upload" enctype="multipart/form-data" id="analysisForm">
            <div class="form-section">
                <!-- 客户信息 -->
                <div class="card">
                    <h3>👤 客户信息</h3>
                    <div class="form-group">
                        <label>姓名</label>
                        <input type="text" name="name" placeholder="请输入客户姓名" required>
                    </div>
                    <div class="form-group">
                        <label>年龄（岁）</label>
                        <input type="number" name="age" min="10" max="100" placeholder="如：35" required>
                    </div>
                    <div class="form-group">
                        <label>性别</label>
                        <div class="gender-select">
                            <div class="gender-btn" onclick="selectGender(this, 'male')">♂ 男</div>
                            <div class="gender-btn" onclick="selectGender(this, 'female')">♀ 女</div>
                        </div>
                        <input type="hidden" name="gender" id="gender" required>
                    </div>
                    <div class="form-group">
                        <label>身高（cm）</label>
                        <input type="number" name="height" min="100" max="250" placeholder="如：175" required>
                    </div>
                    <div class="form-group">
                        <label>体重（kg）</label>
                        <input type="number" name="weight" min="30" max="200" placeholder="如：70" required>
                    </div>
                </div>
                
                <!-- 视频上传 -->
                <div class="card">
                    <h3>🎬 动作视频上传</h3>
                    <div class="upload-area" id="uploadArea" onclick="document.getElementById('videoFile').click()">
                        <div class="icon">📁</div>
                        <div class="text">点击或拖拽视频到此处</div>
                        <div class="hint">支持 mp4, mov, avi, mkv</div>
                    </div>
                    <input type="file" id="videoFile" name="video" accept=".mp4,.mov,.avi,.mkv" required style="display:none;">
                    <div id="fileInfo">✅ 已选择文件：<span id="fileName"></span></div>
                </div>
            </div>
            
            <button type="submit" class="submit-btn" id="submitBtn">开始分析</button>
        </form>
        
        <!-- 底部 -->
        <div class="footer">
            AFP 智能分析报告系统 v1.0 · 模拟演示版 · 仅供展示使用
        </div>
    </div>
    
    <script>
        function selectGender(el, val) {
            document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('gender').value = val;
        }
        
        document.getElementById('videoFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileName').textContent = file.name;
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('uploadArea').style.borderColor = '#4CAF50';
            }
        });
        
        // 拖拽上传
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#4CAF50';
        });
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#333';
        });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#333';
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('video/')) {
                document.getElementById('videoFile').files = e.dataTransfer.files;
                document.getElementById('fileName').textContent = file.name;
                document.getElementById('fileInfo').style.display = 'block';
            }
        });
    </script>
</body>
</html>"""

# ==================== 报告页面模板 ====================
REPORT_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFP 智能分析报告 - {{ name }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            background: #0a0a0a; 
            color: #e0e0e0; 
            line-height: 1.6;
        }
        .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
        
        /* 头部 */
        .report-header { 
            text-align: center; 
            margin-bottom: 30px; 
            padding-bottom: 25px; 
            border-bottom: 1px solid #222; 
        }
        .report-header h1 { font-size: 32px; color: #fff; margin-bottom: 8px; }
        .report-header .demo-badge { 
            display: inline-block; 
            padding: 5px 14px; 
            background: #ff9800; 
            color: #000; 
            border-radius: 16px; 
            font-size: 12px; 
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        /* 客户信息 */
        .client-info { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); 
            gap: 15px; 
            margin-bottom: 30px; 
        }
        .info-card { 
            background: #111; 
            padding: 18px; 
            border-radius: 8px; 
            text-align: center;
            border: 1px solid #222;
        }
        .info-card .label { color: #888; font-size: 12px; margin-bottom: 6px; }
        .info-card .value { color: #fff; font-size: 20px; font-weight: 600; }
        .info-card .value.green { color: #4CAF50; }
        .info-card .value.orange { color: #ff9800; }
        
        /* 视频区域 */
        .video-section { 
            background: #111; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            text-align: center;
        }
        .video-section h3 { color: #4CAF50; margin-bottom: 15px; font-size: 16px; }
        .video-section video { 
            max-width: 720px; 
            width: 100%; 
            border-radius: 8px; 
            background: #000;
        }
        
        /* 数据区块 */
        .data-section { 
            background: #111; 
            padding: 25px; 
            border-radius: 10px; 
            margin-bottom: 25px; 
            border: 1px solid #222;
        }
        .data-section h3 { color: #4CAF50; margin-bottom: 20px; font-size: 17px; }
        .chart-container { position: relative; height: 300px; margin-bottom: 20px; }
        
        /* 表格 */
        .data-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 15px;
        }
        .data-table th { 
            padding: 12px; 
            background: #1a1a1a; 
            color: #888; 
            font-size: 13px; 
            text-align: center;
            border-bottom: 1px solid #333;
        }
        .data-table td { 
            padding: 10px 12px; 
            text-align: center; 
            color: #ccc; 
            font-size: 13px; 
            border-bottom: 1px solid #222;
        }
        .data-table tr:hover { background: #1a1a1a; }
        
        /* 解读卡片 */
        .insight-card { 
            background: #0d1a0d; 
            padding: 18px 20px; 
            border-radius: 8px; 
            border-left: 4px solid #4CAF50;
            margin-top: 20px;
        }
        .insight-card h4 { color: #4CAF50; margin-bottom: 12px; font-size: 15px; }
        .insight-card p { color: #aaa; font-size: 13px; line-height: 1.7; }
        .insight-card ul { color: #aaa; font-size: 13px; line-height: 1.7; margin-left: 20px; }
        
        /* 评分 */
        .scores { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 20px; 
            margin-bottom: 25px; 
        }
        .score-card { 
            background: #111; 
            padding: 25px; 
            border-radius: 10px; 
            text-align: center;
            border: 1px solid #222;
        }
        .score-card .label { color: #888; font-size: 13px; margin-bottom: 8px; }
        .score-card .value { font-size: 42px; font-weight: 700; }
        .score-card .value.green { color: #4CAF50; }
        .score-card .value.orange { color: #ff9800; }
        .score-card .value.red { color: #ff5252; }
        
        /* 指导方向 */
        .guidance { 
            background: #111; 
            padding: 25px; 
            border-radius: 10px; 
            margin-top: 25px;
            border: 1px solid #222;
        }
        .guidance h3 { color: #4CAF50; margin-bottom: 18px; font-size: 17px; }
        .guidance-item { 
            padding: 14px 18px; 
            background: #0a0a0a; 
            border-radius: 8px; 
            margin-bottom: 10px; 
            color: #ccc; 
            font-size: 14px; 
            line-height: 1.6;
            border-left: 3px solid #4CAF50;
        }
        
        /* 底部 */
        .report-footer { 
            text-align: center; 
            margin-top: 40px; 
            padding-top: 25px; 
            border-top: 1px solid #222; 
            color: #555; 
            font-size: 12px; 
        }
        
        @media (max-width: 768px) {
            .scores { grid-template-columns: 1fr; }
            .client-info { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="report-header">
            <div class="demo-badge">⚡ 模拟演示版</div>
            <h1>AFP：智能分析报告</h1>
            <p style="color: #888; margin-top: 10px;">报告生成时间：{{ timestamp }}</p>
        </div>
        
        <!-- 客户信息 -->
        <div class="client-info">
            <div class="info-card">
                <div class="label">姓名</div>
                <div class="value">{{ name }}</div>
            </div>
            <div class="info-card">
                <div class="label">年龄</div>
                <div class="value">{{ age }} 岁</div>
            </div>
            <div class="info-card">
                <div class="label">性别</div>
                <div class="value">{{ '男' if gender == 'male' else '女' }}</div>
            </div>
            <div class="info-card">
                <div class="label">身高 / 体重</div>
                <div class="value" style="font-size: 16px;">{{ height }}cm / {{ weight }}kg</div>
            </div>
            <div class="info-card">
                <div class="label">BMI</div>
                <div class="value {{ bmi_color }}">{{ bmi }}</div>
            </div>
            <div class="info-card">
                <div class="label">体重状态</div>
                <div class="value" style="font-size: 14px;">{{ weight_status }}</div>
            </div>
        </div>
        
        <!-- BMI提示 -->
        <div class="insight-card" style="border-left-color: {{ bmi_tip_color }};">
            <h4>📋 体重与关节压力评估</h4>
            <p>{{ pressure_tip }}</p>
        </div>
        
        <!-- 视频播放 -->
        <div class="video-section">
            <h3>🎬 动作分析视频</h3>
            <video controls>
                <source src="{{ video_url }}" type="video/mp4">
                您的浏览器不支持视频播放
            </video>
        </div>
        
        <!-- 重心偏移数据 -->
        <div class="data-section">
            <h3>⚖️ 重心偏移数据</h3>
            <div class="chart-container">
                <canvas id="offsetChart"></canvas>
            </div>
            <div class="insight-card">
                <h4>📌 重心偏移解读</h4>
                <p style="margin-bottom: 10px;">重心偏移反映动作过程中身体重心的左右分布情况：</p>
                <ul style="margin-bottom: 10px;">
                    <li>负值（向左偏移）：重心偏向左脚</li>
                    <li>正值（向右偏移）：重心偏向右脚</li>
                </ul>
                <p><strong>衡量标准：</strong>数值越接近0，说明左右平衡越好。当前重心偏移范围为 {{ offset_min }}～{{ offset_max }}，{{ offset_assessment }}。</p>
            </div>
        </div>
        
        <!-- 对称性数据 -->
        <div class="data-section">
            <h3>🔄 左右对称性数据</h3>
            <div class="chart-container">
                <canvas id="symmetryChart"></canvas>
            </div>
            <div class="insight-card">
                <h4>📌 对称性解读</h4>
                <p style="margin-bottom: 10px;">对称性反映身体左右两侧在动作中的发力均衡程度：</p>
                <ul style="margin-bottom: 10px;">
                    <li>地面反作用力：左右脚踩地力量的对比</li>
                    <li>力矩生成：左右侧发力大小的对比</li>
                    <li>力链传递：左右侧力量传导效率的对比</li>
                </ul>
                <p>当前左右差异为 <strong style="color: {{ sym_color }};">{{ sym_diff }}%</strong>，{{ sym_assessment }}。</p>
            </div>
        </div>
        
        <!-- 逐帧GRF数据 -->
        <div class="data-section">
            <h3>📊 逐帧地面反作用力（GRF）数据</h3>
            <div style="overflow-x: auto;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>帧号</th>
                            <th>左脚 GRF (BW)</th>
                            <th>右脚 GRF (BW)</th>
                            <th>左脚力矩</th>
                            <th>右脚力矩</th>
                        </tr>
                    </thead>
                    <tbody>
                        {{ grf_table_rows }}
                    </tbody>
                </table>
            </div>
            <div class="insight-card">
                <h4>📌 GRF数据解读</h4>
                <p style="margin-bottom: 10px;">地面反作用力（GRF）是脚底踩地时地面给身体的反作用力，反映发力大小：</p>
                <ul style="margin-bottom: 10px;">
                    <li>数值越大 → 踩地越用力</li>
                    <li>左右差异大 → 一侧用力多、一侧用力少</li>
                </ul>
                <p>当前左右GRF平均差异为 <strong style="color: {{ grf_diff_color }};">{{ grf_diff_pct }}%</strong>，{{ grf_assessment }}。</p>
            </div>
        </div>
        
        <!-- 周期动态数据 -->
        <div class="data-section">
            <h3>📈 周期动态数据</h3>
            <div class="chart-container">
                <canvas id="phaseChart"></canvas>
            </div>
            <div class="insight-card">
                <h4>📌 周期动态解读</h4>
                <p style="margin-bottom: 10px;">展示一个完整动作周期中，地面反作用力（GRF）和力传导效率的变化：</p>
                <ul style="margin-bottom: 10px;">
                    <li>GRF波形：脚底踩地力量的变化过程</li>
                    <li>效率波形：力量从脚传到上身的效率</li>
                </ul>
                <p>{{ phase_assessment }}</p>
            </div>
        </div>
        
        <!-- 综合评分 -->
        <h2 style="color: #fff; margin-bottom: 20px; font-size: 22px;">📊 综合评估结果</h2>
        <div class="scores">
            <div class="score-card">
                <div class="label">动作对称性</div>
                <div class="value {{ score_sym_color }}">{{ score_symmetry }}</div>
            </div>
            <div class="score-card">
                <div class="label">力量输出</div>
                <div class="value {{ score_force_color }}">{{ score_force }}</div>
            </div>
            <div class="score-card">
                <div class="label">全身协调性</div>
                <div class="value {{ score_coord_color }}">{{ score_coordination }}</div>
            </div>
        </div>
        
        <!-- 综合能力雷达图 -->
        <div class="data-section">
            <h3>📊 综合能力雷达图</h3>
            <div class="chart-container">
                <canvas id="radarChart"></canvas>
            </div>
        </div>
        
        <!-- 指导方向 -->
        <div class="guidance">
            <h3>🎯 个性化指导方向</h3>
            {% for item in guidance %}
            <div class="guidance-item">{{ item }}</div>
            {% endfor %}
        </div>
        
        <!-- 底部 -->
        <div class="report-footer">
            AFP 智能分析报告系统 v1.0 · 模拟演示版 · 报告数据根据客户信息个性化生成
        </div>
    </div>
    
    <script>
        // 重心偏移图
        new Chart(document.getElementById('offsetChart'), {
            type: 'bar',
            data: {
                labels: ['动作阶段一', '动作阶段二', '动作阶段三', '动作阶段四'],
                datasets: [{
                    label: '重心偏移值',
                    data: {{ center_offset | tojson }},
                    backgroundColor: {{ offset_colors | tojson }},
                    borderColor: '#4CAF50',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: '重心偏移分布', color: '#888', font: { size: 14 } }
                },
                scales: {
                    y: { 
                        grid: { color: '#222' }, 
                        ticks: { color: '#888' },
                        title: { display: true, text: '偏移值（负=左偏，正=右偏）', color: '#888' }
                    },
                    x: { grid: { color: '#222' }, ticks: { color: '#888' } }
                }
            }
        });
        
        // 对称性雷达图
        new Chart(document.getElementById('symmetryChart'), {
            type: 'radar',
            data: {
                labels: ['地面反作用力', '力矩生成', '力链传递'],
                datasets: [
                    {
                        label: '左侧',
                        data: {{ sym_left | tojson }},
                        borderColor: '#4CAF50',
                        backgroundColor: 'rgba(76, 175, 80, 0.2)',
                        borderWidth: 2
                    },
                    {
                        label: '右侧',
                        data: {{ sym_right | tojson }},
                        borderColor: '#2196F3',
                        backgroundColor: 'rgba(33, 150, 243, 0.2)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '左右对称性对比', color: '#888', font: { size: 14 } }
                },
                scales: {
                    r: {
                        grid: { color: '#333' },
                        angleLines: { color: '#333' },
                        pointLabels: { color: '#aaa' },
                        ticks: { color: '#888', backdropColor: 'transparent' }
                    }
                }
            }
        });
        
        // 周期动态图
        new Chart(document.getElementById('phaseChart'), {
            type: 'line',
            data: {
                labels: {{ phase_labels | tojson }},
                datasets: [
                    {
                        label: '左脚 GRF',
                        data: {{ grf_left_wave | tojson }},
                        borderColor: '#4CAF50',
                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: '右脚 GRF',
                        data: {{ grf_right_wave | tojson }},
                        borderColor: '#2196F3',
                        backgroundColor: 'rgba(33, 150, 243, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: '力传导效率',
                        data: {{ eff_wave | tojson }},
                        borderColor: '#ff9800',
                        backgroundColor: 'rgba(255, 152, 0, 0.1)',
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '周期动态变化', color: '#888', font: { size: 14 } }
                },
                scales: {
                    y: { 
                        grid: { color: '#222' }, 
                        ticks: { color: '#888' },
                        title: { display: true, text: 'GRF (BW)', color: '#888' }
                    },
                    y1: {
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#ff9800' },
                        title: { display: true, text: '效率', color: '#ff9800' },
                        min: 0,
                        max: 1
                    },
                    x: { grid: { color: '#222' }, ticks: { color: '#888' } }
                }
            }
        });
        
        // 综合能力雷达图
        new Chart(document.getElementById('radarChart'), {
            type: 'radar',
            data: {
                labels: ['动作对称性', '力量输出', '全身协调', '平衡能力', '力链效率'],
                datasets: [{
                    label: '综合能力',
                    data: [{{ score_symmetry }}, {{ score_force }}, {{ score_coordination }}, {{ base_score }}, {{ eff_avg }}],
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#4CAF50'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '综合能力评估', color: '#888', font: { size: 14 } }
                },
                scales: {
                    r: {
                        min: 0,
                        max: 100,
                        grid: { color: '#333' },
                        angleLines: { color: '#333' },
                        pointLabels: { color: '#aaa' },
                        ticks: { color: '#888', backdropColor: 'transparent', stepSize: 20 }
                    }
                }
            }
        });
    </script>
</body>
</html>"""

# ==================== Flask 路由 ====================
@app.route('/')
def index():
    return INDEX_HTML

@app.route('/upload', methods=['POST'])
def upload():
    # 获取表单数据
    name = request.form.get('name', '未命名')
    age = int(request.form.get('age', 30))
    gender = request.form.get('gender', 'male')
    height = float(request.form.get('height', 170))
    weight = float(request.form.get('weight', 65))
    
    # 保存视频（模拟）
    video_filename = None
    if 'video' in request.files:
        file = request.files['video']
        if file and file.filename != '' and allowed_file(file.filename):
            video_filename = f"{int(time.time())}_{file.filename}"
            file.save(UPLOAD_FOLDER / video_filename)
    
    # 生成个性化数据
    data = generate_personalized_data(age, gender, height, weight)
    
    # 预处理：生成表格行HTML
    grf_table_rows = ''
    grf_left = data['grf_left_frames']
    grf_right = data['grf_right_frames']
    torque_left = data['torque_left_frames']
    torque_right = data['torque_right_frames']
    for i in range(10):
        grf_table_rows += f'<tr><td>帧{i+1}</td><td>{grf_left[i]:.3f}</td><td>{grf_right[i]:.3f}</td><td>{torque_left[i]:.3f}</td><td>{torque_right[i]:.3f}</td></tr>'
    
    # 预处理：判断颜色和评价
    offset_min = min(data['center_offset'])
    offset_max = max(data['center_offset'])
    offset_colors = ['#ff5252' if x < 0 else '#4CAF50' for x in data['center_offset']]
    
    if offset_max - offset_min < 5:
        offset_assessment = "重心偏移在合理范围内，左右平衡较好"
        offset_color = '#4CAF50'
    else:
        offset_assessment = "重心偏移较大，建议加强核心稳定性训练"
        offset_color = '#ff9800'
    
    if data['sym_diff'] < 8:
        sym_assessment = "左右对称性良好，发力均衡"
        sym_color = '#4CAF50'
    else:
        sym_assessment = "左右差异较大，建议进行对称性训练"
        sym_color = '#ff9800'
    
    if data['grf_diff_pct'] < 8:
        grf_assessment = "左右GRF差异在合理范围内"
        grf_diff_color = '#4CAF50'
    else:
        grf_assessment = "左右GRF差异较大，提示存在不对称发力"
        grf_diff_color = '#ff9800'
    
    # 评分颜色
    score_sym_color = 'green' if data['score_symmetry'] >= 80 else ('orange' if data['score_symmetry'] >= 70 else 'red')
    score_force_color = 'green' if data['score_force'] >= 80 else ('orange' if data['score_force'] >= 70 else 'red')
    score_coord_color = 'green' if data['score_coordination'] >= 80 else ('orange' if data['score_coordination'] >= 70 else 'red')
    
    # BMI颜色
    bmi = data['bmi']
    if bmi < 18.5:
        bmi_color = 'orange'
        bmi_tip_color = '#ff9800'
    elif bmi < 24:
        bmi_color = 'green'
        bmi_tip_color = '#4CAF50'
    else:
        bmi_color = 'orange'
        bmi_tip_color = '#ff9800'
    
    # 周期动态评价
    eff_avg = sum(data['eff_wave']) / len(data['eff_wave'])
    if eff_avg >= 0.8:
        phase_assessment = "力传导效率较高，动作流畅度好，身体各部位配合协调。"
    elif eff_avg >= 0.7:
        phase_assessment = "力传导效率一般，部分动作阶段存在力量损耗，建议优化动作模式。"
    else:
        phase_assessment = "力传导效率偏低，动作不够流畅，建议从基础动作模式开始改善。"
    
    # 视频URL
    video_url = f"/video/{video_filename}" if video_filename else ""
    
    timestamp = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    
    return render_template_string(
        REPORT_HTML,
        name=name,
        age=age,
        gender=gender,
        height=height,
        weight=weight,
        bmi=data['bmi'],
        bmi_color=bmi_color,
        bmi_tip_color=bmi_tip_color,
        weight_status=data['weight_status'],
        pressure_tip=data['pressure_tip'],
        center_offset=data['center_offset'],
        offset_colors=offset_colors,
        offset_min=offset_min,
        offset_max=offset_max,
        offset_assessment=offset_assessment,
        offset_color=offset_color,
        sym_left=data['sym_left'],
        sym_right=data['sym_right'],
        sym_diff=data['sym_diff'],
        sym_assessment=sym_assessment,
        sym_color=sym_color,
        grf_table_rows=grf_table_rows,
        grf_diff_pct=data['grf_diff_pct'],
        grf_assessment=grf_assessment,
        grf_diff_color=grf_diff_color,
        phase_labels=data['phase_labels'],
        grf_left_wave=data['grf_left_wave'],
        grf_right_wave=data['grf_right_wave'],
        eff_wave=data['eff_wave'],
        eff_avg=round(eff_avg, 3),
        phase_assessment=phase_assessment,
        score_symmetry=data['score_symmetry'],
        score_force=data['score_force'],
        score_coordination=data['score_coordination'],
        base_score=round(data['base_score'], 1),
        score_sym_color=score_sym_color,
        score_force_color=score_force_color,
        score_coord_color=score_coord_color,
        guidance=data['guidance'],
        video_url=video_url,
        timestamp=timestamp
    )

@app.route('/video/<filename>')
def serve_video(filename):
    return send_file(UPLOAD_FOLDER / filename, mimetype='video/mp4')

if __name__ == '__main__':
    print("=" * 60)
    print("  AFP 智能模拟演示系统 v1.0")
    print("=" * 60)
    print(f"  访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False)
