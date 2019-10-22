import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfbackup",
    version="1.1.0",
    author="Mario Harjac",
    author_email="m@harja.ch",
    description="pfSense config backup tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mharjac/pfbackup",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'pfbackup = pfbackup.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)