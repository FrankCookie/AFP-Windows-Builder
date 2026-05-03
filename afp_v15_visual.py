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
    <title>AFP 智能运动分析</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: #0f0f0f; 
            color: #e2e8f0; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
        }
        .container { max-width: 900px; width: 100%; }
        h1 { 
            font-size: 56px; 
            font-weight: 800; 
            text-align: center; 
            margin-bottom: 12px; 
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }
        .subtitle { 
            text-align: center; 
            color: #64748b; 
            margin-bottom: 60px; 
            font-size: 16px; 
            letter-spacing: 0.5px;
            font-weight: 400;
        }
        .upload-box { 
            border: 2px dashed #1e293b; 
            border-radius: 24px; 
            padding: 80px 40px; 
            text-align: center; 
            background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .upload-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        .upload-box:hover { 
            border-color: #3b82f6; 
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(59, 130, 246, 0.2);
        }
        .upload-box:hover::before {
            opacity: 1;
        }
        .upload-icon { 
            font-size: 56px; 
            margin-bottom: 24px; 
            display: block; 
            filter: grayscale(0.2);
        }
        .upload-text { 
            color: #94a3b8; 
            font-size: 18px; 
            margin-bottom: 8px; 
            font-weight: 500;
        }
        .upload-hint { 
            color: #64748b; 
            font-size: 14px; 
        }
        input[type="file"] { 
            margin-top: 24px; 
            color: #e2e8f0; 
            font-size: 14px;
            background: transparent;
        }
        input[type="file"]::-webkit-file-upload-button {
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-right: 12px;
            transition: all 0.3s;
        }
        input[type="file"]::-webkit-file-upload-button:hover {
            background: #334155;
            border-color: #3b82f6;
        }
        button { 
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); 
            color: white; 
            padding: 18px 48px; 
            border: none; 
            border-radius: 16px; 
            font-size: 17px; 
            font-weight: 600; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 32px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }
        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4); 
        }
        button:hover::before {
            left: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AFP</h1>
        <p class="subtitle">Applied Functional Physics · 智能运动分析系统 v15.0</p>
        
        <div class="upload-box">
            <span class="upload-icon">🎬</span>
            <div class="upload-text">上传运动视频进行AI智能分析</div>
            <div class="upload-hint">支持 MP4、MOV、AVI 格式 · 最大 500MB</div>
            <form action="/analyze" method="post" enctype="multipart/form-data" id="uploadForm">
                <input type="file" name="video" accept="video/*" required id="fileInput">
                <br>
                <button type="submit" id="submitBtn">开始智能分析 🚀</button>
            </form>
        </div>
    </div>
    
    <script>
        // 文件选择反馈
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                document.querySelector('.upload-text').textContent = `已选择: ${fileName}`;
                document.querySelector('.upload-hint').textContent = '点击按钮开始分析';
            }
        });
        
        // 提交时显示加载状态
        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('submitBtn').textContent = '正在分析视频中...';
            document.getElementById('submitBtn').disabled = true;
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
    
    # 模拟详细分析结果 - v15.0 专业可视化版
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>分析完成 - AFP v15.0</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: #0f0f0f; 
            color: #e2e8f0; 
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ 
            max-width: 1600px; 
            margin: auto; 
            display: flex; 
            gap: 40px; 
            align-items: flex-start;
        }}
        .left-panel {{ 
            flex: 1; 
            max-width: 640px; 
            position: sticky; 
            top: 40px; 
        }}
        .right-panel {{ 
            flex: 1.2; 
            max-width: 900px; 
        }}
        
        /* 视频容器 */
        .video-container {{ 
            background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
            border-radius: 20px; 
            padding: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            border: 1px solid #1e293b;
        }}
        video {{ 
            width: 100%; 
            border-radius: 12px; 
            display: block; 
        }}
        .video-title {{ 
            color: #94a3b8; 
            font-size: 14px; 
            margin-top: 16px; 
            text-align: center; 
            font-weight: 500;
        }}
        
        /* 分析头部 */
        .analysis-header {{ 
            font-size: 36px; 
            font-weight: 800; 
            margin-bottom: 32px; 
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }}
        
        /* 综合评分卡片 */
        .score-overview {{
            background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
            border: 1px solid #1e293b;
            display: flex;
            align-items: center;
            gap: 40px;
            animation: fadeInUp 0.6s ease-out;
        }}
        .overall-score {{
            text-align: center;
            min-width: 150px;
        }}
        .score-number {{
            font-size: 72px;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }}
        .score-label {{
            color: #64748b;
            font-size: 14px;
            margin-top: 8px;
            font-weight: 500;
        }}
        .score-details {{
            flex: 1;
        }}
        .score-details h3 {{
            color: #e2e8f0;
            font-size: 20px;
            margin-bottom: 16px;
            font-weight: 600;
        }}
        .quick-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }}
        .stat-item {{
            background: #0f172a;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #60a5fa;
        }}
        .stat-label {{
            font-size: 12px;
            color: #64748b;
            margin-top: 4px;
        }}
        
        /* 图表容器 */
        .charts-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        .chart-card {{
            background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
            border-radius: 20px;
            padding: 24px;
            border: 1px solid #1e293b;
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        .chart-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .chart-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .chart-card h3 {{
            color: #e2e8f0;
            font-size: 18px;
            margin-bottom: 16px;
            font-weight: 600;
        }}
        .chart-card canvas {{
            width: 100% !important;
            height: 250px !important;
        }}
        
        /* 指标卡片 */
        .metric-card {{ 
            background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
            border-radius: 16px; 
            padding: 24px; 
            margin-bottom: 20px; 
            border: 1px solid #1e293b;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        .metric-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .metric-card:nth-child(2) {{ animation-delay: 0.15s; }}
        .metric-card:nth-child(3) {{ animation-delay: 0.2s; }}
        .metric-card:nth-child(4) {{ animation-delay: 0.25s; }}
        .metric-card:nth-child(5) {{ animation-delay: 0.3s; }}
        .metric-card:nth-child(6) {{ animation-delay: 0.35s; }}
        .metric-card:nth-child(7) {{ animation-delay: 0.4s; }}
        .metric-card:nth-child(8) {{ animation-delay: 0.45s; }}
        .metric-card:hover {{ 
            border-color: #3b82f6; 
            transform: translateX(8px) translateY(-2px); 
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        }}
        .metric-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 16px; 
        }}
        .metric-name {{ 
            color: #94a3b8; 
            font-size: 16px; 
            font-weight: 500; 
        }}
        .metric-score {{ 
            font-size: 32px; 
            font-weight: 700; 
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .metric-bar {{ 
            height: 10px; 
            background: #0f172a; 
            border-radius: 5px; 
            overflow: hidden; 
            margin-top: 12px;
            position: relative;
        }}
        .metric-fill {{ 
            height: 100%; 
            border-radius: 5px; 
            transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}
        .metric-fill::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}
        .metric-detail {{ 
            color: #64748b; 
            font-size: 14px; 
            margin-top: 16px; 
            line-height: 1.6;
            padding: 12px;
            background: #0f172a;
            border-radius: 8px;
        }}
        
        /* 返回链接 */
        .back-link {{
            display: inline-block;
            margin-top: 40px;
            color: #60a5fa;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.3s;
            padding: 12px 24px;
            border-radius: 12px;
            background: #111827;
            border: 1px solid #1e293b;
        }}
        .back-link:hover {{ 
            background: #1e293b; 
            border-color: #3b82f6;
            transform: translateX(-4px);
        }}
        
        /* 动画 */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        /* 响应式 */
        @media (max-width: 1200px) {{
            .container {{ flex-direction: column; }}
            .left-panel, .right-panel {{ max-width: 100%; }}
            .left-panel {{ position: relative; top: 0; }}
            .charts-container {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 左侧：视频播放 -->
        <div class="left-panel">
            <div class="video-container">
                <video controls autoplay>
                    <source src="/uploads/{filename}" type="video/mp4">
                    您的浏览器不支持视频播放
                </video>
                <div class="video-title">📹 分析视频：{filename}</div>
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
                        <div class="stat-item">
                            <div class="stat-value">6/8</div>
                            <div class="stat-label">达标指标</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">12%</div>
                            <div class="stat-label">左右差异</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">优</div>
                            <div class="stat-label">总体评价</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 图表区域 -->
            <div class="charts-container">
                <div class="chart-card">
                    <h3>📊 八维雷达图</h3>
                    <canvas id="radarChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>📈 重心变化曲线</h3>
                    <canvas id="centerChart"></canvas>
                </div>
            </div>
            
            <!-- 详细指标 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🎯 动作流畅度</span>
                    <span class="metric-score">85/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 动作衔接自然，无明显卡顿<br>
                    💡 建议在过渡阶段加强 core 稳定性训练<br>
                    📌 关键帧分析：第12秒处动作略有停顿
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🤸 全身协调性</span>
                    <span class="metric-score">78/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #8b5cf6, #a78bfa);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 上下肢配合良好<br>
                    ⚠️ 左右对称性需改善（差异 12%）<br>
                    💡 建议增加单侧训练，如单腿深蹲
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">⚖️ 拓扑平衡</span>
                    <span class="metric-score">88/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #10b981, #34d399);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 重心控制优秀<br>
                    ✅ 动态平衡能力强<br>
                    💡 继续保持当前训练强度
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">📍 重心变化</span>
                    <span class="metric-score">82/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
                </div>
                <div class="metric-detail">
                    ✅ 重心转移平滑<br>
                    ⚠️ 落地时略有偏移（偏移量 3.2cm）<br>
                    💡 建议加强足弓力量和本体感觉训练
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🦴 关节角度</span>
                    <span class="metric-score">76/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 0%; background: linear-gradient(90deg, #ef4444, #f87171);"></div>
                </div>
                <div class="metric-detail">
                    ⚠️ 膝关节屈曲角度不足（当前 135°，理想 150°）<br>
                    ✅ 髋关节活动度良好（活动范围 120°）<br>
                    💡 建议增加膝关节灵活性训练
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
                    ✅ 臀大肌激活充分（激活度 85%）<br>
                    ⚠️ 腘绳肌参与度低（激活度 45%）<br>
                    💡 建议增加 hip hinge 动作训练
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
                    ⚠️ 左右侧差异 12%（正常 &lt;8%）<br>
                    ⚠️ 右侧力量较强（右 85% vs 左 73%）<br>
                    💡 需平衡训练，加强左侧力量
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
                    ✅ 单腿支撑时间长（平均 3.2秒）<br>
                    ✅ 动态稳定性优秀<br>
                    ⚠️ 踝关节稳定性需稍加强（摆动幅度 8°）
                </div>
            </div>
            
            <a href="/" class="back-link">← 返回重新上传</a>
        </div>
    </div>
    
    <script>
        // 页面加载后初始化图表和动画
        window.addEventListener('load', function() {{
            // 延迟启动动画，让页面先渲染
            setTimeout(() => {{
                // 启动进度条动画
                document.querySelectorAll('.metric-fill').forEach((fill, index) => {{
                    const widths = [85, 78, 88, 82, 76, 81, 73, 86];
                    fill.style.width = widths[index] + '%';
                }});
            }}, 300);
            
            // 雷达图
            const radarCtx = document.getElementById('radarChart').getContext('2d');
            new Chart(radarCtx, {{
                type: 'radar',
                data: {{
                    labels: ['流畅度', '协调性', '平衡', '重心', '关节', '肌肉', '对称', '稳定'],
                    datasets: [{{
                        label: '实际得分',
                        data: [85, 78, 88, 82, 76, 81, 73, 86],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderWidth: 2,
                        pointBackgroundColor: '#60a5fa',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }}, {{
                        label: '理想范围',
                        data: [90, 85, 90, 85, 80, 85, 80, 88],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        pointBackgroundColor: '#34d399',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{
                                color: '#94a3b8',
                                font: {{ size: 12 }}
                            }}
                        }}
                    }},
                    scales: {{
                        r: {{
                            angleLines: {{ color: '#1e293b' }},
                            grid: {{ color: '#1e293b' }},
                            pointLabels: {{ 
                                color: '#94a3b8',
                                font: {{ size: 13 }}
                            }},
                            ticks: {{
                                color: '#64748b',
                                backdropColor: 'transparent',
                                font: {{ size: 10 }}
                            }},
                            suggestedMin: 0,
                            suggestedMax: 100
                        }}
                    }}
                }}
            }});
            
            // 重心变化折线图
            const centerCtx = document.getElementById('centerChart').getContext('2d');
            new Chart(centerCtx, {{
                type: 'line',
                data: {{
                    labels: ['0s', '2s', '4s', '6s', '8s', '10s', '12s', '14s', '16s', '18s', '20s'],
                    datasets: [{{
                        label: 'X轴偏移 (cm)',
                        data: [0, 2, 5, 3, 8, 6, 4, 7, 5, 3, 2],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }}, {{
                        label: 'Y轴偏移 (cm)',
                        data: [0, 1, 3, 5, 4, 7, 8, 6, 4, 2, 1],
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{
                                color: '#94a3b8',
                                font: {{ size: 12 }}
                            }}
                        }},
                        tooltip: {{
                            mode: 'index',
                            intersect: false
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: '#1e293b' }},
                            ticks: {{ color: '#64748b' }}
                        }},
                        y: {{
                            grid: {{ color: '#1e293b' }},
                            ticks: {{ color: '#64748b' }},
                            title: {{
                                display: true,
                                text: '偏移量 (cm)',
                                color: '#94a3b8'
                            }}
                        }}
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>'''

if __name__ == '__main__':
    print("=" * 70)
    print("  AFP 智能运动分析系统 v15.0")
    print("  专业可视化版 - Chart.js图表 + 动画效果")
    print("=" * 70)
    print()
    
    # 自动查找可用端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print(f"  访问地址: http://127.0.0.1:{port}")
    print("  新增功能:")
    print("    ✨ Chart.js 雷达图 - 八维能力可视化")
    print("    ✨ 重心变化折线图 - 动态轨迹分析")
    print("    ✨ 卡片动画效果 - 渐入动画")
    print("    ✨ 进度条闪光动画 - 流光效果")
    print("    ✨ 详细数据分析 - 具体数值和建议")
    print()
    print("=" * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
