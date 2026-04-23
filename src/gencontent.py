from htmlnode import HTMLNode
from node_maker import markdown_to_html_node
from pathlib import Path
import os
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2::].strip()
    raise Exception("No title found!")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #Reading the markdown file
    md_file = open(from_path)
    md_file_contents = md_file.read()
    md_file.close()
    #Reading the template file
    template_file = open(template_path)
    template_file_contents = template_file.read()
    template_file.close()
    #Convert the markdown into html
    markdown_html = markdown_to_html_node(md_file_contents).to_html()
    #Get the title and replace the stuff in the template
    page_title = extract_title(md_file_contents)
    filled_template = template_file_contents.replace("{{ Title }}", page_title).replace("{{ Content }}", markdown_html)
    filled_template = filled_template.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(filled_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        dir_path = os.path.join(dir_path_content,file)
        dest_path = os.path.join(dest_dir_path, file)
        if not os.path.isfile(dir_path):
            generate_pages_recursive(dir_path, template_path, dest_path, basepath)
        else:
            html_dest_path = Path(dest_path).with_suffix(".html")
            generate_page(dir_path, template_path, html_dest_path, basepath)
            







