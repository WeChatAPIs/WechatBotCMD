from bot.infrastructure.wexin import WechatUtils

class CdnNativeApi:
    """
    CDN原生接口
    """
    pass

def upload_to_cdn(wechatId: object, file_path: object, type: object = 5) -> object:
    """
    上传文件到微信CDN
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    # 如果是http开头的，下载到本地，然后上传
    # 如果是本地文件，直接上传
    local_file_path, md5 = WechatUtils.getFilePathAndMd5(file_path)
    resdata = WechatUtils._post_wx_request(wechatId, {
        "type": 7,
        "filePath": local_file_path,
        "aeskey": md5,
        "fileType": type,
    })
    return resdata["data"]["fileId"]


def upload_img_to_cdn(wechatId: object, file_path: object) -> object:
    """
    上传图片到微信CDN
    :param wechatId:
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    return upload_to_cdn(wechatId, file_path, 2)


def upload_audio_to_cdn(wechatId: object, file_path: object) -> object:
    """
    上传语音
    :param wechatId:
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    return upload_to_cdn(wechatId, file_path, 15)