import requests
from pathlib import Path

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

def validate_locations(file_path, calculator):
    """验证存储空间分配是否正确"""
    locations = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) != 2:
                continue
            torrent_name, location = parts
            locations[torrent_name] = location

    torrents_info = calculator.get_torrents_info()
    torrent_size_map = {torrent['name']: torrent['size'] for torrent in torrents_info}

    storage_usage = {}
    for torrent_name, location in locations.items():
        if torrent_name in torrent_size_map:
            size = torrent_size_map[torrent_name]
            storage_usage[location] = storage_usage.get(location, 0) + size

    return storage_usage

# 设置 qBittorrent Web API 的连接信息
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

calculator = DiskTorrentCalculator(qb_url, qb_username, qb_password)

# 验证 final_locations.txt 中的存储空间分配
locations_file = 'final_locations.txt'
usage = validate_locations(locations_file, calculator)

# 打印各盘符下种子的占用情况
for drive, size in usage.items():
    print(f"Drive {drive} usage: {size} bytes")
