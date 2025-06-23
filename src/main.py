from pathlib import Path
import os
import shutil

def main():
    pub_path = "/Users/andrewthul/workspace/github.com/thulio63/staticsitegen/public"
    stat_path = "/Users/andrewthul/workspace/github.com/thulio63/staticsitegen/static"
    public_contents = os.listdir(pub_path)
    static_contents = os.listdir(stat_path)
    
    if len(public_contents) > 0:
        print("/public has contents")
        for path in public_contents:
            child_path = f"{pub_path}/{path}"
            # checks that path exists
            if not os.path.exists(child_path):
                print(f"{child_path}:\tthis path is fake!!!")
                continue
            if os.path.isdir(child_path):
                # deletes if path is dir
                print("deleting...")
                shutil.rmtree(child_path)
            else:
                # deletes if path is file
                print("deleting...")
                os.remove(child_path)
        # ensures public is now empty
        public_contents = os.listdir(pub_path)
        if len(public_contents) == 0:
            print("/public is now empty")
        else:
            raise Exception("Something survived the purge")
    else:
        print("/public is empty")

    if ".DS_Store" in static_contents:
        static_contents.remove(".DS_Store")
    if len(static_contents) > 0:
        print("/static has contents")
        for path in static_contents:
            # ensures that static path exists
            if not os.path.exists(f"{stat_path}/{path}"):
                print(f"{stat_path}/{path}:\t doesn't exist!")
                continue
            print(f"copying {stat_path}/{path} to public")
            if os.path.isfile(f"{stat_path}/{path}"):
                shutil.copy(f"{stat_path}/{path}", f"{pub_path}/{path}")
                print("copied!")
            else:
                shutil.copytree(f"{stat_path}/{path}", f"{pub_path}/{path}")
                print("copied!")
    else:
        print("/static is empty")
    
    public_contents = os.listdir(pub_path)
    print("The following now exist in /public:")
    for path in public_contents:
        if os.path.isfile(f"{pub_path}/{path}"):
            print(f"file:\t{path}")
        if os.path.isdir(f"{pub_path}/{path}"):
            print(f"dir:\t{path}")
    
main()