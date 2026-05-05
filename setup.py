"""
Competitor Tracker CLI - Setup script
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name='squad-competitor-tracker',
    version='1.0.0',
    description='Track AI company product launches and features for blog research and competitive intelligence',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='OpenSeneca Squad',
    author_email='squad@openseneca.org',
    url='https://github.com/OpenSeneca/competitor-tracker',
    license='MIT',
    packages=find_packages(),
    py_modules=['main'],
    python_requires='>=3.6',
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        'console_scripts': [
            'competitor-tracker=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='ai competitive intelligence tracker blog research',
)
