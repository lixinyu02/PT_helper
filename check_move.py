from disk_torrent_calculator import DiskTorrentCalculator

class MoveChecker:
    def __init__(self, calculator):
        self.calculator = calculator

    def check_and_rearrange_moves(self, cross_drive_moves_file):
        torrents_info = self.calculator.get_torrents_info()
        disk_space = self.calculator.get_disk_space()

        valid_moves = []
        problematic_moves = []
        with open(cross_drive_moves_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    torrent_name, move_info = parts
                    move_parts = move_info.split(" -> ")
                    if len(move_parts) == 2:
                        from_drive, to_drive = move_parts[0].strip()  , move_parts[1].strip() + ':\\'
                        size = next((torrent['size'] for torrent in torrents_info if torrent['name'] == torrent_name), None)

                        if size and disk_space.get(to_drive, 0) >= size:
                            valid_moves.append((torrent_name, from_drive, to_drive))
                            disk_space[to_drive] -= size
                            disk_space[from_drive] += size
                        else:
                            problematic_moves.append((torrent_name, from_drive, to_drive))

        return valid_moves, problematic_moves

# 使用示例代码
qb_url = 'http://localhost:8080/'
qb_username = ''
qb_password = ''

calculator = DiskTorrentCalculator(qb_url, qb_username, qb_password)
checker = MoveChecker(calculator)
valid_moves, problematic_moves = checker.check_and_rearrange_moves('cross_drive_moves.txt')

# 输出有效移动和问题移动
print("Valid Moves:")
for move in valid_moves:
    print(move)

print("\nProblematic Moves:")
for problematic_move in problematic_moves:
    print(problematic_move)
