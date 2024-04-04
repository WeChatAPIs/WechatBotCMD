from datetime import datetime, timedelta
from typing import Dict

from bot.infrastructure.plugins.Plugin import Plugin


class NowTimePlugin(Plugin):
    """
    用于获取当前天气和一个地点的7天每日预报的插件
    A plugin to get the current weather and 7-day daily forecast for a location
    """

    def get_source_name(self) -> str:
        return "NowTime"

    def get_spec(self) -> [Dict]:
        return [
            {
                "name": "get_now_time",
                "description": "Get the time for today and tomorrow",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "return": {
                    "type": "object",
                    "properties": {
                        "current_time": {
                            "type": "string",
                            "format": "time",
                            "description": "Current time formatted as 'YYYY-MM-DD HH:MM:SS'"
                        },
                        "today_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Today's date formatted as 'YYYY-MM-DD'"
                        },
                        "tomorrow_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Tomorrow's date formatted as 'YYYY-MM-DD'"
                        }
                    }
                }
            }
        ]

    async def execute(self, function_name, **kwargs) -> Dict:
        # 返回当前时间
        current_datetime = datetime.now()
        # 计算明天的日期
        tomorrow_date = current_datetime + timedelta(days=1)
        return {
            'current_time': current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'today_date': current_datetime.strftime('%Y-%m-%d'),
            'tomorrow_date': tomorrow_date.strftime('%Y-%m-%d')
        }
