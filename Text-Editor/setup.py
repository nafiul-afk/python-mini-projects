#!/usr/bin/env python3
"""
Setup script for Advanced Text Editor
"""

from setuptools import setup, find_packages
import os

# Read the README file if it exists
long_description = "A feature-rich text editor built with Python and Tkinter"

setup(
    name="advanced-text-editor",
    version="1.0.0",
    description="A professional text editor with modern features",
    long_description=long_description,
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/advanced-text-editor",
    license="MIT",
    
    # Package configuration
    py_modules=["app"],
    
    # Dependencies
    install_requires=[
        # Tkinter comes with Python, no additional deps needed
    ],
    
    # Entry points for command-line execution
    entry_points={
        'console_scripts': [
            'text-editor=app:main',
        ],
        'gui_scripts': [
            'text-editor-gui=app:main',
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Editors",
    ],
    
    # Python version requirement
    python_requires='>=3.6',
    
    # Include additional files
    include_package_data=True,
)
