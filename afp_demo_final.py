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
        body { 
            font-family: system-ui, sans-serif; 
            background: #0a0a0a; 
            color: #e2e8f0; 
            margin: 0; 
            padding: 40px; 
        }
        .container { max-width: 820px; margin: auto; }
        h1 { 
            font-size: 32px; 
            font-weight: 600; 
            text-align: center; 
            margin-bottom: 8px; 
            color: #60a5fa; 
        }
        .subtitle { 
            text-align: center; 
            color: #94a3b8; 
            margin-bottom: 40px; 
            font-size: 16px; 
        }
        .intro { 
            background: #111827; 
            padding: 28px; 
            border-radius: 20px; 
            margin-bottom: 40px; 
            border: 1px solid #1f2937;
            line-height: 1.8;
        }
        .upload-box { 
            border: 2px dashed #334155; 
            border-radius: 20px; 
            padding: 60px 40px; 
            text-align: center; 
            background: #111827; 
        }
        button { 
            background: #3b82f6; 
            color: white; 
            padding: 16px 48px; 
            border: none; 
            border-radius: 12px; 
            font-size: 17px; 
            font-weight: 500; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 28px;
        }
        button:hover { background: #2563eb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AFP</h1>
        <p class="subtitle">Applied Functional Physics · 实用功能性物理 · 第一性功能训练体系</p>
        
        <div class="intro">
            <strong>我们做什么？</strong><br>
            用物理定律和人类进化原理，帮助你从根源解决肩膝腰慢性疼痛，同时提升运动表现。<br>
            核心动作：走 · 跑 · 跳 · 投掷<br>
            重点：动作流畅度 + 全身协调性 + 动态平衡
        </div>
        
        <div class="upload-box">
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="video" accept="video/*" style="margin-bottom:24px; color: #e2e8f0;">
                <br>
                <button type="submit">开始动态拓扑分析</button>
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
    
    # 模拟分析结果
    analysis_html = '''
    <h2 style="color: #60a5fa; margin-bottom: 20px;">✅ AFP 动态拓扑分析完成</h2>
    
    <div style="background: #111827; padding: 20px; border-radius: 12px; margin: 20px 0;">
        <div style="margin-bottom: 15px;">
            <div style="color: #94a3b8; font-size: 14px;">动作流畅度</div>
            <div style="color: #e2e8f0; font-size: 18px; font-weight: 600;">85/100</div>
            <div style="height: 8px; background: #3b82f6; border-radius: 4px; margin-top: 8px; width: 85%;"></div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="color: #94a3b8; font-size: 14px;">全身协调性</div>
            <div style="color: #e2e8f0; font-size: 18px; font-weight: 600;">78/100</div>
            <div style="height: 8px; background: #3b82f6; border-radius: 4px; margin-top: 8px; width: 78%;"></div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="color: #94a3b8; font-size: 14px;">拓扑平衡</div>
            <div style="color: #e2e8f0; font-size: 18px; font-weight: 600;">88/100</div>
            <div style="height: 8px; background: #3b82f6; border-radius: 4px; margin-top: 8px; width: 88%;"></div>
        </div>
    </div>
    
    <div style="background: #111827; padding: 20px; border-radius: 12px; margin-top: 20px;">
        <strong style="color: #e2e8f0;">AFP 动态指导方向：</strong><br><br>
        1. 强化走跑跳投掷动态联动练习<br>
        2. 提升拓扑平衡能力<br>
        3. 让身体自然优化（解决慢性疼痛 + 提高运动表现）
    </div>
    '''
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>分析完成 - AFP</title>
    <style>
        body {{ 
            font-family: system-ui, sans-serif; 
            background: #0a0a0a; 
            color: #e2e8f0; 
            margin: 0; 
            padding: 40px; 
        }}
        .container {{ max-width: 820px; margin: auto; }}
        video {{ 
            width: 100%; 
            max-width: 720px; 
            border-radius: 16px; 
            margin: 32px 0; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        }}
        .back-link {{
            display: block;
            text-align: center;
            margin-top: 48px;
            color: #60a5fa;
            text-decoration: none;
            font-weight: 500;
        }}
        .video-info {{
            text-align: center;
            color: #94a3b8;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 32px; color: #60a5fa;">
            ✅ 动态拓扑分析完成
        </h1>
        
        <p class="video-info">视频文件：{filename}</p>
        
        <video controls>
            <source src="/uploads/{filename}" type="video/mp4">
            您的浏览器不支持视频播放
        </video>
        
        {analysis_html}
        
        <a href="/" class="back-link">← 重新上传视频</a>
    </div>
</body>
</html>'''

if __name__ == '__main__':
    print("=" * 70)
    print("  AFP 智能运动分析系统 v13.0")
    print("  最终修复版 - 视频播放已修复")
    print("=" * 70)
    print()
    
    # 自动查找可用端口
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    print(f"  访问地址: http://127.0.0.1:{port}")
    print("  特点: 极简 | 可视化进度条 | 视频播放已修复")
    print()
    print("=" * 70)
    print()
    
    app.run(host='127.0.0.1', port=port, debug=False)
