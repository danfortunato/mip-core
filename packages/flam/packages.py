#!/usr/bin/env python3
import os
import shutil
import subprocess
from mip_build_helpers import collect_exposed_symbols_recursive

class FlamPackage:
    def __init__(self):
        self.name = "flam"
        self.description = "Fast Linear Algebra in MATLAB (FLAM) - A library for hierarchical matrices and fast direct solvers."
        self.version = "unspecified"
        self.build_number = 1
        self.dependencies = []
        self.homepage = "https://github.com/klho/FLAM"
        self.repository = "https://github.com/klho/FLAM"
        self.matlab_tag = "any"
        self.abi_tag = "none"
        self.platform_tag = "any"

        # The following are filled in during prepare
        self.exposed_symbols = []
    
    def prepare(self, mhl_dir: str):
        # Clone the repository with submodules
        repository_url = self.repository
        clone_dir = "FLAM"
        print(f'Cloning {repository_url} with submodules...')
        subprocess.run(
            ["git", "clone", "--recurse-submodules", repository_url, clone_dir],
            check=True
        )

        # Remove .git directories to reduce size
        print("Removing .git directories...")
        for root, dirs, files in os.walk(clone_dir):
            if ".git" in dirs:
                git_dir = os.path.join(root, ".git")
                shutil.rmtree(git_dir)
                dirs.remove(".git")

        # Move FLAM to flam in the mhl directory (lowercase for consistency)
        flam_dir = os.path.join(mhl_dir, "flam")
        print(f'Moving FLAM to flam...')
        shutil.move(clone_dir, flam_dir)

        # Create setup.m file
        setup_m_path = os.path.join(mhl_dir, "setup.m")
        print("Creating setup.m...")
        with open(setup_m_path, 'w') as f:
            f.write("% Add flam to the MATLAB path and run startup\n")
            f.write("flam_path = fullfile(fileparts(mfilename('fullpath')), 'flam');\n")
            f.write("addpath(flam_path);\n")
            f.write("startup_file = fullfile(flam_path, 'startup.m');\n")
            f.write("if exist(startup_file, 'file')\n")
            f.write("    run(startup_file);\n")
            f.write("end\n")

        # Collect exposed symbols recursively (excluding test and paper directories)
        print("Collecting exposed symbols...")
        self.exposed_symbols = collect_exposed_symbols_recursive(
            flam_dir, 
            "flam", 
            exclude_dirs=['test', 'paper']
        )

if os.environ.get('BUILD_TYPE') == 'standard':
    packages = [FlamPackage()]
else:
    packages = []
