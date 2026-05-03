from flask import Flask, request, send_from_directory, jsonify
import os
import socket
import random
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template_v23.html')

def read_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>AFP 运动康复AI分析系统</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }
        .container { max-width: 1200px; width: 100%; margin: 0 auto; }
        .header-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 24px;
        }
        .logo {
            font-size: 80px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
            letter-spacing: -2px;
            text-align: center;
        }
        .subtitle {
            color: #64748b;
            font-size: 18px;
            margin-bottom: 30px;
            font-weight: 500;
            text-align: center;
        }
        .afp-intro {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }
        .afp-intro h2 { color: #1e293b; font-size: 24px; margin-bottom: 16px; font-weight: 700; }
        .afp-intro p { color: #475569; font-size: 15px; line-height: 1.8; margin-bottom: 12px; }
        .afp-highlight {
            background: rgba(102, 126, 234, 0.08);
            padding: 16px;
            border-radius: 12px;
            margin-top: 16px;
        }
        .afp-highlight strong { color: #667eea; font-weight: 600; }
        .comparison-section {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .comparison-section h2 { color: #1e293b; font-size: 24px; margin-bottom: 24px; font-weight: 700; text-align: center; }
        .comparison-table { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .comparison-card { padding: 20px; border-radius: 12px; border: 2px solid #e2e8f0; }
        .comparison-card.traditional { background: #fef2f2; border-color: #fecaca; }
        .comparison-card.afp { background: #f0fdf4; border-color: #bbf7d0; }
        .comparison-card h3 { font-size: 18px; margin-bottom: 12px; font-weight: 600; }
        .comparison-card.traditional h3 { color: #dc2626; }
        .comparison-card.afp h3 { color: #16a34a; }
        .comparison-card ul { list-style: none; padding: 0; }
        .comparison-card li { color: #475569; font-size: 14px; line-height: 1.6; margin-bottom: 8px; padding-left: 20px; position: relative; }
        .comparison-card.traditional li:before { content: "❌"; position: absolute; left: 0; }
        .comparison-card.afp li:before { content: "✅"; position: absolute; left: 0; }
        .client-form {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .client-form h2 { color: #1e293b; font-size: 20px; margin-bottom: 20px; font-weight: 700; }
        .form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }
        .form-group label { display: block; color: #475569; font-size: 13px; font-weight: 600; margin-bottom: 6px; }
        .form-group input, .form-group select {
            width: 100%; padding: 10px 12px; border: 2px solid #e2e8f0;
            border-radius: 8px; font-size: 14px; color: #1e293b;
            background: #f8fafc; transition: border-color 0.2s;
        }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #667eea; background: white; }
        .upload-area { 
            border: 3px dashed #667eea; border-radius: 16px; padding: 60px 40px; 
            text-align: center; background: #f8fafc; transition: all 0.3s; cursor: pointer;
        }
        .upload-area:hover { border-color: #764ba2; background: #f1f5f9; transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102,126,234,0.2); }
        .upload-icon { font-size: 64px; margin-bottom: 20px; display: block; }
        .upload-text { color: #1e293b; font-size: 20px; margin-bottom: 12px; font-weight: 600; }
        .upload-hint { color: #64748b; font-size: 14px; }
        input[type="file"] { margin-top: 24px; font-size: 16px; }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
            padding: 16px 48px; border: none; border-radius: 12px; font-size: 18px; 
            font-weight: 600; cursor: pointer; width: 100%; margin-top: 24px;
            transition: all 0.3s; box-shadow: 0 4px 12px rgba(102,126,234,0.4);
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,0.6); }
        @media (max-width: 768px) { .form-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 480px) { .form-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-card">
            <div class="logo">AFP</div>
            <p class="subtitle">Applied Functional Physics · 运动康复AI分析系统</p>
            <div class="afp-intro">
                <h2>🧬 什么是 Applied Functional Physics (AFP)？</h2>
                <p><strong>Applied Functional Physics（实用功能性物理）</strong>是熊异自主研发的一套基于物理定律和人类进化原理的运动康复与训练体系。</p>
                <p><strong>🔬 核心理念：回归第一性原理</strong></p>
                <p>AFP用物理定律（<strong>力、平衡、适应</strong>）分析和训练身体，以<strong>人类自然功能动作（走、跑、跳、投掷）</strong>为核心。</p>
                <p><strong>🎯 独特优势：从根源解决问题</strong></p>
                <p>不是"哪里痛就治哪里"，而是找到根本原因；不是"只练单个肌肉"，而是全身联动。</p>
                <div class="afp-highlight">
                    <p><strong>🌟 AFP与传统方法的本质区别：</strong></p>
                    <p>✅ <strong>平衡强弱侧，像天平一样</strong></p>
                    <p>✅ <strong>全身联动训练</strong> - 不搞局部孤立训练</p>
                    <p>✅ <strong>用自然动作训练</strong> - 走、跑、跳、投掷</p>
                    <p>✅ <strong>长期自我优化</strong> - 不依赖治疗师</p>
                </div>
            </div>
            <div class="comparison-section">
                <h2>⚖️ AFP vs 传统康复方法对比</h2>
                <div class="comparison-table">
                    <div class="comparison-card traditional">
                        <h3>❌ 传统康复方法</h3>
                        <ul>
                            <li>哪里痛就治哪里，治标不治本</li>
                            <li>只练单个肌肉，缺乏整体性</li>
                            <li>固定模板静态动作，不自然</li>
                            <li>被动治疗，患者依赖治疗师</li>
                        </ul>
                    </div>
                    <div class="comparison-card afp">
                        <h3>✅ AFP科学康复方法</h3>
                        <ul>
                            <li>系统性分析，找到根本原因</li>
                            <li>平衡强弱侧，像天平一样精准</li>
                            <li>全身联动训练，提升协调性</li>
                            <li>用自然动作训练（走、跑、跳）</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="client-form">
                <h2>📋 客户基础信息（选填，填写后分析更精准）</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="age">年龄</label>
                        <input type="number" id="age" name="age" min="1" max="120" placeholder="如：35">
                    </div>
                    <div class="form-group">
                        <label for="gender">性别</label>
                        <select id="gender" name="gender">
                            <option value="">请选择</option>
                            <option value="male">男</option>
                            <option value="female">女</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="height">身高 (cm)</label>
                        <input type="number" id="height" name="height" min="50" max="250" placeholder="如：170">
                    </div>
                    <div class="form-group">
                        <label for="weight">体重 (kg)</label>
                        <input type="number" id="weight" name="weight" min="20" max="300" placeholder="如：65">
                    </div>
                </div>
            </div>
            <div class="upload-area">
                <span class="upload-icon">🎬</span>
                <div class="upload-text">上传运动视频进行智能分析</div>
                <div class="upload-hint">支持 MP4、MOV、AVI 格式</div>
                <form action="/analyze" method="post" enctype="multipart/form-data" id="uploadForm">
                    <input type="hidden" name="age" id="formAge">
                    <input type="hidden" name="gender" id="formGender">
                    <input type="hidden" name="height" id="formHeight">
                    <input type="hidden" name="weight" id="formWeight">
                    <input type="file" name="video" accept="video/*" required>
                    <br>
                    <button type="submit" class="btn">开始分析 🚀</button>
                </form>
            </div>
        </div>
    </div>
    <script>
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            document.getElementById('formAge').value = document.getElementById('age').value;
            document.getElementById('formGender').value = document.getElementById('gender').value;
            document.getElementById('formHeight').value = document.getElementById('height').value;
            document.getElementById('formWeight').value = document.getElementById('weight').value;
        });
    </script>
</body>
</html>'''

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'video' not in request.files:
        return "没有上传视频", 400
    file = request.files['video']
    if file.filename == '':
        return "没有选择文件", 400
    
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    age = request.form.get('age', '')
    gender = request.form.get('gender', '')
    height = request.form.get('height', '')
    weight = request.form.get('weight', '')
    
    # 生成模拟参数（基于客户信息）
    params = generate_simulation_params(age, gender, height, weight)
    
    # 构建客户信息卡片
    client_info_html = build_client_info(age, gender, height, weight)
    
    # 读取模板并替换占位符
    html = read_template()
    html = html.replace('VIDEO_FILE_NAME', filename)
    html = html.replace('CLIENT_INFO_PLACEHOLDER', client_info_html)
    
    # 将模拟参数作为JSON嵌入到HTML中
    import json
    params_json = json.dumps(params, ensure_ascii=False)
    params_script = '<script>window.SIMULATION_PARAMS = %s;</script>' % params_json
    html = html.replace('</head>', params_script + '\n</head>')
    
    return html

def build_client_info(age, gender, height, weight):
    has_info = age or gender or height or weight
    if not has_info:
        return '<div class="client-info-card"><div class="info-empty">未填写基础信息，<a href="/" style="color: #667eea;">点击返回填写</a>可获得更精准的分析</div></div>'
    
    html = '<div class="client-info-card"><h3>📋 客户基础信息</h3><div class="client-info-grid">'
    
    # 年龄
    if age:
        html += '<div class="info-item"><div class="info-value">%s岁</div><div class="info-label">年龄</div></div>' % age
    else:
        html += '<div class="info-item"><div class="info-value">-</div><div class="info-label">年龄</div></div>'
    
    # 性别
    if gender:
        g_text = '男' if gender == 'male' else '女'
        html += '<div class="info-item"><div class="info-value">%s</div><div class="info-label">性别</div></div>' % g_text
    else:
        html += '<div class="info-item"><div class="info-value">-</div><div class="info-label">性别</div></div>'
    
    # 身高
    if height:
        html += '<div class="info-item"><div class="info-value">%scm</div><div class="info-label">身高</div></div>' % height
    else:
        html += '<div class="info-item"><div class="info-value">-</div><div class="info-label">身高</div></div>'
    
    # 体重
    if weight:
        html += '<div class="info-item"><div class="info-value">%skg</div><div class="info-label">体重</div></div>' % weight
    else:
        html += '<div class="info-item"><div class="info-value">-</div><div class="info-label">体重</div></div>'
    
    html += '</div></div>'
    
    # 基于真实数据给出分析（不夸大）
    notes = []
    if age:
        age_i = int(age)
        if age_i < 30:
            notes.append('年龄 %s岁：处于运动能力巅峰期，关节灵活性好，恢复快' % age)
        elif age_i < 50:
            notes.append('年龄 %s岁：肌肉力量稳定，需注意关节保养和柔韧性维持' % age)
        else:
            notes.append('年龄 %s岁：关节灵活性自然下降，需加强热身和恢复性训练' % age)
    
    if height and weight:
        h_m = int(height) / 100.0
        w_kg = int(weight)
        bmi = w_kg / (h_m * h_m)
        if bmi < 18.5:
            notes.append('BMI %.1f：偏瘦，肌肉量不足可能影响关节稳定性' % bmi)
        elif bmi < 24:
            notes.append('BMI %.1f：正常范围，身体条件良好' % bmi)
        elif bmi < 28:
            notes.append('BMI %.1f：偏重，额外负荷可能影响关节压力和动作流畅度' % bmi)
        else:
            notes.append('BMI %.1f：超重，建议结合低冲击运动（如游泳）减少关节负担' % bmi)
    
    if notes:
        html += '<div class="detail-section" style="margin-top:12px;"><h4>📊 基于您的基础信息的分析参考</h4>'
        for n in notes:
            html += '<p style="margin-bottom:6px;">• %s</p>' % n
        html += '</div>'
    
    return html

def generate_simulation_params(age, gender, height, weight):
    """
    根据客户信息生成模拟参数
    返回：字典，包含各种基准分数和调整因子
    """
    random.seed(int(time.time() * 1000) % 1000000)  # 基于时间戳的随机种子
    
    params = {}
    
    # 1. 年龄影响（20岁=95分，60岁=75分，线性插值）
    if age:
        age_int = int(age)
        base_score = 95 - (age_int - 20) * (20.0 / 40.0)  # 20→95, 60→75
        base_score = max(75, min(95, base_score))  # 限制在75-95之间
    else:
        base_score = 85 + random.uniform(-5, 5)  # 没有年龄信息，给个中间值
    
    params['base_score'] = round(base_score, 1)
    
    # 2. 性别影响（男性左右差异小，女性左右差异大）
    if gender == 'male':
        left_right_diff = random.uniform(0.10, 0.15)  # 男性差异10-15%
    elif gender == 'female':
        left_right_diff = random.uniform(0.15, 0.20)  # 女性差异15-20%
    else:
        left_right_diff = random.uniform(0.12, 0.18)  # 未知性别，中间值
    
    params['left_right_diff'] = round(left_right_diff, 3)
    
    # 3. BMI影响（BMI高→分数低，关节压力大）
    if height and weight:
        height_m = int(height) / 100.0
        weight_kg = int(weight)
        bmi = weight_kg / (height_m * height_m)
        params['bmi'] = round(bmi, 1)
        
        if bmi < 18.5:
            bmi_penalty = 0  # 偏瘦，无惩罚
            params['joint_pressure'] = 'low'
        elif bmi < 24:
            bmi_penalty = 0  # 正常，无惩罚
            params['joint_pressure'] = 'normal'
        elif bmi < 28:
            bmi_penalty = 5  # 偏重，扣分
            params['joint_pressure'] = 'moderate'
        else:
            bmi_penalty = 10  # 超重，扣分多
            params['joint_pressure'] = 'high'
    else:
        bmi_penalty = 0
        params['bmi'] = None
        params['joint_pressure'] = 'unknown'
    
    params['bmi_penalty'] = bmi_penalty
    
    # 4. 计算各项得分（基于基准分 + 随机波动 - BMI惩罚）
    score_symmetry = params['base_score'] - random.uniform(0, 10) - bmi_penalty
    score_force = params['base_score'] - random.uniform(5, 15) - bmi_penalty
    score_stability = params['base_score'] - random.uniform(10, 20) - bmi_penalty
    score_balance = params['base_score'] - random.uniform(5, 15) - bmi_penalty
    score_fluency = params['base_score'] - random.uniform(10, 20) - bmi_penalty
    
    params['score_symmetry'] = max(60, min(98, round(score_symmetry)))
    params['score_force'] = max(60, min(98, round(score_force)))
    params['score_stability'] = max(60, min(98, round(score_stability)))
    params['score_balance'] = max(60, min(98, round(score_balance)))
    params['score_fluency'] = max(60, min(98, round(score_fluency)))
    
    # 5. 生成重心偏移数据（基于左右差异因子）
    # 左侧偏移最大值（负相关）
    params['left_offset_max'] = -1 * round(random.uniform(6, 10) * (1 + params['left_right_diff']), 1)
    # 右侧偏移最大值
    params['right_offset_max'] = round(random.uniform(6, 10), 1)
    # 前倾偏移最大值
    params['forward_offset_max'] = round(random.uniform(6, 10), 1)
    
    # 6. 生成时间参数（偏移发生的时间点）
    params['left_offset_time'] = random.randint(6, 10)
    params['right_offset_time'] = random.randint(10, 14)
    params['forward_offset_time'] = params['right_offset_time']  # 通常同时发生
    
    return params
    print('=' * 70)
    print('  AFP 运动康复AI分析系统 v23.0')
    print('  ✅ 数据表达清晰版 - 每个数字都有明确含义')
    print('=' * 70)
    print()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print('  访问地址: http://127.0.0.1:%d' % port)
    print('  改进内容：')
    print('    ✅🔥 1.重心数据明细表 - "次大右偏" → "右侧偏移 6cm（第二高值）"')
    print('    ✅🔥 2.重心数据明细表 - "回归中线" → "重心回到中心线附近（左-2，右1，前倾1）"')
    print('    ✅🔥 3.每个数据都加了"具体解读"列，每句话对应具体数字')
    print('    ✅🔥 4.重心偏移详细分析 - 每句话都对应具体数字，不含模糊词')
    print('    ✅   5.数据解读说明 - 解释每个术语的含义')
    print('    ✅   6.客户信息卡片 - 结合真实数据给出分析（不夸大）')
    print()
    print('=' * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
