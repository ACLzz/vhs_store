""" Script for Blender3D.
    You *must* run it with:
    `blender cassette.blend -P cassette_constructor.py --python-use-system-env --factory-startup`
  """
from random import randint
from requests import get
from os import remove
from sys import path
from string import whitespace, punctuation

path.append('.')

import django_setup
from drive import Drive
from store.models import Film, Cassette

import bpy


class CassetteRender:
    palletes = {
        1: {
            "basic": [0.034340, 0.036889, 0.035601, 1.000000],
            "sharp": [0.116971, 0.102242, 0.351533, 1.000000],
        },
        2: {
            "basic": [0.033105, 0.033105, 0.033105, 1.000000],
            "sharp": [0.046964, 0.046964, 0.046964, 1.000000],
        },
        3: {
            "basic": [0.059511, 0.043735, 0.057805, 1.000000],
            "sharp": [0.064803, 0.007499, 0.054480, 1.000000],
        },
        4: {
            "basic": [0.009721, 0.116971, 0.258183, 1.000000],
            "sharp": [0.003035, 0.012983, 0.051269, 1.000000],
        },
        5: {
            "basic": [0.036889, 0.149960, 0.149960, 1.000000],
            "sharp": [0.391572, 0.814847, 0.318547, 1.000000],
        },
        6: {
            "basic": [0.198069, 0.059511, 0.102242, 1.000000],
            "sharp": [0.346704, 0.174647, 0.099899, 1.000000],
        }
    }

    tex = None
    title = None

    torender = None

    texture = bpy.data.materials['sticker_face'].node_tree.nodes['Image Texture']
    basic = bpy.data.materials['basic'].node_tree.nodes['RGB'].outputs[0]
    sharp = bpy.data.materials['top_sharped_face'].node_tree.nodes['RGB'].outputs[0]
    color = bpy.data.materials['base_case'].node_tree.nodes['RGB'].outputs[0]

    def assemble(self):
        # Replace texture
        self.texture.image.filepath = self.tex
        # Replace render image name, to name of texture
        bpy.context.scene.render.filepath = self.title
        # Choose one of six presets to cassette
        n = randint(1, 6)
        preset = self.palletes[n]
        # Install presets to cassette
        self.basic.default_value = preset['basic']  # basic option
        self.sharp.default_value = preset['sharp']  # sharped option
        self.color.default_value = preset['basic']  # color

    def render(self, title, path):
        self.tex = path
        self.title = title
        self.assemble()
        # Rendering
        bpy.ops.render.render(write_still=True)


def handle_title(title):
    new_title = ''
    for ch in title:
        if ch in whitespace or ch in punctuation:
            ch = '_'
        new_title += ch

    return new_title


if __name__ == "__main__":
    cr = CassetteRender()
    drive = Drive
    drive.default_folder = 'vhs_store'
    drv = drive()

    to_render_films = Film.objects.filter(cassette__film_id=None)

    for film in to_render_films:
        cover = get(film.image)
        title = handle_title(film.title)
        filename = f'{title}.png'
        rendername = f'{title}_render.png'

        with open(filename, 'wb') as f:
            f.write(cover.content)

        cr.render(rendername, filename)
        link = drv.add_file(filename=rendername, title=title).get('webContentLink')
        cassette = film.cassette_set.create(cover=link, price=15)
        cassette.save()

        remove(rendername)
        remove(filename)

    exit(0)
