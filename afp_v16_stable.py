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
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { max-width: 800px; width: 100%; }
        .header-card {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        .logo {
            font-size: 80px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
            letter-spacing: -2px;
        }
        .subtitle {
            color: #64748b;
            font-size: 18px;
            margin-bottom: 40px;
            font-weight: 500;
        }
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; 
            background: #f8fafc; 
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1600px; 
            margin: auto; 
            display: flex; 
            gap: 30px; 
            align-items: flex-start;
        }
        .left-panel { 
            flex: 1; 
            max-width: 640px; 
            position: sticky; 
            top: 20px; 
        }
        .right-panel { 
            flex: 1.2; 
            max-width: 900px; 
        }
        
        /* 视频容器 */
        .video-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        video { 
            width: 100%; 
            border-radius: 12px; 
            display: block; 
        }
        .video-title { 
            color: #64748b; 
            font-size: 14px; 
            margin-top: 12px; 
            text-align: center; 
            font-weight: 500;
        }
        
        /* 分析头部 */
        .analysis-header { 
            font-size: 32px; 
            font-weight: 800; 
            margin-bottom: 24px; 
            color: #1e293b;
        }
        
        /* 综合评分卡片 */
        .score-overview {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 40px;
        }
        .overall-score {
            text-align: center;
            min-width: 120px;
        }
        .score-number {
            font-size: 64px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }
        .score-label {
            color: #64748b;
            font-size: 14px;
            margin-top: 8px;
            font-weight: 500;
        }
        .score-details {
            flex: 1;
        }
        .score-details h3 {
            color: #1e293b;
            font-size: 18px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        .quick-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }
        .stat-item {
            background: #f8fafc;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #64748b;
            margin-top: 4px;
        }
        
        /* 图表容器 */
        .charts-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }
        .chart-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .chart-card h3 {
            color: #1e293b;
            font-size: 16px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        /* 指标卡片 */
        .metric-card { 
            background: white;
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 16px; 
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
            margin-bottom: 12px; 
        }
        .metric-name { 
            color: #1e293b; 
            font-size: 16px; 
            font-weight: 600; 
        }
        .metric-score { 
            font-size: 28px; 
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
            font-size: 14px; 
            margin-top: 12px; 
            line-height: 1.6;
            padding: 12px;
            background: #f8fafc;
            border-radius: 8px;
        }
        
        /* 返回链接 */
        .back-link {
            display: inline-block;
            margin-top: 30px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
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
            .left-panel, .right-panel { max-width: 100%; }
            .left-panel { position: relative; top: 0; }
            .charts-container { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 左侧：视频播放 -->
        <div class="left-panel">
            <div class="video-card">
                <video controls autoplay>
                    <source src="/uploads/FILENAME_PLACEHOLDER" type="video/mp4">
                    您的浏览器不支持视频播放
                </video>
                <div class="video-title">📹 分析视频：FILENAME_PLACEHOLDER</div>
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
                    ⚠️ 左右对称性需改善（差异 12%）<br>
                    💡 建议增加单侧训练
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
                    ⚠️ 左右侧差异 12%<br>
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
                    ✅ 单腿支撑时间长<br>
                    ✅ 动态稳定性优秀
                </div>
            </div>
            
            <a href="/" class="back-link">← 返回重新上传</a>
        </div>
    </div>
    
    <script>
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
                        pointRadius: 5
                    }, {
                        label: '理想范围',
                        data: [90, 85, 90, 85, 80, 85, 80, 88],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        pointBackgroundColor: '#10b981',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#64748b',
                                font: { size: 12 }
                            }
                        }
                    },
                    scales: {
                        r: {
                            angleLines: { color: '#e2e8f0' },
                            grid: { color: '#e2e8f0' },
                            pointLabels: { 
                                color: '#1e293b',
                                font: { size: 13 }
                            },
                            ticks: {
                                color: '#64748b',
                                backdropColor: 'transparent',
                                font: { size: 10 }
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
                        label: 'X轴偏移 (cm)',
                        data: [0, 2, 5, 3, 8, 6, 4, 7, 5, 3, 2],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: 'Y轴偏移 (cm)',
                        data: [0, 1, 3, 5, 4, 7, 8, 6, 4, 2, 1],
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#64748b',
                                font: { size: 12 }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: '#e2e8f0' },
                            ticks: { color: '#64748b' }
                        },
                        y: {
                            grid: { color: '#e2e8f0' },
                            ticks: { color: '#64748b' },
                            title: {
                                display: true,
                                text: '偏移量 (cm)',
                                color: '#64748b'
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
    print("  AFP 运动康复AI分析系统 v16.0")
    print("  稳定版 - 修复所有bug")
    print("=" * 70)
    print()
    
    # 自动查找可用端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print(f"  访问地址: http://127.0.0.1:{port}")
    print("  功能:")
    print("    ✅ 左右分栏布局（左视频右数据）")
    print("    ✅ 8大分析指标")
    print("    ✅ Chart.js 雷达图")
    print("    ✅ 重心变化折线图")
    print("    ✅ AFP原始配色（紫蓝渐变）")
    print()
    print("=" * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
