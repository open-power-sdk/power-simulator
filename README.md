[![Build Status](https://travis-ci.org/open-power-sdk/power-simulator.svg?branch=master)](https://travis-ci.org/open-power-sdk/power-simulator)

# Project Description
The Power Functional Simulator Setup aims to easy the setup and startup of the IBM POWER Functional Simulator. It automatizes all the required procedures like dependencies
installation, network configuration and the simulator usage.

## Contributing to the project
We welcome contributions to the Power Functional Simulator Setup Project in many forms. There's always plenty to do! Full details of how to contribute to this project are documented in the
[CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainers
The project's [maintainers](MAINTAINERS.txt): are responsible for reviewing and merging all pull requests and they guide the over-all technical direction of the project.

## Communication <a name="communication"></a>
We use [Slack](https://toolsforpower.slack.org/) for communication.

## Supported Architecture and Operating Systems

x86_64: Ubuntu 16.04, CentOS7, RHEL 7.3, SLES12, Fedora 25.

## Installing

Requirements: python-pip, python-pylint, python-virtualenv, python-docsutil

Build: ./dev release

Build and install: ./dev install

Execution: mambo --help

## Documentation

usage: mambo [-h] [-V | -i | -s {power8,power9}]

Configures and starts the IBM POWER8 and POWER9 Functional Simulator

  -h, --help            show the help message and exit
  
  -V, --version         show program's version number and exit
  
  -i, --install         install the simulator and its dependencies
  
  -s {power8,power9}, --start {power8,power9}       start the a selected version of the simulator


## Still Have Questions?
For general purpose questions, please use [StackOverflow](http://stackoverflow.com/questions/tagged/toolsforpower).

## License <a name="license"></a>
The Power Functional Simulator Setup Project uses the [Apache License Version 2.0](LICENSE) software license.

## Related information
[POWER Functional Simulator](https://www-304.ibm.com/webapp/set2/sas/f/pwrfs/pwr9/home.html)
