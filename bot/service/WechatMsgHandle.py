import logging
import re
import time

from bot.config.config_loader import WechatConfig_chatRoomPrompt, WechatConfig_adminWxid, WechatConfig_enable_gpt, \
    WechatConfig_msgReplay, WechatConfig_is_debug, \
    WechatConfig_debugFromName, WechatConfig_free_call_ai
from bot.infrastructure.chatgpt.OpenAIHelper import OpenAIHelper
from bot.infrastructure.wexin import SendMsgNativeApi, GroupNativeApi

log = logging.getLogger(__name__)

class WechatMsgHandle:

    def __init__(self):

        self.chatgpt_client = OpenAIHelper()
        # 呼叫管理员的用户
        self.callAdminUser = {}
        # 今天用户消耗的token
        self.userToken = {}
        # 用户今天的聊天次数
        self.userChatCount = {}
        # 今天日期，当日期变化时，清空用户聊天次数
        self.today = time.strftime("%Y-%m-%d", time.localtime())
        pass

    def userCanChatAi(self, wechatId, fromWechatId, type):
        if self.today != time.strftime("%Y-%m-%d", time.localtime()):
            return True
        userKey = fromWechatId + "_" + type
        if wechatId not in self.userChatCount:
            return True
        if userKey not in self.userChatCount[wechatId]:
            return True
        maxCount = WechatConfig_free_call_ai[wechatId][type] if wechatId in WechatConfig_free_call_ai and type in \
                                                                WechatConfig_free_call_ai[wechatId] else 2
        if self.userChatCount[wechatId][userKey] < maxCount:
            return True
        return False

    def addUserToken(self, wechatId, fromWechatId, type, total_tokens):
        if wechatId not in self.userToken:
            self.userToken[wechatId] = {}
        if fromWechatId not in self.userToken[wechatId]:
            self.userToken[wechatId][fromWechatId] = 0
        self.userToken[wechatId][fromWechatId] += total_tokens

        if self.today != time.strftime("%Y-%m-%d", time.localtime()):
            self.today = time.strftime("%Y-%m-%d", time.localtime())
            self.userToken = {}
            self.userChatCount = {}

        userKey = fromWechatId + "_" + type
        # 增加用户今天的聊天次数
        if wechatId not in self.userChatCount:
            self.userChatCount[wechatId] = {}
        if userKey not in self.userChatCount[wechatId]:
            self.userChatCount[wechatId][userKey] = 0
        self.userChatCount[wechatId][userKey] += 1

    async def handle_user_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml, response_content_body):
        debugAndconnect =  self.checkDebugConnect(wechatId, fromWechatId, msgContent, msgXml, response_content_body)
        if not debugAndconnect:
            return

        if msgContent == "清除记忆":
            self.chatgpt_client.reset_chat_history(fromWechatId)
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId, "清除记忆成功")
            return
        if wechatId in WechatConfig_msgReplay and msgContent in WechatConfig_msgReplay[wechatId]:
            self.handle_MsgReplay(wechatId, fromWechatId, msgContent, msgXml, response_content_body)
            return

        if self.callAdminUser.get(wechatId) and self.callAdminUser.get(wechatId)[fromWechatId] and \
                time.time() - self.callAdminUser.get(wechatId)[fromWechatId] < 600:
            return

            # 如果是管理员发的消息
        adminMsgFlag = self.chekAdminMsgFlag(wechatId, fromWechatId)
        # 如果开启聊天功能
        await self.getAiChatResponse(wechatId, fromWechatId, msgContent)

        return
    def checkDebugConnect(self, wechatId, fromWechatId, msgContent, msgXml, response_content_body):
        # 不是debug模式，返回继续
        if wechatId not in WechatConfig_is_debug or not WechatConfig_is_debug[wechatId]:
            return True
        fromName = response_content_body["talkerInfo"]["nickName"]
        if wechatId in WechatConfig_is_debug and WechatConfig_is_debug[wechatId] \
                and wechatId in WechatConfig_debugFromName and self.contains_substring(fromName, WechatConfig_debugFromName[wechatId]):
            return True
        return False
    def contains_substring(self,main_string, string_list):
        for s in string_list:
            if s in main_string:
                return True
        return False
    async def handle_group_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml, response_content_body):
        debugAndconnect =  self.checkDebugConnect(wechatId, fromWechatId, msgContent, msgXml, response_content_body)
        if not debugAndconnect:
            return
        # 如果是管理员发的消息
        adminMsgFlag = self.chekAdminMsgFlag(wechatId, fromWechatId)

        # 如果reversed1中atuserlist标签中包含自己的id，说明是@自己的消息
        send_content = msgContent.split(":\n")
        group_mes_send_user, msgContent = send_content[0], send_content[1]
        msgContent = re.sub(r'@[^\u2005]+ ', '', msgContent).strip()
        # 开启了chat聊天 并且被@了
        if wechatId in msgXml and self.getChatRoomCanAi(wechatId, fromWechatId):
            # 调用chatgpt回复
            await self.getAiChatResponse(wechatId, group_mes_send_user, msgContent,
                                         fromWechatId)

    async def getAiChatResponse(self, wechatId, userId, msgContent, groupId=None):
        if not WechatConfig_enable_gpt[wechatId]:
            return
        type = "text" if not groupId else self.getChatRoomType(wechatId, groupId)
        chatId = userId if not groupId else groupId + userId

        if not self.userCanChatAi(wechatId, userId, type):
            # 用户今天的免费聊天次数已经用完回复
            if groupId:
                replaceContent = "今日免费聊天次数已用完，明天再来吧~\n\n付费解锁畅聊版本，请与群主私聊"
            else:
                replaceContent = "今日免费聊天次数已用完，明天再来吧~\n\n付费解锁畅聊版本，请直接转账\n 1天1元，1月20元"
            SendMsgNativeApi.send_text_message_base(wechatId
                                                    , groupId if groupId else userId
                                                    , replaceContent
                                                    , [userId] if groupId else [])
            return
        if type == "text":
            maxCount = None if not groupId else self.getChatRoomMaxCount(wechatId, groupId)
            initPrompt = None if not groupId else self.getChatRoomPrompt(wechatId, groupId)
            response, total_tokens = await self.chatgpt_client.get_chat_response(chat_id=chatId, query=msgContent,prompt=initPrompt, maxCount=maxCount)
            # response, total_tokens = msgContent, 0
            # 调用微信发送消息接口
            SendMsgNativeApi.send_text_message_base(wechatId, groupId if groupId else userId, response, [userId] if groupId else [])
            self.addUserToken(wechatId, userId, type, total_tokens)
        if type == "image":
            chatRoomGroup = self.getChatRoomConfig(wechatId, groupId)
            imageModel, imageSize, imageQuality = chatRoomGroup["image_model"], chatRoomGroup["image_size"], \
                chatRoomGroup["image_quality"]

            b64_json = await self.chatgpt_client.generate_image(msgContent, imageModel, imageSize, imageQuality)
            SendMsgNativeApi.send_image_base64_message(wechatId, groupId if groupId else userId, b64_json)
            # 发送引用消息，但没找到@的方法 先文本@吧
            SendMsgNativeApi.send_text_message_base(wechatId, groupId if groupId else userId, "好咯好咯，我已经帮你处理好啦~", [userId] if groupId else [])
            self.addUserToken(wechatId, userId, type, 0)
        return

    def callAdmin(self, wechatId, fromWechatId, msgContent, msgXml, response_content_body):
        if wechatId not in self.callAdminUser:
            self.callAdminUser[wechatId] = {}
        self.callAdminUser[wechatId][fromWechatId] = time.time()
        adminwechat = WechatConfig_adminWxid[wechatId]
        fromUser = response_content_body["talkerInfo"]["nickName"]
        SendMsgNativeApi.send_text_message_base(wechatId, adminwechat, "有人找你，快去看看吧！\n" + fromUser)
        SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId,"你好，我正在穿衣服！请在10分钟内完成留言！我穿好衣服会回复你~")

    def chekAdminMsgFlag(self, wechatId, fromWechatId):
        return WechatConfig_adminWxid[wechatId] == fromWechatId if wechatId in WechatConfig_adminWxid else False

    def getChatRoomPrompt(self, wechatId, groupId):
        if self.getChatRoomCanAi(wechatId, groupId):
            return WechatConfig_chatRoomPrompt[wechatId][groupId]["prompt"]
        return ''

    def getChatRoomType(self, wechatId, groupId):
        if self.getChatRoomCanAi(wechatId, groupId):
            return WechatConfig_chatRoomPrompt[wechatId][groupId]["type"]
        return ''

    def getChatRoomConfig(self, wechatId, groupId):
        if self.getChatRoomCanAi(wechatId, groupId):
            return WechatConfig_chatRoomPrompt[wechatId][groupId]
        return ''

    def getChatRoomCanAi(self, wechatId, groupId):
        return wechatId in WechatConfig_chatRoomPrompt and groupId in WechatConfig_chatRoomPrompt[wechatId]

    def getChatRoomMaxCount(self, wechatId, groupId):
        if self.getChatRoomCanAi(wechatId, groupId):
            return WechatConfig_chatRoomPrompt[wechatId][groupId]["maxCount"]
        return 100

    def handle_MsgReplay(self, wechatId, fromWechatId, msgContent, msgXml, response_content_body):
        """
        处理默认消息回复
        :param wechatId:
        :param fromWechatId:
        :param msgContent:
        :param msgXml:
        :param response_content_body:
        :return:
        """

        defaultReplaceData = WechatConfig_msgReplay[wechatId][msgContent]
        replaceType = defaultReplaceData["replaceType"]
        if replaceType == "callAdmin":
            self.callAdmin(wechatId, fromWechatId, msgContent, msgXml, response_content_body)
            return
        elif replaceType == "inviteGroup":
            groupId = defaultReplaceData["groupId"]
            GroupNativeApi.add_group_member(wechatId, groupId, fromWechatId)
            return
        pass
