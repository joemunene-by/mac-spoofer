from setuptools import setup, find_packages

setup(
    name="mac-spoofer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "mac-spoofer=cli.main:main",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    description="A professional, production-ready MAC Address Spoofer CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mac-address-spoofer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
    ],
)
