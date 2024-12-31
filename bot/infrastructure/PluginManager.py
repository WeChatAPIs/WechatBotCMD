import importlib
import inspect
import json
import os

from bot.config.config_loader import ChatGptConfig
from bot.infrastructure.plugins.Plugin import Plugin


class PluginManager:
    """
    管理插件并调用正确函数的类
    A class to manage the plugins and call the correct functions
    """

    def __init__(self):
        enabled_plugins = ChatGptConfig['plugins'].split(',')
        plugins = []
        # 当前环境是windows电脑
        if os.name == 'nt':
            # 创建目标目录路径
            directory = 'bot\\infrastructure\\plugins'
        else:
            directory = 'bot/infrastructure/plugins'
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = f"bot.infrastructure.plugins.{module_name}"
                module = importlib.import_module(module_path)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                        if obj.get_source_name(self) in enabled_plugins:
                            plugins.append(obj())
        self.plugins = plugins

    def get_functions_specs(self):
        """
        返回模型可以调用的函数规范列表
        Return the list of function specs that can be called by the model
        """
        return [spec for specs in map(lambda plugin: plugin.get_spec(), self.plugins) for spec in specs]

    def call_function(self, function_name, arguments):
        """
        根据提供的名称和参数调用函数
        Call a function based on the name and parameters provided
        """
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return json.dumps({'error': f'Function {function_name} not found'})
        return json.dumps(plugin.execute(function_name, **json.loads(arguments)), default=str)

    def get_plugin_source_name(self, function_name) -> str:
        """
        返回插件的源名称
        Return the source name of the plugin
        """
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return ''
        return plugin.get_source_name(self)

    def __get_plugin_by_function_name(self, function_name):
        # 按函数名获取插件
        return next((plugin for plugin in self.plugins
                     if function_name in map(lambda spec: spec.get('name'), plugin.get_spec())), None)


