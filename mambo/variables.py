#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C) 2017 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Rafael Peria de Sene <rpsene@br.ibm.com>
'''

import os
from os.path import expanduser

HOME = expanduser("~")
DOWNLOAD_DIR = HOME + "/systemsim_execution/"
UBUNTU = "Ubuntu"
FEDORA = "Fedora"
SUSE = "SUSE"
RHEL = "Red Hat"
DISK = "/debian-ppc64le.img"
DISK_SYM_LINK = "/disk.img"
VERSIONS = ["/opt/ibm/systemsim-p8", "/opt/ibm/systemsim-p9"]
LOCKFILE = DOWNLOAD_DIR + "/.sysmsimcustomlock"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LICENSES = [DIR_PATH + "/resources/license.config"]
COMMON_FILES = [DIR_PATH + "/resources/rootfsfiles.config"]
DEPENDENCIES = ['xterm', 'bzip2', 'ip', 'ifconfig', 'iptables', 'sysctl']
MOUNT_POINT = "/tmp/systemsimdiskimage"
LICENSE_FILE_ZIP = DOWNLOAD_DIR + "/L-RRKI-ACHTLB.zip"
LICENSE = DOWNLOAD_DIR + "/L-RRKI-ACHTLB/Softcopy/LA_en"
