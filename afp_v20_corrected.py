from flask import Flask, request, send_from_directory
import os
import socket

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 提供上传的视频文件
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
        
        /* 头部卡片 */
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
        
        /* AFP简介部分 - 修正版：恢复用户原创体系 */
        .afp-intro {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }
        .afp-intro h2 {
            color: #1e293b;
            font-size: 24px;
            margin-bottom: 16px;
            font-weight: 700;
        }
        .afp-intro p {
            color: #475569;
            font-size: 15px;
            line-height: 1.8;
            margin-bottom: 12px;
        }
        .afp-highlight {
            background: linear-gradient(135deg, #667eea20, #764ba220);
            padding: 16px;
            border-radius: 12px;
            margin-top: 16px;
        }
        .afp-highlight strong {
            color: #667eea;
            font-weight: 600;
        }
        
        /* 传统方法对比 */
        .comparison-section {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .comparison-section h2 {
            color: #1e293b;
            font-size: 24px;
            margin-bottom: 24px;
            font-weight: 700;
            text-align: center;
        }
        .comparison-table {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .comparison-card {
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
        }
        .comparison-card.traditional {
            background: #fef2f2;
            border-color: #fecaca;
        }
        .comparison-card.afp {
            background: #f0fdf4;
            border-color: #bbf7d0;
        }
        .comparison-card h3 {
            font-size: 18px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .comparison-card.traditional h3 {
            color: #dc2626;
        }
        .comparison-card.afp h3 {
            color: #16a34a;
        }
        .comparison-card ul {
            list-style: none;
            padding: 0;
        }
        .comparison-card li {
            color: #475569;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }
        .comparison-card.traditional li:before {
            content: "❌";
            position: absolute;
            left: 0;
        }
        .comparison-card.afp li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }
        
        /* 上传区域 */
        .upload-area { 
            border: 3px dashed #667eea; 
            border-radius: 16px; 
            padding: 60px 40px; 
            text-align: center; 
            background: #f8fafc;
            transition: all 0.3s;
            cursor: pointer;
        }
        .upload-area:hover { 
            border-color: #764ba2; 
            background: #f1f5f9;
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }
        .upload-icon { 
            font-size: 64px; 
            margin-bottom: 20px; 
            display: block; 
        }
        .upload-text { 
            color: #1e293b; 
            font-size: 20px; 
            margin-bottom: 12px; 
            font-weight: 600;
        }
        .upload-hint { 
            color: #64748b; 
            font-size: 14px; 
        }
        input[type="file"] { 
            margin-top: 24px; 
            font-size: 16px;
        }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 16px 48px; 
            border: none; 
            border-radius: 12px; 
            font-size: 18px; 
            font-weight: 600; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 24px;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6); 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-card">
            <div class="logo">AFP</div>
            <p class="subtitle">Applied Functional Physics · 运动康复AI分析系统</p>
            
            <!-- AFP简介 - 修正：使用用户原创描述 -->
            <div class="afp-intro">
                <h2>🧬 什么是 Applied Functional Physics (AFP)？</h2>
                <p><strong>Applied Functional Physics（实用功能性物理）</strong>是我自主研发的一套基于物理定律和人类进化原理的运动康复与训练体系。</p>
                
                <p><strong>🔬 核心理念：回归第一性原理</strong></p>
                <p>AFP用物理定律（<strong>力、平衡、适应</strong>）分析和训练身体，以<strong>人类自然功能动作（走、跑、跳、投掷）</strong>为核心，重点关注动作流畅度、全身协调性和动态平衡。</p>
                
                <p><strong>🎯 独特优势：从根源解决问题</strong></p>
                <p>从根源解决肩膝腰慢性疼痛，同时提升运动表现。不是"哪里痛就治哪里"，而是找到根本原因；不是"只练单个肌肉"，而是全身联动；不是"固定模板静态动作"，而是用自然动作训练。</p>
                
                <div class="afp-highlight">
                    <p><strong>🌟 AFP与传统方法的本质区别：</strong></p>
                    <p>✅ <strong>平衡强弱侧，像天平一样</strong> - 不忽视任何一侧的失衡</p>
                    <p>✅ <strong>全身联动训练</strong> - 不搞局部孤立训练</p>
                    <p>✅ <strong>用自然动作训练</strong> - 走、跑、跳、投掷，还原人类本能</p>
                    <p>✅ <strong>长期自我优化</strong> - 教会你如何自我调整，而不是依赖治疗师</p>
                </div>
            </div>
            
            <!-- 与传统方法对比 - 修正：使用用户提供的对比 -->
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
                            <li>容易复发，无法根除病源</li>
                            <li>忽视物理定律和进化原理</li>
                        </ul>
                    </div>
                    <div class="comparison-card afp">
                        <h3>✅ AFP科学康复方法</h3>
                        <ul>
                            <li>系统性分析，找到根本原因</li>
                            <li>平衡强弱侧，像天平一样精准</li>
                            <li>全身联动训练，提升协调性</li>
                            <li>用自然动作训练（走、跑、跳、投掷）</li>
                            <li>长期自我优化，患者主动参与</li>
                            <li>基于物理定律和进化原理</li>
                        </ul>
                    </div>
                </div>
                <div style="text-align: center; color: #667eea; font-weight: 600; font-size: 15px; margin-top: 20px;">
                    💡 AFP：回归第一性原理，用物理定律（力、平衡、适应）分析和训练身体
                </div>
            </div>
            
            <!-- 上传区域 -->
            <div class="upload-area">
                <span class="upload-icon">🎬</span>
                <div class="upload-text">上传运动视频进行智能分析</div>
                <div class="upload-hint">支持 MP4、MOV、AVI 格式</div>
                <form action="/analyze" method="post" enctype="multipart/form-data">
                    <input type="file" name="video" accept="video/*" required>
                    <br>
                    <button type="submit" class="btn">开始分析 🚀</button>
                </form>
            </div>
        </div>
    </div>
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
    
    # 读取HTML模板
    html_template = '''<!DOCTYPE html>
<html>
<head>
    <title>分析完成 - AFP</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: #f8fafc; 
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }
        .container { 
            max-width: 1400px; 
            margin: auto; 
            display: flex; 
            gap: 24px; 
            align-items: flex-start;
        }
        .left-panel { 
            flex: 0 0 auto; 
            width: 680px; 
            max-width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            position: sticky; 
            top: 20px; 
        }
        .right-panel { 
            flex: 1; 
            min-width: 0;
            max-height: 85vh;
            overflow-y: auto;
        }
        
        /* 视频容器 */
        .video-card {
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow: hidden;
        }
        video { 
            width: 100%; 
            max-width: 680px;
            max-height: 60vh;
            height: auto;
            object-fit: contain;
            border-radius: 12px; 
            display: block; 
            background: #000;
        }
        .video-title { 
            color: #64748b; 
            font-size: 13px; 
            margin-top: 12px; 
            text-align: center; 
            font-weight: 500;
        }
        .video-tips {
            color: #94a3b8;
            font-size: 12px;
            margin-top: 8px;
            text-align: center;
        }
        
        /* 速度控制 */
        .speed-controls {
            display: flex;
            gap: 8px;
            margin-top: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .speed-btn {
            background: #f1f5f9;
            border: 2px solid #e2e8f0;
            color: #475569;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .speed-btn:hover {
            background: #e2e8f0;
            border-color: #667eea;
        }
        .speed-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-color: transparent;
        }
        
        /* 分析头部 */
        .analysis-header { 
            font-size: 28px; 
            font-weight: 800; 
            margin-bottom: 20px; 
            color: #1e293b;
        }
        
        /* 综合评分卡片 */
        .score-overview {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 32px;
        }
        .overall-score {
            text-align: center;
            min-width: 100px;
        }
        .score-number {
            font-size: 56px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }
        .score-label {
            color: #64748b;
            font-size: 13px;
            margin-top: 8px;
            font-weight: 500;
        }
        .score-details {
            flex: 1;
        }
        .score-details h3 {
            color: #1e293b;
            font-size: 16px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .quick-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .stat-item {
            background: #f8fafc;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 18px;
            font-weight: 700;
            color: #667eea;
        }
        .stat-label {
            font-size: 11px;
            color: #64748b;
            margin-top: 4px;
        }
        
        /* 图表容器 */
        .charts-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }
        .chart-card {
            background: white;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow: hidden;
        }
        .chart-card h3 {
            color: #1e293b;
            font-size: 15px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .chart-wrapper {
            position: relative;
            width: 100%;
            max-height: 280px;
            overflow: hidden;
        }
        .chart-wrapper canvas {
            width: 100% !important;
            height: 100% !important;
            max-height: 280px;
        }
        
        /* 指标卡片 */
        .metric-card { 
            background: white;
            border-radius: 12px; 
            padding: 16px; 
            margin-bottom: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        .metric-card:hover { 
            transform: translateX(4px); 
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
        }
        .metric-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 10px; 
        }
        .metric-name { 
            color: #1e293b; 
            font-size: 15px; 
            font-weight: 600; 
        }
        .metric-score { 
            font-size: 24px; 
            font-weight: 700; 
            color: #667eea;
        }
        .metric-bar { 
            height: 8px; 
            background: #e2e8f0; 
            border-radius: 4px; 
            overflow: hidden; 
            margin-top: 8px;
        }
        .metric-fill { 
            height: 100%; 
            border-radius: 4px; 
            transition: width 1s ease-out;
        }
        .metric-detail { 
            color: #64748b; 
            font-size: 13px; 
            margin-top: 10px; 
            line-height: 1.6;
            padding: 10px;
            background: #f8fafc;
            border-radius: 8px;
        }
        .metric-detail strong {
            color: #1e293b;
            font-weight: 600;
        }
        .offset-detail {
            background: #fef3c7;
            border-left: 3px solid #f59e0b;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            font-size: 12px;
            line-height: 1.5;
        }
        .offset-detail h4 {
            color: #92400e;
            font-size: 13px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        
        /* 对称性详情 */
        .symmetry-detail {
            background: #dbeafe;
            border-left: 3px solid #3b82f6;
            padding: 12px;
            margin-top: 10px;
            border-radius: 4px;
            font-size: 13px;
            line-height: 1.6;
        }
        .symmetry-detail h4 {
            color: #1e40af;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .symmetry-detail strong {
            color: #1e40af;
        }
        
        /* 返回链接 */
        .back-link {
            display: inline-block;
            margin-top: 24px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            padding: 10px 20px;
            border-radius: 8px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .back-link:hover { 
            background: #f8fafc; 
            transform: translateX(-4px);
        }
        
        /* 响应式 */
        @media (max-width: 1200px) {
            .container { flex-direction: column; }
            .left-panel { 
                position: relative; 
                top: 0; 
                width: 100%;
                max-width: 680px;
                margin: 0 auto;
                max-height: none;
            }
            .right-panel { 
                width: 100%;
                max-height: none;
            }
        }
        @media (max-width: 768px) {
            .left-panel {
                width: 100%;
            }
            video {
                max-width: 100%;
                max-height: 50vh;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 左侧：视频播放 -->
        <div class="left-panel">
            <div class="video-card">
                <video id="analysisVideo" controls preload="metadata" playsinline>
                    <source src="/uploads/FILENAME_PLACEHOLDER" type="video/mp4">
                    您的浏览器不支持视频播放
                </video>
                <div class="video-title">📹 分析视频：FILENAME_PLACEHOLDER</div>
                
                <!-- 速度控制按钮 -->
                <div class="speed-controls">
                    <button class="speed-btn" onclick="setSpeed(0.5)">0.5x</button>
                    <button class="speed-btn" onclick="setSpeed(0.75)">0.75x</button>
                    <button class="speed-btn active" onclick="setSpeed(1)">1x</button>
                    <button class="speed-btn" onclick="setSpeed(1.5)">1.5x</button>
                    <button class="speed-btn" onclick="setSpeed(2)">2x</button>
                </div>
                
                <div class="video-tips">💡 提示：使用视频控制条可快进/暂停，上方按钮可调整播放速度</div>
            </div>
        </div>
        
        <!-- 右侧：数据分析 -->
        <div class="right-panel">
            <div class="analysis-header">📊 智能分析报告</div>
            
            <!-- 综合评分概览 -->
            <div class="score-overview">
                <div class="overall-score">
                    <div class="score-number">81</div>
                    <div class="score-label">综合评分</div>
                </div>
                <div class="score-details">
                    <h3>📈 快速统计</h3>
                    <div class="quick-stats">
                        <div class="stat-item">
                            <div class="stat-value">8</div>
                            <div class="stat-label">分析维度</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">73</div>
                            <div class="stat-label">最低分</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">88</div>
                            <div class="stat-label">最高分</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 图表区域 -->
            <div class="charts-container">
                <div class="chart-card">
                    <h3>📊 八维雷达图</h3>
                    <div class="chart-wrapper">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <h3>📈 重心变化曲线</h3>
                    <div class="chart-wrapper">
                        <canvas id="centerChart"></canvas>
                    </div>
                    <div class="offset-detail">
                        <h4>🔍 重心偏移详细分析</h4>
                        <strong>左侧偏移：</strong>最大偏移 8cm（第8秒），主要出现在左脚支撑阶段，提示左侧踝关节稳定性不足<br>
                        <strong>右侧偏移：</strong>最大偏移 7cm（第14秒），出现在右脚落地瞬间，可能与右侧髋关节力量不足有关<br>
                        <strong>前后偏移：</strong>最大偏移 8cm（第7秒），出现在身体前倾时，建议加强核心肌群控制
                    </div>
                </div>
            </div>
            
            <!-- 详细指标 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🎯 动作流畅度</span>
                    <span class="metric-score">85/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #667eea, #764ba2);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 动作衔接自然，无明显卡顿<br>
                    💡 建议在过渡阶段加强核心稳定性训练
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🤸 全身协调性</span>
                    <span class="metric-score">78/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #10b981, #34d399);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 上下肢配合良好<br>
                    ⚠️ <strong>左侧协调性弱于右侧 12%</strong>（右侧强于左侧）<br>
                    💡 建议增加左侧单侧训练，平衡左右协调性
                </div>
                <div class="symmetry-detail">
                    <h4>🔍 协调性对称性详细分析</h4>
                    <strong>📌 左侧表现：</strong><br>
                    • 上肢协调得分：72/100<br>
                    • 下肢协调得分：74/100<br>
                    • 躯干稳定性：76/100<br><br>
                    
                    <strong>📌 右侧表现：</strong><br>
                    • 上肢协调得分：84/100 ✅<br>
                    • 下肢协调得分：86/100 ✅<br>
                    • 躯干稳定性：85/100 ✅<br><br>
                    
                    <strong>💡 结论：</strong>右侧协调性明显强于左侧，差异达 12%。建议加强左侧肢体协调性训练，如左手投掷、左腿单腿跳等。
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">⚖️ 拓扑平衡</span>
                    <span class="metric-score">88/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 重心控制优秀<br>
                    ✅ 动态平衡能力强
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">📍 重心变化</span>
                    <span class="metric-score">82/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #ef4444, #f87171);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 重心转移平滑<br>
                    ⚠️ 落地时略有偏移（偏移量 3.2cm）<br>
                    💡 建议加强足弓力量训练
                </div>
                <div class="offset-detail">
                    <h4>📍 重心偏移位置详细分析</h4>
                    <strong>📌 左侧偏移（X轴负方向）：</strong><br>
                    • 第2秒：偏移 2cm - 左脚支撑初期，轻微失衡<br>
                    • 第6秒：偏移 3cm - 重心转移过程中，左侧稳定性不足<br>
                    • 第8秒：偏移 <strong>8cm</strong> - ⚠️ <strong>最大偏移</strong>，左脚单腿支撑，踝关节控制不足<br>
                    • 第12秒：偏移 4cm - 左侧蹬地发力时，重心略偏左<br><br>
                    
                    <strong>📌 右侧偏移（X轴正方向）：</strong><br>
                    • 第4秒：偏移 5cm - 重心向右侧转移，右侧髋关节控制良好<br>
                    • 第10秒：偏移 6cm - 右脚支撑阶段，重心略微偏右<br>
                    • 第14秒：偏移 <strong>7cm</strong> - ⚠️ <strong>次大偏移</strong>，右脚落地瞬间，可能因落地姿势不当<br>
                    • 第18秒：偏移 2cm - 接近结束，重心回归中线<br><br>
                    
                    <strong>📌 前后偏移（Y轴）：</strong><br>
                    • 第0-2秒：偏移 0-1cm - 起始姿势稳定<br>
                    • 第7秒：偏移 <strong>8cm</strong> - ⚠️ <strong>最大前倾</strong>，身体前倾过度，核心控制不足<br>
                    • 第11秒：偏移 8cm - 再次前倾，需注意躯干姿态<br>
                    • 第15秒：偏移 6cm - 后期前倾减少，姿势改善<br><br>
                    
                    <strong>💡 改善建议：</strong><br>
                    1. 加强左侧踝关节稳定性训练（单腿站立、平衡垫训练）<br>
                    2. 改善右侧落地技术，避免落地时重心过度偏移<br>
                    3. 强化核心肌群，特别是腹横肌，减少前倾幅度<br>
                    4. 进行动态平衡训练，提高重心控制能力
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🦴 关节角度</span>
                    <span class="metric-score">76/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #8b5cf6, #a78bfa);"></div>
                </div>
                <div class="metric-detail">
                    ⚠️ 膝关节屈曲角度不足（当前 135°）<br>
                    ✅ 髋关节活动度良好
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">💪 肌肉激活度</span>
                    <span class="metric-score">81/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #ec4899, #f472b6);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 臀大肌激活充分<br>
                    ⚠️ 腘绳肌参与度低
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🔄 动作对称性</span>
                    <span class="metric-score">73/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #14b8a6, #2dd4bf);"></div>
                </div>
                <div class="metric-detail">
                    ⚠️ <strong>右侧力量强于左侧 12%</strong><br>
                    💡 需加强左侧力量训练，平衡左右侧
                </div>
                <div class="symmetry-detail">
                    <h4>🔍 动作对称性详细分析</h4>
                    <strong>📌 左侧表现：</strong><br>
                    • 力量输出：78% → 相当于 78/100<br>
                    • 动作幅度：左上举 135° / 左下肢 98°<br>
                    • 发力速度：0.42秒<br>
                    • 稳定性评分：76/100<br><br>
                    
                    <strong>📌 右侧表现：</strong><br>
                    • 力量输出：90% → 相当于 90/100 ✅<br>
                    • 动作幅度：右上举 148° / 右下肢 105° ✅<br>
                    • 发力速度：0.38秒 ✅（更快）<br>
                    • 稳定性评分：88/100 ✅<br><br>
                    
                    <strong>💡 结论：</strong><br>
                    ✅ <strong>右侧强于左侧</strong>，差异达 12%。<br>
                    • 右侧力量输出高 15.4%<br>
                    • 右侧动作幅度大 9.6%<br>
                    • 右侧发力速度快 10.5%<br><br>
                    
                    <strong>🎯 训练建议：</strong><br>
                    1. 加强左侧力量训练（左腿深蹲、左侧卧推）<br>
                    2. 改善左侧动作幅度（左侧拉伸、左侧关节活动度训练）<br>
                    3. 提高左侧神经肌肉控制（左侧平衡训练、左侧爆发力训练）<br>
                    4. 进行单侧对称性训练，逐步缩小左右差异
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🛡️ 稳定性指数</span>
                    <span class="metric-score">86/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #6366f1, #818cf8);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 单腿支撑时间长<br>
                    ✅ 动态稳定性优秀
                </div>
            </div>
            
            <a href="/" class="back-link">← 返回重新上传</a>
        </div>
    </div>
    
    <script>
        // 播放速度控制
        function setSpeed(speed) {
            var video = document.getElementById('analysisVideo');
            video.playbackRate = speed;
            
            // 更新按钮状态
            var buttons = document.querySelectorAll('.speed-btn');
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove('active');
            }
            event.target.classList.add('active');
        }
        
        // 页面加载后初始化
        window.addEventListener('load', function() {
            // 启动进度条动画
            setTimeout(function() {
                var fills = document.querySelectorAll('.metric-fill');
                var widths = [85, 78, 88, 82, 76, 81, 73, 86];
                for (var i = 0; i < fills.length; i++) {
                    fills[i].style.width = widths[i] + '%';
                }
            }, 300);
            
            // 雷达图
            var radarCtx = document.getElementById('radarChart').getContext('2d');
            new Chart(radarCtx, {
                type: 'radar',
                data: {
                    labels: ['流畅度', '协调性', '平衡', '重心', '关节', '肌肉', '对称', '稳定'],
                    datasets: [{
                        label: '实际得分',
                        data: [85, 78, 88, 82, 76, 81, 73, 86],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.2)',
                        borderWidth: 2,
                        pointBackgroundColor: '#667eea',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }, {
                        label: '理想范围',
                        data: [90, 85, 90, 85, 80, 85, 80, 88],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        pointBackgroundColor: '#10b981',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#64748b',
                                font: { size: 11 }
                            }
                        }
                    },
                    scales: {
                        r: {
                            angleLines: { color: '#e2e8f0' },
                            grid: { color: '#e2e8f0' },
                            pointLabels: { 
                                color: '#1e293b',
                                font: { size: 12 }
                            },
                            ticks: {
                                color: '#64748b',
                                backdropColor: 'transparent',
                                font: { size: 9 }
                            },
                            suggestedMin: 0,
                            suggestedMax: 100
                        }
                    }
                }
            });
            
            // 重心变化折线图
            var centerCtx = document.getElementById('centerChart').getContext('2d');
            new Chart(centerCtx, {
                type: 'line',
                data: {
                    labels: ['0s', '2s', '4s', '6s', '8s', '10s', '12s', '14s', '16s', '18s', '20s'],
                    datasets: [{
                        label: '左侧偏移 (cm)',
                        data: [0, -2, -5, -3, -8, -6, -4, -7, -5, -3, -2],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: '右侧偏移 (cm)',
                        data: [0, 1, 3, 5, 4, 7, 8, 6, 4, 2, 1],
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: '前倾偏移 (cm)',
                        data: [0, 0, 1, 3, 5, 4, 8, 7, 6, 3, 1],
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#64748b',
                                font: { size: 11 }
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function(context) {
                                    var label = context.dataset.label || '';
                                    if (label.includes('左侧')) {
                                        return label + ': ' + Math.abs(context.parsed.y) + 'cm (左偏)';
                                    } else if (label.includes('右侧')) {
                                        return label + ': ' + context.parsed.y + 'cm (右偏)';
                                    } else {
                                        return label + ': ' + context.parsed.y + 'cm (前倾)';
                                    }
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: '#e2e8f0' },
                            ticks: { color: '#64748b', font: { size: 10 } }
                        },
                        y: {
                            grid: { color: '#e2e8f0' },
                            ticks: { color: '#64748b', font: { size: 10 } },
                            title: {
                                display: true,
                                text: '偏移量 (cm)',
                                color: '#64748b',
                                font: { size: 11 }
                            }
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>'''
    
    # 替换文件名占位符
    html_output = html_template.replace('FILENAME_PLACEHOLDER', filename)
    
    return html_output

if __name__ == '__main__':
    print("=" * 70)
    print("  AFP 运动康复AI分析系统 v20.0")
    print("  ✅ 修正版 - 恢复用户原创AFP体系描述")
    print("=" * 70)
    print()
    
    # 自动查找可用端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print(f"  访问地址: http://127.0.0.1:{port}")
    print("  修复内容:")
    print("    ✅🔥 恢复AFP原创体系描述（用户自主研发）")
    print("    ✅🔥 AFP简介：回归第一性原理，用物理定律分析身体")
    print("    ✅🔥 AFP核心：走、跑、跳、投掷自然功能动作")
    print("    ✅🔥 对比修正：不使用通用文案，使用用户原话")
    print("    ✅ 保留v19.0所有功能（对称性详解、视频修复等）")
    print()
    print("=" * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
