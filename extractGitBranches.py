#! /usr/bin/env python
import sys
import getopt
import optparse
import commands
import os
import time
import datetime
import subprocess

def getBranches(options):
    gitCmd = 'git branch -r'
    if options.showCmd: print '##command: '+gitCmd
    
    getBranchProc = subprocess.Popen(gitCmd,shell=True,cwd=options.localDest+options.repoRoot+'/',stdout=subprocess.PIPE)
    (branchOut,branchOutErr) = getBranchProc.communicate()
    
    branches = []
    for i, branch in enumerate(branchOut.split('\n')):
        b = branch[ branch.rfind('/')+1: ]
        if len(b) > 0:
            branches.append(b);
    return sorted(set(branches))

def getTags(options):
    cmdGitTags = 'git tag -l'
    if options.showCmd: print '##command: '+cmdGitTags
    getTagsProc = subprocess.Popen(cmdGitTags,shell=True,cwd=options.localDest+options.repoRoot+'/',stdout=subprocess.PIPE)
    (tagOut,tagOutErr) = getTagsProc.communicate()
    
    tags = []
    for i, tag in enumerate(tagOut.split('\n')):
        if len(tag) > 0:
            tags.append(tag);
    return sorted(set(tags))

def go(options):
    print '------------------------------------------------------'
    if not os.path.exists(options.localDest):
        print '--direcotry does not exist'
        sys.exit(1)

    if not os.path.isdir(options.localDest):
        print '--direcotry is not a directory'
        sys.exit(1)

    if len(os.listdir(options.localDest))>0:
        print '--direcotry is not empty. assuming clone already done. fetching updates...'
        cmdPull = 'git fetch'
        if options.showCmd: print '##command: '+cmdPull
        gitPullProc = subprocess.Popen(cmdPull,shell=True,cwd=options.localDest+options.repoRoot+'/',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (cmdOut,cmdErr) = gitPullProc.communicate()
        print cmdOut,cmdErr
    else:
        print '--direcotry is empty. cloning repo...'
        if not options.repoUrl:
            print '--repoUrl must be specified'
            sys.exit(1)
        cmdClone = 'git clone '+options.repoUrl+' '+options.localDest+options.repoRoot+'/'
        if options.showCmd: print '##command: '+cmdClone
        gitCloneProc = subprocess.Popen(cmdClone,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (cmdOut,cmdErr) = gitCloneProc.communicate()
        print cmdOut, cmdErr

    prefixDir = ''
    if options.organize:
        prefixDir = 'branches/'

    branches = getBranches(options)
    for branch in branches:
        print '##starting branch '+branch
        
        prefix = '../'+ prefixDir + branch +'/'
        gitCmd = 'git reset --hard origin/' + branch + ';'
        gitCmd += 'rm -fr '+ prefix + ';'
        gitCmd += 'git checkout-index -f -a --prefix='+ prefix +';'
        if options.showCmd: print '##command: '+ gitCmd
        
        gitCheckoutProc = subprocess.Popen(gitCmd, shell=True, cwd=options.localDest+options.repoRoot+'/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (cmdOut,cmdErr) = gitCheckoutProc.communicate()
        
        print cmdOut,cmdErr
        
    if options.getTags :
        
        prefixDir = ''
        if options.organize: 
            prefixDir = 'tags/'

        tags = getTags(options)
        for tag in tags:
            print '##starting tag '+tag

            prefix = '../'+ prefixDir + tag +'/'
            gitCmd = 'git reset --hard '+ tag +';'
            gitCmd += 'rm -fr '+ prefix + ';'
            gitCmd += 'git checkout-index -f -a --prefix=../'+ prefixDir + tag +'/'
            if options.showCmd: print '##command: '+ gitCmd
            
            gitCheckoutProc = subprocess.Popen(gitCmd, shell=True, cwd=options.localDest+options.repoRoot+'/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (cmdOut,cmdErr) = gitCheckoutProc.communicate()
            
            print cmdOut,cmdErr

    #to avoid the use of json lib (and maintain compatability in python 2.4) hack the json together
    if options.jsonFile:        
        j = '{'        
        jBranches = '","'.join(branches)
        jBranches = '"branches":["'+jBranches+'"]'
        j = j+jBranches        
        
        if options.getTags :
            jTags = '","'.join(tags)
            jTags = '"tags":["'+jTags+'"]'
            j = j+ ','+jTags
            
        j = j+"}"  
        
        f = open(options.jsonFile,'w')
        f.write(j)
            
    print 'done.'
    print '------------------------------------------------------'

def main():
    parser = optparse.OptionParser()
    parser.add_option("--repourl", dest="repoUrl", help="eg 'optional. only required if doing a clone (running the command for first time). git@github.com:someuser/ninja.git'.")
    parser.add_option("--directory", dest="localDest", help="local path where you want all branches saved. must have trailing slash.")    
    parser.add_option("--workingdir", dest="repoRoot", help="optional. this will be the actual git clone located within --directory. All branches are copied from here.", default="reporoot")
    parser.add_option("--showcmds", dest="showCmd", action="store_true", help="optional. used for debugging. will print every command while executing.")
    parser.add_option("--tags", dest="getTags", action="store_true", help="optional. get tags as well as branches.")
    parser.add_option("--branchJsonFile", dest="jsonFile", help="optional. If specified, a file containing all branches in json format.")
    parser.add_option("--organize", dest="organize", action="store_true", help="optional. Put branches and tags in sub-directory. May be required if branch and tag names collide.")
    (options,args) = parser.parse_args(sys.argv[1:])
    go(options)

if __name__ == "__main__":
    main()
