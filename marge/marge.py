#!/usr/bin/env python

# marge.py
# This tool is meant to provide an advance check on merging in features in development.
# It can be used directly or in conjunction with a service such as Jenkins.
# Copyright © 2015 WalmartLabs. All rights reserved.

import os
import sys
import shutil
import subprocess

# Constants

REPO_ORIGIN_PREFIX = 'origin/'

# Utilities

def delete_repo_at_path(path):
    print "Cleaning up"
    print "Deleting the test directory at " + path
    shutil.rmtree(path, True)

def git_command(args):
    command_output = ''
    error = False
    try:
        command_output = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as call_error:
        command_output = call_error.output
        error = True
    return (command_output, error)

def submodule_paths():
    (command_output, error) = git_command(['git', 'submodule'])
    submodules = ''
    if error == False:
        submodules = command_output.split('\n')
    paths = []
    for a_submodule in submodules:
        if a_submodule != '':
            path = a_submodule.split(' ')[2]
            paths.append(path)
    return paths

def check_and_merge_submodules(paths, base_branch, branches):
    start_dir = os.getcwd()
    for a_path in paths:
        os.chdir(start_dir + "/" + a_path)
        print os.getcwd()
        (command_output, error) = git_command(['git', 'checkout', base_branch])
        if error == False:
            print "Checked out branch: " + base_branch
            for a_branch in branches:
                merge_message = "Merging branch " + a_branch
                (command_output, error) = git_command(['git', 'merge', '-m', merge_message, a_branch])
                if error == False:
                    print "Merged branch: " + a_branch
                else:
                    print "There is no branch: " + a_branch
        else:
            # base_branch does not exist. Check to see if other branches exist.
            # if they exist, then this is an error because convention dictates that they shouldn't exist w/o the base_branch
            print "There is no base branch: " + base_branch
            for a_branch in branches:
                (command_output, error) = git_command(['git', 'checkout', a_branch])
                if error == False:
                    print "Checked out branch: " + a_branch + ". This is BAD as it is against naming convention."
                    return 1
                else:
                    print "There is no branch: " + a_branch + ". This is GOOD."
    os.chdir(start_dir)
    return 0

def cleanup_files_and_exit(path, exit_code):
    delete_repo_at_path(path)
    exit(exit_code)

# Main

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "This script requires the following arguments, and at least one branch besides the <base_branch>:"
        print "marge.py <git clone path/URL> <path to clone to> <base_branch> <branch1> <branch2> ..."
        print "All branches are merged serially into the <base_branch>, unless there's a conflict, which aborts the process and prints relevant information to the log."
        print "This tool relies on the convention that the base_branch ought to also exist in submodules that have corresponding branches to <branch1> branch2>, etc."
        exit(0)
    
    cloning_url = sys.argv[1]
    path_to_clone_to = sys.argv[2]
    branches_to_compare = sys.argv[3:]
    
    # Derive the name from the repo name
    local_repo_dir_name = cloning_url.split('/')[1].split('.')[0]
    repo_dir_path = path_to_clone_to + "/marge/"
    
    # Clean up remnants, if any, from a previous run
    if os.path.isdir(local_repo_dir_name):
        delete_repo_at_path(repo_dir_path)
    
    os.makedirs(repo_dir_path)
    os.chdir(repo_dir_path)
    
    base_branch = branches_to_compare[0]
    other_branches = branches_to_compare[1:]
    
    print "Cloning " + cloning_url + " into: " + repo_dir_path
    subprocess.call(['git', 'clone', '--recursive', '--branch', base_branch, cloning_url])
    
    os.chdir(local_repo_dir_name)
    
    # Get the list paths of all submodules
    paths = submodule_paths()
    
    # Walk and merge the submodules following naming convention
    exit_code = check_and_merge_submodules(paths, base_branch, other_branches)

    if exit_code != 0:
        # Clean up and exit
        cleanup_files_and_exit(repo_dir_path, exit_code)

    # Submodule branches merged in fine. Now lets attempt merging branches.
    for branch_name in other_branches:
        full_branch_name = REPO_ORIGIN_PREFIX + branch_name
        merge_message = "Merging branch " + branch_name
        
        (command_output, error) = git_command(['git', 'merge', '-m', merge_message, full_branch_name])
        
        prefix = "[RESULT] "
        if command_output.find('CONFLICT') == -1:
            if command_output.find('not something we can merge') == -1:
                # There was no conflict and no merge issue
                print prefix + "MERGED " + full_branch_name + "."
            else:
                # There was no conflict but this branch cannot be merged
                print prefix + "COULD NOT MERGE " + full_branch_name + "."
                exit_code = 1
                break
        else:
            # There was a conflict
            print prefix + "CONFLICT in merging " + full_branch_name + "."
            print "BEGIN CONFLICT MERGE OUTPUT"
            print command_output
            print "END CONFLICT MERGE OUTPUT"
            exit_code = 1
            break
    
    # Clean up and exit
    cleanup_files_and_exit(repo_dir_path, exit_code)
