#!/bin/bash
# AFP AI 分析系统启动脚本 v12.0

echo "================================================"
echo "  AFP 运动康复 AI 分析系统"
echo "  v12.0 集成增强版"
echo "================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 检查依赖
echo ""
echo "检查 Python 依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

echo "✓ Python 依赖已安装"

# 检查 Wine (macOS 需要)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "检测到 macOS 系统"
    if ! command -v wine &> /dev/null; then
        echo "⚠️  Wine 未安装（用于运行 .exe 文件）"
        echo ""
        echo "安装选项："
        echo "  1. 使用 Homebrew 安装: brew install --cask wine"
        echo "  2. 使用 Whisky: https://getwhisky.app"
        echo ""
        read -p "是否现在通过 Homebrew 安装 Wine? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "正在安装 Wine..."
            brew install --cask wine
        fi
    else
        echo "✓ Wine 已安装: $(wine --version)"
    fi
fi

# 检查 .exe 文件
EXE_PATH="$HOME/Documents/DataTool/AFP/运动康复AI分析系统_v12.0_集成增强版.exe"
if [ ! -f "$EXE_PATH" ]; then
    echo ""
    echo "⚠️  未找到 AI 分析系统 .exe 文件"
    echo "预期路径: $EXE_PATH"
    echo ""
    echo "系统将以模拟模式运行（用于测试界面）"
    echo "如需完整功能，请将 .exe 文件放到上述路径"
    echo ""
else
    echo "✓ 找到 AI 分析系统: $EXE_PATH"
fi

# 创建必要目录
mkdir -p uploads results static templates
echo "✓ 目录结构已创建"

echo ""
echo "================================================"
echo "启动服务器..."
echo "================================================"
echo ""
echo "访问地址:"
echo "  本地: http://127.0.0.1:5000"
echo "  局域网: http://$(ipconfig getifaddr en0 2>/dev/null || echo '未知'):5000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"
echo ""

# 启动 Flask 应用
python3 app.py
