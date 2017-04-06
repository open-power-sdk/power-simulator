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
import time
import sys
import variables as var
from core import SetupSimulator


def run(args):
    """
    Executes the correct action according the user input.

    Parameters:
        args - arguments collected by argparser
    """
    # Declares an instance of SetupSimulator()
    setup = SetupSimulator()
    if args.install:
        # Cleanup the screen
        setup.clear()
        # Get the moment when the installation started
        start_time = time.time()
        # Check internet connection
        if not setup.is_connected_internet():
            print "Ensure you have internet connection"
            sys.exit(1)
        # Pretty print an initial message
        setup.pretty_print("Installing")
        # Check and install missing dependencies.
        setup.verify_dependencies()
        # Create a directory where all packages will be stored.
        create_directory(var.DOWNLOAD_DIR, setup)
        # Download and show the license
        download_license(var.LICENSES, var.DOWNLOAD_DIR, setup)
        # Continue the installation process only if the user
        # agreed with the license.
        if setup.read_license():
            download_common_pckg(var.COMMON_FILES, var.DOWNLOAD_DIR, setup)
            download_by_distro(setup.get_distro(), var.DIR_PATH,
                               var.DOWNLOAD_DIR, setup)
            setup.check_sum(var.DOWNLOAD_DIR)
            install_packages(var.VERSIONS, var.DOWNLOAD_DIR, setup)
            extract_img(var.DISK, var.DOWNLOAD_DIR, setup)
            # customize_img(var.DISK, var.LOCKFILE, var.MOUNT_POINT,
            #               var.DOWNLOAD_DIR, setup)
            create_symlink(var.DISK_SYM_LINK, var.DISK, var.DOWNLOAD_DIR,
                           setup)
            if setup.cmd_exists('mambo'):
                setup.execute_cmd('mambo --help')
        print "Execution time: %s seconds." % (time.time() - start_time)
    elif args.start:
        try:
            start_simulator(args.start, setup)
        except (KeyboardInterrupt, SystemExit, RuntimeError):
            exit(1)


def create_directory(target_directory, setup_simulator):
    '''
    Create a directory where all packages will be stored.
    '''
    if setup_simulator.directory_exists(target_directory):
        setup_simulator.remove_directory(target_directory)
    else:
        setup_simulator.create_directory(target_directory)


def download_license(licenses, download_directory, setup_simulator):
    '''
    Download and show the license
    '''
    for lcs in licenses:
        with open(lcs) as lcs_file:
            ftp_url = lcs_file.readline().strip('\n')
            packages = lcs_file.readlines()
            size = len(packages)
        for pckg in range(size):
            fname = download_directory + "/" + packages[pckg].strip('\n')
            if not setup_simulator.file_exists(fname):
                print " * Downloading " + packages[pckg].strip('\n')
                setup_simulator.download(ftp_url, packages[pckg].strip('\n'),
                                         download_directory)
    setup_simulator.configure_license()


def download_common_pckg(common_files, download_directory, setup_simulator):
    '''
    Download the necessary packages. They are stored into the files
    license and simulator. The first line contains the base URI and
    the rest of the file contains the packages.
    '''
    setup_simulator.print_line()
    for download in common_files:
        with open(download) as fdownload:
            ftpurl = fdownload.readline().strip('\n')
            packages = fdownload.readlines()
            size = len(packages)
        for pkg in range(size):
            fname = download_directory + "/" + packages[pkg].strip('\n')
            if not setup_simulator.file_exists(fname):
                print " * Downloading " + packages[pkg].strip('\n')
                setup_simulator.download(ftpurl, packages[pkg].strip('\n'),
                                         download_directory)


def download_by_distro(distro, dir_path, download_directory, setup_simulator):
    '''
    Download the necessary packages by distro.
    '''
    if var.UBUNTU in distro:
        dfile = dir_path + "/resources/distros/ubuntu.config"
    elif var.FEDORA in distro:
        dfile = dir_path + "/resources/distros/fedora.config"
    else:
        dfile = dir_path + "/resources/distros/suserhelcentos.config"
    with open(dfile) as fdownload:
        packages = fdownload.readlines()
        size = len(packages)
        for pkg in range(size):
            # brake the file remote location
            aux = packages[pkg].split("/")
            # gets the last index with contains the package name
            sim_package = aux[len(aux) - 1]
            # remove the last item
            aux.pop()
            # concatenates creating the URL
            ftpurl = '/'.join(aux)
            fname = download_directory + "/" + sim_package.strip('\n')
            if not setup_simulator.file_exists(fname):
                print " * Downloading " + sim_package.strip('\n')
                setup_simulator.download(ftpurl + "/", sim_package.strip('\n'),
                                         download_directory)


def install_packages(simulator_versions, download_directory, setup_simulator):
    '''
    Install the simulator packages for p8 and p9 according
    the host distro
    '''
    for simulator_version in simulator_versions:
        if not setup_simulator.directory_exists(simulator_version):
            setup_simulator.print_line()
            print "Installing the simulator packages..."
            if var.UBUNTU in setup_simulator.get_distro():
                for deb_pkg in os.listdir(download_directory):
                    if deb_pkg.endswith(".deb"):
                        pkg_name = download_directory + "/" + deb_pkg
                        setup_simulator.install_deb(pkg_name)
            else:
                for rpm_pkg in os.listdir(download_directory):
                    if rpm_pkg.endswith(".rpm"):
                        pkg_name = download_directory + "/" + rpm_pkg
                        setup_simulator.install_rpm(pkg_name)


def extract_img(disk_img, download_directory, setup_simulator):
    '''
    Extract the bzip2 file which contains the Debian sysroot
    '''
    full_img_path = download_directory + disk_img
    try:
        if not setup_simulator.file_exists(full_img_path):
            if setup_simulator.file_exists(full_img_path + ".bz2"):
                setup_simulator.print_line()
                print "Extracting the image (it will take a while)..."
                cmd = "bzip2 -dkv " + full_img_path + ".bz2"
                setup_simulator.execute_cmd(cmd)
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        raise


def customize_img(disk_img, lock, mount, download_directory, setup_simulator):
    '''
    Customize the disk img by copying the script which installs the SDK
    and its dependencies inside it
    '''
    full_img_path = download_directory + disk_img
    if not setup_simulator.file_exists(lock):
        setup_simulator.print_line()
        print "Customizing the image..."
        setup_simulator.configure_image(full_img_path, lock, mount)
    else:
        print "Image alredy customized"


def create_symlink(sym_link, disk, download_directory, setup_simulator):
    '''
    Configure a symlink to be used by the tcl script
    '''
    if not setup_simulator.file_exists(download_directory + sym_link):
        cmd = download_directory + disk + " " + download_directory + sym_link
        setup_simulator.execute_cmd("ln -s " + cmd)


def set_network(setup_simulator):
    '''
    Set the tap0 network interface and allocate a valid
    IP for it. The img used with the simulator has it
    IP address already set.
    '''
    print "\n\nConfiguring network to access the simulator...\n"
    ip_address = "172.19.98.108/16"
    netmask = "netmask 255.255.255.254"
    broadcast = "broadcast 172.19.255.255"
    set_ip_cmds = [
        'ip tuntap add tap0 mode tap',
        'ifconfig tap0 ' + ip_address + ' ' + netmask + ' ' + broadcast,
        'iptables -t nat -A POSTROUTING -j MASQUERADE',
        'iptables -I FORWARD -s ' + ip_address + ' -i tap0 -j ACCEPT',
        'iptables -I FORWARD -d ' + ip_address + ' -o tap0 -j ACCEPT',
        '-k'
    ]
    for cmd in set_ip_cmds:
        setup_simulator.execute_cmd('sudo ' + cmd)


def unset_network(setup_simulator):
    '''
    Unset the tap0 network interface
    '''
    print "\n\nRemoving network configuration to access the simulator...\n"
    unset_ip_cmds = [
        'ip tuntap del tap0 mode tap',
        'iptables -D FORWARD -s 172.19.0.0/16 -i tap0 -j ACCEPT',
        'iptables -D FORWARD -d 172.19.0.0/16 -o tap0 -j ACCEPT',
        'iptables -t nat -D POSTROUTING -j MASQUERADE',
        '-k'
    ]
    for cmd in unset_ip_cmds:
        setup_simulator.execute_cmd('sudo ' + cmd)


def start_simulator(version, setup_simulator):
    '''
    starts the simulator according the version selected by the user
    '''
    if setup_simulator.show_connection_info(version):
        os.chdir(var.DOWNLOAD_DIR)
        set_network(setup_simulator)
        if 'power8' in version:
            p8_prefix = '/opt/ibm/systemsim-p8/run/pegasus/'
            p8_sim = p8_prefix + 'power8 -W -f'
            p8_tcl = p8_prefix + 'linux/boot-linux-le.tcl'
            setup_simulator.execute_cmd(p8_sim + ' ' + p8_tcl)
        elif 'power9' in version:
            p9_prefix = '/opt/ibm/systemsim-p9/run/p9/'
            p9_sim = p9_prefix + 'power9 -W -f'
            p9_tcl = p9_prefix + 'linux/boot-linux-le-skiboot.tcl'
            setup_simulator.execute_cmd(p9_sim + ' ' + p9_tcl)
        unset_network(setup_simulator)
