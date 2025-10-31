"""
Setup configuration for testinium-qa-python test automation framework.

This package provides a Python-based Selenium + Behave BDD test automation
framework, migrated from the original Java + Cucumber implementation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as fh:
        long_description = fh.read()

# Core dependencies - required for test execution
# Versions match requirements from Agent Action Plan section 0.6.2
install_requires = [
    # Core Testing Framework
    "selenium>=4.15.2",
    "behave>=1.2.6",
    "pytest>=7.4.3",
    "pytest-bdd>=6.1.1",
    
    # WebDriver Management
    "webdriver-manager>=4.0.1",
    
    # Test Data Generation
    "Faker>=20.1.0",
    
    # Configuration Management
    "python-dotenv>=1.0.0",
    "PyYAML>=6.0.1",
    
    # Reporting and Visualization
    "allure-behave>=2.13.2",
    "allure-pytest>=2.13.2",
    "pytest-html>=4.1.1",
    "behave-html-formatter>=0.9.10",
    
    # Parallel Execution
    "pytest-xdist>=3.5.0",
    
    # Utilities
    "requests>=2.31.0",
]

# Development dependencies - for code quality and testing
extras_require = {
    "dev": [
        "pylint>=3.0.3",
        "black>=23.12.1",
        "mypy>=1.7.1",
        "pytest-cov>=4.1.0",
        "isort>=5.12.0",
        "bandit>=1.7.5",
        "safety>=2.3.5",
    ],
}

# Package metadata
setup(
    name="testinium-qa-python",
    version="1.0.0",
    description="Python Selenium + Behave BDD test automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Testinium QA Team",
    author_email="qa-team@testinium.com",
    url="https://github.com/testinium/testinium-qa-python",
    license="MIT",
    
    # Package discovery
    packages=find_packages(exclude=["tests*", "docs*", "target*", "reports*"]),
    
    # Include package data (feature files, config files)
    include_package_data=True,
    package_data={
        "": ["*.feature", "*.yaml", "*.yml", "*.ini"],
    },
    
    # Python version requirement
    python_requires=">=3.9",
    
    # Dependencies
    install_requires=install_requires,
    extras_require=extras_require,
    
    # Entry points for command-line tools (optional)
    entry_points={
        "console_scripts": [
            # Add CLI commands here if needed
            # Example: "testinium-run=utilities.test_runner:main",
        ],
    },
    
    # PyPI classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
        "Framework :: Selenium",
        "Natural Language :: English",
    ],
    
    # Keywords for PyPI search
    keywords=[
        "selenium",
        "behave",
        "bdd",
        "test-automation",
        "testing",
        "qa",
        "webdriver",
        "cucumber",
        "gherkin",
        "page-object-model",
    ],
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/testinium/testinium-qa-python/issues",
        "Source": "https://github.com/testinium/testinium-qa-python",
        "Documentation": "https://github.com/testinium/testinium-qa-python/wiki",
    },
    
    # Zip safe flag
    zip_safe=False,
)
