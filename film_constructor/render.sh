export COUNT=0
# ### Run blender ### #
blender cassette.blend -P cassette_constructor.py --python-use-system-env --factory-startup
