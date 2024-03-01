# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('templates/canyon_cave/*.PNG', 'templates/canyon_cave/'),
    ('templates/caves/*.PNG', 'templates/caves/'),
    ('templates/entrance_to_the_cave/*.PNG', 'templates/entrance_to_the_cave/'),
    ('templates/equipment/*.PNG', 'templates/equipment/'),
    ('templates/right_cave/*.PNG', 'templates/right_cave/'),
    ('templates/river_cave/*.PNG', 'templates/river_cave/'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AlphaFarm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
