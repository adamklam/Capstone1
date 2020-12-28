# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['simple1.py'],
             pathex=['/home/adam/Desktop/assignments/Capstone 1 '],
             binaries=[],
             datas=[('arcweldingsim.txt', '.'), ('blackbodysim.txt', '.'), ('halogensim.txt', '.'), ('flourescentLamp6inrandommod.txt', '.'), ('acetylene.txt', '.'), ('methane.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='simple1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
