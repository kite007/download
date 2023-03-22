import os
import glob

from pathlib import Path

def change_file_extensions(root_dir, old_ext, new_ext):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(old_ext):
                old_path = Path(os.path.join(dirpath, filename))
                new_path = old_path.with_suffix(new_ext)
                old_path.rename(new_path)

if __name__ == "__main__":
    root_directory = "/Users/a07874/work/getfiles/jinstale.tistory.com" # 원하는 디렉토리로 변경하세요.
    old_extension = ""
    new_extension = ".mp3"

    change_file_extensions(root_directory, old_extension, new_extension)


# def change_file_extension(root_directory, old_extension, new_extension):
#     # 하위 디렉토리를 포함하여 모든 파일을 찾습니다.
#     search_pattern = f"{root_directory}/**/*{old_extension}"
#     files = glob.glob(search_pattern, recursive=True)

#     # 각 파일의 확장자를 변경합니다.
#     for file in files:
#         file_base, _ = os.path.splitext(file)
#         new_file = f"{file_base}{new_extension}"
#         os.rename(file, new_file)
#         print(f"{file} -> {new_file}")

# if __name__ == "__main__":
#     root_directory = "/Users/a07874/work/getfiles/jinstale.tistory.com" # 원하는 디렉토리로 변경하세요.
#     old_extension = ""
#     new_extension = ".mp3"
#     change_file_extension(root_directory, old_extension, new_extension)
