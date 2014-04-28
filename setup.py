try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Fish shoaling simulation.',
    'author': 'Thomas Hettinger',
    'url': 'https://github.com/tomhettinger/shoaling',
    'download_url': 'Where to download it.',
    'author_email': 'tomhettinger@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'pygame'],
    'packages': ['shoaling'],
    'scripts': [],
    'name': 'shoaling'
}

setup(**config)
