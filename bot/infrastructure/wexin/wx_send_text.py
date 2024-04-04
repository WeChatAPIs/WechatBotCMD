from typing import Dict

from .httputils import _post_wx_request
from bot.infrastructure.plugins.Plugin import Plugin


class SendTextMessage(Plugin):

    def send_text_message(self, userName, msgContent):
        """
        发送文本消息。
        :param user_name: 接收消息的用户wxid。
        :param msg_content: 要发送的消息内容。
        :return: 发送消息的API响应数据。
        """
        return _post_wx_request({
            "type": 10009,
            "userName": userName,
            "msgContent": msgContent
        })

    """
    A plugin to fetch the current rate of various cryptocurrencies
    """

    @staticmethod
    def get_source_name(self) -> str:
        return "send_text"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "send_text_message",
            "description": "发送文本消息",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {
                        "type": "string",
                        "description": "接收消息的用户wxid"
                    },
                    "msg_content": {
                        "type": "string",
                        "description": "要发送的消息内容"
                    }
                }
            }
        }
        ]

    async def execute(self, function_name, **kwargs) -> Dict:
        user_name = kwargs['user_name']
        msg_content = kwargs['msg_content']
        return self.send_text_message(user_name, msg_content)
