from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'pyranch',
    version = '0.1dev',
    packages = ['pyranch',],
    author = '',
    author_email = '',
    url = 'https://github.com/fedetorre/pyranch',
    license = '',
    install_requires=required,
    long_description = open('README.md').read(),
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries',
    ]
)
