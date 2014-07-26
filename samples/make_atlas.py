#!/usr/bin/env python


import sys
import os
import json


DIRECTORY = os.path.dirname(__file__)
PARENT_DIRECTORY = os.path.dirname(DIRECTORY)

if (DIRECTORY.endswith("samples")):
    sys.path.append(PARENT_DIRECTORY)


from sprite.component import SpriteComponent
from sprite.atlas import Atlas


IMG_DIR = os.path.join(DIRECTORY, "img")
SHEET_PATH = os.path.join(DIRECTORY, "sample_atlas.png")
META_PATH = os.path.join(DIRECTORY, "sample_atlas.json")



def make_atlas():
    a = Atlas("SAMPLE SPRITE\n{size}", min_size=(128, 128))
    for filename in os.listdir(IMG_DIR):
        filepath = os.path.join(IMG_DIR, filename)
        name = filename.split(".")[0]
        component = SpriteComponent(name, filepath=filepath)
        a.add_component(component)
    a.dump_atlas(SHEET_PATH)
    with open(META_PATH, "w") as f:
        json.dump(a.get_meta(), f, indent=4)



if __name__ == "__main__":
    make_atlas()

