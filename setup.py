try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Fish shoaling simulation.',
    'author': 'Thomas Hettinger',
    'url': 'https://github.com/tomhettinger/shoaling',
    'author_email': 'tomhettinger@gmail.com',
    'version': '1.0',
    'install_requires': ['nose', 'pygame'],
    'packages': ['shoaling'],
    'scripts': ['bin/shoaling'],
    'name': 'shoaling',
    'license':'LICENSE'
}

setup(**config)
