#/bin/bash

set -ex

export BUILD_TYPE="linux_workstation"

# change to the directory of this script
cd "$(dirname "$0")"

rm -rf ../build

echo "Preparing packages using prepare_packages.py..."
python prepare_packages.py

echo "Running compile_packages.m from MATLAB..."
matlab -batch "compile_packages"

echo "Bundling and uploading packages using bundle_and_upload_packages.py..."
python bundle_and_upload_packages.py

echo "Assemble index using assemble_index.py..."
python assemble_index.py

