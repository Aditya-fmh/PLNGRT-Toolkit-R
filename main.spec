# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define or import get_resource_path function
def get_resource_path(relative_path):
    import os
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),  # Include config.py in the root of the dist folder
        ('resource', 'resource'),  # Include the entire resource folder
        ('config', 'config'),  # Include the entire config folder
    ],
    hiddenimports=[
        'scipy._lib._util',  # Add hidden imports here
        'scipy._lib.array_api_compat.numpy',
        'numpy.f2py',
        'numpy.f2py.auxfuncs',
        'numpy.f2py.cfuncs',
        'qfluentwidgets.components.navigation.navigation_panel',
        'qfluentwidgets.components.widgets.acrylic_label',
        'qfluentwidgets.common.image_utils',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False if you don't want a console window
    icon=get_resource_path('resource/icon2.ico')  # Specify your icon file here
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)