import requests
from pathlib import Path
class TorrentMover:
    def __init__(self, qb_url, qb_username, qb_password):
        self.qb_url = qb_url
        self.qb_username = qb_username
        self.qb_password = qb_password
        self.session = requests.Session()
        self.session.post(f"{self.qb_url}api/v2/auth/login", data={'username': self.qb_username, 'password': self.qb_password})

    def get_torrents_info(self):
        response = self.session.get(f"{self.qb_url}api/v2/torrents/info")
        return response.json()

    def move_same_name_torrents(self):
        torrents_info = self.get_torrents_info()
        same_name_groups = self.group_by_name(torrents_info)

        for name, torrents in same_name_groups.items():
            print(f"Processing torrents with name: {name}")
            target_path = self.find_target_path(torrents)

            if target_path:
                print(f"Target path for '{name}': {target_path}")
                for torrent in torrents:
                    if torrent['save_path'] != target_path:
                        print(f"Moving torrent '{torrent['name']}' from {torrent['save_path']} to {target_path}")
                        self.set_torrent_location(torrent['hash'], target_path)

    def group_by_name(self, torrents_info):
        groups = {}
        for torrent in torrents_info:
            groups.setdefault(torrent['name'], []).append(torrent)
        return groups

    def find_target_path(self, torrents):
        for torrent in torrents:
            # 使用 Path 来处理路径，并检查路径部分中是否包含 'hardLink'
            if 'hardLink' in Path(torrent['save_path']).parts:
                return torrent['save_path']
        return None

    def set_torrent_location(self, torrent_hash, location):
        print(f"Setting new location for torrent {torrent_hash}: {location}")  # 调试信息
        self.session.post(f"{self.qb_url}api/v2/torrents/setLocation", data={'hashes': torrent_hash, 'location': location})

# 使用示例
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

mover = TorrentMover(qb_url, qb_username, qb_password)
mover.move_same_name_torrents()
