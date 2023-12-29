import requests
import shutil
import os
from pathlib import Path
from collections import defaultdict

class DiskTorrentCalculator:
    def __init__(self, qb_url, qb_username, qb_password):
        self.qb_url = qb_url
        self.qb_username = qb_username
        self.qb_password = qb_password

    def get_torrents_info(self):
        """ 获取所有种子信息 """
        session = requests.Session()
        session.post(f"{self.qb_url}api/v2/auth/login", data={'username': self.qb_username, 'password': self.qb_password})
        response = session.get(f"{self.qb_url}api/v2/torrents/info")
        return response.json()

    def calculate_storage_usage(self, torrents):
        """ 计算每个盘符下种子的存储占用 """
        storage_usage = defaultdict(int)
        unique_torrents = set()

        for torrent in torrents:
            name = torrent['name']
            size = torrent['size']
            save_path = Path(torrent['save_path'])
            drive = save_path.drive

            unique_identifier = (name, str(save_path))
            if unique_identifier not in unique_torrents:
                unique_torrents.add(unique_identifier)
                storage_usage[drive] += size

        return storage_usage

    def get_disk_space(self):
        """ 获取每个盘符的剩余存储空间 """
        disk_space = {}
        drives = [f"{drive}:\\" for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{drive}:\\")]
        for drive in drives:
            total, used, free = shutil.disk_usage(drive)
            disk_space[drive] = free
        return disk_space

    def combine_disk_and_torrent_usage(self, disk_space, storage_usage):
        """ 结合盘符剩余空间和种子存储占用情况 """
        combined_usage = {}
        for drive_with_colon, usage in storage_usage.items():
            drive = drive_with_colon.split(':')[0] + ':\\'
            if drive in disk_space:
                combined_usage[drive] = disk_space[drive] + usage
            else:
                print(f"Warning: Drive {drive} found in torrent usage but not in disk space data.")
        return combined_usage

    def save_combined_usage_to_file(self, combined_usage, file_path):
        """ 保存结合后的使用情况到TXT文件 """
        with open(file_path, 'w') as file:
            for drive, usage in combined_usage.items():
                file.write(f"{drive}: {usage} bytes\n")

# 使用示例
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

calculator = DiskTorrentCalculator(qb_url, qb_username, qb_password)
torrents = calculator.get_torrents_info()
storage_usage = calculator.calculate_storage_usage(torrents)
disk_space = calculator.get_disk_space()
combined_usage = calculator.combine_disk_and_torrent_usage(disk_space, storage_usage)

# 保存结合后的使用情况到TXT文件
combined_usage_file = 'combined_usage_info.txt'
calculator.save_combined_usage_to_file(combined_usage, combined_usage_file)
