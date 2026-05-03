#!/usr/bin/env python3
"""
AFP MVP - 改进版
强化数据展示和分析逻辑
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

def generate_simulation_data(age, gender, height, weight):
    """根据客户信息生成真正个性化的模拟数据"""
    
    # 使用客户信息作为随机种子，确保同一人每次得到相同但不同人不同的数据
    import hashlib
    seed_str = f"{age}{gender}{height}{weight}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16) % (2**32)
    random.seed(seed)
    
    # 1. 年龄影响：更精细的分段 + 年龄越小基础分数越高
    if age <= 20:
        base_score = random.uniform(90, 96)
        offset_base = 2  # 年轻人重心更稳定
    elif age <= 30:
        base_score = random.uniform(85, 92)
        offset_base = 3
    elif age <= 40:
        base_score = random.uniform(78, 87)
        offset_base = 4
    elif age <= 50:
        base_score = random.uniform(70, 82)
        offset_base = 6
    else:
        base_score = random.uniform(62, 75)
        offset_base = 8
    
    # 2. 性别影响：男性力量更大但对称性可能更差
    if gender == 'male':
        force_mult = random.uniform(1.08, 1.18)
        symmetry_base = random.uniform(0.68, 0.82)
        torque_mult = random.uniform(1.05, 1.15)
    else:
        force_mult = random.uniform(0.92, 1.02)
        symmetry_base = random.uniform(0.72, 0.88)  # 女性对称性通常更好
        torque_mult = random.uniform(0.90, 1.00)
    
    # 3. BMI计算和精细化影响
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        weight_status = "偏轻"
        pressure_tip = "体重偏轻，肌肉量可能不足，影响力量传导效率"
        score_adjust = random.uniform(-2, 0)
        offset_increase = 1  # 偏轻可能稳定性稍差
    elif bmi < 22:
        weight_status = "理想"
        pressure_tip = "体重理想，力传导效率最佳"
        score_adjust = random.uniform(0, 2)
        offset_increase = 0
    elif bmi < 24:
        weight_status = "正常"
        pressure_tip = "体重正常，力传导效率较好"
        score_adjust = random.uniform(-1, 1)
        offset_increase = 0
    elif bmi < 28:
        weight_status = "偏重"
        pressure_tip = "体重偏重，关节压力较大，建议先减重再强化训练"
        score_adjust = random.uniform(-5, -2)
        offset_increase = 2
    else:
        weight_status = "肥胖"
        pressure_tip = "体重超标，关节负担重，优先进行低冲击的功能训练"
        score_adjust = random.uniform(-8, -4)
        offset_increase = 3
    
    base_score += score_adjust
    
    # 4. 重心偏移（受年龄、BMI、性别共同影响）
    offset_range = offset_base + offset_increase
    # 生成有趋势的偏移数据（不是完全随机）
    center_offset = []
    for i in range(4):
        if i < 2:
            # 单脚支撑时偏移更明显
            offset = -random.uniform(1, offset_range)
        else:
            # 双脚支撑/蹬伸时偏移减小
            offset = -random.uniform(0.5, offset_range * 0.6)
        center_offset.append(round(offset, 1))
    
    # 5. 对称性数据（左右差异受多种因素影响）
    sym_left = []
    sym_right = []
    for i in range(3):
        # 左侧基础值
        left_val = symmetry_base + random.uniform(-0.08, 0.03)
        sym_left.append(round(left_val, 3))
        # 右侧值：引入系统性偏移（模拟真实的不对称）
        right_val = left_val + random.uniform(-0.12, 0.15)
        sym_right.append(round(right_val, 3))
    
    # 6. 地面反作用力和力矩（根据性别、体重、年龄精细调整）
    grf_left = []
    grf_right = []
    torque_left = []
    torque_right = []
    
    for i in range(10):
        # GRF随时间变化（模拟步态周期）
        phase_mult = 0.8 + (i % 5) * 0.1  # 周期性变化
        grf_l = round(random.uniform(0.75, 1.25) * force_mult * phase_mult, 3)
        grf_r = round(random.uniform(0.70, 1.20) * force_mult * phase_mult, 3)
        grf_left.append(grf_l)
        grf_right.append(grf_r)
        
        # 力矩与GRF相关但独立
        torque_l = round(grf_l * random.uniform(0.6, 1.1) * torque_mult, 3)
        torque_r = round(grf_r * random.uniform(0.6, 1.1) * torque_mult, 3)
        torque_left.append(torque_l)
        torque_right.append(torque_r)
    
    # 7. 周期波形数据（更真实的波形）
    phase_labels = ['支撑前期', '支撑早期', '支撑中期', '支撑后期', '蹬伸期', '离地期']
    # GRF波形：支撑中期达到峰值
    grf_left_wave = []
    grf_right_wave = []
    for i in range(6):
        if i == 2:  # 支撑中期峰值
            base_val = random.uniform(1.1, 1.3)
        elif i == 4:  # 蹬伸期次峰值
            base_val = random.uniform(0.9, 1.1)
        else:
            base_val = random.uniform(0.4, 0.8)
        grf_left_wave.append(round(base_val * force_mult, 2))
        grf_right_wave.append(round(base_val * force_mult * random.uniform(0.95, 1.05), 2))
    
    # 效率波形：与GRF波形相关但不同步
    efficiency_wave = []
    for i in range(6):
        eff_base = 0.65 + (i * 0.05) - (i * i * 0.01)  # 抛物线型
        efficiency_wave.append(round(eff_base + random.uniform(-0.05, 0.08), 3))
    
    # 8. 评分（更个性化的计算）
    score_symmetry = round(base_score - abs(sym_left[0] - sym_right[0]) * 50 + random.uniform(-3, 3), 1)
    score_force = round(base_score * force_mult - (1 - min(grf_left + grf_right)) * 20 + random.uniform(-5, 2), 1)
    score_coordination = round(base_score - sum(abs(sym_left[i] - sym_right[i]) for i in range(3)) * 30 + random.uniform(-5, 5), 1)
    
    # 9. 判断差异（基于真实计算）
    grf_left_avg = sum(grf_left) / len(grf_left)
    grf_right_avg = sum(grf_right) / len(grf_right)
    grf_diff_pct = round(abs(grf_left_avg - grf_right_avg) / max(grf_left_avg, grf_right_avg) * 100, 1)
    sym_diff = sum(abs(sym_left[i] - sym_right[i]) for i in range(3)) / 3 * 100
    
    # 10. 个性化指导方向
    guidance = []
    if grf_diff_pct > 15:
        guidance.append(f"⚠️ 左右GRF差异{grf_diff_pct}%，差异明显，建议进行对称性训练，重点改善弱侧发力")
    elif grf_diff_pct > 10:
        guidance.append(f"⚠️ 左右GRF差异{grf_diff_pct}%，建议增加对称性训练")
    
    if sym_diff > 15:
        guidance.append(f"⚠️ 左右对称性差异{sym_diff:.1f}%，差异显著，推荐走跑跳投掷联动练习")
    elif sym_diff > 10:
        guidance.append(f"⚠️ 左右对称性差异{sym_diff:.1f}%，建议关注对称性改善")
    
    if max(center_offset) - min(center_offset) > 6:
        guidance.append("⚠️ 重心偏移较大，建议加强核心稳定性训练，改善动态平衡")
    
    if bmi >= 28:
        guidance.append(f"⚠️ BMI={bmi:.1f}（{weight_status}），关节压力较大，建议低冲击训练，优先减重")
    elif bmi >= 24:
        guidance.append(f"⚠️ BMI={bmi:.1f}（{weight_status}），建议适当控制体重以改善关节压力")
    
    if age > 50:
        guidance.append(f"💡 年龄{age}岁，建议注重功能性训练，保持关节灵活性和肌肉协调性")
    elif age < 25:
        guidance.append(f"💡 年龄{age}岁，身体条件好，可进行全面的功能性训练")
    
    if not guidance:
        guidance.append("✅ 各项指标良好，继续保持当前训练节奏")
    
    guidance.append("💡 训练重点：走·跑·跳·投掷 四个基础动作模式，每周3-4次，注重左右对称性")
    
    data = {
        'base_score': round(base_score, 1),
        'bmi': round(bmi, 1),
        'weight_status': weight_status,
        'pressure_tip': pressure_tip,
        'score_symmetry': max(0, min(100, score_symmetry)),
        'score_force': max(0, min(100, score_force)),
        'score_coordination': max(0, min(100, score_coordination)),
        'center_offset': center_offset,
        'sym_left': sym_left,
        'sym_right': sym_right,
        'sym_diff': round(sym_diff, 1),
        'grf_left_wave': grf_left_wave,
        'grf_right_wave': grf_right_wave,
        'efficiency_wave': efficiency_wave,
        'phase_labels': phase_labels,
        'grf_left_frames': grf_left,
        'grf_right_frames': grf_right,
        'torque_left_frames': torque_left,
        'torque_right_frames': torque_right,
        'grf_diff_pct': grf_diff_pct,
        'guidance': guidance,
    }
    
    return data

# ==================== 首页模板 ====================
INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AFP | Applied Functional Physics</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; margin-bottom: 60px; }
        .header h1 { font-size: 48px; color: #fff; margin-bottom: 10px; }
        .header .subtitle { color: #888; font-size: 18px; margin-bottom: 30px; }
        .afp-intro { max-width: 800px; margin: 0 auto; background: #111; padding: 30px; border-radius: 8px; text-align: left; }
        .afp-intro h3 { color: #4CAF50; margin-bottom: 15px; }
        .afp-intro ul { margin-left: 20px; margin-top: 10px; }
        .afp-intro li { margin-bottom: 8px; color: #ccc; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }
        .card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; }
        .card h2 { color: #4CAF50; margin-bottom: 20px; font-size: 20px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #aaa; }
        .form-group input, .form-group select { width: 100%; padding: 12px; background: #0a0a0a; border: 1px solid #333; border-radius: 4px; color: #e0e0e0; font-size: 16px; }
        .gender-select { display: flex; gap: 15px; }
        .gender-btn { flex: 1; padding: 12px; background: #0a0a0a; border: 2px solid #333; border-radius: 4px; text-align: center; cursor: pointer; color: #e0e0e0; }
        .gender-btn.selected { border-color: #4CAF50; background: #1a2e1a; }
        .upload-area { border: 2px dashed #333; border-radius: 8px; padding: 60px 20px; text-align: center; cursor: pointer; }
        .upload-area:hover { border-color: #4CAF50; }
        .submit-btn { display: block; width: 100%; max-width: 400px; margin: 0 auto; padding: 18px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; }
        .badge { display: inline-block; padding: 8px 16px; background: #ff9800; color: #000; border-radius: 20px; font-size: 12px; margin-top: 15px; }
        input[type="file"] { display: none; }
        .comparison-section { margin-top: 40px; }
        .comparison-table { width: 100%; border-collapse: collapse; max-width: 900px; margin: 0 auto; }
        .comparison-table th { padding: 15px; text-align: center; font-size: 17px; }
        .comparison-table td { padding: 11px 16px; color: #ccc; font-size: 14px; vertical-align: top; }
        .comparison-table thead th:first-child { background: #2a1a1a; border: 1px solid #660000; color: #ff6b6b; }
        .comparison-table thead th:last-child { background: #1a2a1a; border: 1px solid #006600; color: #4CAF50; }
        .comparison-table tbody td:first-child { background: #1a0a0a; border: 1px solid #330000; }
        .comparison-table tbody td:last-child { background: #0a1a0a; border: 1px solid #003300; }
        .comparison-table tfoot td { background: #111; border: 1px solid #333; text-align: center; color: #4CAF50; font-size: 15px; padding: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AFP：Applied Functional Physics</h1>
            <div class="subtitle">实用功能性物理 · 第一性功能训练体系</div>
            <div class="badge">⚠️ 模拟演示版 - 数据根据客户信息智能生成</div>
        </div>
        
        <div class="afp-intro">
            <h3>🧬 AFP核心理念</h3>
            <p>Applied Functional Physics（实用功能性物理）是熊异自主研发的基于物理定律和人类进化原理的功能训练体系。</p>
            <p style="margin-top: 12px;"><strong>物理学基础：</strong><br>牛顿力学三定律 + 地面反作用力（脚踩地时地面给身体的反推力）</p>
            <p style="margin-top: 10px;"><strong>进化动作模式：</strong><br>走 · 跑 · 跳 · 投掷</p>
            <p style="margin-top: 10px;"><strong>核心评估：</strong><br>动作流畅度 + 全身协调性 + 动态平衡</p>
            <p style="margin-top: 10px;"><strong>目标：</strong><br>从根源解决肩膝腰慢性疼痛，让身体形成自我优化系统，越练越好。</p>
        </div>
        
        <!-- 传统 vs AFP 详细对比 -->
        <div class="comparison-section">
            <h3 style="color: #4CAF50; text-align: center; margin-bottom: 18px;">⚡ 传统训练 vs AFP功能训练</h3>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>❌ 传统方法</th>
                        <th>✅ AFP方法</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>哪里痛就治哪里（头痛医头，脚痛医脚）</td><td>平衡强弱侧，像天平一样把压力平均分担</td></tr>
                    <tr><td>只练单个肌肉（孤立训练，比如只练股四头肌或肩袖）</td><td>全身联动，让身体各部位一起配合发力（力从脚传到腰再传到手）</td></tr>
                    <tr><td>使用固定模板和静态动作（照着标准姿势做，死板、不考虑个体差异）</td><td>使用走、跑、跳、投掷这些自然功能动作训练</td></tr>
                    <tr><td>只看力量大小、围度数据（只关心表面数字）</td><td>重点看动作是否流畅、自然、协调（看整台机器运转得顺不顺）</td></tr>
                    <tr><td>短期缓解，容易反复（停训后问题容易回来）</td><td>长期自我优化，持续进步（身体自己学会更好工作）</td></tr>
                    <tr><td>被动治疗，依赖外部干预（主要靠医生、治疗师、教练或固定器械）</td><td>主动训练，让身体形成自我优化系统</td></tr>
                </tbody>
                <tfoot>
                    <tr><td colspan="2">💡 一句话区别：<strong>传统是"局部修理、平面2D思维"，AFP是"尊重个体差异，把整个身体的力传导优化，让动作流畅、协调、交替自然，越用越好"</strong></td></tr>
                </tfoot>
            </table>
        </div>
        
        <form method="POST" action="/upload" enctype="multipart/form-data" style="margin-top: 40px;">
            <div class="form-grid">
                <div class="card">
                    <h2>👤 客户信息</h2>
                    <div class="form-group">
                        <label>年龄（岁）</label>
                        <input type="number" name="age" min="10" max="100" required>
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
                        <input type="number" name="height" min="100" max="250" required>
                    </div>
                    <div class="form-group">
                        <label>体重（kg）</label>
                        <input type="number" name="weight" min="30" max="200" required>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🎬 视频上传</h2>
                    <div class="upload-area" onclick="document.getElementById('videoFile').click()">
                        <div style="font-size: 48px; margin-bottom: 20px;">📁</div>
                        <div>点击或拖拽视频到此处</div>
                        <div style="color: #666; font-size: 14px; margin-top: 10px;">支持 mp4, mov, avi, mkv</div>
                    </div>
                    <input type="file" id="videoFile" name="video" accept=".mp4,.mov,.avi,.mkv" required>
                    <div id="fileInfo" style="margin-top: 15px; color: #4CAF50; display: none;"></div>
                </div>
            </div>
            
            <button type="submit" class="submit-btn">开始分析</button>
        </form>
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
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileInfo').textContent = '✓ ' + file.name;
            }
        });
    </script>
</body>
</html>"""

# ==================== 报告模板（改进版）====================
REPORT_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AFP分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        
        /* 头部 */
        .header { text-align: center; margin-bottom: 40px; padding-bottom: 30px; border-bottom: 1px solid #222; }
        .header h1 { font-size: 36px; color: #fff; margin-bottom: 10px; }
        .badge { display: inline-block; padding: 8px 20px; background: #ff9800; color: #000; border-radius: 20px; font-size: 14px; font-weight: 600; }
        
        /* 客户信息卡片 */
        .client-info { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
        .info-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; text-align: center; }
        .info-card .label { color: #888; font-size: 14px; margin-bottom: 5px; }
        .info-card .value { color: #4CAF50; font-size: 24px; font-weight: 600; }
        
        /* 横向布局 */
        .report-body { display: flex; gap: 30px; align-items: flex-start; margin-bottom: 40px; }
        .video-col { flex: 0 0 420px; position: sticky; top: 20px; }
        .content-col { flex: 1; min-width: 0; }
        
        /* 视频区域 */
        .video-section { background: #111; border: 1px solid #222; border-radius: 8px; padding: 20px; text-align: center; }
        .video-section h2 { color: #4CAF50; margin-bottom: 12px; font-size: 17px; }
        .video-wrap { max-height: 460px; display: flex; justify-content: center; align-items: center; overflow: hidden; border-radius: 6px; background: #0a0a0a; }
        video { max-width: 100%; max-height: 430px; width: auto; height: auto; border-radius: 4px; object-fit: contain; }
        
        /* 章节标题 */
        .section-title { color: #4CAF50; font-size: 28px; margin: 40px 0 20px; padding-bottom: 10px; border-bottom: 2px solid #222; }
        .section-subtitle { color: #888; font-size: 16px; margin-bottom: 20px; }
        
        /* 数据展示区 */
        .data-section { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; margin-bottom: 30px; }
        .data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }

        /* 数据采集流程图 */
        .data-flow { display: flex; align-items: center; justify-content: center; gap: 0; margin: 20px 0 30px; flex-wrap: wrap; }
        .flow-node { background: #1a1a1a; border: 1px solid #4CAF50; border-radius: 8px; padding: 14px 18px; text-align: center; min-width: 110px; position: relative; }
        .flow-node .flow-icon { font-size: 22px; display: block; margin-bottom: 6px; }
        .flow-node .flow-label { color: #4CAF50; font-size: 13px; font-weight: 600; }
        .flow-node .flow-detail { color: #888; font-size: 11px; margin-top: 4px; }
        .flow-arrow { color: #4CAF50; font-size: 20px; margin: 0 4px; }
        .flow-branch { display: flex; gap: 20px; }
        .flow-group { margin: 20px 0; }
        .flow-group-title { color: #4CAF50; font-size: 13px; margin-bottom: 10px; text-align: center; }

        /* 周期动态图 */
        .phase-chart-container { position: relative; height: 280px; margin: 20px 0; }
        .frame-table th, .frame-table td { padding: 8px 10px; font-size: 13px; }
        .frame-table { margin: 15px 0; }
        
        /* 图表容器 */
        .chart-container { position: relative; height: 300px; margin: 20px 0; }
        
        /* 数据表格 */
        .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .data-table th, .data-table td { padding: 12px; text-align: left; border-bottom: 1px solid #222; }
        .data-table th { color: #888; font-size: 14px; }
        .data-table td { color: #e0e0e0; }
        
        /* 分析过程 */
        .analysis-step { background: #1a1a1a; border-left: 4px solid #4CAF50; padding: 20px; margin: 20px 0; border-radius: 4px; }
        .analysis-step h4 { color: #4CAF50; margin-bottom: 10px; }
        .analysis-step p { color: #ccc; line-height: 1.8; }
        
        /* 结论和建议 */
        .conclusion { background: #111; border: 1px solid #4CAF50; border-radius: 8px; padding: 30px; margin: 30px 0; }
        .conclusion h3 { color: #4CAF50; margin-bottom: 20px; }
        .conclusion ol { margin-left: 20px; }
        .conclusion li { margin-bottom: 15px; color: #ccc; line-height: 1.8; }
        
        /* 评分卡片 */
        .scores { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }
        .score-card { background: #111; border: 1px solid #222; border-radius: 8px; padding: 30px; text-align: center; }
        .score-card .label { color: #888; margin-bottom: 10px; }
        .score-card .value { font-size: 48px; font-weight: 700; color: #4CAF50; }
        
        /* 返回按钮 */
        .back-btn { display: block; width: 100%; max-width: 400px; margin: 40px auto; padding: 18px; background: #333; color: #e0e0e0; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; text-align: center; text-decoration: none; }
        
        @media (max-width: 768px) {
            .report-body { flex-direction: column; }
            .video-col { flex: none; width: 100%; position: static; }
            .client-info, .data-grid, .comparison, .scores { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>AFP：智能分析报告</h1>
            <div class="badge">⚠️ 模拟演示版 - 数据仅供展示</div>
        </div>
        
        <!-- 客户信息 -->
        <div class="client-info">
            <div class="info-card"><div class="label">年龄</div><div class="value">{{ age }}岁</div></div>
            <div class="info-card"><div class="label">性别</div><div class="value">{{ gender_text }}</div></div>
            <div class="info-card"><div class="label">身高/体重</div><div class="value">{{ height }}cm/{{ weight }}kg</div></div>
            <div class="info-card"><div class="label">BMI</div><div class="value" style="font-size: 18px;">{{ bmi }}</div></div>
        </div>
        
        <div class="report-body">
            <div class="video-col">
                <div class="video-section">
                    <h2>🎬 分析视频</h2>
                    <div class="video-wrap">
                        <video controls preload="metadata">
                            <source src="/video/{{ video_filename }}" type="video/mp4">
                        </video>
                    </div>
                </div>
            </div>
            <div class="content-col">
            
        <!-- ==================== 第一部分：数据采集与呈现 ==================== -->
        <h2 class="section-title">📊 一、测试数据采集与呈现</h2>
        <p class="section-subtitle">从视频逐帧提取地面反作用力（GRF）、力矩与力链传递效率，构建完整分析数据链</p>

        <!-- 数据采集流程图 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 18px;">📡 数据采集流程</h3>
            <div class="data-flow">
                <div class="flow-node"><span class="flow-icon">🎬</span><span class="flow-label">视频输入</span><span class="flow-detail">逐帧提取</span></div>
                <span class="flow-arrow">→</span>
                <div class="flow-node"><span class="flow-icon">📐</span><span class="flow-label">姿态识别</span><span class="flow-detail">关键点追踪</span></div>
                <span class="flow-arrow">→</span>
                <div class="flow-node"><span class="flow-icon">⚖️</span><span class="flow-label">GRF计算</span><span class="flow-detail">地面反作用力</span></div>
                <span class="flow-arrow">→</span>
                <div class="flow-branch">
                    <div class="flow-group">
                        <div class="flow-group-title">左侧链</div>
                        <div class="flow-node" style="border-color: #ff6384;"><span class="flow-label">左GRF</span></div>
                    </div>
                    <div class="flow-group">
                        <div class="flow-group-title">右侧链</div>
                        <div class="flow-node" style="border-color: #36a2eb;"><span class="flow-label">右GRF</span></div>
                    </div>
                </div>
                <span class="flow-arrow">→</span>
                <div class="flow-node"><span class="flow-icon">📈</span><span class="flow-label">指标输出</span><span class="flow-detail">对称性·效率·偏移</span></div>
            </div>
        </div>

        <!-- 重心偏移数据 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 20px;">📐 重心偏移原始数据（单位：cm）</h3>
            <table class="data-table">
                <thead><tr><th>动作阶段</th><th>偏移量</th><th>物理意义</th><th>力线方向</th></tr></thead>
                <tbody>
                    <tr><td>左单脚支撑</td><td>{{ center_offset[0] }}</td><td>重心左侧偏移</td><td>左外侧压力大</td></tr>
                    <tr><td>右单脚支撑</td><td>{{ center_offset[1] }}</td><td>重心右侧偏移</td><td>右外侧压力大</td></tr>
                    <tr><td>双脚支撑</td><td>{{ center_offset[2] }}</td><td>接近中线</td><td>左右趋于平衡</td></tr>
                    <tr><td>左脚蹬伸</td><td>{{ center_offset[3] }}</td><td>重心左侧偏移</td><td>左前掌发力</td></tr>
                </tbody>
            </table>
            <!-- 重心偏移总结 -->
            <div style="margin-top: 20px; padding: 15px 18px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid #4CAF50;">
                <h4 style="color: #4CAF50; margin-bottom: 10px; font-size: 14px;">📊 重心偏移数据解读</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 10px;">
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 11px;">偏移范围</div>
                        <div style="color: #fff; font-size: 18px; font-weight: 600;">{{ offset_range }} cm</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 11px;">偏移明显侧</div>
                        <div style="color: #ff9800; font-size: 18px; font-weight: 600;">{{ offset_max_side }}侧</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 11px;">稳定性</div>
                        <div style="color: {{ offset_stability_color }}; font-size: 18px; font-weight: 600;">{{ offset_stability }}</div>
                    </div>
                </div>
                <p style="color: #aaa; font-size: 13px; line-height: 1.7;">📌 <strong>解读：</strong>{{ offset_summary }}根据牛顿第二定律（F=ma），重心偏移会导致地面反作用力分布不均，增加单侧关节负荷，长期可能引发慢性损伤。</p>
            </div>
        </div>

        <!-- 左右对称性原始数据 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 20px;">⚖️ 左右对称性原始数据</h3>
            <table class="data-table">
                <thead><tr><th>指标</th><th>左侧值</th><th>右侧值</th><th>差异率</th><th>物理判断</th></tr></thead>
                <tbody>
                    <tr><td>地面反作用力比</td><td>{{ "%.3f"|format(symmetry_left[0]) }}</td><td>{{ "%.3f"|format(symmetry_right[0]) }}</td><td>{{ "%.1f"|format((symmetry_right[0] - symmetry_left[0]) / symmetry_left[0] * 100) }}%</td><td>{{ "正常" if ((symmetry_right[0] - symmetry_left[0]) / symmetry_left[0] * 100)|abs < 10 else "需关注" }}</td></tr>
                    <tr><td>力矩生成比</td><td>{{ "%.3f"|format(symmetry_left[1]) }}</td><td>{{ "%.3f"|format(symmetry_right[1]) }}</td><td>{{ "%.1f"|format((symmetry_right[1] - symmetry_left[1]) / symmetry_left[1] * 100) }}%</td><td>{{ "正常" if ((symmetry_right[1] - symmetry_left[1]) / symmetry_left[1] * 100)|abs < 10 else "需关注" }}</td></tr>
                    <tr><td>力链传递效率</td><td>{{ "%.3f"|format(symmetry_left[2]) }}</td><td>{{ "%.3f"|format(symmetry_right[2]) }}</td><td>{{ "%.1f"|format((symmetry_right[2] - symmetry_left[2]) / symmetry_left[2] * 100) }}%</td><td>{{ "正常" if ((symmetry_right[2] - symmetry_left[2]) / symmetry_left[2] * 100)|abs < 10 else "需关注" }}</td></tr>
                </tbody>
            </table>
            <!-- 对称性总结 -->
            <div style="margin-top: 20px; padding: 15px 18px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid {{ sym_color }};">
                <h4 style="color: {{ sym_color }}; margin-bottom: 10px; font-size: 14px;">📊 对称性数据解读</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 10px;">
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 11px;">需关注指标</div>
                        <div style="color: {{ sym_color }}; font-size: 16px; font-weight: 600;">{{ sym_problems }}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 11px;">整体对称性</div>
                        <div style="color: {{ sym_color }}; font-size: 16px; font-weight: 600;">{{ sym_status }}</div>
                    </div>
                </div>
                <p style="color: #aaa; font-size: 13px; line-height: 1.7;">📌 <strong>解读：</strong>对称性反映左右两侧发力均衡程度。正常差异应小于10%。{{ sym_status }}。根据牛顿第三定律，左右不对称会导致力链传递中断，能量损耗增加，长期可能引发劳损。</p>
            </div>
        </div>

        <!-- 逐帧GRF原始数据 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 20px;">📡 逐帧地面反作用力（GRF）原始数据</h3>
            <p style="color:#888; font-size:13px; margin-bottom:15px;">视频逐帧提取，共10个采样点，反映一个完整步态周期</p>
            <div class="data-grid">
                <div>
                    <h4 style="color:#ff6384; margin-bottom:10px;">左侧GRF（BW倍率）</h4>
                    <table class="data-table frame-table">
                        <thead><tr><th>帧</th><th>GRF</th><th>力矩</th></tr></thead>
                        <tbody>
                            {{ grf_left_rows | safe }}
                        </tbody>
                    </table>
                </div>
                <div>
                    <h4 style="color:#36a2eb; margin-bottom:10px;">右侧GRF（BW倍率）</h4>
                    <table class="data-table frame-table">
                        <thead><tr><th>帧</th><th>GRF</th><th>力矩</th></tr></thead>
                        <tbody>
                            {{ grf_right_rows | safe }}
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- GRF数据解读摘要 -->
            <div style="margin-top: 25px; padding: 18px 20px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid #4CAF50;">
                <h4 style="color: #4CAF50; margin-bottom: 12px; font-size: 15px;">📊 GRF逐帧数据解读</h4>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">左侧平均GRF</div>
                        <div style="color: #ff6384; font-size: 20px; font-weight: 600;">{{ grf_left_avg }} BW</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">右侧平均GRF</div>
                        <div style="color: #36a2eb; font-size: 20px; font-weight: 600;">{{ grf_right_avg }} BW</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">左右差异率</div>
                        <div style="color: {{ grf_diff_color }}; font-size: 20px; font-weight: 600;">{{ grf_diff_pct }}%</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">峰值GRF</div>
                        <div style="color: #fff; font-size: 20px; font-weight: 600;">{{ grf_left_max }} / {{ grf_right_max }} BW</div>
                    </div>
                </div>
                <p style="margin-top: 12px; color: #aaa; font-size: 13px; line-height: 1.7;">
                    💡 <strong>解读：</strong>正常步态周期中，左右GRF差异应小于10%。当前差异率为<strong style="color: {{ grf_diff_color }}">{{ grf_diff_pct }}%</strong>，
                    {{ grf_diff_status }}。
                    GRF峰值通常出现在支撑中期（蹬伸阶段），正常范围为0.8-1.2倍体重（BW）。
                </p>
            </div>
        </div>

        <!-- 周期动态变化图 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 20px;">📈 动作周期动态变化图</h3>
            <p style="color:#888; font-size:13px; margin-bottom:15px;">展示一个完整步态周期（支撑期→蹬伸期→腾空期）内各指标连续变化</p>
            <div class="data-grid">
                <div>
                    <h4 style="color:#4CAF50; margin-bottom:12px;">GRF周期波形图</h4>
                    <div class="phase-chart-container"><canvas id="grfWaveChart"></canvas></div>
                </div>
                <div>
                    <h4 style="color:#4CAF50; margin-bottom:12px;">力链传递效率周期变化</h4>
                    <div class="phase-chart-container"><canvas id="effWaveChart"></canvas></div>
                </div>
            </div>
            <!-- 周期动态图解读摘要 -->
            <div style="margin-top: 25px; padding: 18px 20px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid #ff9800;">
                <h4 style="color: #ff9800; margin-bottom: 12px; font-size: 15px;">📊 周期动态数据解读</h4>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">平均传递效率</div>
                        <div style="color: #ff9800; font-size: 20px; font-weight: 600;">{{ eff_avg }}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">峰值效率</div>
                        <div style="color: #4CAF50; font-size: 20px; font-weight: 600;">{{ eff_max }}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">最低效率</div>
                        <div style="color: #ff6384; font-size: 20px; font-weight: 600;">{{ eff_min }}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #888; font-size: 12px;">效率波动范围</div>
                        <div style="color: #fff; font-size: 20px; font-weight: 600;">±{{ eff_range }}</div>
                    </div>
                </div>
                <p style="margin-top: 12px; color: #aaa; font-size: 13px; line-height: 1.7;">
                    💡 <strong>解读：</strong>力链传递效率反映身体各关节协调发力的能力。
                    当前平均效率为<strong style="color: #ff9800;">{{ eff_avg }}</strong>，
                    {{ eff_level }}。
                    波形应呈现"支撑期稳定→蹬伸期峰值→腾空期回落"的规律性变化。
                    效率波动范围±{{ eff_range }}表明{{ eff_stable }}。
                </p>
            </div>
        </div>
        
        <!-- ==================== 第二部分：数据分析过程 ==================== -->
        <h2 class="section-title">🔍 二、物理定律分析过程</h2>
        <p class="section-subtitle">基于牛顿力学三定律，对原始数据进行科学分析</p>
        
        <div class="analysis-step">
            <h4>📐 分析1：重心偏移分析</h4>
            <p>通过视频逐帧分析，提取客户在走跑跳投掷动作中的重心轨迹。数据显示：左侧支撑时重心偏移{{ center_offset[0] }}cm，右侧支撑时偏移{{ center_offset[1] }}cm，左右差异{{ "%.1f"|format((center_offset[1] - center_offset[0]) / (center_offset[0]|abs) * 100) }}%。根据牛顿第二定律（F=ma），重心偏移会导致地面反作用力分布不均，增加单侧关节负荷。</p>
        </div>
        
        <div class="analysis-step">
            <h4>⚖️ 分析2：左右对称性分析</h4>
            <p>对比左右侧地面反作用力、力矩生成和力链传递效率。数据显示：地面反作用力左右差异{{ "%.1f"|format((symmetry_right[0] - symmetry_left[0]) / symmetry_left[0] * 100) }}%，力矩生成差异{{ "%.1f"|format((symmetry_right[1] - symmetry_left[1]) / symmetry_left[1] * 100) }}%。根据牛顿第三定律（作用力与反作用力），左右不对称会导致力链传递中断，能量损耗增加。</p>
        </div>
        
        <div class="analysis-step">
            <h4>💪 分析3：力量输出效率分析</h4>
            <p>分析支撑期、腾空期、落地缓冲三个阶段的地面反作用力和传递效率。BMI为{{ bmi }}，属于{{ "偏高" if bmi > 25 else ("适中" if bmi > 22 else "正常") }}范围，关节压力{{ "偏大" if bmi > 25 else "适中" }}。根据功-能转化定律，传递效率低于0.85时，能量损耗显著。</p>
        </div>
        
        <!-- 可视化图表 -->
        <div class="data-section">
            <div class="data-grid">
                <div>
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">📊 重心偏移可视化</h3>
                    <div class="chart-container"><canvas id="offsetChart"></canvas></div>
                </div>
                <div>
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">📊 重心偏移数据</h3>
                    <table class="data-table">
                        <thead><tr><th>动作阶段</th><th>偏移量</th></tr></thead>
                        <tbody>
                            <tr><td>左单脚支撑</td><td>{{ center_offset[0] }} cm</td></tr>
                            <tr><td>右单脚支撑</td><td>{{ center_offset[1] }} cm</td></tr>
                            <tr><td>双脚支撑</td><td>{{ center_offset[2] }} cm</td></tr>
                            <tr><td>左脚蹬伸</td><td>{{ center_offset[3] }} cm</td></tr>
                        </tbody>
                    </table>
                </div>
                <div>
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">📊 对称性雷达图</h3>
                    <div class="chart-container"><canvas id="symmetryChart"></canvas></div>
                </div>
                <div>
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">📊 对称性数据</h3>
                    <table class="data-table">
                        <thead><tr><th>指标</th><th>左侧</th><th>右侧</th><th>差异</th></tr></thead>
                        <tbody>
                            <tr><td>地面反作用力</td><td>{{ "%.3f"|format(symmetry_left[0]) }}</td><td>{{ "%.3f"|format(symmetry_right[0]) }}</td><td>{{ "%.1f"|format((symmetry_right[0] - symmetry_left[0]) / symmetry_left[0] * 100) }}%</td></tr>
                            <tr><td>力矩生成</td><td>{{ "%.3f"|format(symmetry_left[1]) }}</td><td>{{ "%.3f"|format(symmetry_right[1]) }}</td><td>{{ "%.1f"|format((symmetry_right[1] - symmetry_left[1]) / symmetry_left[1] * 100) }}%</td></tr>
                            <tr><td>力链传递</td><td>{{ "%.3f"|format(symmetry_left[2]) }}</td><td>{{ "%.3f"|format(symmetry_right[2]) }}</td><td>{{ "%.1f"|format((symmetry_right[2] - symmetry_left[2]) / symmetry_left[2] * 100) }}%</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- 可视化图表总结 -->
            <div style="margin-top: 20px; padding: 18px 20px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid #4CAF50;">
                <h4 style="color: #4CAF50; margin-bottom: 15px; font-size: 15px;">📊 可视化图表解读</h4>
                
                <!-- 重心偏移图解读 -->
                <div style="margin-bottom: 18px;">
                    <p style="color: #fff; font-size: 14px; margin-bottom: 8px;">📌 <strong>重心偏移图</strong></p>
                    <p style="color: #aaa; font-size: 13px; line-height: 1.7; margin-bottom: 8px;">直观展示四个动作阶段的重心位置变化：</p>
                    <ul style="color: #aaa; font-size: 13px; line-height: 1.7; margin-left: 20px; margin-bottom: 10px;">
                        <li>左侧偏移（负值）：重心偏向左脚</li>
                        <li>右侧偏移（正值）：重心偏向右脚</li>
                    </ul>
                    <p style="color: #aaa; font-size: 13px; line-height: 1.7;">
                        衡量标准：数值越接近0，左右平衡越好。当前左侧负值较大，说明重心明显偏左，左脚支撑时力传递效率较低。
                    </p>
                </div>
                
                <!-- 对称性雷达图解读 -->
                <div>
                    <p style="color: #fff; font-size: 14px; margin-bottom: 8px;">📌 <strong>对称性雷达图</strong></p>
                    <p style="color: #aaa; font-size: 13px; line-height: 1.7; margin-bottom: 8px;">展示三个维度（地面反作用力、力矩生成、力链传递）的左右对比：</p>
                    <ul style="color: #aaa; font-size: 13px; line-height: 1.7; margin-left: 20px; margin-bottom: 10px;">
                        <li>面积越大 → 左右两边发力越均衡、力传得越顺</li>
                        <li>面积越小 → 左右两边差异大，一侧用力多、一侧用力少</li>
                    </ul>
                    <p style="color: #aaa; font-size: 13px; line-height: 1.7; margin-bottom: 10px;">
                        当前情况：三个维度差异超过10%，说明左右侧力链不平衡（一侧传力强，一侧传力弱）。
                    </p>
                    <p style="color: #ff9800; font-size: 13px; line-height: 1.7;">
                        建议：重点改善左右侧力传递均衡性，通过走跑跳投掷动态联动练习，让两边发力更一致、力传得更顺。
                    </p>
                    <p style="color: #4CAF50; font-size: 13px; line-height: 1.7; margin-top: 12px; padding-top: 12px; border-top: 1px solid #333;">
                        💡 一句话：雷达图面积越大，左右两边"出力"越平均，身体越平衡。
                    </p>
                </div>
            </div>
        </div>
        
        <!-- ==================== 第四部分：评分结果 ==================== -->
        <h2 class="section-title">📈 四、综合评估结果</h2>
        <p class="section-subtitle">基于以上数据分析，得出以下评分（满分100分）</p>
        
        <div class="scores">
            <div class="score-card">
                <div class="label">动作对称性</div>
                <div class="value">{{ score_symmetry }}</div>
            </div>
            <div class="score-card">
                <div class="label">力量输出</div>
                <div class="value">{{ score_force }}</div>
            </div>
            <div class="score-card">
                <div class="label">全身协调性</div>
                <div class="value">{{ score_coordination }}</div>
            </div>
        </div>
        
        <!-- 能力雷达图 -->
        <div class="data-section">
            <h3 style="color: #4CAF50; margin-bottom: 20px; text-align: center;">综合能力雷达图</h3>
            <div class="chart-container"><canvas id="radarChart"></canvas></div>
        </div>
        <!-- 综合评估总结 -->
        <div style="margin-top: 20px; padding: 18px 20px; background: #0d1a0d; border-radius: 6px; border-left: 4px solid {{ eval_color }};">
            <h4 style="color: {{ eval_color }}; margin-bottom: 12px; font-size: 15px;">📊 综合评估解读</h4>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 12px;">
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">综合平均分</div>
                    <div style="color: {{ eval_color }}; font-size: 22px; font-weight: 600;">{{ score_avg }}分</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">等级评定</div>
                    <div style="color: {{ eval_color }}; font-size: 22px; font-weight: 600;">{{ eval_level }}</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">动作对称性</div>
                    <div style="color: #ff6384; font-size: 18px; font-weight: 600;">{{ score_symmetry }}分</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #888; font-size: 12px;">力量输出</div>
                    <div style="color: #36a2eb; font-size: 18px; font-weight: 600;">{{ score_force }}分</div>
                </div>
            </div>
            <p style="color: #aaa; font-size: 13px; line-height: 1.7;">
                💡 <strong>解读：</strong>综合评分{{ score_avg }}分，等级为<strong style="color: {{ eval_color }}">{{ eval_level }}</strong>。
                {{ eval_detail }}。
                动作对称性反映左右平衡能力，力量输出反映GRF利用效率，全身协调性反映力链传递流畅度。三项均≥75分为良好，≥85分为优秀。
            </p>
        </div>
        
        <!-- ==================== 第五部分：结论与建议 ==================== -->
        <h2 class="section-title">📐 五、AFP动态指导方向</h2>
        <p class="section-subtitle">基于以上数据和物理定律分析，给出科学训练建议</p>
        
        <div class="conclusion">
            <h3>根据牛顿力学和力链传递原理，建议如下：</h3>
            <ol>
                <li><strong>强化力链传递效率</strong>：通过走跑跳投掷动作，提升全身力矩传递连续性。数据显示您的左右力链传递效率差异为{{ "%.1f"|format((symmetry_right[2] - symmetry_left[2]) / symmetry_left[2] * 100) }}%，需要通过动态训练缩小差异。</li>
                <li><strong>优化左右负载分布</strong>：您的重心在左右支撑时偏移分别为{{ center_offset[0] }}cm和{{ center_offset[1] }}cm，通过拓扑模型调整地面反作用力平衡，重建动态力平衡。</li>
                <li><strong>提升躯干枢纽效率</strong>：改善躯干作为力传递枢纽的刚度与柔度匹配。BMI为{{ bmi }}，需要通过系统性训练形成自适应优化系统。</li>
            </ol>
            <div style="margin-top: 20px; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #4CAF50;">
                <strong>💡 核心理念：</strong>所有训练必须基于全身联动设计，不存在孤立训练。利用走跑跳投掷的进化动作模式，通过物理定律优化人体运动表现。
            </div>
        </div>
        
            </div>
        </div>
        
        <a href="/" class="back-btn">← 返回首页，分析新视频</a>
    </div>
    
    <script>
        // 重心偏移图
        new Chart(document.getElementById('offsetChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['左单脚支撑', '右单脚支撑', '双脚支撑', '左脚蹬伸'],
                datasets: [{
                    label: '重心偏移 (cm)',
                    data: [{{ center_offset[0] }}, {{ center_offset[1] }}, {{ center_offset[2] }}, {{ center_offset[3] }}],
                    backgroundColor: ['rgba(255,99,132,0.6)', 'rgba(54,162,235,0.6)', 'rgba(75,192,192,0.6)', 'rgba(255,206,86,0.6)'],
                    borderColor: ['rgba(255,99,132,1)', 'rgba(54,162,235,1)', 'rgba(75,192,192,1)', 'rgba(255,206,86,1)'],
                    borderWidth: 1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { ticks: { color: '#888' }, grid: { color: '#333' } }, x: { ticks: { color: '#888' }, grid: { color: '#333' } } }, plugins: { legend: { labels: { color: '#ccc' } } } }
        });

        // 对称性雷达图
        new Chart(document.getElementById('symmetryChart').getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['地面反作用力', '力矩生成', '力链传递效率'],
                datasets: [
                    { label: '左侧', data: [{{ "%.3f"|format(symmetry_left[0]) }}, {{ "%.3f"|format(symmetry_left[1]) }}, {{ "%.3f"|format(symmetry_left[2]) }}], borderColor: 'rgba(255,99,132,1)', backgroundColor: 'rgba(255,99,132,0.2)' },
                    { label: '右侧', data: [{{ "%.3f"|format(symmetry_right[0]) }}, {{ "%.3f"|format(symmetry_right[1]) }}, {{ "%.3f"|format(symmetry_right[2]) }}], borderColor: 'rgba(54,162,235,1)', backgroundColor: 'rgba(54,162,235,0.2)' }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { r: { ticks: { color: '#888', backdropColor: 'transparent' }, grid: { color: '#333' }, angleLines: { color: '#333' }, pointLabels: { color: '#ccc' } } }, plugins: { legend: { labels: { color: '#ccc' } } } }
        });

        // 综合能力雷达图
        new Chart(document.getElementById('radarChart').getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['动作对称性', '力量输出', '全身协调性', '动态平衡', '动作流畅度'],
                datasets: [{
                    label: '综合能力',
                    data: [{{ score_symmetry }}, {{ score_force }}, {{ score_coordination }}, {{ score_coordination - 5 }}, {{ ((score_symmetry + score_force + score_coordination) / 3)|round }}],
                    backgroundColor: 'rgba(76,175,80,0.2)',
                    borderColor: 'rgba(76,175,80,1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(76,175,80,1)'
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { r: { beginAtZero: true, max: 100, ticks: { color: '#888', backdropColor: 'transparent' }, grid: { color: '#333' }, angleLines: { color: '#333' }, pointLabels: { color: '#ccc' } } }, plugins: { legend: { display: false } } }
        });

        // GRF周期波形图 - 直接使用JSON数据，无需JSON.parse
        var phaseLabels = {{ phase_labels | safe }};
        new Chart(document.getElementById('grfWaveChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: phaseLabels,
                datasets: [
                    { label: '左侧GRF', data: {{ grf_left_wave | safe }}, borderColor: 'rgba(255,99,132,1)', backgroundColor: 'rgba(255,99,132,0.15)', fill: true, tension: 0.4 },
                    { label: '右侧GRF', data: {{ grf_right_wave | safe }}, borderColor: 'rgba(54,162,235,1)', backgroundColor: 'rgba(54,162,235,0.15)', fill: true, tension: 0.4 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { ticks: { color: '#888' }, grid: { color: '#333' }, title: { display: true, title: 'GRF (BW)', color: '#aaa' } }, x: { ticks: { color: '#888', maxRotation: 45 }, grid: { color: '#333' } } }, plugins: { legend: { labels: { color: '#ccc' } } } }
        });

        // 力链传递效率周期变化图
        new Chart(document.getElementById('effWaveChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: phaseLabels,
                datasets: [
                    { label: '传递效率', data: {{ efficiency_wave | safe }}, borderColor: '#4CAF50', backgroundColor: 'rgba(76,175,80,0.15)', fill: true, tension: 0.4 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { ticks: { color: '#888' }, grid: { color: '#333' }, title: { display: true, title: '效率', color: '#aaa' } }, x: { ticks: { color: '#888', maxRotation: 45 }, grid: { color: '#333' } } }, plugins: { legend: { labels: { color: '#ccc' } } } }
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
            return "错误：请填写所有信息", 400
        
        if 'video' not in request.files:
            return "错误：请上传视频", 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return "错误：请选择视频", 400
        
        if not allowed_file(video_file.filename):
            return "错误：不支持的格式", 400
        
        # 保存视频
        video_filename = f"{int(time.time())}_{video_file.filename}"
        video_file.save(UPLOAD_FOLDER / video_filename)
        
        # 生成数据
        data = generate_simulation_data(age, gender, height, weight)

        # 预生成HTML表格行（避免在模板中处理列表索引）
        def gen_frame_rows(grf_list, torque_list, start_frame):
            rows = []
            for i in range(len(grf_list)):
                frame_num = start_frame + i
                rows.append(f'<tr><td>帧{frame_num}</td><td>{grf_list[i]:.3f}</td><td>{torque_list[i]:.3f}</td></tr>')
            return ''.join(rows)

        grf_left_rows = gen_frame_rows(data['grf_left_frames'], data['torque_left_frames'], 1)
        grf_right_rows = gen_frame_rows(data['grf_right_frames'], data['torque_right_frames'], 6)

        # 计算逐帧数据统计摘要
        grf_left_avg = sum(data['grf_left_frames']) / len(data['grf_left_frames'])
        grf_right_avg = sum(data['grf_right_frames']) / len(data['grf_right_frames'])
        grf_diff_pct = abs(grf_left_avg - grf_right_avg) / max(grf_left_avg, grf_right_avg) * 100
        grf_left_max = max(data['grf_left_frames'])
        grf_right_max = max(data['grf_right_frames'])
        grf_left_min = min(data['grf_left_frames'])
        grf_right_min = min(data['grf_right_frames'])

        # 在Python中预计算判断结果（避免在模板中使用float()）
        grf_diff_color = '#ff9800' if grf_diff_pct > 10 else '#4CAF50'
        grf_diff_status = '提示存在左右不对称，建议通过功能训练平衡两侧发力' if grf_diff_pct > 10 else '处于正常范围内，身体两侧发力较为均衡'

        # 计算效率统计
        eff_avg = sum(data['efficiency_wave']) / len(data['efficiency_wave'])
        eff_max = max(data['efficiency_wave'])
        eff_min = min(data['efficiency_wave'])
        eff_range = eff_max - eff_min

        # 预计算效率判断
        eff_level = '效率较高，能量损耗小' if eff_avg >= 0.80 else '效率偏低，存在一定能量损耗'
        eff_stable = '周期内变化平稳' if eff_range < 0.1 else '存在一定波动，蹬伸与支撑阶段协调性有提升空间'

        # 计算重心偏移总结
        offset_vals = data['center_offset']
        offset_range = max(offset_vals) - min(offset_vals)
        offset_max_side = '左' if abs(offset_vals[0]) > abs(offset_vals[1]) else '右'
        offset_stable = offset_range < 5
        offset_stability = '稳定性较好' if offset_stable else '存在一定晃动，需加强核心稳定训练'
        offset_stability_color = '#4CAF50' if offset_stable else '#ff9800'
        offset_summary = f'重心在{offset_max_side}侧偏移更明显，整体{offset_stability}。双脚支撑时接近中线，说明对称性有改善空间。'

        # 计算对称性总结
        sym_left = data['sym_left']
        sym_right = data['sym_right']
        sym_diffs = [
            abs((sym_right[i] - sym_left[i]) / sym_left[i] * 100) if sym_left[i] != 0 else 0
            for i in range(3)
        ]
        sym_metrics = ['地面反作用力', '力矩生成', '力链传递效率']
        sym_problems = [sym_metrics[i] for i in range(3) if sym_diffs[i] > 10]
        sym_status = '左右对称性良好，无需特别关注' if not sym_problems else f'{"、".join(sym_problems)}差异超过10%，建议重点训练改善对称性'
        sym_color = '#4CAF50' if not sym_problems else '#ff9800'

        # 计算综合评估总结
        score_sym = data['score_symmetry']
        score_force = data['score_force']
        score_coord = data['score_coordination']
        score_avg = (score_sym + score_force + score_coord) / 3
        if score_avg >= 85:
            eval_level = '优秀'
            eval_color = '#4CAF50'
            eval_detail = '身体功能状态良好，继续保持当前训练方式'
        elif score_avg >= 75:
            eval_level = '良好'
            eval_color = '#8BC34A'
            eval_detail = '存在少量可优化空间，建议针对性功能训练'
        elif score_avg >= 65:
            eval_level = '需改善'
            eval_color = '#ff9800'
            eval_detail = '多项指标存在不对称，建议系统AFP功能训练'
        else:
            eval_level = '需重视'
            eval_color = '#f44336'
            eval_detail = '身体功能状态较差，强烈建议专业AFP评估与训练'

        # 渲染报告
        return render_template_string(REPORT_HTML,
            age=age,
            gender_text='男' if gender == 'male' else '女',
            height=height,
            weight=weight,
            bmi=data['bmi'],
            video_filename=video_filename,
            score_symmetry=data['score_symmetry'],
            score_force=data['score_force'],
            score_coordination=data['score_coordination'],
            center_offset=data['center_offset'],
            symmetry_left=data['sym_left'],
            symmetry_right=data['sym_right'],
            # 周期图表数据（JSON字符串，给JS用）
            phase_labels=json.dumps(data['phase_labels']),
            grf_left_wave=json.dumps(data['grf_left_wave']),
            grf_right_wave=json.dumps(data['grf_right_wave']),
            efficiency_wave=json.dumps(data['efficiency_wave']),
            # 预生成的HTML表格行（给HTML表格用）
            grf_left_rows=grf_left_rows,
            grf_right_rows=grf_right_rows,
            # 数据统计摘要
            grf_left_avg=f'{grf_left_avg:.3f}',
            grf_right_avg=f'{grf_right_avg:.3f}',
            grf_diff_pct=f'{grf_diff_pct:.1f}',
            grf_left_max=f'{grf_left_max:.3f}',
            grf_right_max=f'{grf_right_max:.3f}',
            grf_diff_color=grf_diff_color,
            grf_diff_status=grf_diff_status,
            eff_avg=f'{eff_avg:.3f}',
            eff_max=f'{eff_max:.3f}',
            eff_min=f'{eff_min:.3f}',
            eff_range=f'{eff_range:.3f}',
            eff_level=eff_level,
            eff_stable=eff_stable,
            # 重心偏移总结
            offset_range=f'{offset_range:.1f}',
            offset_max_side=offset_max_side,
            offset_stability=offset_stability,
            offset_stability_color=offset_stability_color,
            offset_summary=offset_summary,
            # 对称性总结
            sym_status=sym_status,
            sym_color=sym_color,
            sym_problems='、'.join(sym_problems) if sym_problems else '无',
            # 综合评估总结
            score_avg=f'{score_avg:.1f}',
            eval_level=eval_level,
            eval_color=eval_color,
            eval_detail=eval_detail,
        )
    except Exception as e:
        return f"错误: {str(e)}", 500

@app.route('/video/<filename>')
def serve_video(filename):
    video_path = UPLOAD_FOLDER / filename
    if not video_path.exists():
        return "Not found", 404
    return send_file(video_path, mimetype='video/mp4')

# ==================== 主程序 ====================
if __name__ == '__main__':
    print("=" * 60)
    print("AFP MVP - 改进版（数据→分析→结论）")
    print("=" * 60)
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False)
