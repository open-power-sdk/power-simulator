#!/bin/bash
#
# Copyright (C) 2017 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#    Contributors:
#        * Paul Clarke <pacman@us.ibm.com>
#        * Rafael Sene <rpsene@br.ibm.com>

[[ "$(id -u)" != 0 ]] && echo "This script must be run with root priviledges." && exit 1

if [[ ! ( "$1" == "--yes" || "$1" == "-y" ) ]]; then
	echo "This script will configure and enable new software repositories on this system."
	read -N 1 -p 'Proceed? (y/N) ' p
	echo
	if [[ ! ( "$p" =~ [yY] ) ]]; then
		exit 1
	fi
fi

source /etc/os-release
case "$ID" in
	debian)
		package_manager=apt-get;;
	*)
		echo unsupported operating system
		exit 1;;
esac

GET=""
GET2PIPE=""
if which curl >/dev/null; then
	GET="curl -O"
	GET2PIPE="curl"
elif which wget >/dev/null; then
	GET="wget"
	GET2PIPE="wget -O-"
fi

function download {
	if [ -z "$GET" ]; then
		echo "I need curl or wget to continue"; exit 1
	fi
	$GET $@
}

function download2pipe {
	if [ -z "$GET2PIPE" ]; then
		echo "I need curl or wget to continue"; exit 1
	fi
	$GET2PIPE $@
}

case "$package_manager" in
	apt-get)
		apt-get install software-properties-common # for apt-add-repository

		REPO_URI=ftp://ftp.unicamp.br/pub/linuxpatch/toolchain/at/ubuntu

		# apt-key add 6976a827.gpg.key
		key="$(download2pipe $REPO_URI/dists/trusty/6976a827.gpg.key)"
		if [ $? -eq 0 ]; then
			echo "$key" | apt-key add -
		fi

		AT_RELEASES="$(download2pipe $REPO_URI/dists/trusty/Release | sed '/Components/s/^Components: \(.*\)$/\1/;tcontinue;d;:continue')"
		apt-add-repository "deb$arch $REPO_URI trusty $AT_RELEASES"

		REPO_URI=ftp://public.dhe.ibm.com/software/server/iplsdk/latest/packages/deb/repo

		# apt-key add B346CA20.gpg.key
		key="$(download2pipe $REPO_URI/dists/trusty/B346CA20.gpg.key)"
		if [ $? -eq 0 ]; then
			echo "$key" | apt-key add -
		fi

		apt-add-repository "deb$arch $REPO_URI trusty sdk"

		apt-get update
		;;
	*)
		echo "I don't know how to set up your package management system."
		exit 1
		;;
esac

# enable XL compiler repo
arch=$(uname -p)
if [ "$arch" = ppc64le ]; then
	XL_REPO_ROOT=http://public.dhe.ibm.com/software/server/POWER/Linux/xl-compiler/eval/$arch
	case "$ID" in
		debian)
			download2pipe $XL_REPO_ROOT/ubuntu/public.gpg | apt-key add -
			apt-add-repository "deb $XL_REPO_ROOT/ubuntu/ trusty main"
			sudo apt-get update
			;;
	esac
fi
