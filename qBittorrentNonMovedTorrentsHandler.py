import requests
import os

class TorrentMover:
    def __init__(self, qb_url, qb_username, qb_password, non_moved_file_path):
        self.qb_url = qb_url
        self.qb_username = qb_username
        self.qb_password = qb_password
        self.non_moved_file_path = non_moved_file_path

    def move_torrents(self):
        # 登录 qBittorrent Web API
        session = requests.Session()
        session.post(f"{self.qb_url}api/v2/auth/login", data={'username': self.qb_username, 'password': self.qb_password})

        # 读取未移动种子文件
        with open(self.non_moved_file_path, 'r') as file:
            non_moved_torrents = [line.strip() for line in file.readlines()]

        # 获取所有种子的信息
        response = session.get(f"{self.qb_url}api/v2/torrents/info")
        torrents_info = {torrent['name']: torrent for torrent in response.json()}

        # 展示所有预定的移动操作
        print("Planned torrent moves:")
        planned_moves = []
        for torrent_name in non_moved_torrents:
            torrent_info = torrents_info.get(torrent_name)
            if torrent_info:
                drive = os.path.splitdrive(torrent_info['save_path'])[0]
                hardlink_folder = os.path.join(drive, '\hardLink')
                new_save_path = os.path.join(hardlink_folder, os.path.basename(torrent_info['save_path']))
                planned_moves.append((torrent_info, new_save_path))
                print(f"'{torrent_name}' from '{torrent_info['save_path']}' to '{new_save_path}'")

        # 等待用户确认
        confirm = input("\nConfirm moves? (y/n): ")
        if confirm.lower() == 'y':
            # 执行移动操作
            for torrent_info, new_save_path in planned_moves:
                self._set_new_save_path(session, torrent_info, new_save_path)
        else:
            print("Move operation cancelled.")

    def _set_new_save_path(self, session, torrent_info, new_save_path):
        # 创建 hardLink 文件夹（如果不存在）
        if not os.path.exists(os.path.dirname(new_save_path)):
            os.makedirs(os.path.dirname(new_save_path))

        # 通过 API 设置新的保存路径
        session.post(f"{self.qb_url}api/v2/torrents/setLocation", data={'hashes': torrent_info['hash'], 'location': new_save_path})
        print(f"Set new save path for '{torrent_info['name']}' to '{new_save_path}'")

# 使用示例
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''
non_moved_file_path = 'non_moved_torrents.txt' # 未移动种子文件路径

mover = TorrentMover(qb_url, qb_username, qb_password, non_moved_file_path)
mover.move_torrents()
