import os
import shutil
import sys
from pathlib import Path
from splitter import markdown_to_html_node
from htmlnode import HTMLNode

def display_contents(search_path:str):
    """Displays all contents currently in directory."""
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
    
def dir_crawler(path_to_search: str, curr_dir=os.getcwd()):
    """Returns list of all files"""
    search_path = f"{curr_dir}/{path_to_search}"
    list_of_contents = []
    if os.path.isfile(search_path):
        # this should return the file probably for recursive calls
        return path_to_search
    elif os.path.isdir(search_path):
        path_contents = os.listdir(search_path)
        path_contents.reverse()
        for con in path_contents:
            list_of_contents.append(dir_crawler(con, search_path))
        
        return [path_to_search, list_of_contents]
    else:
        raise Exception("Not a dir or a file what the fuck is this")

def dir_crawler_painter(list_of_contents):
    """Takes a file structure from dir_crawler and prints it cleanly."""
    
    pass

def clear_and_copy(private_path, public_path, verbose=False):
    """Empties public dir and populates it with data in static dir."""
    proj_home = "/Users/andrewthul/workspace/github.com/thulio63/staticsitegen" 
    pub_path = f"{proj_home}/{public_path}"
    priv_path = f"{proj_home}/{private_path}"
    public_contents = os.listdir(pub_path)
    static_contents = os.listdir(priv_path)
    
    if len(public_contents) > 0:
        if verbose:
            print(f"/{public_path} has contents")
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
                print(f"/{public_path} is now empty\n")
        else:
            if verbose:
                raise Exception("Something survived the purge")
    else:
        if verbose:
            print(f"/{public_path} is empty")

    if ".DS_Store" in static_contents:
        static_contents.remove(".DS_Store")
    if len(static_contents) > 0:
        if verbose:
            print(f"/{private_path} has contents")
        for path in static_contents:
            # ensures that static path exists
            if not os.path.exists(f"{priv_path}/{path}"):
                if verbose:
                    print(f"{priv_path}/{path}:\t doesn't exist!")
                continue
            if verbose:
                print(f"copying {priv_path}/{path} to public")
            if os.path.isfile(f"{priv_path}/{path}"):
                shutil.copy(f"{priv_path}/{path}", f"{pub_path}/{path}")
                if verbose:
                    print("copied!")
            else:
                shutil.copytree(f"{priv_path}/{path}", f"{pub_path}/{path}")
                if verbose:
                    print("copied!")
    else:
        if verbose:
            print(f"/{private_path} is empty")
    
    if verbose:
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

def generate_page(from_path, template_path, dest_path, basepath, verbose=False):
    if verbose:
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
    if verbose:
        print("Title replaced")
    template_file = template_file.replace("{{ Content }}", site_html)
    if verbose:
        print("Content replaced")
    template_file = template_file.replace('href="/', f'href="{basepath}')
    if verbose:
        print("href= replaced")
    template_file = template_file.replace('src="/', f'src="{basepath}')
    if verbose:
        print("src= replaced")
    site_file_path = Path(f"{curr_dir}/{dest_path}")
    site_file_path.parent.mkdir(parents=True, exist_ok=True)
    if verbose:
        print("Parent directories created")
    with open(site_file_path, 'w') as f:
        f.write(template_file)
    print(f"\nFile {dest_path} and any parent directories have been created.\n")
    
def generate_all_md_pages(from_dir_path, template_path, dest_dir_path, basepath):
    """Finds all .md files in a dir and generates .html files in a target dir."""
    curr_dir = os.getcwd()
    from_path = f"{curr_dir}/{from_dir_path}"
    # calls itself on dirs
    if os.path.isdir(from_path):
        from_path_contents = os.listdir(from_path)
        for path in from_path_contents:
            generate_all_md_pages(f"{from_dir_path}/{path}",template_path, f"{dest_dir_path}/{path}", basepath)
    # generates page on .md files
    elif os.path.isfile(from_path) and from_dir_path[-3:] == ".md":
        dest_dir_path = dest_dir_path[:-3]
        dest_dir_path += ".html"
        generate_page(from_dir_path, template_path, dest_dir_path, basepath)
    # skips non .md files
    elif os.path.isfile(from_path):
        pass
    # shit
    else:
        raise Exception("Error: i got lost oops")

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        print(sys.argv[1])
        basepath = sys.argv[1]
    clear_and_copy("static", "docs")
    #display_contents("public")
    generate_all_md_pages("./content","template.html","./docs", basepath)
    
main()