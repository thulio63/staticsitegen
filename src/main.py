import os
import shutil
from pathlib import Path
from splitter import markdown_to_html_node
from htmlnode import HTMLNode

def display_contents(search_path:str, verbose=False):
    curr_dir = os.getcwd()
    content_path = f"{curr_dir}/{search_path}"
    if os.path.isfile(content_path):
        print(f"The provided path ({content_path}) points to a file, not a directory")
        return
    contents_to_display = os.listdir(content_path)
    print(f"\nThe following now exist in {search_path}:")
    for path in contents_to_display:
        if os.path.isfile(f"{content_path}/{path}"):
            print(f"file:\t{path}")
        # note- implement child displays to look cooler/be more helpful
        if os.path.isdir(f"{content_path}/{path}"):
            print(f"dir:\t{path}")
    print("")

def clear_and_copy(verbose=False):
    pub_path = "/Users/andrewthul/workspace/github.com/thulio63/staticsitegen/public"
    stat_path = "/Users/andrewthul/workspace/github.com/thulio63/staticsitegen/static"
    public_contents = os.listdir(pub_path)
    static_contents = os.listdir(stat_path)
    
    if len(public_contents) > 0:
        if verbose:
            print("/public has contents")
        for path in public_contents:
            child_path = f"{pub_path}/{path}"
            # checks that path exists
            if not os.path.exists(child_path):
                if verbose:
                    print(f"{child_path}:\tthis path is fake!!!")
                continue
            if os.path.isdir(child_path):
                # deletes if path is dir
                if verbose:
                    print("deleting...")
                shutil.rmtree(child_path)
            else:
                # deletes if path is file
                if verbose:
                    print("deleting...")
                os.remove(child_path)
        # ensures public is now empty
        public_contents = os.listdir(pub_path)
        if len(public_contents) == 0:
            if verbose:
                print("/public is now empty\n")
        else:
            if verbose:
                raise Exception("Something survived the purge")
    else:
        if verbose:
            print("/public is empty")

    if ".DS_Store" in static_contents:
        static_contents.remove(".DS_Store")
    if len(static_contents) > 0:
        if verbose:
            print("/static has contents")
        for path in static_contents:
            # ensures that static path exists
            if not os.path.exists(f"{stat_path}/{path}"):
                if verbose:
                    print(f"{stat_path}/{path}:\t doesn't exist!")
                continue
            if verbose:
                print(f"copying {stat_path}/{path} to public")
            if os.path.isfile(f"{stat_path}/{path}"):
                shutil.copy(f"{stat_path}/{path}", f"{pub_path}/{path}")
                if verbose:
                    print("copied!")
            else:
                shutil.copytree(f"{stat_path}/{path}", f"{pub_path}/{path}")
                if verbose:
                    print("copied!")
    else:
        if verbose:
            print("/static is empty")
    
    display_contents("public", verbose)

def extract_title(markdown: str, is_file=False, verbose=False):
    curr_dir = os.getcwd()
    if os.path.exists(f"{curr_dir}/{markdown}") and is_file:
        if verbose:
            print("submitted str is a path, reading file")
        with open(f"{curr_dir}/{markdown}", 'r') as file:
            md_content = file.read()
    else:
        md_content = markdown
    first_header = md_content.split("#", 1)
    # only finds h1 if it is at top of doc- can revise later
    if len(first_header) == 1 or first_header[1].startswith("#"):
        raise Exception
    header_text = first_header[1].split("\n",1)
    header_val = header_text[0].strip()
    return header_val

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    curr_dir = os.getcwd()
    with open(f"{curr_dir}/{from_path}", 'r') as file:
        md_file = file.read()
    with open(f"{curr_dir}/{template_path}", 'r') as file:
        template_file = file.read()
    site_html_node = markdown_to_html_node(md_file)
    site_html = site_html_node.to_html()
    site_title = extract_title(md_file)
    template_file = template_file.replace("{{ Title }}", site_title)
    template_file = template_file.replace("{{ Content }}", site_html)
    site_file_path = Path(f"{curr_dir}/{dest_path}")
    site_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(site_file_path, 'w') as f:
        f.write(template_file)
    print(f"File {dest_path} and any parent directories have been created.")

def main():
    clear_and_copy()
    #md_file = input("file to extract from:\t")
    #extract_title("content/index.md", True)
    generate_page("content/index.md", "template.html", "public/index.html")
    display_contents("public")
    
    
main()