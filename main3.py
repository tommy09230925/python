import os
from PIL import Image
from tkinter import filedialog, Tk
import time

# 命名規則選項及對應中文翻譯
rename_options = {
    1: ("#", "檔案編號"),
    2: ("File name without extension", "不帶副檔名的檔案名稱"),
    3: ("File name with extension", "帶副檔名的檔案名稱"),
    4: ("Image width", "圖片寬度"),
    5: ("Image height", "圖片高度"),
    6: ("Modification date", "修改日期"),
    7: ("Current date", "當前日期"),
    8: ("Size (auto)", "檔案大小（自動）"),
    9: ("Size (kilo-octets)", "檔案大小（千字節）"),
    10: ("Size (octets)", "檔案大小（字節）")
}

# 讓使用者選擇命名規則
def choose_naming_rule():
    print("請選擇命名規則（可以選擇多項）:")
    for key, value in rename_options.items():
        print(f"{key}. {value[1]}")
    
    choices = input("輸入選擇的數字（用逗號分隔，如 1,3,5）: ").split(",")
    return [int(choice.strip()) for choice in choices if choice.strip().isdigit() and int(choice.strip()) in rename_options]

# 讓使用者選擇壓縮比例 (5% 到 95%)
def choose_compression_ratio():
    while True:
        try:
            compression_ratio = int(input("請輸入壓縮比例 (5% ~ 95%)(只要輸入數字即可): "))
            if 5 <= compression_ratio <= 95:
                return compression_ratio / 100
            else:
                print("請輸入一個介於 5% 和 95% 之間的數字。(只要輸入數字即可)")
        except ValueError:
            print("請輸入有效的數字。")

# 讓使用者選擇多張圖片
def select_images():
    root = Tk()
    root.withdraw()  # 隱藏 Tkinter 主視窗
    file_paths = filedialog.askopenfilenames(
        title="選擇圖片",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    return file_paths

# 創建唯一的資料夾，若資料夾已存在，則加上編號
def create_unique_folder(base_folder_name):
    folder_name = base_folder_name
    counter = 1
    while os.path.exists(folder_name):
        folder_name = f"{base_folder_name}({counter})"
        counter += 1
    os.makedirs(folder_name)
    return folder_name

# 壓縮圖片的函數
def compress_images(file_paths, ratio):
    output_folder = create_unique_folder("compressed_images")
    
    full_output_path = os.path.abspath(output_folder)
    print(f"壓縮後的圖片將保存至: {full_output_path}")
    
    compressed_files = []
    for file_path in file_paths:
        with Image.open(file_path) as img:
            width, height = img.size
            new_size = (int(width * ratio), int(height * ratio))
            
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(output_folder, file_name)  # 檔名維持不變
            img_resized.save(new_file_path, quality=95)
            compressed_files.append(new_file_path)
            print(f"已壓縮並保存圖片: {new_file_path}")
    
    return compressed_files

# 根據選擇的命名規則重新命名圖片
def rename_images(file_paths, rules, output_folder):
    output_folder = create_unique_folder(output_folder)

    full_output_path = os.path.abspath(output_folder)
    print(f"重新命名後的圖片將保存至: {full_output_path}")
    
    for index, file_path in enumerate(file_paths, start=1):
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        new_name_parts = []
        
        for rule in rules:
            if rule == 1:  # 檔案編號
                new_name_parts.append(str(index))
            elif rule == 2:  # 不帶副檔名的檔案名稱
                new_name_parts.append(file_name)
            elif rule == 3:  # 帶副檔名的檔案名稱
                new_name_parts.append(f"{file_name}{file_extension}")
            elif rule == 4 or rule == 5:  # 圖片寬度和高度
                with Image.open(file_path) as img:
                    width, height = img.size
                    if rule == 4:
                        new_name_parts.append(str(width))  # 圖片寬度
                    else:
                        new_name_parts.append(str(height))  # 圖片高度
            elif rule == 6:  # 修改日期
                mod_time = time.strftime('%Y%m%d', time.gmtime(os.path.getmtime(file_path)))
                new_name_parts.append(mod_time)
            elif rule == 7:  # 當前日期
                current_date = time.strftime('%Y%m%d', time.localtime())
                new_name_parts.append(current_date)
            elif rule == 8:  # 檔案大小（自動）
                new_name_parts.append(str(os.path.getsize(file_path)))
            elif rule == 9:  # 檔案大小（千字節）
                new_name_parts.append(f"{os.path.getsize(file_path) // 1024}KB")
            elif rule == 10:  # 檔案大小（字節）
                new_name_parts.append(f"{os.path.getsize(file_path)}B")
        
        new_file_name = "_".join(new_name_parts) + file_extension
        new_file_path = os.path.join(output_folder, new_file_name)
        
        with Image.open(file_path) as img:
            img.save(new_file_path)
        
        print(f"已重新命名並保存圖片: {new_file_path}")

def main():
    print("請選擇要執行的操作：")
    print("1. 壓縮圖片")
    print("2. 重新命名圖片")
    print("3. 兩者皆執行")
    choice = input("輸入選擇的數字 (1, 2, 3): ").strip()
    
    if choice not in ['1', '2', '3']:
        print("無效的選擇，請重新運行程式。")
        return
    
    image_files = select_images()
    
    if not image_files:
        print("未選擇任何圖片。")
        return
    
    compressed_files = image_files
    
    # 如果選擇壓縮
    if choice in ['1', '3']:
        compression_ratio = choose_compression_ratio()
        compressed_files = compress_images(image_files, compression_ratio)
    
    # 如果選擇重新命名
    if choice in ['2', '3']:
        rules = choose_naming_rule()
        output_folder = create_unique_folder("final_images") if choice == '3' else create_unique_folder("renamed_images")
        rename_images(compressed_files, rules, output_folder)
    
    print("操作完成。")

if __name__ == "__main__":
    main()
