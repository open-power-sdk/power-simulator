#!/bin/bash

#LICENSE INFORMATION
#
#Copyright (c) 2016 IBM Corporation.
#All rights reserved.
#
#The Programs listed below are licensed under the following terms and
#conditions in addition to those of the IBM International License
#Agreement for Non-Warranted Programs (IBM form number Z125-5589-05).
#
#Program Name: IBM Software Development Kit for Linux on Power v1
#Program Number: SDK
#
#Source Components and Sample Materials
#
#The Program may include some components in source code form ("Source
#Components") and other materials identified as Sample Materials.
#Licensee may copy and modify Source Components and Sample Materials
#for internal use only provided such use is within the limits of the
#license rights under this Agreement, provided however that Licensee
#may not alter or delete any copyright information or notices
#contained in the Source Components or Sample Materials. IBM provides
#the Source Components and Sample Materials without obligation of
#support and "AS IS", WITH NO WARRANTY OF ANY KIND, EITHER EXPRESS OR
#IMPLIED, INCLUDING THE WARRANTY OF TITLE, NON-INFRINGEMENT OR
#NON-INTERFERENCE AND THE IMPLIED WARRANTIES AND CONDITIONS OF
#MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#L/N:  L-WSMA-9PYJJ6
#D/N:  L-WSMA-9PYJJ6
#P/N:  L-WSMA-9PYJJ6
#
#Contributors:
#    Rafael Peria de Sene <rpsene@br.ibm.com> - Initial Implementation

#Creates a zip file which contains the set of files necessary to 
#install and execute the IBM POWER Functional Simulator.

if [ "$1" != "release" ]; then
	echo
else
	#gets the date to be used as part of the .zip name
	VAR=$(date +%m%d%Y%H%M%S | sed 's/\(:[0-9][0-9]\)[0-9]*$/\1/')
fi

#check if the required program exists.
if which zip >/dev/null; then
	#clear old zip files.
	rm -f ./*.zip
	mkdir ./sdk-systemsim
	cp -rf ../packages/ ../README.md ../repos/ ../scripts/ ../setupsimulator ./sdk-systemsim
	#create the .zip file with the structure systemsim_$VAR.zip
	zip -r systemsim$VAR.zip ./sdk-systemsim
	rm -rf ./sdk-systemsim
else
    echo "Could not find zip program. Please install it and try again."
fi
