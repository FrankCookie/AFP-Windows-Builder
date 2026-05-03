#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AFP 运动康复 AI 分析系统 v13.0
四领域融合版 - 修复完成版
确保上传、分析、结果显示全部正常工作
"""

from flask import Flask, request, render_template_string, flash, redirect, url_for
import subprocess
import os
import sys
import time
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'afp_v13_secret_key_2026'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# v13.0 exe 路径
EXE_PATH = os.path.expanduser("~/AFP_AI/运动康复AI分析系统_v13.0_四领域融合版.exe")

print("=" * 70)
print("  AFP 智能运动分析系统 v13.0")
print("  四领域融合版 - 修复完成版")
print("=" * 70)
print()
print(f"  [检查] 上传目录: {os.path.abspath(UPLOAD_FOLDER)}")
print(f"  [检查] v13.0 exe: {EXE_PATH}")
print(f"  [检查] v13.0 存在: {os.path.exists(EXE_PATH)}")
print(f"  [检查] 工作目录: {os.path.abspath('.')}")
print()
print("=" * 70)
print()

@app.route('/')
def home():
    """首页 - 上传视频"""
    print(f"\n[访问] 首页 - {datetime.now().strftime('%H:%M:%S')}")
    
    exe_exists = os.path.exists(EXE_PATH)
    print(f"  [状态] v13.0 exe 存在: {exe_exists}")
    
    # 简化的首页模板
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AFP智能运动分析系统 v13.0</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; 
                background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);
                color: #e2e8f0; 
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container { 
                max-width: 800px; 
                width: 100%;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            h1 { 
                color: #60a5fa; 
                font-size: 36px;
                margin-bottom: 10px;
            }
            .version-badge {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                margin-left: 10px;
            }
            .subtitle { 
                color: #94a3b8; 
                font-size: 18px; 
            }
            .upload-card {
                background: #1e2937;
                border-radius: 16px;
                padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            .upload-area { 
                border: 3px dashed #60a5fa; 
                border-radius: 12px; 
                padding: 60px 40px; 
                text-align: center; 
                background: rgba(96, 165, 250, 0.05);
                transition: all 0.3s;
            }
            .upload-area:hover {
                border-color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
            .upload-icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
            h2 {
                color: #e2e8f0;
                font-size: 24px;
                margin-bottom: 15px;
            }
            .upload-hint {
                color: #94a3b8;
                margin-bottom: 30px;
                font-size: 15px;
            }
            input[type="file"] {
                display: block;
                margin: 0 auto 25px;
                color: #e2e8f0;
                font-size: 15px;
                padding: 10px;
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 8px;
                width: 100%;
                max-width: 400px;
            }
            button { 
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white; 
                padding: 16px 50px; 
                border: none; 
                border-radius: 10px; 
                font-size: 18px; 
                cursor: pointer; 
                transition: all 0.3s;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            }
            button:hover {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
            }
            .status {
                margin-top: 30px;
                padding: 15px;
                border-radius: 8px;
                font-size: 14px;
            }
            .status-ok {
                background: #052e16;
                border: 1px solid #10b981;
                color: #4ade80;
            }
            .status-warn {
                background: #451a03;
                border: 1px solid #f59e0b;
                color: #fbbf24;
            }
            .steps {
                display: flex;
                justify-content: space-around;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 1px solid #334155;
            }
            .step {
                text-align: center;
                flex: 1;
            }
            .step-num {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background: #3b82f6;
                color: white;
                border-radius: 50%;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .step-text {
                color: #94a3b8;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AFP智能运动分析系统 <span class="version-badge">v13.0</span></h1>
                <p class="subtitle">实用功能性物理 · 第一性功能训练体系</p>
            </div>
            
            <div class="upload-card">
                <div class="upload-area">
                    <div class="upload-icon">📹</div>
                    <h2>上传学员训练视频</h2>
                    <p class="upload-hint">支持 MP4、MOV、AVI 格式，最大 500MB</p>
                    
                    <form action="/analyze" method="post" enctype="multipart/form-data" onsubmit="showLoading()">
                        <input type="file" name="video" accept="video/*" required>
                        <br>
                        <button type="submit" id="submit-btn">🚀 开始 AI 分析</button>
                    </form>
                </div>
                
                {% if exe_exists %}
                <div class="status status-ok">
                    ✅ <strong>v13.0 四领域融合版已就绪</strong><br>
                    系统将调用 AI 分析引擎进行专业分析
                </div>
                {% else %}
                <div class="status status-warn">
                    ⚠️ <strong>v13.0 分析引擎未找到</strong><br>
                    系统将使用模拟模式生成专业分析报告
                </div>
                {% endif %}
                
                <div class="steps">
                    <div class="step">
                        <div class="step-num">1</div>
                        <div class="step-text">上传视频</div>
                    </div>
                    <div class="step">
                        <div class="step-num">2</div>
                        <div class="step-text">AI 分析</div>
                    </div>
                    <div class="step">
                        <div class="step-num">3</div>
                        <div class="step-text">获取报告</div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function showLoading() {
                document.getElementById('submit-btn').disabled = true;
                document.getElementById('submit-btn').innerText = '⏳ 正在分析，请稍候...';
                return true;
            }
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html, exe_exists=exe_exists)

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析视频"""
    print(f"\n[分析] 开始分析 - {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # 检查是否有文件
        if 'video' not in request.files:
            print("  [错误] 没有上传视频")
            return error_page("没有上传视频文件")
        
        file = request.files['video']
        
        if file.filename == '':
            print("  [错误] 没有选择文件")
            return error_page("没有选择文件")
        
        print(f"  [信息] 文件名: {file.filename}")
        print(f"  [信息] 文件大小: {file.content_length if hasattr(file, 'content_length') else '未知'}")
        
        # 保存上传的文件
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        print(f"  [保存] 保存到: {filepath}")
        file.save(filepath)
        print(f"  [保存] 保存成功: {os.path.exists(filepath)}")
        
        # 分析视频
        print(f"  [分析] 开始调用分析引擎...")
        analysis = None
        mode = "未知"
        
        if os.path.exists(EXE_PATH):
            print(f"  [分析] v13.0 exe 存在，尝试调用...")
            
            try:
                # 检查 Wine
                wine_result = subprocess.run(["which", "wine"], capture_output=True, text=True, timeout=5)
                
                if wine_result.returncode == 0:
                    print(f"  [分析] Wine 已安装，调用 v13.0...")
                    
                    try:
                        result = subprocess.run(
                            ["wine", EXE_PATH, filepath],
                            capture_output=True,
                            text=True,
                            timeout=120,
                            cwd=os.path.dirname(EXE_PATH)
                        )
                        
                        print(f"  [分析] v13.0 返回码: {result.returncode}")
                        
                        if result.returncode == 0 and result.stdout.strip():
                            analysis = result.stdout
                            mode = "真实分析（v13.0 四领域融合版）"
                            print(f"  [分析] 真实分析成功，输出长度: {len(analysis)}")
                        else:
                            print(f"  [分析] v13.0 返回空或失败，使用模拟模式")
                            print(f"  [分析] stderr: {result.stderr[:200] if result.stderr else '无'}")
                            analysis = generate_v13_analysis(filename)
                            mode = "模拟分析（v13.0 专业模拟）"
                    
                    except subprocess.TimeoutExpired:
                        print(f"  [分析] v13.0 调用超时")
                        analysis = generate_v13_analysis(filename)
                        mode = "模拟分析（v13.0 专业模拟 - 超时）"
                    
                    except Exception as e:
                        print(f"  [分析] v13.0 调用异常: {e}")
                        analysis = generate_v13_analysis(filename)
                        mode = "模拟分析（v13.0 专业模拟 - 异常）"
                
                else:
                    print(f"  [分析] Wine 未安装，使用模拟模式")
                    analysis = generate_v13_analysis(filename)
                    mode = "模拟分析（v13.0 专业模拟 - Wine 未安装）"
            
            except Exception as e:
                print(f"  [分析] 系统异常: {e}")
                analysis = generate_v13_analysis(filename)
                mode = "模拟分析（v13.0 专业模拟 - 系统异常）"
        
        else:
            print(f"  [分析] v13.0 exe 不存在，使用模拟模式")
            analysis = generate_v13_analysis(filename)
            mode = "模拟分析（v13.0 专业模拟 - exe 未找到）"
        
        # 最终保护
        if not analysis:
            print(f"  [分析] analysis 为空，使用最后保护")
            analysis = generate_v13_analysis(filename)
            mode = "模拟分析（v13.0 专业模拟 - 最后保护）"
        
        print(f"  [完成] 分析完成，模式: {mode}")
        print(f"  [完成] 报告长度: {len(analysis)} 字符")
        
        # 显示结果
        return result_page(filename, analysis, mode)
    
    except Exception as e:
        print(f"\n[异常] 分析过程发生异常:")
        print(traceback.format_exc())
        return error_page(f"分析过程发生异常: {str(e)}")

def result_page(filename, analysis, mode):
    """显示结果页面"""
    print(f"\n[结果] 渲染结果页面...")
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>分析结果 - AFP v13.0</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; 
                background: #0f172a; 
                color: #e2e8f0; 
                padding: 20px;
                line-height: 1.6;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            h1 { 
                color: #60a5fa; 
                font-size: 32px;
                margin-bottom: 15px;
            }
            .info-box {
                background: #1e2937;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 30px;
                border-left: 4px solid #10b981;
            }
            .info-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                font-size: 14px;
            }
            .info-label {
                color: #94a3b8;
            }
            .info-value {
                color: #e2e8f0;
                font-weight: 600;
            }
            .mode-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
                margin-left: 10px;
            }
            .mode-real {
                background: #052e16;
                color: #4ade80;
                border: 1px solid #10b981;
            }
            .mode-sim {
                background: #451a03;
                color: #fbbf24;
                border: 1px solid #f59e0b;
            }
            .result-box { 
                background: #1e2937; 
                padding: 30px; 
                border-radius: 12px; 
                white-space: pre-wrap; 
                line-height: 1.8;
                font-family: 'Courier New', Consolas, monospace;
                font-size: 14px;
                border: 1px solid #334155;
                overflow-x: auto;
            }
            .back-link {
                display: block;
                text-align: center;
                margin-top: 30px;
                padding: 15px;
                background: #1e2937;
                color: #60a5fa;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                transition: all 0.3s;
            }
            .back-link:hover {
                background: #263548;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ 分析完成</h1>
            </div>
            
            <div class="info-box">
                <div class="info-row">
                    <span class="info-label">📁 视频文件：</span>
                    <span class="info-value">{{ filename }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">🔬 分析模式：</span>
                    <span class="info-value">
                        {{ mode }}
                        <span class="mode-badge {% if '真实' in mode %}mode-real{% else %}mode-sim{% endif %}">
                            {% if '真实' in mode %}✓ 真实{% else %}⚠ 模拟{% endif %}
                        </span>
                    </span>
                </div>
                <div class="info-row">
                    <span class="info-label">🕐 分析时间：</span>
                    <span class="info-value">{{ timestamp }}</span>
                </div>
            </div>
            
            <div class="result-box">{{ analysis }}</div>
            
            <a href="/" class="back-link">← 返回首页，上传新视频</a>
        </div>
    </body>
    </html>
    '''
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"  [结果] 渲染完成，准备返回...")
    
    return render_template_string(
        html, 
        filename=filename, 
        analysis=analysis, 
        mode=mode,
        timestamp=timestamp
    )

def error_page(message):
    """错误页面"""
    print(f"\n[错误] 显示错误页面: {message}")
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>分析失败 - AFP v13.0</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; 
                background: #0f172a; 
                color: #e2e8f0; 
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .error-box {
                background: #1e2937;
                padding: 50px;
                border-radius: 16px;
                text-align: center;
                max-width: 600px;
                border-left: 4px solid #ef4444;
            }
            h1 {
                color: #ef4444;
                font-size: 32px;
                margin-bottom: 20px;
            }
            .message {
                color: #e2e8f0;
                font-size: 16px;
                line-height: 1.8;
                margin-bottom: 30px;
                padding: 20px;
                background: #0f172a;
                border-radius: 8px;
                text-align: left;
            }
            .back-link {
                display: inline-block;
                padding: 12px 30px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s;
            }
            .back-link:hover {
                background: #2563eb;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="error-box">
            <h1>❌ 分析失败</h1>
            <div class="message">{{ message }}</div>
            <a href="/" class="back-link">← 返回首页重新尝试</a>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html, message=message)

def generate_v13_analysis(filename):
    """生成 v13.0 四领域融合版分析报告"""
    print(f"  [模拟] 生成 v13.0 模拟报告...")
    
    # 模拟处理时间
    time.sleep(2)
    
    report = f'''
╔══════════════════════════════════════════════════════════════════════╗
║          AFP 运动康复 AI 分析系统 v13.0                              ║
║              四领域融合版 · 专业分析报告                              ║
╚══════════════════════════════════════════════════════════════════════╝

📁 视频文件：{filename}
🕐 分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🤖 分析引擎：v13.0 四领域融合版（模拟模式）

{"=" * 72}
📊 四领域综合评估
{"=" * 72}

┌────────────────────────────────────────────────────────────────┐
│ 领域一：动作质量评估                                          │
└────────────────────────────────────────────────────────────────┘

  总体评分：       84/100  ████████████░░░
  动作流畅度：     优秀（8.4/10）
  关节活动范围：   正常（未见明显受限）
  代偿模式检测：   轻微（右侧髋关节）
  
  ✓ 动作节奏：良好
  ✓ 重心控制：稳定
  ⚠ 右侧支撑期：稍短（建议加强）
  ✓ 落地缓冲：正常


┌────────────────────────────────────────────────────────────────┐
│ 领域二：对称性分析                                              │
└────────────────────────────────────────────────────────────────┘

  对称性指数：   0.81  （优秀 >0.75）
  左右差异：     11%   （正常 <15%）
  
  详细对比：
  - 步幅对称性：     0.83  ✓ 优秀
  - 支撑时间对称性： 0.79  ✓ 良好
  - 摆臂对称性：     0.81  ✓ 优秀
  - 重心偏移：       轻微向左（2.3cm）


┌────────────────────────────────────────────────────────────────┐
│ 领域三：稳定性检测                                              │
└────────────────────────────────────────────────────────────────┘

  静态稳定性：   A-  （优秀）
  动态稳定性：   B+  （良好）
  姿势控制：     0.84/1.0
  
  测试项目：
  ✓ 单腿站立（左）：  28秒
  ✓ 单腿站立（右）：  24秒  ⚠ 右侧稍弱
  ⚠ 动态平衡：        中等偏上
  ✓ 本体感觉：        正常


┌────────────────────────────────────────────────────────────────┐
│ 领域四：功能性动作筛查（FMS）                                    │
└────────────────────────────────────────────────────────────────┘

  深蹲：         3/3  ✓ 正常
  跨栏步：       2/3  ⚠ 右侧稍差
  直线弓步：     2/3  ⚠ 右侧稳定性不足
  肩部活动度：   3/3  ✓ 正常
  主动直腿抬高： 3/3  ✓ 正常
  躯干稳定俯卧撑：2/3  ⚠ 核心控制需加强
  旋转稳定性：   2/3  ⚠ 躯干旋转不足

  总分：14/21（中等偏上，有提升空间）


{"=" * 72}
💡 AFP 四领域融合训练建议
{"=" * 72}

  基于 v13.0 四领域融合分析，制定个性化训练方案：

  【第一性功能训练】强化右侧支撑功能

    1. 单腿支撑训练（第一性功能）
       - 右侧单腿站立：30秒 × 3组
       - 闭眼单腿站立：15秒 × 3组（进阶）
       - 目的：强化右侧髋关节稳定性


  【对称性矫正】改善左右差异

    2. 对称性训练
       - 镜像训练：面对镜子做动作，观察对称性
       - 节拍器训练：用节拍器统一左右节奏
       - 弱侧加强：右侧单独加练 10-15%
    

  【稳定性提升】动态平衡训练

    3. 动态稳定性训练
       - 八字走：每天 5分钟
       - 平衡垫训练：单腿站立 + 抛接球
       - 多方向跳跃：提升神经肌肉控制


  【功能性强化】FMS 针对性训练

    4. 跨栏步优化
       - 辅助跨栏步练习（降低高度）
       - 髋屈肌拉伸 + 臀肌激活
    
    5. 核心控制训练
       - 死虫式：15次 × 3组
       - 鸟狗式：12次 × 3组（每侧）
       - 侧平板支撑：30秒 × 2组（每侧）


{"=" * 72}
🎯 AFP 训练计划（四领域融合）
{"=" * 72}

  训练频率：每周 4-5 次
  每次时长：60 分钟
  训练周期：8 周（建议复评）


  【第1-2周】基础激活期
    - 重点：动作模式重建
    - 强度：低-中等
    - 核心：第一性功能训练 + 基础稳定性


  【第3-4周】对称性矫正期
    - 重点：改善左右差异
    - 强度：中等
    - 核心：镜像训练 + 弱侧加强


  【第5-6周】动态整合期
    - 重点：功能性动作整合
    - 强度：中-高
    - 核心：FMS 针对性训练


  【第7-8周】性能提升期
    - 重点：综合能力提升
    - 强度：高
    - 核心：四领域均衡发展


{"=" * 72}
📌 注意事项与进阶建议
{"=" * 72}

  ⚠️ 训练原则：
     1. 质量 > 数量（动作标准优先）
     2. 循序渐进（切勿急功近利）
     3. 疼痛立即停止（避免代偿模式）


  💪 进阶标准：
     - 对称性指数 >0.85
     - 右侧单腿站立 >35秒
     - FMS 总分 >18/21


  📅 复评建议：
     - 每 2 周复评一次
     - 记录训练日志（视频对比）
     - 根据复评结果调整训练计划


{"=" * 72}
🏆 AFP 训练体系 · 实用功能性物理 · 第一性功能训练
{"=" * 72}

  核心理念：回归第一性原理，从物理定律出发
  训练目标：让身体形成自我优化系统，越练越好！

  报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
  分析引擎：AFP v13.0 四领域融合版（模拟模式）
  
╚══════════════════════════════════════════════════════════════════════╝

【说明】
此为专业模拟分析报告，用于演示 v13.0 四领域融合版功能。
所有数据均为模拟生成，仅供参考。

如需真实分析，请确保：
  1. Wine 已安装（运行 Windows .exe 文件）
  2. v13.0 exe 文件路径正确
  3. 系统资源充足（内存 >4GB）

'''
    
    print(f"  [模拟] 报告生成完成，长度: {len(report)} 字符")
    
    return report

if __name__ == '__main__':
    print()
    print("  " + "=" * 66)
    print("    AFP 智能运动分析系统 v13.0")
    print("    四领域融合版 - 修复完成版")
    print("  " + "=" * 66)
    print()
    print("    [√] 完整错误处理")
    print("    [√] 详细日志输出")
    print("    [√] 上传、分析、显示全部修复")
    print("    [√] 支持真实模式 + 模拟模式")
    print()
    print("    访问地址: http://127.0.0.1:8080")
    print("    按 Ctrl+C 停止服务")
    print()
    print("  " + "=" * 66)
    print()
    
    # 使用 8080 端口，避免冲突
    app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
