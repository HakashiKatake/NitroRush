
from distutils.core import setup
import py2exe

setup(windows=[{
            "script":"Nitro Rush.py",
            "icon_resources": [(1, "assets/nitro_rush.ico")]}])