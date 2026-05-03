from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <body style="background:#0a0a0a;color:#4CAF50;font-family:sans-serif;padding:50px;">
        <h1>✅ AFP MVP 服务器正常运行</h1>
        <p style="color:#ccc;">如果您能看到这个页面，说明服务器工作正常。</p>
        <p style="color:#888;margin-top:20px;">现在请访问：<a href="/full" style="color:#4CAF50;">完整版首页</a></p>
    </body>
    </html>
    '''

@app.route('/full')
def full():
    return open('afp_mvp.py', 'r').read()[:1000]  # 只返回部分内容作为测试

if __name__ == '__main__':
    print("测试服务器启动在 http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=False)
