# setup.py
from setuptools import setup, find_packages

setup(
    name="ml-project-launch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "loguru",
        "rich",
        "python-dotenv",
        "openai",
    ],
)