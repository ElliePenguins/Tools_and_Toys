#!/usr/bin/python3
# check if repo already exists
# and create a new repo if it does not.

# TODO: dependency management.
# TODO: create initialization (create/import base hooks.)
# TODO: report back repo information.
# TODO: allow some way to stop the buildcmd.
#       think like, in post-recieve if script.sh is modified
#       don't run it that push? or some means to inject a
#       different build script.
# TODO: find a way to keep cd $1 out of the build script.

import os;
import sys;
import subprocess

class ServerManager:

    username = "" 
    newRepo = ""
    deployment = ""
    hookStrings = ""
    hooks = "base_hooks"
    # use this to trigger a script in the repo
    # that can be used to build or run software.
    buildCmds = ""

    # low priority, for future builds.
    repoDir = ""
    deployDir = ""

    ok = False;

    def __init__(self, username, repoDir, deployDir,
            repoName, deployment, buildCmds=""):
        ok = True;
        if len(username) > 0:
            self.username = username;
        else:
            ok = False;
        if len(repoName) > 0:
            self.newRepo = repoName;
        else:
            ok = False;
        if len(deployment) > 0:
            self.deployment = deployment;
        else:
            ok = False;

        if len(repoDir) > 0:
            self.repoDir = repoDir;
        else:
            ok = False;

        if len(deployDir) > 0:
            self.deployDir = deployDir;
        else:
            ok = False;

        # build cmds can be empty
        self.buildCmds = buildCmds
        

        if ok == False:
            exit();

        #this could be moved into a higher level
        #class, as it is just init stuff.
        self.createRepositoryDIR(self.repoDir)
        self.createDeploymentDIR(self.deployDir)
        self.createHooksDIR(self.hooks)

        self.createDeployment();
        self.createRepository();

        self.createHooks();

        self.ok = ok;

    # does the repo already exist.
    def checkRepository(self):
        return not os.path.isdir(self.repoDir +
                "/" + self.newRepo);

    # is the deployment directory valid.
    def checkDeployment(self):
        return not os.path.isdir(self.deployDir +
                "/" + self.deployment);

    def createRepository(self):
        if self.checkRepository():
            # gitpython is too much overhead
            # for just creating repos.
            subprocess.call("git init --bare " + self.repoDir + "/"
                    + self.newRepo,
                    shell=True);

    def createDeployment(self):
        if self.checkDeployment():
            # gitpython is too much overhead
            # for just creating repos.
            subprocess.call("git init " + self.deployDir + "/" 
                    + self.deployment,
                    shell=True);

    # used in initial run only!
    def createDeploymentDIR(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory);

    def createRepositoryDIR(self, repository):
        if not os.path.isdir(repository):
            os.makedirs(repository);

    def createHooksDIR(self, hooks):
        if not os.path.isdir(hooks):
            os.makedirs(hooks);

    def createHooks(self):  
        interpreter="#!/bin/bash\n\n"
        successMessage = "DEPLOY=\"Successful deployment.\"\n"
        failMessage = "NO_DEPLOY=\"Did not deploy.\"\n"

        # directory of build script, note that the first
        # argument to the script is the deploy directory.
        build="BUILD=" + "\"/home/" + self.username +\
               "/" + self.deployDir + "/" +\
               self.deployment + "/" + self.buildCmds + "\"\n\n"# +\

        deploy="RUN=\"/home/" + self.username + "/" + \
               self.deployDir + "/" + self.deployment + "\"\n"

        run = "CMD=\"--work-tree=/home/" + \
                self.username + "/" +\
              self.deployDir + "/" + self.deployment + \
              " --git-dir=/home/" + self.username + "/" + \
              self.repoDir + "/" + self.newRepo + \
              " checkout -f master\"\n" # other branches later. 

        fptr = open(self.hooks + "/post-receive");
        data = fptr.read();
        fptr.close();

        fptr = open(self.repoDir + "/" + \
                self.newRepo + "/hooks/post-receive", "w");
        fptr.write(interpreter);
        fptr.write(successMessage);
        fptr.write(failMessage);
        fptr.write(run);
        fptr.write(deploy);
        if len(self.buildCmds) > 0:
            fptr.write(build);
        else:
            fptr.write("BUILD=\"no-build\"\n\n")
        fptr.write(data);

        # make it executable.
        subprocess.call("chmod +x " + self.repoDir + "/" +\
                self.newRepo + "/hooks/post-receive",\
                shell=True);

if len(sys.argv) > 6:
    sm = ServerManager(sys.argv[1], # username
                      sys.argv[2],  # repositores directory 
                      sys.argv[3],  # deployments directory 
                      sys.argv[4],  # repository 
                      sys.argv[5],  # deployment
                      sys.argv[6]); # build/run script.

# probbobly can be handled better with overloading or something.
elif len(sys.argv) > 5:
    sm = ServerManager(sys.argv[1], # username
                      sys.argv[2],  # repositores directory 
                      sys.argv[3],  # deployments directory 
                      sys.argv[4],  # repository 
                      sys.argv[5]); # deployment.

else:
    print("\nUsage: ./servermanager <username> <repo-directory>\n" +\
            "<deploy-directory> <repo-name> <deploy-name>\n" +\
            "[build-script-name]\n")

