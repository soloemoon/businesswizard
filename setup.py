from setuptools import setup, find_packages
from setuptools.command.install import install
import glob
import os
import shutil
import atexit

VERSION = '0.0.2'
DESCRIPTION = 'Helpful Business Functions'
setup(
    name = 'businesswizard',
    version=VERSION,
    author='Solomon Moon',
    author_email = '<soloemoon@gmail.com>',
    description=DESCRIPTION,
    packages = find_packages(),
    install_requires = ['pandas', 'numpy', 'pyjanitor', 'datetime', 'python-dateutil', 'xlwings', 'polars'],
    keywords = ['python','bizwiz', 'businesswizard', 'business', 'helper'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows'
    ]

)


def install_styles():
    stylefiles = glob.glob('styles/**/*.mplstyle', recursive=True)
    mpl_stylelib_dir = os.path.join(matplotlib.get_configdir(),'stylelib')
    if not os.path.exists(mpl_stylelib_dir):
        os.makedirs(mpl_stylelib_dir)
    
    for stylefile in stylefiles:
        print(os.path.basename(stylefile))
        shutil.copy(
            stylefile,
            os.path.join(mpl_stylelib_dir, os.path.basename(stylefile))
        )
    
class PostInstallMoveFile(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(install_styles)



