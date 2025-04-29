from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join("src", "smartsense", "__init__.py"), "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string")

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define package metadata and dependencies
setup(
    name="smartsense",
    version=version,
    author="Aaron Jacobs",
    author_email="git@aaronemail.xyz",
    description="A sophisticated IoT environmental monitoring and automation platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaronjacobs-chelt/SmartSense",
    project_urls={
        "Bug Tracker": "https://github.com/aaronjacobs-chelt/SmartSense/issues",
        "Documentation": "https://aaronjacobs-chelt.github.io/SmartSense/",
        "Source Code": "https://github.com/aaronjacobs-chelt/SmartSense",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: System :: Monitoring",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn>=0.21.1",
        "pydantic>=1.10.7",
        "numpy>=1.24.2",
        "pandas>=2.0.0",
        "plotly>=5.14.1",
        "dash>=2.9.3",
        "sqlalchemy>=2.0.9",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "aiohttp>=3.8.4",
        "colorlog>=6.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "mypy>=1.2.0",
            "flake8>=6.0.0",
            "pre-commit>=3.2.2",
            "sphinx>=6.1.3",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "raspberry": [
            "RPi.GPIO>=0.7.1",
            "adafruit-circuitpython-dht>=3.7.8",
        ],
        "ml": [
            "scikit-learn>=1.2.2",
            "pytorch>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartsense=smartsense.cli:main",
            "smartsense-dashboard=smartsense.dashboard:main",
        ],
    },
    zip_safe=False,
    include_package_data=True,
)

