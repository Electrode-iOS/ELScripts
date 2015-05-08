#!/bin/bash
set -e

###########################################################
# Usage and other information
# 
# marge_jenkins.sh provides an interface between a Jenkins task
# and marge.py that executes the task.
# 
# Default values are set below. To use this file correct,
# it should be executed on a Jenkins server. It is possible 
# to pass in environmental variables via Jenkins. 
#
#

###########################################################
# Requirements Check

# Check for CLONING_URL, if it isn't set, bomb out
if [ -n "$CLONING_URL" ]; then echo ; else echo "CLONING_URL Missing"; exit 1; fi

# Check for BASE_BRANCH, if it isn't set, bomb out
if [ -n "$BASE_BRANCH" ]; then echo ; else echo "BASE_BRANCH Missing"; exit 1; fi

# Check for OTHER_BRANCHES, if it isn't set, bomb out
if [ -n "$OTHER_BRANCHES" ]; then echo ; else echo "OTHER_BRANCHES Missing"; exit 1; fi

###########################################################
# Initial Build

# Call marge
/usr/local/bin/marge.py "$CLONING_URL" "$BASE_BRANCH" "$OTHER_BRANCHES"
