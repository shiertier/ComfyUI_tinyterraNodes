from .ttNpy.tinyterraNodes import TTN_VERSIONS
from .ttNpy import ttNserver  # Do Not Remove
import configparser
import folder_paths
import subprocess
import shutil
import os

# ------- CONFIG -------- #
cwd_path = os.path.dirname(os.path.realpath(__file__))
js_path = os.path.join(cwd_path, "js")
comfy_path = folder_paths.base_path

# 定义默认配置
default_config = {
    "Versions": {
        "tinyterranodes": "2.0.3",
        "pipeloader": "1.1.2",
        "pipeksampler": "1.0.5",
        "pipeksampleradvanced": "1.0.5",
        "pipeloadersdxl": "1.1.2",
        "pipeksamplersdxl": "1.0.2",
        "pipein": "1.1.0",
        "pipeout": "1.1.0",
        "pipeedit": "1.1.1",
        "pipe2basic": "1.1.0",
        "pipe2detailer": "1.2.0",
        "xyplot": "1.2.0",
        "pipeencodeconcat": "1.0.2",
        "multilorastack": "1.1.1",
        "multimodelmerge": "1.1.0",
        "text": "1.0.0",
        "textdebug": "1.0.",
        "concat": "1.0.0",
        "text3box_3wayconcat": "1.0.0",
        "text7box_concat": "1.0.0",
        "imageoutput": "1.2.0",
        "imagerembg": "1.0.0",
        "hiresfixscale": "1.1.0",
        "int": "1.0.0",
        "float": "1.0.0",
        "seed": "1.0.0",
        "pipeloader_v2": "2.1.0",
        "tinyksampler": "2.3.1",
        "tinyloader": "1.1.0",
        "tinyconditioning": "1.0.0",
        "pipeksampler_v2": "2.3.1",
        "pipeksampleradvanced_v2": "2.3.0",
        "pipeloadersdxl_v2": "2.1.0",
        "pipeksamplersdxl_v2": "2.3.1",
        "advanced xyplot": "1.2.0",
        "advplot range": "1.1.0",
        "advplot string": "1.0.0",
        "advplot combo": "1.0.0",
        "debuginput": "1.0.0",
        "textcycleline": "1.0.0",
        "advplot images": "1.0.0",
        "textoutput": "1.0.1",
    },
    "Option Values": {
        "auto_update": ('true', 'false'),
        "enable_embed_autocomplete": ('true', 'false'),
        "enable_interface": ('true', 'false'),
        "enable_fullscreen": ('true', 'false'),
        "enable_dynamic_widgets": ('true', 'false'),
        "enable_dev_nodes": ('true', 'false'),
    },
    "ttNodes": {
        "auto_update": False,
        "enable_interface": True,
        "enable_fullscreen": True,
        "enable_embed_autocomplete": True,
        "enable_dynamic_widgets": True,
        "enable_dev_nodes": False,
    }
}

def get_default_config():
    """返回默认配置字典。"""
    return default_config

def config_value_validator(section, option, default):
    value = str(config_data[section][option]).lower()
    if value not in optionValues[option]:
        print(f'\033[92m[{section} Config]\033[91m {option} - \'{value}\' not in {optionValues[option]}, reverting to default.\033[0m')
        return default
    else:
        return value

# 使用默认配置
config_data = get_default_config()

# Autoupdate if True
if config_value_validator("ttNodes", "auto_update", 'false') == 'true':
    try:
        with subprocess.Popen(["git", "pull"], cwd=cwd_path, stdout=subprocess.PIPE) as p:
            p.wait()
            result = p.communicate()[0].decode()
            if result != "Already up to date.\n":
                print("\033[92m[t ttNodes Updated t]\033[0m")
    except:
        pass

# --------- WEB ---------- #
# Remove old web JS folder
web_extension_path = os.path.join(comfy_path, "web", "extensions", "tinyterraNodes")

if os.path.exists(web_extension_path):
    try:
        shutil.rmtree(web_extension_path)
    except:
        print("\033[92m[ttNodes] \033[0;31mFailed to remove old web extension.\033[0m")

js_files = {
    "interface": "enable_interface",
    "fullscreen": "enable_fullscreen",
    "embed_autocomplete": "enable_embed_autocomplete",
    "dynamic_widgets": "enable_dynamic_widgets",
}
for js_file, config_key in js_files.items():
    file_path = os.path.join(js_path, f"ttN{js_file}.js")
    if config_value_validator("ttNodes", config_key, 'true') == 'false' and os.path.isfile(file_path):
        os.rename(file_path, f"{file_path}.disable")
    elif config_value_validator("ttNodes", config_key, 'true') == 'true' and os.path.isfile(f"{file_path}.disable"):
        os.rename(f"{file_path}.disable", file_path)

# Enable Dev Nodes if True
if config_value_validator("ttNodes", "enable_dev_nodes", 'true') == 'true':
    from .ttNdev import NODE_CLASS_MAPPINGS as ttNdev_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ttNdev_DISPLAY_NAME_MAPPINGS
else:
    ttNdev_CLASS_MAPPINGS = {}
    ttNdev_DISPLAY_NAME_MAPPINGS = {}

# ------- MAPPING ------- #
from .ttNpy.tinyterraNodes import NODE_CLASS_MAPPINGS as TTN_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as TTN_DISPLAY_NAME_MAPPINGS
from .ttNpy.ttNlegacyNodes import NODE_CLASS_MAPPINGS as LEGACY_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LEGACY_DISPLAY_NAME_MAPPINGS

NODE_CLASS_MAPPINGS = {**TTN_CLASS_MAPPINGS, **LEGACY_CLASS_MAPPINGS, **ttNdev_CLASS_MAPPINGS}
NODE_DISPLAY_NAME_MAPPINGS = {**TTN_DISPLAY_NAME_MAPPINGS, **LEGACY_DISPLAY_NAME_MAPPINGS, **ttNdev_DISPLAY_NAME_MAPPINGS}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
