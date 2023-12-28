"""
setup.py: Setup script for CouchCrasher application.

Usage:
    python3 -m build --wheel
"""

from setuptools import setup, find_packages


def get_version():
    for line in open("couchcrasher.py", "r").readlines():
        if not line.startswith("PROJECT_VERSION:"):
            continue
        return line.split("=")[1].strip().strip('"')


setup(
    name="couchcrasher",
    version=get_version(),
    description="Multi-platform persistence tool for user-provided payloads.",
    author="Ezra Fast, Mitchell Nicholson, Mykola Grymalyuk, Scott Banister and Ulysses Hill",
    author_email="",
    url="https://github.com/Couch-Crasher-ISS-Capstone/Couch-Crasher-Code",
    python_requires='>=3.6',
    packages=find_packages(include=['*', 'support', 'support.*']),
    package_data={
        '': ['couchcrasher.py'],
        'support': ['*'],
        'support.*': ['*'],
    },
    include_package_data=True,
)