from setuptools import setup, find_packages

VERSION = "1.1.0"
PACKAGE_NAME = "sublib"
AUTHOR = "Dawid Jach"
AUTHOR_EMAIL = "jach.developer@protonmail.com"
URL = "https://github.com/TheFifthLeaf/sublib"

LICENSE = "GNU General Public License v3.0"
DESCRIPTION = "Python library for easier management and processing of subtitle files."
with open("README.md", "r", encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()
LONG_DESC_TYPE = "text/markdown"

KEYWORDS = ["python", "subtitle", "sublib", "subrip", "microdvd", "mplayer", "mplayer2", "tmplayer"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    packages=find_packages(),
    keywords=KEYWORDS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
