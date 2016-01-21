# ELScripts
A collection of tools for managing and monitoring the processes of software development.

### marge
- `marge.py` is meant to provide an advance check on merging in features in development. It can be used directly or in conjunction with a service such as Jenkins.
- `marge_jenkins.sh` provides an interface between a Jenkins task and `marge.py` that executes the task.

### renaming
- `xcoderename.sh` is a script to rename Xcode projects. It updates all files and their contents to make for a smoother transition than can be done by Xcode itself.
