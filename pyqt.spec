# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['pyqt.py'],
<<<<<<< HEAD
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
=======
    pathex=['C:\\Users\\Gilbert\\PycharmProjects\\Doc_Art2'],
    binaries=[],
    datas=[('main.py','.'),('Type205.py','.')],
    hiddenimports=['numbers'],
>>>>>>> 0.2.2
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pyqt',
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
