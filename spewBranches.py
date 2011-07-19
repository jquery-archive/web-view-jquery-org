#! /usr/bin/env python
import sys
import getopt
import optparse
import commands
import os
import time
import datetime
import subprocess

print '------------------------------------------------------'

def getBranches(options):
	cmdGitBranch = 'git branch -r'
	getBranchProc = subprocess.Popen(cmdGitBranch,shell=True,cwd=options.localDest+'/reporoot/',stdout=subprocess.PIPE)
	(branchOut,branchOutErr) = getBranchProc.communicate()
	branches = branchOut.split('\n')	
	
	for i, branch in enumerate(branches):
		branches[i] = branch[ branch.rfind('/')+1: ]

	return branches


def go(options):
	
	if not os.path.exists(options.localDest):
		print '--localDest does not exist'
		sys.exit(1)

	if not os.path.isdir(options.localDest):
		print '--localDest is not a directory'
		sys.exit(1)

	if not os.path.isdir(options.localDest):
		print '--localDest is not a directory'

	if len(os.listdir(options.localDest))>0:
		print '--localDest is not empty. assuming clone already done. pulling updates...'
		cmdPull = 'git pull'

		gitPullProc = subprocess.Popen(cmdPull,shell=True,cwd=options.localDest+'/reporoot/',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(cmdOut,cmdErr) = gitPullProc.communicate()
		print cmdOut,cmdErr

	else:
		print '--localDest is empty. cloning repo...'
		cmdClone = 'git clone git@'+options.repoUrl+':'+options.username+'/jquery-ui.git ./reporoot'
		gitCloneProc = subprocess.Popen(cmdClone,shell=True,cwd=options.localDest,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(cmdOut,cmdErr) = gitCloneProc.communicate()
		print cmdOut

	branches = getBranches(options)
	
	print '#checking out branches to seperate directories... '
	for branch in branches:
		if len(branch)<1:
			continue
		
		print '##starting branch '+branch
		
		#CHECKOUT COMMAND change the branch
		gitCheckoutCmd = 'git checkout '+branch+';'
		if options.showCmd: print '##command:\n'+gitCheckoutCmd+'\n'
		gitCheckoutProc = subprocess.Popen(gitCheckoutCmd, shell=True, cwd=options.localDest+'/reporoot/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(cmdOut,cmdErr) = gitCheckoutProc.communicate()		
		print cmdOut,cmdErr
		
		#CHECKOUT-INDEX COMMAND copy over to directory
		gitCheckoutIndexCmd = 'git checkout-index -f -a --prefix=../'+branch+'/'
		if options.showCmd: print '##command:\n'+gitCheckoutIndexCmd+'\n'			
		gitCheckoutProc = subprocess.Popen(gitCheckoutIndexCmd, shell=True, cwd=options.localDest+'/reporoot/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(cmdOut,cmdErr) = gitCheckoutProc.communicate()			
		print cmdOut,cmdErr
			
	if False:
		for root,dirs,files in os.walk(options.localDest,topdown=True):
			for dir in dirs:
				print root+dir
			for file in files:
				print root+'/'+file
				

def main():
		parser = optparse.OptionParser()
		
		parser.add_option("--localdest", dest="localDest", help="path where you want all branches saved")
		parser.add_option("--username", dest="username",help="optional. only required if --repourl present")
		parser.add_option("--repourl", dest="repoUrl", help="optional. only required if doing a clone (running the command for first time)")
		parser.add_option("--maindir", dest="repoRoot", help="optional. the directory name for the clone. all branches will be copied from here. default reporoot", default="reporoot")
		parser.add_option("--showcmds", dest="showCmd", help="optional. used for debuggin. will print every command while executing")
		(options,args) = parser.parse_args(sys.argv[1:])
		
		go(options)
		
if __name__ == "__main__":
		main()


