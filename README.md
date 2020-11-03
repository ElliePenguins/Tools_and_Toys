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
  name to be run every time the server repository is pushed too.
