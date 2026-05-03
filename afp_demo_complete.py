from flask import Flask, request, send_from_directory
import os

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
            font-family: system-ui, sans-serif; 
            background: #0a0a0a; 
            color: #e2e8f0; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }
        .container { max-width: 900px; width: 100%; }
        h1 { 
            font-size: 48px; 
            font-weight: 700; 
            text-align: center; 
            margin-bottom: 12px; 
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { 
            text-align: center; 
            color: #64748b; 
            margin-bottom: 60px; 
            font-size: 15px; 
            letter-spacing: 0.5px;
        }
        .upload-box { 
            border: 2px dashed #1e293b; 
            border-radius: 24px; 
            padding: 80px 40px; 
            text-align: center; 
            background: #111827; 
            transition: all 0.3s;
            cursor: pointer;
        }
        .upload-box:hover { 
            border-color: #3b82f6; 
            background: #1e293b; 
        }
        .upload-icon { 
            font-size: 48px; 
            margin-bottom: 20px; 
            display: block; 
        }
        .upload-text { 
            color: #94a3b8; 
            font-size: 16px; 
            margin-bottom: 8px; 
        }
        .upload-hint { 
            color: #64748b; 
            font-size: 13px; 
        }
        input[type="file"] { 
            margin-top: 24px; 
            color: #e2e8f0; 
            font-size: 14px;
        }
        button { 
            background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
            color: white; 
            padding: 18px 48px; 
            border: none; 
            border-radius: 16px; 
            font-size: 17px; 
            font-weight: 600; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 32px;
            transition: all 0.3s;
            letter-spacing: 0.5px;
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3); 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AFP</h1>
        <p class="subtitle">Applied Functional Physics · 智能运动分析系统</p>
        
        <div class="upload-box">
            <span class="upload-icon">🎬</span>
            <div class="upload-text">上传运动视频进行分析</div>
            <div class="upload-hint">支持 MP4、MOV、AVI 格式</div>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="video" accept="video/*" required>
                <br>
                <button type="submit">开始智能分析</button>
            </form>
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
    
    # 模拟详细分析结果 - 包含多个指标
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>分析完成 - AFP</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: system-ui, sans-serif; 
            background: #0a0a0a; 
            color: #e2e8f0; 
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ 
            max-width: 1400px; 
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
            flex: 1; 
            max-width: 700px; 
        }}
        .video-container {{ 
            background: #111827; 
            border-radius: 20px; 
            padding: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
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
        }}
        .analysis-header {{ 
            font-size: 32px; 
            font-weight: 700; 
            margin-bottom: 32px; 
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .metric-card {{ 
            background: #111827; 
            border-radius: 16px; 
            padding: 24px; 
            margin-bottom: 20px; 
            border: 1px solid #1e293b;
            transition: all 0.3s;
        }}
        .metric-card:hover {{ 
            border-color: #3b82f6; 
            transform: translateX(4px); 
        }}
        .metric-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 12px; 
        }}
        .metric-name {{ 
            color: #94a3b8; 
            font-size: 15px; 
            font-weight: 500; 
        }}
        .metric-score {{ 
            color: #60a5fa; 
            font-size: 28px; 
            font-weight: 700; 
        }}
        .metric-bar {{ 
            height: 8px; 
            background: #1e293b; 
            border-radius: 4px; 
            overflow: hidden; 
            margin-top: 12px;
        }}
        .metric-fill {{ 
            height: 100%; 
            border-radius: 4px; 
            transition: width 1s ease-out;
        }}
        .metric-detail {{ 
            color: #64748b; 
            font-size: 13px; 
            margin-top: 12px; 
            line-height: 1.6;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 40px;
            color: #60a5fa;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        
        @media (max-width: 1200px) {{
            .container {{ flex-direction: column; }}
            .left-panel, .right-panel {{ max-width: 100%; }}
            .left-panel {{ position: relative; top: 0; }}
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
            
            <!-- 动作流畅度 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🎯 动作流畅度</span>
                    <span class="metric-score">85/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 85%; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
                </div>
                <div class="metric-detail">
                    动作衔接自然，无明显卡顿。建议在过渡阶段加强 core 稳定性训练。
                </div>
            </div>
            
            <!-- 全身协调性 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🤸 全身协调性</span>
                    <span class="metric-score">78/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 78%; background: linear-gradient(90deg, #8b5cf6, #a78bfa);"></div>
                </div>
                <div class="metric-detail">
                    上下肢配合良好，但左右对称性需改善。建议增加单侧训练。
                </div>
            </div>
            
            <!-- 拓扑平衡 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">⚖️ 拓扑平衡</span>
                    <span class="metric-score">88/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 88%; background: linear-gradient(90deg, #10b981, #34d399);"></div>
                </div>
                <div class="metric-detail">
                    重心控制优秀，动态平衡能力强。继续保持当前训练强度。
                </div>
            </div>
            
            <!-- 重心变化 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">📍 重心变化</span>
                    <span class="metric-score">82/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 82%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
                </div>
                <div class="metric-detail">
                    重心转移平滑，但落地时略有偏移。建议加强足弓力量和本体感觉训练。
                </div>
            </div>
            
            <!-- 关节角度 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🦴 关节角度</span>
                    <span class="metric-score">76/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 76%; background: linear-gradient(90deg, #ef4444, #f87171);"></div>
                </div>
                <div class="metric-detail">
                    膝关节屈曲角度不足（当前 135°，理想 150°）。髋关节活动度良好。
                </div>
            </div>
            
            <!-- 肌肉激活度 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">💪 肌肉激活度</span>
                    <span class="metric-score">81/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 81%; background: linear-gradient(90deg, #ec4899, #f472b6);"></div>
                </div>
                <div class="metric-detail">
                    臀大肌激活充分，但腘绳肌参与度低。建议增加 hip hinge 动作。
                </div>
            </div>
            
            <!-- 动作对称性 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🔄 动作对称性</span>
                    <span class="metric-score">73/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 73%; background: linear-gradient(90deg, #14b8a6, #2dd4bf);"></div>
                </div>
                <div class="metric-detail">
                    左右侧差异 12%（正常 <8%）。右侧力量较强，需平衡训练。
                </div>
            </div>
            
            <!-- 稳定性指数 -->
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-name">🛡️ 稳定性指数</span>
                    <span class="metric-score">86/100</span>
                </div>
                <div class="metric-bar">
                    <div class="metric-fill" style="width: 86%; background: linear-gradient(90deg, #6366f1, #818cf8);"></div>
                </div>
                <div class="metric-detail">
                    单腿支撑时间长，动态稳定性优秀。踝关节稳定性需稍加强。
                </div>
            </div>
            
            <a href="/" class="back-link">← 返回重新上传</a>
        </div>
    </div>
</body>
</html>'''

if __name__ == '__main__':
    print("=" * 70)
    print("  AFP 智能运动分析系统 v14.0")
    print("  完整版 - 左右分栏 + 8大分析指标")
    print("=" * 70)
    print()
    
    # 自动查找可用端口
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print(f"  访问地址: http://127.0.0.1:{port}")
    print("  特点: 左右分栏 | 8大分析指标 | 重心变化 | 关节角度")
    print()
    print("=" * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
