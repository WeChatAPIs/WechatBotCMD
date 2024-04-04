from abc import abstractmethod, ABC
from typing import Dict


class Plugin(ABC):
    """
    一个插件接口，可用于为ChatGPT API创建插件。
    A plugin interface which can be used to create plugins for the ChatGPT API.
    """

    @abstractmethod
    def get_source_name(self) -> str:
        """
        返回插件源的名称。
        Return the name of the source of the plugin.
        """
        pass

    @abstractmethod
    def get_spec(self) -> [Dict]:
        """
        OpenAI文档中指定的JSON模式形式的函数规范：
        Function specs in the form of JSON schema as specified in the OpenAI documentation:
        https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions
        """
        pass

    @abstractmethod
    async def execute(self, function_name, **kwargs) -> Dict:
        """
        执行插件并返回JSON可序列化响应
        Execute the plugin and return a JSON serializable response
        """
        pass
