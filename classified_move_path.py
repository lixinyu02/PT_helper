from disk_torrent_calculator import DiskTorrentCalculator
from pathlib import Path

def process_torrents(torrents, final_locations):
    # 读取最终位置文件
    with open(final_locations, 'r', encoding='utf-8') as file:
        final_locations_dict = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in file}

    # 初始化列表
    cross_drive_moves = []
    non_moved_torrents = []
    processed_torrent_names = set()

    for torrent in torrents:
        torrent_name = torrent['name']
        original_drive = Path(torrent['save_path']).drive + '\\'
        final_drive = final_locations_dict.get(torrent_name, None)

        if torrent_name not in processed_torrent_names:
            if final_drive and original_drive != final_drive:
                cross_drive_moves.append(f"{torrent_name}: {original_drive} -> {final_drive}")
            else:
                non_moved_torrents.append(torrent_name)

            processed_torrent_names.add(torrent_name)

    return cross_drive_moves, non_moved_torrents

# 使用示例代码
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

calculator = DiskTorrentCalculator(qb_url, qb_username, qb_password)
torrents = calculator.get_torrents_info()

# 处理种子并获取需要移动和未移动的种子列表
cross_drive_moves, non_moved_torrents = process_torrents(torrents, 'final_locations.txt')

# 保存需要跨盘移动的种子信息到文件
with open('cross_drive_moves.txt', 'w', encoding='utf-8') as file:
    for item in cross_drive_moves:
        file.write(item + "\n")

# 保存未移动的种子信息到文件
with open('non_moved_torrents.txt', 'w', encoding='utf-8') as file:
    for item in non_moved_torrents:
        file.write(item + "\n")

print(f"Cross drive moves saved to 'cross_drive_moves.txt'.")
print(f"Non-moved torrents saved to 'non_moved_torrents.txt'.")
