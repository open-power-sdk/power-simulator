LICENSE INFORMATION

The Programs listed below are licensed under the following terms and conditions in addition to those of the IBM International License Agreement for Non-Warranted Programs (IBM form number Z125-5589-05).
Program Name: IBM POWER8 Functional Simulator version 1.0-2
Program Number: tool

Non-Production Limitation
If the Program is designated as "Non-Production", the Program can only be deployed as part of the Licensee's internal development and test environment for internal non-production activities, including but not limited to testing, performance tuning, fault diagnosis, internal benchmarking, staging, quality assurance activity and/or developing internally used additions or extensions to the Program using published application programming interfaces. Licensee is not authorized to use any part of the Program for any other purposes without acquiring the appropriate production entitlements.

Development Tool
This Program is designed to aid in the development of software applications and systems. Licensee is solely responsible for the applications and systems that it develops by using this Program and assumes all risk and responsibility therefor.

Source Components and Sample Materials
The Program may include some components in source code form ("Source Components") and other materials identified as Sample Materials. Licensee may copy and modify Source Components and Sample Materials for internal use only provided such use is within the limits of the license rights under this Agreement, provided however that Licensee may not alter or delete any copyright information or notices contained in the Source Components or Sample Materials. IBM provides the Source Components and Sample Materials without obligation of support and "AS IS", WITH NO WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING THE WARRANTY OF TITLE, NON-INFRINGEMENT OR NON-INTERFERENCE AND THE IMPLIED WARRANTIES AND CONDITIONS OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

Third Party Data and Services
The Program may contain links to or be used to access third party data services, databases, web services, software, or other third party content (all, "content"). Access to this content is provided "AS-IS", WITH NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING THE WARRANTY OF TITLE, NON-INFRINGEMENT OR NON-INTERFERENCE AND THE IMPLIED WARRANTIES AND CONDITIONS OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. Access can be terminated by the relevant third parties at their sole discretion at any time. Licensee may be required to enter into separate agreements with the third parties for the access to or use of such content. IBM is not a party to any such separate agreements and as an express condition of this license Licensee agrees to comply with the terms of such separate agreements.

L/N: L-LJLT-9Q4D8R
D/N: L-LJLT-9Q4D8R
P/N: L-LJLT-9Q4D8R

Contributors: 
	Rafael Peria de Sene <rpsene@br.ibm.com> - Initial Implementation

This set of scritps installs and configures the IBM Power Functional Simulator on a x86_64 machine. It can either be used stand alone or within the IBM SDK for Linux on Power. 

The files available are:
	.
	├── LICENSE
	├── packages
	│   ├── license (FTP URL and the list of licenses)
	│   └── simulator (FTP URL and the list of packages used by the setup)
	├── README.md
	├── repos
	│   └── configurerepos.sh (this script is copied into the disc image and allows users to configure repositories)
	├── scripts
	│   └── startsimulator (script which starts the simulator)
	└── setupsimulator (the main script which installs the simulator)
	
	All this files are located under sdk_systemsim.

	NOTE:   There is a default location where the files used by the simulator are stored: /home/<USER>/systemsim_execution.

 * Install:
    setupsimulator -i
    
 * Remove:
    setupsimulator -u
  
 * Run stand alone:
	cd /home/<USER>/systemsim_execution
	startsimulator [-p8 or -p9]
