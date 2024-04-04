# 微信机器人 🤖

微信机器人是一个基于Python 3.11开发的项目，它利用API调用微信原生能力，并与人工智能集成，以帮助用户完成一系列任务。这些任务包括但不限于：以高情商回复心仪的女生、制作头像、AI绘画、通过文字完成多个API处理（如获取天气、根据天气生成图片并自动发布到朋友圈等功能）。

## 特色功能 ✨
- 聊天画图：结合ChatGPT模型的高级聊天和绘图能力，提供丰富的交互体验。
- 上下文记忆：自动记忆与用户的对话上下文，如果10分钟内无回复，则忘记上下文。
- 对话历史限制：最多记忆10条对话历史，确保交互的连贯性。
- 自动通过好友、自动拉群
- 自动发朋友圈、自动点赞
- 直播间自动发弹幕
- 视频号自动回复等

## 功能 🌟

- 高情商回复 💬
- 头像制作 🎨
- AI绘画、梦境展现 🎞️
- 多API集成处理（如天气获取、自动发朋友圈、查询币价） 🌦️

## 系统要求 💻

- Windows操作系统 或 Windows云服务器
- Python 3.11

## 安装 🔧

### 微信启动

1. 将 `dll` 文件放置在与 `start_wechat.py` 同一目录下。 [DLL来源](https://github.com/kawika-git/wechatAPI)
2. 运行 `start_wechat.py`（默认HTTP端口号为8888，可根据需要修改）。

### 启动程序

1. 复制 `env_wechat_back.json` 文件并将其重命名为 `env_wechat.json`，然后修改文件内容。
2. 进入 `wechatSDK` 目录，并运行 `app.py`。

## 依赖 📦

项目依赖于 [wechatAPI](https://github.com/kawika-git/wechatAPI)。请确保安装所有必要的依赖。

## 如何贡献 🤝

欢迎通过Pull Requests来贡献代码。请确保您的代码符合项目的编码标准并通过所有测试。

## 效果展示 🖼️
![img_1_base.png](img%2Fimg_1_base.png)
![img_1_img.png](img%2Fimg_1_img.png)
![img_2_base.png](img%2Fimg_2_base.png)
![img_2_img.png](img%2Fimg_2_img.png)
![img_chat_base.png](img%2Fimg_chat_base.png)
![img.png](img%2Fimg.png)
## 许可证 📄

该项目根据MIT许可证授权
