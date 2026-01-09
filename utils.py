import shutil

def clean_dir(directory):
    shutil.rmtree(directory, ignore_errors=True)