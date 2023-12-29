import requests

class MoveInfoExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_moves(self):
        # 读取文件并解析出移动信息
        moves = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    torrent_name, move_info = parts
                    move_parts = move_info.split(" -> ")
                    if len(move_parts) == 2:
                        from_drive, to_drive = move_parts[0].strip()  , move_parts[1].strip() + ':\\'
                moves.append((torrent_name, from_drive, to_drive))
        return moves

import requests

class TorrentMover:
    def __init__(self, qb_url, qb_username, qb_password, move_file_path):
        self.qb_url = qb_url
        self.qb_username = qb_username
        self.qb_password = qb_password
        self.move_file_path = move_file_path
        self.session = requests.Session()

    def login(self):
        # 登录 qBittorrent Web API
        response = self.session.post(f"{self.qb_url}api/v2/auth/login", data={'username': self.qb_username, 'password': self.qb_password})
        if response.text != 'Ok.':
            print("登录失败，请检查用户名和密码")
            return False
        return True

    def get_torrents_info(self):
        # 获取所有种子信息
        response = self.session.get(f"{self.qb_url}api/v2/torrents/info")
        return {torrent['name']: torrent for torrent in response.json()}

    def move_torrents(self):
        # 从文件中提取移动信息
        extractor = MoveInfoExtractor(self.move_file_path)
        move_info = extractor.extract_moves()

        torrents_info = self.get_torrents_info()

        # 展示所有预计的种子移动路径
        for torrent_name, from_drive, to_drive in move_info:
            if torrent_name in torrents_info:
                torrent = torrents_info[torrent_name]
                new_save_path = f"{to_drive}\\hardLink\\{torrent['name']}"
                print(f"Planned move: '{torrent['name']}' from {from_drive} to {new_save_path}")

        # 获取用户确认
        confirm = input("Confirm all moves? (y/n): ")
        if confirm.lower() == 'y':
            for torrent_name, from_drive, to_drive in move_info:
                if torrent_name in torrents_info:
                    self.move_torrent(torrents_info[torrent_name], to_drive)
        else:
            print("All moves cancelled.")

    def move_torrent(self, torrent, to_drive):
        # 移动单个种子到新的盘符
        new_save_path = f"{to_drive}\\hardLink\\{torrent['name']}"
        self.session.post(f"{self.qb_url}api/v2/torrents/setLocation", data={'hashes': torrent['hash'], 'location': new_save_path})
        print(f"Moved '{torrent['name']}' to {new_save_path}")

# 使用示例
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''
move_file_path = 'cross_drive_moves.txt'

mover = TorrentMover(qb_url, qb_username, qb_password, move_file_path)
if mover.login():
    mover.move_torrents()


