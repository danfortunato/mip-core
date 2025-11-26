import os

def generate_recursive_subdir_list(mhl_dir, *, base_dir: str, exclude_dirs=None) -> list[str]:
    """
    Generate a list of all subdirectories under base_dir (relative to mhl_dir).
    
    Args:
        mhl_dir: The MHL directory
        base_dir: The base directory (relative to mhl_dir) to search for subdirectories
        exclude_dirs: List of directory names to exclude from the search

    Returns:
        List of subdirectory paths relative to mhl_dir
    """
    if exclude_dirs is None:
        exclude_dirs = []
    subdirs = []
    def process_dir(current_dir, relative_path):
        for entry in os.listdir(current_dir):
            entry_path = os.path.join(current_dir, entry)
            if os.path.isdir(entry_path):
                if entry in exclude_dirs:
                    continue
                rel_subdir_path = os.path.join(relative_path, entry)
                subdirs.append(rel_subdir_path)
                process_dir(entry_path, rel_subdir_path)

    base_dir_full_path = os.path.join(mhl_dir, base_dir)
    process_dir(base_dir_full_path, base_dir)
    return subdirs

def create_load_and_unload_scripts(mhl_dir, *, dirs_to_add_to_path: list[str]):
    """
    Create load_package.m and unload_package.m files that add/remove specified directories to/from the MATLAB path.
    
    Args:
        mhl_dir: The MHL directory where load_package.m and unload_package.m will be created
        dirs_to_add_to_path: List of directories (relative to mhl_dir) to add to the MATLAB path
    """
    load_m_path = os.path.join(mhl_dir, "load_package.m")
    unload_m_path = os.path.join(mhl_dir, "unload_package.m")
    print("Creating load_package.m and unload_package.m...")

    with open(load_m_path, 'w') as f:
        for dir_rel_path in dirs_to_add_to_path:
            f.write(f"addpath(fullfile(fileparts(mfilename('fullpath')), '{dir_rel_path}'));\n")

    # Create unload_package.m file
    with open(unload_m_path, 'w') as f:
        for dir_rel_path in reversed(dirs_to_add_to_path):
            f.write(f"rmpath(fullfile(fileparts(mfilename('fullpath')), '{dir_rel_path}'));\n")
