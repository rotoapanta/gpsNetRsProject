from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpsNetRsProject",
    version="1.0.0",
    author='Roberto Toapanta',
    author_email='robertocarlos.toapanta@gmail.com',
    description="Proyecto para monitorear el estado de salud de GPS",
    long_description='Obtiene los valores de voltaje, temperatura, numero de serie',
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/gpsNetRsProject",
    packages=find_packages(),
    install_requires=[
        "py-zabbix",  # Lista tus dependencias aquí
        "ping3",
        "requests"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
