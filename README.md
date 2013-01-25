#web-view-jquery-org
* This is a python script. 
* It will extract all branches and tags for a specific git repo to the local file system.
* You COULD then hook up the file system to a web server with directory-browsing enabled, and use ```--branchJsonFile``` and index.html[1] to serve up your repo (like we do here [1][2])

#CLI options
```
$ ./extractGitBranches.py --help
Usage: extractGitBranches.py [options]

Options:
  -h, --help            show this help message and exit
  --repourl=REPOURL     eg 'optional. only required if doing a clone (running
                        the command for first time).
                        git@github.com:someuser/ninja.git'.
  --directory=LOCALDEST
                        local path where you want all branches saved. must
                        have trailing slash.
  --workingdir=REPOROOT
                        optional. this will be the actual git clone located
                        within --directory. All branches are copied from here.
  --showcmds            optional. used for debugging. will print every command
                        while executing.
  --tags                optional. get tags as well as branches.
  --branchJsonFile=JSONFILE
                        optional. If specified, a file containing all branches
                        in json format.
  --organize            optional. Put branches and tags in sub-directory. May
                        be required if branch and tag names collide.
```

#example usage:
```
$ extractGitBranches.py --tags --directory /var/www/view.jqueryui.com/htdocs/ --repourl git://github.com/jquery/jquery-ui.git --branchJsonFile /var/www/view.jqueryui.com/htdocs/branches.json
```

[1]https://github.com/jquery/web-view-jquery-org/blob/master/htdocs/index.htm

[2]http://view.jqueryui.com/

[3]http://view.jquery.com/
