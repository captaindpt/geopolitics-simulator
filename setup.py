from setuptools import setup, find_packages

setup(
    name="geopolitics-simulator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=8.0.0",
        "pytest-cov>=4.1.0",
        "mypy>=1.8.0",
        "openai>=1.12.0",
    ],
    python_requires=">=3.8",
) 