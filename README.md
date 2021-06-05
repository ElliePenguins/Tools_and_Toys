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
  

This works great for building pipelines on local infra with jenkins.
For example, if the repo exists in the users home dir, use the format:

  ssh://\<username\>@\<ip_address\>/~/\<repository_dir\>/\<repository_name\>
  

---
<br/>

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


---
<br/>

## Wait-Service  
This can be used to make sure that commands are run or services come up in a proper order across multiple machines. For example: a server (physical or virtual) that gets its data from an nfs share on a seperate machine would need to bring its services up after the other machine is booted. 
  
To do this, there is a unit file and script named start.sh
  1. Modify the IP_ADDR variable in the start.sh script to reference the IP of the server you want the machine to wait for.
  2. Replace the echo commands with the commands you wish to run once a ping response has been recieved.
     Like any other script multiple commands can be entered here 
  3. Place the start.sh script where ever is appropriate for your system, as long as it is accessable to the unit file.
  4. Modify the waitstart.service unit file's description= directive as you feel appropriate
  5. Modify the waitstart.service unit file's execstart= directive to point to the absolute location of the start.sh script.
  6. Place the waitstart.service unit file into the appropriate directory for your system. eg. /etc/systemd/system
  7. Run: "systemctl daemon-reload" to make systemd aware of the new unit file
  8. Run: "systemctl enable waitstart.service" to run the script at startup.
  
Note: Currently start.sh pings 256 times and then fails. You can modify this number as appropriate for your machine.
  
