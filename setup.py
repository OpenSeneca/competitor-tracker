from setuptools import setup, find_packages

setup(
    name="competitor-tracker",
    version="1.0.0",
    description="AI company announcement tracker for competitive intelligence",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="OpenSeneca",
    author_email="opensource@seneca.ai",
    url="https://github.com/openseneca/competitor-tracker",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
    ],
    entry_points={
        'console_scripts': [
            'competitor-tracker=competitor_tracker:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
