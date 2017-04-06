#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0904

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

import subprocess
import urllib2
import zipfile
import os
import sys
import pwd
import socket
import variables as var


class SetupSimulator(object):
    '''
    Functional class that provides most of the methods necessary
    to configure the simulator.
    '''

    @staticmethod
    def get_distro():
        '''get distro name'''
        with open("/etc/os-release") as distro_file:
            lines = distro_file.readlines()
            return lines[0].split("=", 1)[1].replace("\"", "")

    @staticmethod
    def execute_cmd(command):
        '''execute a cmd'''
        subp = subprocess.call(command, shell=True)
        return subp == 0

    @staticmethod
    def cmd_exists(command):
        '''check if a command exists'''
        subp = subprocess.call("type " + command, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return subp == 0

    @staticmethod
    def is_connected_internet():
        '''check the internet connectivity'''
        try:
            socket.create_connection(("23.202.38.212", 80), 2)
            return True
        except IOError:
            return False

    @staticmethod
    def get_user_name():
        '''get username'''
        return pwd.getpwuid(os.getuid())[0]

    def clear(self):
        '''clear the terminal'''
        self.execute_cmd("clear")

    @staticmethod
    def directory_exists(location):
        '''check if a directory exists'''
        return os.path.exists(location)

    @staticmethod
    def file_exists(location):
        '''check if a file exists'''
        return os.path.isfile(location)

    def create_directory(self, location):
        '''create a directory'''
        if not self.directory_exists(location):
            if not os.path.exists(location):
                os.makedirs(location)

    def remove_directory(self, location):
        '''clean a directory'''
        self.print_line()
        opt = raw_input(" * Would you like to clean " + location + "? [Y/N] ")
        if "Y" in opt or "y" in opt:
            if self.directory_exists(location):
                self.execute_cmd("rm -rf " + location + "/*")
                self.print_line()
        elif "N" in opt or "n" in opt:
            pass
        else:
            print "    * Please, select one of the available options: Y or N"
            sys.exit(1)

    def install_rpm(self, package):
        '''install RPM file'''
        try:
            if self.cmd_exists("dnf"):
                self.execute_cmd('sudo dnf install -y ' + package)
            elif self.cmd_exists("zypper"):
                self.execute_cmd('sudo zypper --non-interactive install ' + package)
            else:
                self.execute_cmd('sudo yum install -y ' + package)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            exit(1)

    def install_deb(self, package):
        '''install DEB file'''
        try:
            self.execute_cmd('sudo dpkg -i ' + package)
            self.execute_cmd('sudo apt-get -fy install')
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            raise

    def install_deb_apt(self, package):
        '''install DEB file via apt-get'''
        try:
            self.execute_cmd('sudo apt-get -y install ' + package)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            raise

    def remove_rpm(self, package):
        '''remove RPM file'''
        try:
            self.execute_cmd('sudo rpm -e ' + package)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            raise

    def remove_deb(self, package):
        '''remove DEB file'''
        try:
            self.execute_cmd('sudo apt-get purge -y ' + package)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            raise

    def configure_image(self, disk_img, lock, mount_point):
        '''configure the image, copying the configurerepos.sh into it.'''
        try:
            # create mount point
            self.execute_cmd('sudo mkdir ' + mount_point)
            # mount images
            self.execute_cmd('sudo mount -o loop ' + disk_img + ' ' + mount_point)
            # copy file inside the images
            mtp = mount_point + "/home"
            cmd = var.DOWNLOAD_DIR + 'configurerepos.sh' + ' ' + mtp
            self.execute_cmd('sudo cp -rp ' + cmd)
            # umount
            self.execute_cmd('sudo umount ' + mount_point)
            # remove mount point
            self.execute_cmd('sudo rm -rf ' + mount_point)
            # create lock file that block continuing customization
            self.execute_cmd('touch ' + lock)
            print "done"
        except (KeyboardInterrupt, SystemExit, RuntimeError, OSError, IOError):
            print "\n   ERROR: could not configure the " + disk_img
            print "   exiting now!"
            sys.exit(1)

    def verify_dependencies(self):
        '''verify if the required dependencies are installed'''
        self.print_line()
        print " * Checking dependencies..."
        try:
            for dep in var.DEPENDENCIES:
                if not self.cmd_exists(dep):
                    self.install_dependencies(dep)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            sys.exit(1)

    def install_dependencies(self, dep):
        '''install the required dependencies'''
        try:
            if var.UBUNTU in self.get_distro():
                self.install_deb_apt(dep)
            else:
                self.install_rpm(dep)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            sys.exit(1)

    @staticmethod
    def size_of(value):
        '''return the size of file formated'''
        for unit in ['', 'Ki', 'Mi']:
            if abs(value) < 1024.0:
                return "%3.1f %s%s" % (value, unit, 'B')
            value = value / 1024.0
        return "%.1f%s%s" % (value, 'Yi', 'B')

    def download(self, base_url, file_name, location):
        '''download'''
        try:
            block_size = 10240
            url_info = urllib2.urlopen(base_url + file_name)
            download_file = open(location + "/" + file_name, 'wb')
            download_meta_info = url_info.info()
            clength = int(download_meta_info.getheaders("Content-Length")[0])
            print "   \\__(%s)" % (self.size_of(clength)),
            while True:
                download_buffer = url_info.read(block_size)
                if not download_buffer:
                    break
                download_file.write(download_buffer)
            download_file.close()
            print "done."
        except (OSError, IOError):
            print "\n   ERROR: could not download " + file_name
            print "   " + base_url + " is not available."

    def check_sum(self, location, checksumfile):
        '''verifies the packages integrity'''
        self.print_line()
        if self.file_exists(location + checksumfile):
            print "Checking the files integrity..."
            self.execute_cmd('cd ' + location + ' && md5sum -c ' + checksumfile)
        else:
            print '\n   ERROR: could not verify the files integrity.'
            print "   " + checksumfile + ' is not available.'

    @staticmethod
    def configure_license():
        '''extract and convert the license from dos to unix'''
        try:
            licensezip = zipfile.ZipFile(var.LICENSE_FILE_ZIP, 'r')
            licensezip.extractall(var.DOWNLOAD_DIR)
            licensezip.close()
            licensetext = open(var.LICENSE, 'rb').read().replace('\r\n', '\n')
            open(var.LICENSE, 'wb').write(licensetext)
        except (OSError, IOError):
            print "\n   ERROR: could not configure the license."

    def read_license(self):
        '''read license'''
        try:
            # ask if the user wants to read the license
            self.print_line()
            opt = raw_input(" * Would you like to read the license? [Y/N] ")
            if "Y" in opt or "y" in opt:
                self.execute_cmd('vi ' + var.LICENSE)
                print ""
            elif "N" in opt or "n" in opt:
                pass
            else:
                print " * Please, select one of the available options: Y or N"
                sys.exit(0)
            # ask if the user agrees with the license
            opt = raw_input(" * Do you agree with the license? [Y/N] ")
            if "Y" in opt or "y" in opt:
                return True
            else:
                self.print_line()
                sys.exit(0)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            sys.exit(1)

    @staticmethod
    def pretty_print(action):
        '''print the initial message'''
        print "\n " + action + " the POWER Functional Simulator.\n"
        print " WARNING: Ensure you are running this script as an user"
        print "          with admin rights. You will be prompt to enter"
        print "          your password during this process.\n"

    @staticmethod
    def print_line():
        '''print a line'''
        print "----------------------------------------------"

    def show_connection_info(self, version):
        '''Show to the user how to connect to the simulator'''
        try:
            self.print_line()
            sversion = 'IBM POWER' + version[-1:] + ' Functional Simulator'
            print '\nYou are starting the ' + sversion
            print 'When the boot process is complete, use the following'
            print 'credentials to access it via ssh:\n'
            print '     ssh root@172.19.98.109'
            print '     password: mambo'
            opt = raw_input("\n     Would you like to start it now? [Y/N] ")
            if "Y" in opt or "y" in opt:
                return True
            elif "N" in opt or "n" in opt:
                sys.exit(0)
            else:
                print "    Please, select one of the available options: Y or N"
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            sys.exit(1)
