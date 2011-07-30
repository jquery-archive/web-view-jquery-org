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
        cmdGitBranch = 'git branch -r'
        if options.showCmd: print '##command:\n'+cmdGitBranch
        getBranchProc = subprocess.Popen(cmdGitBranch,shell=True,cwd=options.localDest+options.repoRoot+'/',stdout=subprocess.PIPE)
        (branchOut,branchOutErr) = getBranchProc.communicate()
        branchesOutput = branchOut.split('\n')

        branches = []
        for i, branch in enumerate(branchesOutput):
                b = branch[ branch.rfind('/')+1: ]
                if len(b) > 0:
                        branches.append(b);
        return branches


def go(options):
        print '------------------------------------------------------'
        if not os.path.exists(options.localDest):
                print '--direcotry does not exist'
                sys.exit(1)

        if not os.path.isdir(options.localDest):
                print '--direcotry is not a directory'
                sys.exit(1)

        if not os.path.isdir(options.localDest):
                print '--direcotry is not a directory'

        if len(os.listdir(options.localDest))>0:
                print '--direcotry is not empty. assuming clone already done. pulling updates...'
                cmdPull = 'git pull'
                if options.showCmd: print '##command:\n'+cmdPull
                gitPullProc = subprocess.Popen(cmdPull,shell=True,cwd=options.localDest+options.repoRoot+'/',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (cmdOut,cmdErr) = gitPullProc.communicate()
                print cmdOut,cmdErr

        else:
                print '--direcotry is empty. cloning repo...'
                if not options.repoUrl:
                        print '--repoUrl must be specified'
                        return
                cmdClone = 'git clone '+options.repoUrl+' '+options.localDest+options.repoRoot+'/'
                if options.showCmd: print '##command:\n'+cmdClone
                gitCloneProc = subprocess.Popen(cmdClone,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (cmdOut,cmdErr) = gitCloneProc.communicate()
                print cmdOut, cmdErr

        branches = getBranches(options)

        if(options.jsonFile):
                #to avoid the use of json lib (and maintain compatability in python 2.4) hack the json together
                j = '","'.join(branches)
                f = open(options.jsonFile,'w')
                f.write('["'+j+'"]')

        for branch in branches:
                print '##starting branch '+branch

                #CHECKOUT COMMAND change the branch
                gitCheckoutCmd = 'git checkout ' + branch + ';'
                # pull branch down, and set the HEAD to origin's
                gitCheckoutCmd += 'git pull; git reset --hard origin/' + branch + ';'
                if options.showCmd: print '##command:\n'+gitCheckoutCmd
                gitCheckoutProc = subprocess.Popen(gitCheckoutCmd, shell=True, cwd=options.localDest+options.repoRoot+'/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (cmdOut,cmdErr) = gitCheckoutProc.communicate()
                print cmdOut,cmdErr

                #CHECKOUT-INDEX COMMAND copy over to directory
                gitCheckoutIndexCmd = 'git checkout-index -f -a --prefix=../'+branch+'/'
                if options.showCmd: print '##command:\n'+gitCheckoutIndexCmd+'\n'
                gitCheckoutProc = subprocess.Popen(gitCheckoutIndexCmd, shell=True, cwd=options.localDest+options.repoRoot+'/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (cmdOut,cmdErr) = gitCheckoutProc.communicate()
                print cmdOut,cmdErr

        print 'done.'
        print '------------------------------------------------------'

def main():
        parser = optparse.OptionParser()

        parser.add_option("--directory", dest="localDest", help="local path where you want all branches saved. must have trailing slash.")
        parser.add_option("--repourl", dest="repoUrl", help="eg 'optional. only required if doing a clone (running the command for first time). git@github.com:someuser/ninja.git'.")
        parser.add_option("--workingdir", dest="repoRoot", help="optional. this will be the actual git clone located within --directory. All branches are copied from here.", default="reporoot")
        parser.add_option("--showcmds", dest="showCmd", help="optional. used for debugging. will print every command while executing.")
        parser.add_option("--branchJsonFile", dest="jsonFile", help="optional. If specified, a file containing all branches in json format.")
        (options,args) = parser.parse_args(sys.argv[1:])

        go(options)

if __name__ == "__main__":
        main()
