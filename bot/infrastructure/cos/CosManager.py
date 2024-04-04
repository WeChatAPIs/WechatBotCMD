import logging
import os
import threading
import time

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from bot.config import config_loader
from bot.data import DbCos

log = logging.getLogger(__name__)


class CosManager:
    def __init__(self):
        cosConfig = config_loader.loadCosConfig()
        self.enable = cosConfig["enable"]
        if cosConfig["enable"] == "false":
            return
        region, secret_id, secret_key = cosConfig['region'], cosConfig['secret_id'], cosConfig['secret_key']
        self.cos_client = CosS3Client(CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key))

        self.bucket = cosConfig["bucket"] if cosConfig["bucket"] else "examplebucket-1250000000"
        self.checkAndCreateBucket(self.bucket)
        # 省钱任务
        schedule_delete_file = threading.Thread(target=self.schedule_delete_file)
        schedule_delete_file.start()

    def checkAndCreateBucket(self, bucket):
        exists = self.cos_client.bucket_exists(
            Bucket=bucket
        )
        if exists:
            return True
        self.cos_client.create_bucket(
            Bucket=bucket
        )

    def checkOpen(self):
        return self.enable == "true"

    def put_object(self, file_path):
        # 文件不存在
        if not os.path.exists(file_path):
            return None
        # 获取文件名
        file_name = os.path.basename(file_path)

        has_object = self.cos_client.object_exists(
            Bucket=self.bucket,
            Key=file_name)
        if not has_object:
            self.cos_client.upload_file(
                Bucket=self.bucket,
                LocalFilePath=file_path,
                Key=file_name,
                PartSize=1,
                MAXThread=10,
                EnableMD5=False
            )
        DbCos.insert_wait_delete_file(file_name)
        data = self.cos_client.get_object_url(
            Bucket=self.bucket,
            Key=file_name
        )
        return data

    def schedule_delete_file(self):
        while config_loader.App_Run_Status:
            # 通过好友验证
            data = DbCos.select_wait_delete_file()
            for id, file_key in data:
                self.del_object(id, file_key)
            time.sleep(60)

    def del_object(self, id, file_key):
        has_object = self.cos_client.object_exists(
            Bucket=self.bucket,
            Key=file_key)
        if has_object:
            self.cos_client = self.cos_client.delete_object(
                Bucket=self.bucket,
                Key=file_key
            )
        DbCos.delete_file(id)
        return True
