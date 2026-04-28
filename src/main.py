import os


def copy_file(src_path, dst_path):
    with open(src_path, "rb") as src_file:
        contents = src_file.read()

    with open(dst_path, "wb") as dst_file:
        dst_file.write(contents)


def clear_directory(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            clear_directory(item_path)
            os.rmdir(item_path)


def copy_directory(src, dst):
    if not os.path.exists(src):
        raise Exception(f"Source directory does not exist: {src}")

    if os.path.exists(dst):
        clear_directory(dst)
    else:
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            copy_file(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            copy_directory(src_path, dst_path)


def main():
    copy_directory("../static", "../public")


if __name__ == "__main__":
    main()