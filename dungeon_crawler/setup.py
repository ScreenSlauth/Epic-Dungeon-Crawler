from setuptools import setup, find_packages # type: ignore
import os

# Read the README for the long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name="epic_dungeon_crawler",
    version="1.0.0",
    description="A roguelike dungeon crawler game built with Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pratul Sharma",
    author_email="your.email@example.com",
    packages=find_packages(),
    package_data={
        'dungeon_crawler': ['assets/images/*', 'assets/music/*', 'assets/sounds/*'],
    },
    include_package_data=True,
    install_requires=[
        "pygame>=2.0.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "dungeon-crawler=dungeon_crawler.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
    ],
) 