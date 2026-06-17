"""
setup.py
--------
Packaging config. Installing with `pip install -e .` makes the
`phishing_detector` package importable from anywhere, and creates a
`phishing-detector` command on your PATH (see entry_points below).
"""

from setuptools import setup, find_packages

setup(
    name="phishing-detector",
    version="0.1.0",
    description="Rule-based phishing email detector (Phase 1: core + CLI)",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "phishing-detector=phishing_detector.cli:main",
        ],
    },
)
