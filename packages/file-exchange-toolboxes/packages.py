#!/usr/bin/env python3
import os
import shutil
from mip_build_helpers import download_and_extract_zip, create_load_m_and_unload_m, collect_exposed_symbols_top_level

class GUILayoutToolboxPackage:
    def __init__(self):
        self.name = "gui-layout-toolbox"
        self.description = "Layout manager for MATLAB graphical user interfaces"
        self.version = "2.4.2"
        self.build_number = 1
        self.dependencies = []
        self.homepage = "https://www.mathworks.com/matlabcentral/fileexchange/47982-gui-layout-toolbox"
        self.repository = ""
        self.license = "BSD-2-Clause"
        self.matlab_tag = "any"
        self.abi_tag = "none"
        self.platform_tag = "any"

        # Filled in during prepare
        self.exposed_symbols = []
    
    def prepare(self, mhl_dir: str):
        # Is this permalink to the zip file? Not sure.
        zip_url = "https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/e5af5a78-4a80-11e4-9553-005056977bd0/27611476-c814-450a-b0cb-76c2101f96ed/packages/zip"
        download_and_extract_zip(url=zip_url)

        # copy layout directory to mhl_dir
        layout_source = "layout"
        layout_dest = os.path.join(mhl_dir, "layout")
        shutil.copytree(layout_source, layout_dest)

        # Copy license.txt
        license_source = os.path.join(layout_source, "license.txt")
        license_dest = os.path.join(mhl_dir, "license.txt")
        if not os.path.exists(license_source):
            raise RuntimeError(f"license.txt not found at {license_source}")
        shutil.copyfile(license_source, license_dest)

        create_load_m_and_unload_m(mhl_dir, "layout")

        print("Collecting exposed symbols...")
        self.exposed_symbols = collect_exposed_symbols_top_level(mhl_dir + "/layout")


if os.environ.get('BUILD_TYPE') == 'standard':
    packages = [GUILayoutToolboxPackage()]
else:
    packages = []