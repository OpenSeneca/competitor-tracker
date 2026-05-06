#!/usr/bin/env python3
"""
Setup script for Competitor Tracker CLI tool
"""

from setuptools import setup

setup(
    name="openseneca-competitor-tracker",
    version="1.0.0",
    description="Track AI company shipping activity for blog research",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="OpenSeneca",
    url="https://github.com/OpenSeneca/competitor-tracker",
    py_modules=["main"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "competitor-track=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
)
