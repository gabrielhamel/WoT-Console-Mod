#!/bin/bash

wot_path="/Users/gabriel/Documents/Wargaming.net Games/World_of_Tanks_EU"
flash_sdk_path="/Users/gabriel/Development/wot/tools/flash-sdk/sources"
conda_env_python_2_name=py2

version=$(cat "${wot_path}/version.xml" | grep "<version>" | cut -d'.' -f 2- | cut -d ' ' -f 1)
output=dist/output
echo "Detected version: ${version}"

# Extract flash libraries
rm -rf ${output}/../flash
unzip -j "${wot_path}/res/packages/gui-part1.pkg" gui/flash/swc/*.swc -d ${output}/../flash
unzip -j "${wot_path}/res/packages/gui-part2.pkg" gui/flash/swc/*.swc -d ${output}/../flash

mkdir -p ${output}

# Build python scripts
python_output="${output}/scripts"
rm -rf ${python_output}
cp -r scripts ${python_output}
conda run -n ${conda_env_python_2_name} python -m compileall ${python_output}
find ${python_output} -name "*.py" -delete

# Move the python files into the mod folder
cp ${python_output}/* "${wot_path}/res_mods/${version}/scripts/client/gui/mods"

# Build flash resources
flash_output="${output}/flash"
rm -rf ${flash_output}
asconfigc --sdk ${flash_sdk_path} -p ui

# Move the flash files into the mod folder
cp ${flash_output}/* "${wot_path}/res_mods/${version}/gui/flash/test"
