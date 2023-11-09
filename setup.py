from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpsNetRsProject",
    version="1.0.0",
    author='Roberto Toapanta',
    author_email='robertocarlos.toapanta@gmail.com',
    description="Project for monitoring the health status of GPS NetRS receivers",
    long_description="Retrieves voltage, temperature, and serial number values from the devices for comprehensive "
                     "monitoring.",
    long_description_content_type="text/markdown",
    url="https://github.com/rotoapanta/gpsNetRsProject.git",
    packages=find_packages(),
    install_requires=[
        "py-zabbix==1.1.7",  # List your dependencies here
        "requests~=2.31.0",
        "brotlipy==0.7.0",
        "setuptools~=68.0.0"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
