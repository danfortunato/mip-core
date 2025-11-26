#!/usr/bin/env python3
"""
Helper functions for building MATLAB package (.mhl) files.
"""
import os
import json
import subprocess
import shutil
import requests
import zipfile


def clone_repository_and_remove_git(repository_url, clone_dir):
    """
    Clone a git repository and automatically remove all .git directories.
    
    This is useful for package preparation where we want the source code
    but don't need the git history, reducing package size.
    
    Args:
        repository_url: The URL of the git repository to clone
        clone_dir: The directory name to clone into
    """
    print(f'Cloning {repository_url}...')
    subprocess.run(
        ["git", "clone", repository_url, clone_dir],
        check=True
    )
    
    # Remove .git directories to reduce size
    print("Removing .git directories...")
    for root, dirs, files in os.walk(clone_dir):
        if ".git" in dirs:
            git_dir = os.path.join(root, ".git")
            shutil.rmtree(git_dir)
            dirs.remove(".git")


def download_and_extract_zip(url, extract_dir="."):
    """
    Download a ZIP file from a URL and extract it.
    
    Args:
        url: The URL to download the ZIP file from
        extract_dir: The directory to extract the contents to (default: ".")
    
    Returns:
        None
    """
    download_file = "temp_download.zip"
    
    print(f'Downloading {url}...')
    response = requests.get(url)
    response.raise_for_status()
    
    with open(download_file, 'wb') as f:
        f.write(response.content)
    print('Download complete.')
    
    print("Extracting downloaded zip...")
    with zipfile.ZipFile(download_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Clean up the downloaded file
    os.remove(download_file)

def _extract_symbol_name(item_name):
    """Extract the symbol name from a file or directory name.
    
    Examples:
        'filename.m' → 'filename'
        '+packagename' → 'packagename'
        '@classname' → 'classname'
    
    Args:
        item_name: The file or directory name
    
    Returns:
        The extracted symbol name
    """
    # Remove .m extension if present
    if item_name.endswith('.m'):
        item_name = item_name[:-2]
    
    # Remove + or @ prefix if present
    if item_name.startswith('+') or item_name.startswith('@'):
        item_name = item_name[1:]
    
    return item_name


def collect_exposed_symbols(base_dir: str, *, extensions=None):
    """
    Collect exposed symbols from a directory, including files with specified extensions.
    
    This is useful for packages that expose MEX files (.c, .cpp) in addition to .m files.
    
    Args:
        base_dir: The directory to scan
        extensions: List of file extensions to include (e.g., ['.m', '.c', '.cpp'])
                   If None, defaults to ['.m']
    
    Returns:
        List of symbol names
    """
    if extensions is None:
        extensions = ['.m']
    
    symbols = []

    if not os.path.exists(base_dir):
        return symbols

    items = os.listdir(base_dir)

    for item in sorted(items):
        item_path = os.path.join(base_dir, item)

        if os.path.isfile(item_path):
            # Check if file has one of the specified extensions
            for ext in extensions:
                if item.endswith(ext):
                    # Remove the extension
                    symbols.append(item[:-len(ext)])
                    break
        elif os.path.isdir(item_path) and (item.startswith('+') or item.startswith('@')):
            # Add package or class directory (without + or @)
            symbols.append(item[1:])
    
    return symbols

