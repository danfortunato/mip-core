#!/usr/bin/env python3
import os
import shutil
from mip_build_helpers import download_and_extract_zip, create_load_and_unload_scripts, collect_exposed_symbols


class GUILayoutToolboxPackage:
    def __init__(self):
        self.name = "gui-layout-toolbox"
        self.description = "Layout manager for MATLAB graphical user interfaces"
        self.version = "2.4.2"
        self.build_number = 11
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
        download_and_extract_zip(url=zip_url, extract_dir=mhl_dir + "/toolbox")

        create_load_and_unload_scripts(mhl_dir, dirs_to_add_to_path=["toolbox/layout"])

        print("Collecting exposed symbols...")
        self.exposed_symbols = collect_exposed_symbols(mhl_dir + "/toolbox/layout")


class HungarianAlgorithmForLinearAssignmentProblemsPackage:
    def __init__(self):
        self.name = "hungarian-algorithm-for-linear-assignment-problems"
        self.description = "Hungarian Algorithm for Linear Assignment Problems (V2.3)"
        self.version = "1.4.0.0"
        self.build_number = 11
        self.dependencies = []
        self.homepage = "https://www.mathworks.com/matlabcentral/fileexchange/20652-hungarian-algorithm-for-linear-assignment-problems-v2-3"
        self.repository = ""
        self.license = "BSD-2-Clause"
        self.matlab_tag = "any"
        self.abi_tag = "none"
        self.platform_tag = "any"
        self.usage_examples = [
            """mip load hungarian-algorithm-for-linear-assignment-problems
costMat = [4 2 8; 2 4 6; 8 6 4];
[assignment, cost] = munkres(costMat);
disp(assignment);"""
        ]

        # Filled in during prepare
        self.exposed_symbols = []
    
    def prepare(self, mhl_dir: str):
        zip_url = "https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/20652/versions/5/download/zip"
        download_and_extract_zip(url=zip_url, extract_dir=mhl_dir + "/hungarian_algorithm_for_linear_assignment_problems")

        create_load_and_unload_scripts(mhl_dir, dirs_to_add_to_path=["hungarian_algorithm_for_linear_assignment_problems/munkres"])

        print("Collecting exposed symbols...")
        self.exposed_symbols = collect_exposed_symbols(mhl_dir + "/hungarian_algorithm_for_linear_assignment_problems/munkres")


# https://www.mathworks.com/matlabcentral/fileexchange/53593-hatchfill2
class Hatchfill2Package:
    def __init__(self):
        self.name = "hatchfill2"
        self.description = "Fills an area with hatching or speckling"
        self.version = "3.0.0.0"
        self.build_number = 11
        self.dependencies = []
        self.homepage = "https://www.mathworks.com/matlabcentral/fileexchange/53593-hatchfill2"
        self.repository = ""
        self.license = "BSD-2-Clause"
        self.matlab_tag = "any"
        self.abi_tag = "none"
        self.platform_tag = "any"

        # Filled in during prepare
        self.exposed_symbols = []
    
    def prepare(self, mhl_dir: str):
        zip_url = "https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/53593/versions/10/download/zip"
        download_and_extract_zip(url=zip_url, extract_dir=mhl_dir + "/hatchfill2")

        create_load_and_unload_scripts(mhl_dir, dirs_to_add_to_path=["hatchfill2"])

        print("Collecting exposed symbols...")
        self.exposed_symbols = collect_exposed_symbols(mhl_dir + "/hatchfill2")


if os.environ.get('BUILD_TYPE') == 'standard':
    packages = [
        GUILayoutToolboxPackage(),
        HungarianAlgorithmForLinearAssignmentProblemsPackage(),
        Hatchfill2Package()
    ]
else:
    packages = []