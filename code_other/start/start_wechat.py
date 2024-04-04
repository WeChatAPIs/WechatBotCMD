import ctypes
import json
import os
import time

import requests

rpd = ctypes.cdll.LoadLibrary("./wxrpd64.dll")

rpd_StartWechat = rpd.rpd_StartWechat
rpd_LoadLibrary = rpd.rpd_LoadLibrary
rpd_FreeLibrary = rpd.rpd_FreeLibrary
rpd_CreateRemoteThread = rpd.rpd_CreateRemoteThread

rpd_StartWechat.argtypes = [ctypes.c_char_p]
rpd_StartWechat.restype = ctypes.c_uint

rpd_LoadLibrary.argtypes = [ctypes.c_uint,
                            ctypes.c_char_p]
rpd_LoadLibrary.restype = ctypes.c_ulonglong

rpd_FreeLibrary.argtypes = [ctypes.c_uint,
                            ctypes.c_char_p]
rpd_FreeLibrary.restype = ctypes.c_bool

rpd_CreateRemoteThread.argtypes = [ctypes.c_uint,
                                   ctypes.c_char_p,
                                   ctypes.c_char_p,
                                   ctypes.c_void_p]
rpd_CreateRemoteThread.restype = ctypes.c_uint


# 微信多开
def start_wechat(bin_path: str = "") -> int:
    return rpd_StartWechat(
        ctypes.c_char_p(bin_path.encode("utf-8")) if bin_path else ctypes.c_char_p(0)
    )


# 注入dll
def load_dll(_pid: int, module_path: str) -> bool:
    return rpd_LoadLibrary(
        ctypes.c_uint(_pid),
        ctypes.c_char_p(module_path.encode("utf-8"))
    ) != 0


# 卸载dll
def unload_dll(_pid: int, module_name: str) -> bool:
    return rpd_FreeLibrary(
        ctypes.c_uint(_pid),
        module_name.encode("utf-8")
    )


# 调用远程函数
def call_remote_function(_pid: int,
                         module_name: str,
                         func_name: str,
                         params: int = 0) -> int:
    return rpd_CreateRemoteThread(
        ctypes.c_uint(_pid),
        module_name.encode("utf-8"),
        func_name.encode("utf-8"),
        ctypes.c_void_p(params)
    )


if __name__ == "__main__":
    pid = start_wechat()
    print(pid)
    time.sleep(1)
    local_path = os.path.split(os.path.abspath(__file__))[0]
    print(load_dll(pid, os.path.join(local_path, "wxapi64.dll")))
    print(call_remote_function(pid, "wxapi64.dll", "start_http_server", 8888))
    time.sleep(1)
    # 获取登录二维码
    data = {"type": 28}
    resp = requests.post("http://127.0.0.1:8888/api/", data=json.dumps(data))
    print(resp.status_code)
    if resp.status_code == 200:
        print(resp.text)
