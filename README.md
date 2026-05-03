# AFP 运动康复 AI 分析系统 v12.0

> 实用功能性物理 · 第一性功能训练体系
> 本地部署 + 视频动态分析

## 📋 系统简介

本系统集成「运动康复 AI 分析系统 v12.0」到 AFP 训练体系中，提供：

- 📹 **视频上传**: 支持 MP4、MOV、AVI 格式
- 🤖 **AI 分析**: 调用专业运动康复分析引擎
- 📊 **结果可视化**: 动作质量评分、对称性分析、稳定性评级
- 💡 **AFP 建议**: 基于分析结果生成个性化训练建议

## 🚀 快速开始

### 1. 前置要求

#### macOS 用户（必须）:
```bash
# 安装 Wine（用于运行 .exe 文件）
brew install --cask wine

# 或使用 Whisky（推荐，更简单易用）
# 下载: https://getwhisky.app
```

#### Windows 用户:
- 无需额外安装，可直接运行 .exe

#### 所有用户:
```bash
# 安装 Python 依赖
pip3 install -r requirements.txt
```

### 2. 放置 AI 分析程序

将 `运动康复AI分析系统_v12.0_集成增强版.exe` 放到:

```
~/Documents/DataTool/AFP/运动康复AI分析系统_v12.0_集成增强版.exe
```

（可根据实际情况修改 `app.py` 中的 `EXE_PATH`）

### 3. 启动系统

#### 方法一: 使用启动脚本（推荐）
```bash
cd ~/AFP_AI
./start.sh
```

#### 方法二: 手动启动
```bash
cd ~/AFP_AI
python3 app.py
```

### 4. 访问系统

浏览器打开: **http://127.0.0.1:5000**

## 🎯 使用流程

1. **上传视频**: 拖拽或点击上传学员动作视频
2. **开始分析**: 点击「开始 AI 分析」按钮
3. **查看结果**: 
   - 动作质量评分
   - 对称性指数
   - 稳定性评级
   - 功能动作模式
4. **获取建议**: 查看 AFP 个性化训练建议

## ⚙️ 配置说明

### 修改 .exe 路径

编辑 `app.py`，修改:
```python
EXE_PATH = Path("/你的路径/运动康复AI分析系统_v12.0_集成增强版.exe")
```

### 修改端口

编辑 `app.py` 最后一行:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
# 将 5000 改为其他端口，如 8080
```

### 局域网访问

确保防火墙允许端口 5000，然后访问:
```
http://你的IP地址:5000
```

## 🔧 技术架构

```
┌─────────────────┐
│   浏览器界面     │  (HTML + CSS + JavaScript)
│   (AFP 风格)    │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Flask 服务器   │  (Python + Flask)
│   app.py        │
└────────┬────────┘
         │ subprocess
         ▼
┌─────────────────┐
│  AI 分析系统    │  (运动康复AI分析系统_v12.0.exe)
│   .exe 文件     │
└─────────────────┘
```

## 📦 目录结构

```
~/AFP_AI/
├── app.py              # 主应用程序
├── start.sh            # 启动脚本
├── requirements.txt    # Python 依赖
├── README.md          # 本文件
├── uploads/           # 上传的视频文件
├── results/           # 分析结果（可选）
├── static/            # 静态资源（可选）
└── templates/         # 模板文件（可选）
```

## 🐛 常见问题

### Q1: macOS 上无法运行 .exe 文件？

**A**: macOS 需要 Wine 来运行 Windows .exe 文件:
```bash
brew install --cask wine
```

或使用 **Whisky**（推荐，更简单）:
- 下载: https://getwhisky.app
- 创建容器，在容器中运行 .exe

### Q2: 分析超时怎么办？

**A**: 默认超时为 5 分钟。可修改 `app.py` 中的 `timeout` 参数:
```python
result = subprocess.run(
    ['wine', str(EXE_PATH), str(video_path)],
    capture_output=True,
    text=True,
    timeout=600  # 改为 10 分钟
)
```

### Q3: 如何解析 .exe 的实际输出？

**A**: 修改 `app.py` 中的 `call_ai_system()` 函数，根据实际输出格式解析:
```python
output = result.stdout or result.stderr or ""

# 示例: 如果输出是 JSON
try:
    data = json.loads(output)
    return data
except:
    # 如果不是 JSON，按行解析或正则提取
    pass
```

### Q4: 可以不用 Wine 吗？

**A**: 如果 .exe 文件可以在 Windows 上运行，可以:
1. 在 Windows 机器上部署此系统
2. 或修改 `call_ai_system()` 直接调用 .exe（Windows 原生支持）

## 📝 开发说明

### 模拟模式

如果未找到 .exe 文件，系统会自动进入**模拟模式**，返回模拟分析结果。这可用于:
- 测试界面和功能
- 演示系统流程
- 开发调试

### 自定义分析逻辑

编辑 `call_ai_system()` 函数，根据实际 .exe 的接口调整:
- 命令行参数
- 输出格式解析
- 错误处理

### AFP 风格定制

HTML 模板中的 CSS 使用了 AFP 工业风设计:
- 主色调: 冰蓝 `#5BC8F5`
- 背景色: 深黑 `#090909`
- 金属网格背景
- 斜切角按钮

可在 `HTML_TEMPLATE` 变量中修改样式。

## 📄 许可证

本系统集成代码为 AFP 训练体系专用。

## 📞 支持

如有问题，请联系 AFP 技术支持团队。

---

**AFP 训练体系**  
实用功能性物理 · 第一性功能训练  
v12.0 | 2026
