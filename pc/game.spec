# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/var/folders/75/yw6fwggd2gl35p2d_t3_9qt40000gn/T/.pyxel/app2exe/game.py'],
    pathex=[],
    binaries=[],
    datas=[('../game.pyxapp', '.')],
    hiddenimports=['pyxel'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='game.app',
    icon=None,
    bundle_identifier=None,
)
