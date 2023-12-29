import requests
import subprocess
from urllib.parse import urlparse
from pathlib import Path

class TorrentLinkManager:
    def __init__(self, qb_url, qb_username, qb_password, source_folder, base_dirs, tracker_keywords):
        self.qb_url = qb_url
        self.qb_username = qb_username
        self.qb_password = qb_password
        self.source_folder = Path(source_folder)
        self.base_dirs = base_dirs
        self.tracker_keywords = set(tracker_keywords)

    def create_hard_link(self, source, link_name):
        """ 创建硬链接 """
        subprocess.run(['mklink', '/H', link_name, source], shell=True, check=True)

    def remove_hard_links(self, folder):
        """ 移除文件夹中的所有硬链接 """
        for item in folder.glob('*'):
            if item.is_file():
                try:
                    item.unlink()  # 删除硬链接
                except OSError as e:
                    print(f"Error removing {item}: {e}")

    def replicate_structure_and_link(self, src_folder, dest_base_folder):
        """ 复制目录结构并为每个文件创建硬链接 """
        if src_folder.is_file():
            for base_dir in self.base_dirs:
                dest_file = dest_base_folder.joinpath(src_folder.name)
                self.create_hard_link(str(src_folder), str(dest_file))
        else:
            for src_path in src_folder.rglob('*'):
                if src_path.is_file():
                    rel_path = src_path.relative_to(src_folder)
                    dest_path = dest_base_folder.joinpath(rel_path)
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    self.create_hard_link(str(src_path), str(dest_path))

    def create_links_for_trackers(self):
        """ 为源文件夹在指定tracker目录下创建硬链接 """
        session = requests.Session()
        session.post(f"{self.qb_url}api/v2/auth/login", data={'username': self.qb_username, 'password': self.qb_password})

        for base_dir in self.base_dirs:
            pt_dir = Path(base_dir, 'PT')
            pt_dir.mkdir(parents=True, exist_ok=True)

            for tracker_keyword in self.tracker_keywords:
                tracker_folder = pt_dir.joinpath(tracker_keyword)
                if tracker_folder.exists():
                    self.remove_hard_links(tracker_folder)  # 移除现有的硬链接
                tracker_folder.mkdir(parents=True, exist_ok=True)
                self.replicate_structure_and_link(self.source_folder, tracker_folder)

# 使用示例
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''
source_folder1 = r'D:\hardLink'           # 源文件夹或文件路径
base_dirs1 = ['D:\\']                    # 硬盘路径
source_folder2 = r'F:\hardLink'           # 源文件夹或文件路径
base_dirs2 = ['F:\\']                    # 硬盘路径
source_folder3 = r'G:\hardLink'           # 源文件夹或文件路径
base_dirs3 = ['G:\\']                    # 硬盘路径
tracker_keywords = ['dmhy','nicept','nicept','creditracker']  # 指定的tracker关键字列表

torrent_link_manager1 = TorrentLinkManager(qb_url, qb_username, qb_password, source_folder1, base_dirs1, tracker_keywords)
torrent_link_manager2 = TorrentLinkManager(qb_url, qb_username, qb_password, source_folder2, base_dirs2, tracker_keywords)
torrent_link_manager3 = TorrentLinkManager(qb_url, qb_username, qb_password, source_folder3, base_dirs3, tracker_keywords)
torrent_link_manager1.create_links_for_trackers()
torrent_link_manager2.create_links_for_trackers()
torrent_link_manager3.create_links_for_trackers()
