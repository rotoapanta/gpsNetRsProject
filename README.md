# <p align="center">GPS NetRS with Zabbix

<p align="center">This project aims to monitor the health status of GPS NetRS receivers using Zabbix.</p>

##

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)
[![GitHub issues](https://img.shields.io/github/issues/rotoapanta/botZabbixPackage)](https://github.com/rotoapanta/botZabbixPackage/issues)
![GitHub repo size](https://img.shields.io/github/repo-size/rotoapanta/botZabbixPackage)
![GitHub last commit](https://img.shields.io/github/last-commit/rotoapanta/botZabbixPackage)
![GitHub commit merge status](https://img.shields.io/github/commit-status/rotoapanta/botZabbixPackage/master/d8b7bfe)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/gpl-2.0)
![Discord](https://img.shields.io/discord/996422496842694726)
[![Discord Invite](https://img.shields.io/badge/discord-join%20now-green)](https://discord.gg/Gs9b3HFd)
![GitHub forks](https://img.shields.io/github/forks/rotoapanta/botZabbixPackage?style=social)
[![Zabbix](https://img.shields.io/badge/Zabbix-4.6-orange)](https://www.zabbix.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots)
[![Python](https://img.shields.io/badge/Python-3.11-brightgreen)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-No-brightgreen)](https://www.docker.com/)
[![Author 1](https://img.shields.io/badge/Roberto%20-Toapanta-brightgreen)](link_to_author1)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](link_to_license) 
- [![GitHub](https://img.shields.io/badge/GitHub-Project-brightgreen)](link_to_github)
- [![Documentation](https://img.shields.io/badge/Documentation-Read%20Now-blue)](link_to_docs)

# Contents

- [Getting started](#getting-started)
  - [Getting started with Zabbix and Telegram](#getting-started-with-zabbix-and-telegram)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Components Description](#components-description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running the Project Automatically with Crontab](#running-the-project-automatically-with-crontab)
- [Environment Variables](#environment-variables)
- [Change Log](#change-log)
- [Running Tests](#running-tests)
- [Usage/Examples](#usage-examples)
- [Feedback](#feedback)
  - [Support](#support)
  - [License](#license)
- [Authors](#authors)
- [More Info](#more-info)
- [Links](#links)

## Getting started

### Getting started with Zabbix and Telegram

GPS NetRS receivers are used in various applications, including geodetic surveying, GNSS data collection, and more. Monitoring their health and performance is essential to ensure the reliability of data they provide. This project leverages Zabbix, a popular monitoring solution, to help you keep an eye on your GPS NetRS devices.

Let’s get started!

### Features

- Retrieve various metrics from GPS NetRS devices.
- Send collected data to Zabbix for analysis.
- Easily schedule monitoring tasks using `crontab`.

### Requirements

Before you get started, make sure you have the following:

- Python 3.11 or higher installed on your system.
- [Anaconda](https://www.anaconda.com/) for creating and managing Conda environments.
- A Zabbix server for storing and analyzing the collected data.
- Basic knowledge of using `crontab` for scheduling tasks.
- GPS NetRS devices
- Computer running Anaconda on Windows, Linux or macOS (in this case macOS is used).

### Components Description

- The project consists of the following components:
  - [Component 1](link_to_component_1) - A short description.
  - [Component 2](link_to_component_2) - A short description.

- gpsNetRsProject/
  - api/
    - __init__.py
    - api_zbx_processing.py
    - logs/
      - __init__.py
      - 2023-10-31_gps_netrs.log
      - gps_netrs.log
    - templates/
      - zbx_export_templates.xml
    - test/
      - __init__.py
      - test_gps_netrs_project.py
    - utils/
      - __init__.py
      - utilities.py
  - config.ini          # Archivo de configuración con detalles del proyecto
  - main.py
  - requirements.txt
  - run_gps_netrs.sh
  - setup.py
  - zabbix_sender.py

## Installation

1. Clone the repository to your local machine:

  ```bash
   git clone https://github.com/rotoapanta/gpsNetRsProject.git
  ```
2. To automate the monitoring process, you can use crontab to schedule the execution of the script at specific intervals. The provided run_gps_netrs.sh shell script helps you set up the environment and run the project under cron. 

Here's how to configure and use crontab with the project:

  a. Open the crontab configuration for your user by running the following command

  ```bash
   crontab -e
  ```
 b. Add an entry to schedule the script to run at regular intervals. For example, to run the script every 10 minutes, add the following line:
  
  ```bash
   */10 * * * * bash /path/to/run_gps_netrs.sh >> /path/to/logs/gps_netrs.log 2>&1
  ```
Be sure to replace /path/to with the actual paths to the run_gps_netrs.sh script and the desired log file.

Save and exit the crontab editor.

The script will now run automatically at the specified intervals and log its output to the specified log file.

## Configuration

- Describe how to configure your project, including any settings or environment variables.
- [![Linux](https://img.shields.io/badge/Linux-Supported-brightgreen)](https://www.linux.org/)
- [![Windows](https://img.shields.io/badge/Windows-Supported-brightgreen)](https://www.microsoft.com/)

## Running the Application

- Explain how to run your application.
- [![Docker](https://img.shields.io/badge/Docker-Yes-brightgreen)](https://www.docker.com/)

## Running the Project Automatically with Crontab

- Describe how to set up scheduled tasks using Crontab or similar tools.
- [![Crontab](https://img.shields.io/badge/Crontab-Supported-brightgreen)](link_to_crontab)

## Environment Variables

- Document the available environment variables and their purposes.
- [![Env Vars](https://img.shields.io/badge/Environment-Variables-blue)](link_to_env_vars)

## Change Log

- Document the changes made in each version of your project.
- [![Version](https://img.shields.io/badge/Version-1.0-brightgreen)](link_to_changelog)

## Running Tests

- Provide instructions for running tests.
- [![Testing](https://img.shields.io/badge/Testing-Yes-brightgreen)](link_to_tests)

## Usage/Examples

- Provide examples of how to use your project.
- [![Example](https://img.shields.io/badge/Example-Yes-brightgreen)](link_to_examples)

## Feedback

If you have any feedback, please reach out to us at robertocarlos.toapanta@gmail.com

## Support

For support, email robertocarlos.toapanta@gmail.com or join our Discord channel.

## License

[GPL v2](https://www.gnu.org/licenses/gpl-2.0)

## Autors

- [@rotoapanta](https://github.com/rotoapanta)

## More Info

* [Official documentation for py-zabbix](https://py-zabbix.readthedocs.io/en/latest/)
* [Install py-zabbix 1.1.7](https://pypi.org/project/pyzabbix/)

## Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roberto-carlos-toapanta-g/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/rotoapanta)

