import os
import argparse
from opencc import OpenCC
from send2trash import send2trash


def convert_simp_to_trad_tw(file_path):
    cc = OpenCC('s2twp')

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    converted_content = cc.convert(content)

    directory, filename = os.path.split(file_path)
    new_filename = cc.convert(filename)
    new_file_path = os.path.join(directory, new_filename)

    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(converted_content)

    if new_filename != filename:
        send2trash(file_path)
        print(f"已轉換並更新檔案：{new_file_path}")
    else:
        print(f"檔名未變更，保留原檔案：{file_path}")


def convert_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                convert_simp_to_trad_tw(file_path)


def main():
    parser = argparse.ArgumentParser(description="Convert Simplified Chinese to Traditional Chinese (Taiwan).")
    parser.add_argument('path', help="Path to the file or directory to convert.")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        convert_folder(args.path)
        print("所有資料夾內的檔案轉換完畢！")
    elif os.path.isfile(args.path) and args.path.endswith('.md'):
        convert_simp_to_trad_tw(args.path)
        print("檔案轉換完畢！")
    else:
        print("提供的路徑不是 Markdown 檔案或指向有效資料夾。")


if __name__ == '__main__':
    main()