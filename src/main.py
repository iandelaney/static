import os
import sys

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

    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            copy_file(src_path, dst_path)
        else:
            os.makedirs(dst_path, exist_ok=True)
            copy_directory(src_path, dst_path)


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", content_html)

    # Fix asset paths for basepath
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w") as dest_file:
        dest_file.write(page_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def main():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    static_path = os.path.join(base_path, "static")
    docs_path = os.path.join(base_path, "docs")  # changed from public
    content_path = os.path.join(base_path, "content")
    template_path = os.path.join(base_path, "template.html")

    # CLI basepath (default "/")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists(docs_path):
        clear_directory(docs_path)
    else:
        os.mkdir(docs_path)

    copy_directory(static_path, docs_path)
    generate_pages_recursive(content_path, template_path, docs_path, basepath)

if __name__ == "__main__":
    main()