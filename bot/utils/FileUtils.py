import os
import time

from PIL import Image
from moviepy.editor import VideoFileClip


def get_file_info(file_path) -> object:
    try:
        # 如果是mac电脑，返回默认值
        if os.name == "posix":
            # 生成随机32位字符串
            return {
                "file_size": 1,
                "image_width": 1440.0,
                "image_height": 1080.0,
                "video_duration": None
            }


    # 使用os.stat获取文件元数据 文件大小（以字节为单位）
        file_size = os.stat(file_path).st_size

        # 获取文件扩展名
        file_extension = os.path.splitext(file_path)[1].lower()

        # 初始化图像宽度和高度以及视频时长为None
        image_width = None
        image_height = None
        video_duration = None

        # 如果文件是图像
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            with Image.open(file_path) as img:
                image_width, image_height = img.size

        # 如果文件是视频
        elif file_extension in ['.mp4', '.avi', '.mkv', '.mov', '.flv']:
            try:
                # 使用VideoFileClip加载视频文件，仅读取元信息，不加载整个视频
                with VideoFileClip(file_path, audio=False) as video:
                    video_duration = int(video.duration * 1000)  # 将秒数转换为毫秒
            except Exception as e:
                print(f"无法获取视频时长：{e}")

        return {
            "file_size": file_size,
            "image_width": image_width,
            "image_height": image_height,
            "video_duration": video_duration
        }
    except FileNotFoundError:
        raise FileNotFoundError("文件不存在")
    except Exception as e:
        raise Exception(f"获取文件信息失败，错误信息：{e}")