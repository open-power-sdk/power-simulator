This set of scritps installs and configures the IBM Power Functional Simulator on a x86_64 machine. It can either be used stand alone or within the IBM SDK for Linux on Power. 

 * Install:
    setupsimulator -i
    
 * Remove:
    setupsimulator -u
  
 * Run stand alone:
	cd /home/<USER>/systemsim_execution
	startsimulator [-p8 or -p9]

NOTE:   There is a default location where the files used by the simulator are stored: /home/<USER>/systemsim_execution.
