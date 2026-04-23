import os, shutil

def copy_dir(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    items = os.listdir(source_path)
    for item in items:
        new_source = os.path.join(source_path, item)
        new_destination = os.path.join(destination_path, item)
        if os.path.isfile(new_source):
            print(f"copying {new_source} to {new_destination}")
            shutil.copy(new_source, new_destination)
        else:
            copy_dir(new_source, new_destination)


