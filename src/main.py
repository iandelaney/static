import os

from markdown_to_html import markdown_to_html_node


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


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as dest_file:
        dest_file.write(page_html)


def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path = os.path.join(base_path, "static")
    public_path = os.path.join(base_path, "public")
    content_path = os.path.join(base_path, "content", "index.md")
    template_path = os.path.join(base_path, "template.html")
    output_path = os.path.join(public_path, "index.html")

    copy_directory(static_path, public_path)
    generate_page(content_path, template_path, output_path)


if __name__ == "__main__":
    main()