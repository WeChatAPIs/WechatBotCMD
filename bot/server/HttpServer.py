# HttpServer.py
import json
import logging
import time
import traceback

from flask import Flask, request, jsonify

from bot.server.RequestHandler import RequestHandler

app = Flask(__name__)
request_handler = RequestHandler()
# 禁用 Flask 的启动日志
app.config['startup_log'] = False
log = logging.getLogger(__name__)

# 创建一个FIFO链式数据表缓存
callbackMes = []
lastPullTime = time.time()


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json
    response = request_handler.handle_gpt_request(user_input)
    return jsonify({"response": response})


@app.route('/weixinCallback', methods=['POST'])
async def weixinCallback():
    user_input = request.json
    # 当前时间和最后一次拉取时间间隔5分钟，则追加消息
    global lastPullTime, callbackMes
    # 部署在云服务器上，本地电脑拉取消息，最后一次消息拉取在5分钟内，则新消息会缓存到数组中，让
    if lastPullTime is not None and time.time() - lastPullTime < 300:
        callbackMes.append(user_input)
    else:
        callbackMes = []
    await request_handler.handle_weixin_callback(user_input)  # 异步调用处理函数
    return jsonify({"response": "success"})


@app.route('/weixinCallback', methods=['GET'])
def weixinCallbackMsg():
    # 部署在云服务器上，本地电脑想拉取消息
    global lastPullTime
    lastPullTime = time.time()
    if callbackMes:
        message = callbackMes.pop(0)
        logging.info('Message retrieved and removed from FIFO queue')
        return json.dumps(message), 200
    return '', 200


@app.errorhandler(Exception)
def handle_exception(error):
    """全局异常处理函数"""
    # 获取异常的堆栈信息
    exc_info = traceback.format_exc()
    # 记录错误日志
    logging.error(f"Unhandled Exception: {type(error).__name__}: {error}\n{exc_info}")
    # 返回错误响应
    return f"An error occurred: {error}", 500


def runHttpServer():
    port = 18000
    request_handler.init_weixin_callbackUrl()
    app.run(host='0.0.0.0', port=port, debug=False)
