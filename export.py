import os
import xml.etree.ElementTree as ET
import zipfile
import shutil
import glob

def game_version(game_dir):
    xml = ET.parse(os.path.join(game_dir, "version.xml"))
    version = xml.find("version").text.strip()
    version = version.replace("v.", "")
    version = version.split(" ")[0]
    return version

def extract_flash_libraries(game_dir, output_dir):
    print("Extracting flash libraries from the game")

    archive_path = os.path.join(game_dir, "res", "packages")
    archives = ["gui-part1.pkg", "gui-part2.pkg"]

    try:
        shutil.rmtree(output_dir)
    except:
        pass

    for archive in archives:
        with zipfile.ZipFile(os.path.join(archive_path, archive), 'r') as zip_ref:
            for path in zip_ref.filelist:
                if path.is_dir():
                    continue
                if not path.filename.endswith(".swc"):
                    continue
                zip_ref.extract(path.filename, output_dir)

    source_path = os.path.join(output_dir, "gui", "flash", "swc")
    for file in os.listdir(source_path):
        shutil.move(os.path.join(source_path, file), output_dir)
    shutil.rmtree(os.path.join(output_dir, "gui"))

def build_python_scripts(input_dir, output_dir):
    print("Building python files")

    try:
        shutil.rmtree(output_dir)
    except:
        pass

    shutil.copytree(input_dir, output_dir)
    os.system("conda run -n py2 python -m compileall " + output_dir)
    for py in glob.iglob(os.path.join(output_dir, '*.py')):
        os.remove(py)

def build_flash_project(input_dir, flash_sdk_dir):
    print("Build flash project")

    os.system("asconfigc --sdk " + flash_sdk_dir + " -p " + input_dir)

def export_resources_to_game(game_version, game_dir, resources_dir, output_path):
    destination = os.path.join(game_dir, "res_mods", game_version, output_path)

    try:
        shutil.rmtree(destination)
    except:
        pass

    shutil.copytree(resources_dir, destination)

game_dir = "C:\\Games\\World_of_Tanks_EU"
flash_sdk_dir = "C:\\Users\\gabriel\\Documents\\wot\\apache-flex"

version = game_version(game_dir)
print("Detected game version: " + version)

extract_flash_libraries(game_dir, os.path.join("dist", "flash"))
build_python_scripts("scripts", os.path.join("dist", "output", "scripts"))
build_flash_project("ui", flash_sdk_dir)

export_resources_to_game(version, game_dir, os.path.join("dist", "output", "scripts"), os.path.join("scripts", "client", "gui", "mods"))
export_resources_to_game(version, game_dir, os.path.join("dist", "output", "flash"), os.path.join("gui", "flash", "test"))
