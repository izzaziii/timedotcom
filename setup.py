from setuptools import setup, find_packages

setup(
    name="timedotcom",
    version="0.1.0",
    description="Time.com data processing package",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "pymongo",
        "openpyxl",
        "python-dotenv",
    ],
)
