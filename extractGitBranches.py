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
	branches = branchOut.split('\n')	
	
	for i, branch in enumerate(branches):
		branches[i] = branch[ branch.rfind('/')+1: ]

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
		print cmdOut

	branches = getBranches(options)
	
	print '#checking out branches to separate directories... '
	for branch in branches:
		if len(branch)<1:
			continue
		
		print '##starting branch '+branch
		
		#CHECKOUT COMMAND change the branch
		gitCheckoutCmd = 'git checkout -f' + branch + ';'
		# pull branch down, and set the HEAD to origin's 
		gitChekcoutCmd += 'git pull; git reset --hard origin/' + branch + ';'
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
	(options,args) = parser.parse_args(sys.argv[1:])
		
	go(options)
	
if __name__ == "__main__":
	main()

