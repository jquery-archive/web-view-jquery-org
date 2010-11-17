<?php
error_reporting(PHP_INI_ALL);

require_once('config.php');
require_once('git-proxy.php');

header('Content-type: text/plain');
print_r($_SERVER);

$actions = array('master');
$url = $_SERVER['SCRIPT_URL'];

$git = new GitProxy('jquery', 'jquery-ui');
$parts = explode('/', $url);
array_shift($parts);

//$git->setBranch('master');
$branches = $git->listBranches();
var_dump($branches);

$git->tree($branches->master);

exit;

var_dump( $git->listBranches() );

exit;
$repos = $git->reposShow();
foreach ($repos AS $repo) {
	echo $repo->name . ' (' . $repo->description .')' . "\n";
}


var_dump( $git->reposShow() );

/*
foreach ( $gitRepos AS $k => $git ) {
	if ( strpos($k, $url) !== false ) {
	}
}
*/
/*


$action = array_shift($url);
echo "ACTION: $action";

print_r($url);

switch ( $action ) {
	case 'master':
		
}

*/
