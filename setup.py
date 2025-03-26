from setuptools import setup, find_packages

setup(
    name="geopolitics-simulator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pytest>=7.4.3",
        "typing-extensions>=4.8.0",
    ],
) 