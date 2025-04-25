import os
import sys
from pathlib import Path
import re


def get_extension_path():
    """根據作業系統取得擴充套件路徑"""
    if sys.platform == "win32":
        base_path = os.path.expandvars("%USERPROFILE%\\.vscode\\extensions")
    else:
        base_path = os.path.expanduser("~/.vscode/extensions")
    return Path(base_path)


def find_all_copilot_folders(base_path):
    """尋找所有 Copilot 相關的擴充資料夾"""
    try:
        copilot_pattern = re.compile(r"github\.copilot[.-].*")
        copilot_folders = [
            folder
            for folder in base_path.iterdir()
            if copilot_pattern.match(folder.name)
        ]

        if copilot_folders:
            print(f"找到 {len(copilot_folders)} 個 Copilot 相關資料夾:")
            for folder in copilot_folders:
                print(f"- {folder.name}")
            return copilot_folders

        print("未找到任何 Copilot 相關擴充套件")
        return None

    except Exception as e:
        print(f"搜尋 Copilot 資料夾時發生錯誤: {e}")
        return None


def modify_extension_file(folder_path):
    """讀取並修改 extension.js 檔案"""
    try:
        file_path = folder_path / "dist" / "extension.js"

        if not file_path.exists():
            print(f"找不到檔案: {file_path}")
            return False

        # 讀取並修改檔案內容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace(
            "x-onbehalf-extension-id", "xdisable-onbehalf-extension-id"
        )

        if content == new_content:
            print(f"在 {folder_path.name} 中沒有找到需要替換的文字")
            return False

        # 直接寫入修改後的內容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"成功修改 {folder_path.name} 的檔案內容")
        return True

    except Exception as e:
        print(f"修改檔案時發生錯誤: {e}")
        return False


def main():
    # 取得擴充套件路徑
    extension_path = get_extension_path()
    if not extension_path.exists():
        print(f"找不到擴充套件資料夾: {extension_path}")
        return

    # 尋找所有 Copilot 資料夾
    copilot_folders = find_all_copilot_folders(extension_path)
    if not copilot_folders:
        return

    # 修改所有找到的 Copilot 擴充套件
    modified = False
    for folder in copilot_folders:
        if modify_extension_file(folder):
            modified = True

    if modified:
        print("\n修改完成！請重新啟動 VS Code 使變更生效")
    else:
        print("\n沒有檔案被修改")


if __name__ == "__main__":
    main()
