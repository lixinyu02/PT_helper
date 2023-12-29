### 项目说明

#### 目的

本项目旨在实现在多个磁盘之间均衡分配 qBittorrent 种子文件的存储位置。项目的核心目标是通过一系列自动化脚本，优化种子文件的存储方式，使得各个磁盘的剩余空间更加平均，从而有效利用硬盘资源，避免单个磁盘因过度存储而导致的性能问题。

#### 功能

1. **移动文件和计算路径**：计算最佳移动方案以均衡磁盘使用。
2. **验证和检查移动**：确认移动方案的可行性，确保不会超出磁盘容量限制。
3. **分类和执行移动**：根据计算结果执行实际的移动操作，更新 qBittorrent 中的种子存储位置。
4. **处理重复种子**：解决由于移动操作产生的同名种子位置不一致的问题。

#### 可选项 - 硬链接（Hardlink）

为了进一步优化种子文件的组织和管理，项目提供了创建硬链接的可选功能。通过硬链接，用户可以在不同的位置创建指向同一文件的入口，这样可以在不实际移动文件的情况下，将同一种子文件在 qBittorrent 中显示在不同的目录下。这对于特定的文件管理策略或是节约磁盘空间非常有用。

#### 使用场景

- 用户有多个硬盘，但种子文件的存储未得到很好的均衡，导致某些磁盘空间紧张。
- 用户需要按照特定的规则（如磁盘空间使用率）自动管理和优化种子文件的存储位置。
- 用户希望在保持种子文件组织和结构一致的情况下，有效地使用硬盘空间。

通过本项目，用户可以轻松地管理大量种子文件，确保它们在多个磁盘间均衡分布，同时保持 qBittorrent 中的组织和结构清晰有序

### 准备工作

1. **配置 qBittorrent Web 服务器地址和账号密码**：在每个脚本中设置 qBittorrent 的 Web API 地址、用户名和密码。

### 移动文件和计算路径

2. **随机移动文件**：手动将一些种子文件移动到不同的硬盘盘符下。这一步骤旨在创建一个需要重新平衡种子存储位置的场景。
3. **执行 `move_path_calculator.py`**：此脚本会计算最佳的种子文件移动方案，以达到盘符间存储的均衡。它会生成 `final_locations.txt` 文件，其中包含每个种子最终应该存放的位置。

### 验证和检查移动

4. **执行 `validate_location.py`（可选）**：此脚本用于验证 `final_locations.txt` 中的存储空间分配是否正确。它将打印出每个盘符下种子的占用情况。
5. **执行 `check_move.py`**：此脚本检查 `final_locations.txt` 中的移动方案是否可行，考虑到磁盘空间限制。它将生成两个列表：有效移动和问题移动。

### 分类和执行移动

6. **执行 `classified_move_path.py`**：此脚本根据 `final_locations.txt` 的结果，生成需要跨盘移动的种子列表（`cross_drive_moves.txt`）和未移动的种子列表（`non_moved_torrents.txt`）。
7. **执行 `qBittorrentNonMovedTorrentsHandler.py`**：此脚本处理 `non_moved_torrents.txt` 中的种子，将它们在 qBittorrent 中的保存路径更新到对应盘符下的 `hardLink` 文件夹。
8. **执行 `qBittorrentCrossDriveMover.py`**：此脚本处理 `cross_drive_moves.txt` 中的种子，执行跨盘移动，同时更新 qBittorrent 中的保存路径。

### 处理重复种子

9. **执行 `TorrentLocationConsolidator.py`**：最后，此脚本处理由于之前的移动操作可能产生的同名种子位置不一致的情况。它会确保所有同名种子的保存位置一致。

### 使用建议

- 在执行每个脚本之前，请确保理解其功能并按需调整代码中的配置。
- 建议在执行实际移动操作之前进行充分的测试，以避免数据丢失或错误操作。
- 对于可能影响大量数据的操作，建议先进行备份。

###

### 脚本名称: `move_path_calculator.py`

### 说明文档

#### 功能简介

`move_path_calculator.py` 是一个自动化脚本，用于在 qBittorrent 客户端中平衡种子文件在不同驱动器间的分布。该脚本通过计算各驱动器的剩余空间，找出最佳的种子移动方案以最小化方差，从而实现空间均衡。

#### 使用前提

- qBittorrent 的 Web UI 功能已启用。
- Python 环境已安装。
- 种子信息可通过 qBittorrent 的 Web API 获取。

#### 功能特点

- 自动处理重复的同名种子，确保每个种子仅被处理一次。
- 计算各驱动器的剩余空间，并基于此信息进行种子移动方案的制定。
- 输出最终的种子位置到 `final_locations.txt` 文件中。

#### 如何使用

1. **配置 qBittorrent Web UI**：
  
  - 确保 qBittorrent 客户端的 Web UI 功能已开启并可访问。
  - 获取 Web UI 的 URL、用户名和密码。
2. **准备 Python 环境**：
  
  - 确保已在系统中安装 Python。
  - 安装必要的依赖库，如 `shutil` 和 `pathlib`。
3. **运行脚本**：
  
  - 保存 `move_path_calculator.py` 到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    ```bash
    python move_path_calculator.py
    ```
    
  - 脚本将连接到 qBittorrent 客户端，计算最佳移动方案，并将结果保存到 `final_locations.txt` 文件中。
    

#### 输出文件

- **`final_locations.txt`**：包含每个种子的最终位置。每行格式为 `种子名称: 盘符`，指示种子应移至的驱动器。

#### 注意事项

- 确保 qBittorrent 客户端在执行脚本期间保持运行状态。
- 脚本仅计算最佳移动方案，实际的文件移动需要其他操作或脚本实现。

---

### 脚本名称: `validate_location.py`

### 说明文档

#### 功能简介

`validate_location.py` 是一个 Python 脚本，用于验证种子文件在不同驱动器上的存储空间分配是否正确。它主要根据 `final_locations.txt` 文件中的信息来验证种子文件是否正确地分配到了指定的驱动器上。

#### 使用前提

- `final_locations.txt` 文件已存在且包含种子的最终位置信息。
- Python 环境已安装。
- qBittorrent Web API 可用。

#### 功能特点

- 读取 `final_locations.txt`，获取种子文件的最终位置。
- 使用 qBittorrent Web API 获取所有种子的大小信息。
- 计算每个驱动器上种子文件的总占用空间。

#### 如何使用

1. **准备文件**：
  
  - 确保 `final_locations.txt` 文件存在并包含有效数据。
2. **运行脚本**：
  
  - 保存 `validate_location.py` 到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    ```bash
    python validate_location.py
    ```
    
  - 脚本将分析种子文件的存储分配并打印每个驱动器上种子的总占用空间。
    

#### 输出结果

- 打印各驱动器上种子文件的占用空间，格式为：`Drive [驱动器] usage: [占用空间] bytes`。

#### 注意事项

- 确保 qBittorrent 客户端在运行脚本期间保持运行状态，以便脚本能够从 Web API 获取数据。
- 此脚本不会进行任何种子文件的移动操作，只是用于验证存储空间分配的正确性。

---

### 脚本名称: `check_move.py`

### 说明文档

#### 功能简介

`check_move.py` 是一个 Python 脚本，用于验证和重新安排跨盘移动的种子文件，确保移动操作不会超过目标盘符的存储上限。脚本基于 `cross_drive_moves.txt` 文件中的信息进行操作。

#### 使用前提

- `cross_drive_moves.txt` 文件已存在且包含需要跨盘移动的种子信息。
- Python 环境已安装。
- qBittorrent Web API 可用。

#### 功能特点

- 从 `cross_drive_moves.txt` 读取跨盘移动信息。
- 使用 qBittorrent Web API 获取所有种子的大小和所在盘符的剩余空间。
- 确保每个移动操作不会导致目标盘符的存储空间超过上限。
- 区分有效移动和可能存在问题的移动。

#### 如何使用

1. **准备文件**：
  
  - 确保 `cross_drive_moves.txt` 文件存在并包含有效数据。
2. **运行脚本**：
  
  - 保存 `check_move.py` 到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    bashCopy code
    
    `python check_move.py`
    
  - 脚本将验证每次移动操作，确保不会超过存储上限，并输出有效和问题移动。
    

#### 输出结果

- 打印有效的移动操作，格式为：`(种子名称, 从哪个盘符, 到哪个盘符)`。
- 打印可能存在问题的移动操作，格式同上。

#### 注意事项

- 确保 qBittorrent 客户端在运行脚本期间保持运行状态，以便脚本能够从 Web API 获取数据。
- 此脚本仅用于验证和重新安排移动操作，不会实际执行文件移动。

---

### 脚本名称: `classified_move_path.py`

### 说明文档

#### 功能简介

`classified_move_path.py` 是一个 Python 脚本，旨在分析和分类基于之前的平衡算法生成的种子移动方案。脚本根据 `final_locations.txt` 文件中的信息，区分哪些种子需要跨驱动器移动，以及哪些种子保持在原位置不变。

#### 使用前提

- `final_locations.txt` 文件已存在且包含种子的最终位置信息。
- Python 环境已安装。
- qBittorrent Web API 可用。

#### 功能特点

- 读取 `final_locations.txt`，提取每个种子的最终位置。
- 确定需要跨驱动器移动的种子以及保持原位置不变的种子。
- 输出两个文件：`cross_drive_moves.txt` 和 `non_moved_torrents.txt`。

#### 如何使用

1. **准备文件**：
  
  - 确保 `final_locations.txt` 文件存在并包含有效数据。
2. **运行脚本**：
  
  - 保存 `classified_move_path.py` 到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    ```bash
    python classified_move_path.py
    ```
    
  - 脚本将分析种子的移动方案并生成两个文件。
    

#### 输出文件

- **`cross_drive_moves.txt`**：包含需要跨驱动器移动的种子及其移动方向。格式为 `种子名称: 原始驱动器 -> 目标驱动器`。
- **`non_moved_torrents.txt`**：列出了保持原位置不变的种子名称。

#### 注意事项

- 确保 qBittorrent 客户端在运行脚本期间保持运行状态，以便脚本能够从 Web API 获取数据。
- 脚本不会实际移动文件，仅生成移动方案。

---

### 脚本名称: `qBittorrentNonMovedTorrentsHandler.py`

### 说明文档

#### 功能简介

`qBittorrentNonMovedTorrentsHandler.py` 是一个自动化脚本，用于处理在 qBittorrent 客户端中未跨驱动器移动的种子。脚本根据预先生成的种子列表（通常存储在 `non_moved_torrents.txt` 文件中），更新这些种子的保存路径到特定目录，如每个驱动器的 `hardLink` 文件夹。

#### 使用前提

- qBittorrent 的 Web UI 功能已启用。
- Python 环境已安装。
- `non_moved_torrents.txt` 文件中含有未移动的种子名列表。

#### 功能特点

- 自动读取 `non_moved_torrents.txt` 中的种子名称。
- 对于列表中的每个种子，脚本将更新其在 qBittorrent 客户端中的保存路径到相应驱动器的 `hardLink` 目录下。

#### 如何使用

1. **配置 qBittorrent Web UI**：
  
  - 确保 qBittorrent 客户端的 Web UI 功能已开启并可访问。
  - 记录 Web UI 的 URL、用户名和密码。
2. **准备 Python 环境**：
  
  - 确保已在系统中安装 Python。
  - 安装 `requests` 库（如果尚未安装）。
3. **运行脚本**：
  
  - 将 `qBittorrentNonMovedTorrentsHandler.py` 保存到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    ```bash
    python qBittorrentNonMovedTorrentsHandler.py
    ```
    
  - 脚本将连接到 qBittorrent 客户端，读取 `non_moved_torrents.txt` 文件，并更新种子的保存路径。
    

---

### 脚本名称: `qBittorrentCrossDriveMover.py`

### 说明文档

#### 功能简介

`qBittorrentCrossDriveMover.py` 是专为 qBittorrent 用户设计的脚本，用于处理跨驱动器移动的种子文件。该脚本依据 `cross_drive_moves.txt` 文件中记录的信息，执行跨驱动器的种子文件移动操作。

#### 使用前提

- qBittorrent 的 Web UI 功能已启用。
- Python 环境已安装。
- `cross_drive_moves.txt` 文件包含需要移动的种子信息，格式为：种子名称，原始盘符，目标盘符。

#### 功能特点

- 自动读取 `cross_drive_moves.txt` 文件，获取种子移动信息。
- 使用 qBittorrent Web API 更新种子文件的存储位置，实现跨驱动器移动。

#### 如何使用

1. **配置 qBittorrent Web UI**：
  
  - 确保 qBittorrent 客户端的 Web UI 功能已开启并可访问。
  - 获取 Web UI 的 URL、用户名和密码。
2. **准备 Python 环境**：
  
  - 确保已在系统中安装 Python。
  - 安装 `requests` 库（如果尚未安装）。
3. **运行脚本**：
  
  - 保存 `qBittorrentCrossDriveMover.py` 到您的计算机。
    
  - 打开终端或命令行窗口。
    
  - 执行以下命令：
    
    ```bash
    python qBittorrentCrossDriveMover.py
    ```
    
  - 脚本将连接到 qBittorrent 客户端，读取 `cross_drive_moves.txt` 文件，并执行种子的跨驱动器移动操作。
    

---

### 脚本名称`TorrentLocationConsolidator.py`

### 说明文档

#### 功能简介

`TorrentLocationConsolidator.py` 是一个自动化脚本，旨在统一同名种子文件在 qBittorrent 客户端中的存储位置。当您有多个相同名称但不同哈希值的种子指向同一个实际文件时，此脚本能确保这些种子的存储路径统一指向同一个目录。

#### 使用前提

- qBittorrent 的 Web UI 功能已启用。
- Python 环境已安装。
- 适用于种子名相同但哈希值可能不同的情况。

#### 功能特点

- 自动识别并分组同名种子。
- 确定每组种子中已存在于特定路径（例如 `hardLink` 目录）的种子路径作为目标路径。
- 更新其他同名种子的存储位置到该目标路径。

#### 如何使用

1. **设置 qBittorrent Web UI 访问信息**：
  
  - 确保您的 qBittorrent 客户端的 Web UI 功能开启。
  - 获取 Web UI 的 URL、用户名和密码。
2. **准备 Python 环境**：
  
  - 确保 Python 已安装在您的系统上。
  - 安装所需的 `requests` 库（如果尚未安装）。
3. **运行脚本**：
  
  - 将脚本 `TorrentLocationConsolidator.py` 保存在您的计算机上。
    
  - 打开终端或命令提示符。
    
  - 运行脚本：
    
    ```bash
    python TorrentLocationConsolidator.py
    ```
    
  - 脚本将自动连接到 qBittorrent，获取所有种子信息，并开始统一同名种子的存储位置。
    

#### 注意事项

- 确保在运行脚本前，qBittorrent 客户端已启动并且 Web UI 功能可访问。
- 在执行脚本期间，避免手动更改 qBittorrent 中的种子信息，以免发生数据不一致。
