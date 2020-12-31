# Tools_and_Toys
Random scripts used for systems tasks and software builds.

## git_creation
Can be used to create a local git server repo which can be pulled and pushed to.
*for now* the base_hooks directory will need to be accessable to the creation script,
however this can be written directly into the script itself which would allow
it to work as a self contained entity. **TODO.**

a usage example is:

  ./git_creator.py \<username\> \<repo-dir\> \<deploy-dir\> \<repo-name\> \<deploy-name\> \<build script\>
  
  ./git_creator.py username software deployment example example_deploy run.sh
  
  In the above example this will create a repository for username in the directory software named example.
  It will also create a deployment dir named example_deploy in directory deployment.
  
  The final paramenter <build script> is optional this would allow the ability to include a script of the same
  name to be run every time the server repository is pushed too. This script could contain build commands and/or
  other included tests to run.


## Relay-Beacon
This can be used to run a predefined script on a machine or VM remotely. A practicle example for its use is when creating new VM's, this script can be included in the image to automate tasks or create beacons/heartbeats if combined with crontab depending on which machine the client or server scripts are run.

To use this, pyotp must be installed: pip3 install pyotp
Also you may need to adjust the python3 interpreter location to fit your machine.

The two main components for this program are client and server scripts.

The server script runs with the form:  
./server  \<port\>  \<script\>

Multiple instances of this script can be run on different ports with different scripts, the scripts can also run other scipts and programs. The first argument to the script being the ip address of the machine that tried to run it; this can be used to also have machines announce their presence to other machines. What ever you can think to do with it really.

There is an example script in the directory to test the configuration.

The client script runs with the form:  
./client \<ip_addr\> \<port\>
  
This is the script that connects to the machines running the server script.

Note that the two scripts interact with eachother by each generating a one time password. Beacause of this it is important that each of the machines involed have their times properly syncronized. Also the key to generate these passwords must be the same on the two points.

At this time there is no network encryption. Until that is added the network conditions should be considered.
