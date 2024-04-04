from typing import Dict

from .wx_get_all_user_info import GETAllUserInfoPlugin
from bot.infrastructure.plugins.Plugin import Plugin


class FindUserPlugin(Plugin):

    def find_userName_by_nickName(self, nickName):
        """
        根据微信名检索wxid。
        :param name: 要检索的微信名。
        :return: 对应的wxid，如果未找到则返回None。
        """
        all_user_info = GETAllUserInfoPlugin.get_all_user_info()
        if all_user_info:
            for user_info in all_user_info:
                if user_info.get('nickName') == nickName:
                    return user_info.get('userName')
        return None

    """
    A plugin to fetch the current rate of various cryptocurrencies
    """

    @staticmethod
    def get_source_name(self) -> str:
        return "find_userName_by_nickName"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "find_userName_by_nickName",
            "description": "根据微信名检索微信ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "nickName": {
                        "type": "string",
                        "description": "要检索的微信名"
                    }
                }
            },
            "returns": {
                "description": "对应的微信ID，如果未找到则返回None",
                "type": "string",
                "nullable": "true"
            }
        }
        ]

    async def execute(self, function_name, **kwargs) -> Dict:
        nickName = kwargs['nickName']
        return self.find_userName_by_nickName(nickName)
