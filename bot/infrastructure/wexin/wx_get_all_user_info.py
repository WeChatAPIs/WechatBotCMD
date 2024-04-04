from datetime import datetime, timedelta
from typing import Dict, Any

from bot.infrastructure.plugins.Plugin import Plugin
from bot.infrastructure.wexin.WechatUtils import _post_wx_request


class GETAllUserInfoPlugin(Plugin):

    def __init__(self):
        self.all_user_info_list = []  # 初始化用户信息列表
        self.all_user_info_list_lastTime = datetime.min  # 初始化时间为最小时间

    def get_user_info(self):
        """
        获取登录用户的信息。
        :return: 包含用户信息的JSON数据。
        """
        return _post_wx_request({"type": 28})

    def get_contact_list(self):
        """
        获取通讯录列表，包括好友、关注的公众号、已保存到通讯录的群聊。
        :return: 包含通讯录列表的JSON数据。
        """
        return _post_wx_request({"type": 29})

    def get_specific_user_info(self, user_names):
        """
        获取一个或多个用户的详细信息。
        :param user_names: 用户wxid的列表。
        :return: 包含用户详细信息的JSON数据。
        """
        return _post_wx_request({
            "type": 10015,
            "userName": user_names
        })

    def get_all_user_info(self):
        """
        获取所有用户的详细信息。
        :return: 包含所有用户详细信息的列表。
        """
        if datetime.now() - self.all_user_info_list_lastTime < timedelta(minutes=10):
            # 如果上次更新时间距现在不足10分钟，直接返回现有列表
            print("使用all_user_info_list缓存")
            return self.all_user_info_list

        contact_list_response = self.get_contact_list()
        if contact_list_response and 'data' in contact_list_response and 'data' in contact_list_response['data']:
            user_wxids = contact_list_response['data']['data']['userNames']
            all_user_info = []

            for i in range(0, len(user_wxids), 20):
                batch_wxids = user_wxids[i:i + 20]
                user_info_response = self.get_specific_user_info(batch_wxids)
                if user_info_response and 'data' in user_info_response and 'data' in user_info_response['data']:
                    all_user_info.extend(user_info_response['data']['data']['profiles'])
            print(all_user_info)
            # 解析数据并提取所需信息
            result = []
            for user in all_user_info:
                if user.get("userName") in ["weixin", "fmessage", "medianote", "floatbottle"]:
                    continue
                user_info = {
                    "nickName": user.get("nickName", ""),
                    # "HeadImgUrl": user.get("bigHeadImgUrl", ""),
                    "userName": user.get("userName", ""),
                    "signature": user.get("signature", ""),
                    "userFlag": user.get("userFlag", ""),
                    "alias": user.get("alias", ""),
                    "sex": user.get("sex", 0)
                }
                result.append(user_info)
                self.all_user_info_list = result
                self.all_user_info_list_lastTime = datetime.now()
            return result
        else:
            print("获取通讯录列表失败或格式不正确")
            return None

    """
    A plugin to fetch the current rate of various cryptocurrencies
    """

    @staticmethod
    def get_source_name(self) -> str:
        return "all_user_info"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "get_all_user_info",
            "description": "获取所有微信好友信息",
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "returns": {
                "description": "包含所有微信好友详细信息的列表",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "nickName": {
                            "type": "string",
                            "description": "昵称"
                        },
                        "userName": {
                            "type": "string",
                            "description": "微信ID"
                        },
                        "signature": {
                            "type": "string",
                            "description": "个性签名"
                        },
                        "userFlag": {
                            "type": "integer",
                            "description": "用户类型标识"
                        },
                        "alias": {
                            "type": "string",
                            "description": "微信号"
                        },
                        "sex": {
                            "type": "integer",
                            "description": "好友的性别（0表示未知，1表示男，2表示女）"
                        }
                    }
                }
            }
        }
        ]

    async def execute(self, function_name, **kwargs) -> list[Any] | None:
        return self.get_all_user_info()
