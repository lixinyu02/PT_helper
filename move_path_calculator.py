from disk_torrent_calculator import DiskTorrentCalculator
import shutil
from pathlib import Path

class TorrentBalancer:
    def __init__(self, calculator):
        self.calculator = calculator

    def balance_torrents(self, torrents, combined_usage):
        # 移除同名种子的重复项
        unique_torrents = {torrent['name']: torrent for torrent in torrents}.values()

        # 识别包含种子的盘符
        drives_with_torrents = set(Path(torrent['save_path']).drive + '\\' for torrent in unique_torrents)

        # 计算目标容量
        total_free_space = sum(shutil.disk_usage(drive).free for drive in drives_with_torrents)
        target_capacity = total_free_space / len(drives_with_torrents) if drives_with_torrents else 0

        # 初始化最终位置字典
        final_locations = {torrent['name']: Path(torrent['save_path']).drive + '\\' for torrent in unique_torrents}

        for torrent in unique_torrents:
            current_drive = final_locations[torrent['name']]
            best_drive = None
            smallest_variance = float('inf')

            # 计算移动后最小方差的盘符
            for drive, usage in combined_usage.items():
                if drive != current_drive:
                    temp_combined_usage = combined_usage.copy()
                    temp_combined_usage[drive] -= torrent['size']  # 种子增加，空间减少
                    temp_combined_usage[current_drive] += torrent['size']  # 种子移动，原盘符空间增加

                    # 计算方差
                    variance = sum((temp_combined_usage[d] - target_capacity) ** 2 for d in drives_with_torrents)
                    if variance < smallest_variance:
                        smallest_variance = variance
                        best_drive = drive

            # 执行移动
            if best_drive and combined_usage[best_drive] >= torrent['size']:
                combined_usage[best_drive] -= torrent['size']  # 更新目标盘符的剩余空间
                final_locations[torrent['name']] = best_drive
            else:
                combined_usage[current_drive] -= torrent['size']  # 更新源盘符的剩余空间，即使未移动

        # 保存最终位置到文件
        with open('final_locations.txt', 'w', encoding='utf-8') as file:
            for torrent, location in final_locations.items():
                file.write(f"{torrent}: {location}\n")

        return combined_usage, final_locations

# 使用示例代码
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

calculator = DiskTorrentCalculator(qb_url, qb_username, qb_password)
torrents = calculator.get_torrents_info()
storage_usage = calculator.calculate_storage_usage(torrents)
disk_space = calculator.get_disk_space()
combined_usage = calculator.combine_disk_and_torrent_usage(disk_space, storage_usage)

balancer = TorrentBalancer(calculator)
new_combined_usage, final_locations = balancer.balance_torrents(torrents, combined_usage)

# 打印移动结果和最终盘符剩余空间
print("Final locations saved to 'final_locations.txt'.\n")
for drive, usage in new_combined_usage.items():
    print(f"{drive}: {usage} bytes")
