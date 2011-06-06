<?php
$debug = isset( $_REQUEST['debug'] );

function noHotlink($url) {
	if ( !empty($_SERVER['HTTP_REFERER']) && !preg_match('/^https?\:\/\/([^\/]+\.)?jquery(ui)?\.(com|org)\//', $_SERVER['HTTP_REFERER']) 
		&& !preg_match('/^https?\:\/\/(fiddle\.jshell\.net|jsfiddle\.net|jsbin\.com)\/.*/', $_SERVER['HTTP_REFERER']) ) {
		header('Content-type: text/html');
		header('Expires: Sat, 26 Jul 1997 05:00:00 GMT');
		// fiddle.jshell.net
		?>
		<html>
			<head>
			<title>No Direct File Access</title>
			</head>
		<body>
		<p>The file you're trying to access was linked to from a different site, click the link below to view the file. 
		This step is required to prevent hotlinking.
		</p>
		<p>View: <a href="<?php echo $url ?>"><?php echo $url ?></a></p>
		
		<p>Referer: <?php echo $_SERVER['HTTP_REFERER'] ?></p>

		</body>
		</html>
		<?php
		exit;
	}
}

function proxyUrl($url) {
  if ( $debug ) {
    echo "URL: $url\n";
  }
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );
	$response = curl_exec($ch);
	$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	curl_close($ch);
	if ( $statusCode == '404' ) {
		echo "404 occurred: $url\n";
		return false;
	}
	if ( $debug ) {
	  echo "STATUS: $statusCode\n";
	}
	return $response;
}

$url = substr($_SERVER['SCRIPT_URL'], 1);

// Select our repository based upon hostname
$gitUser = 'jquery';
switch ($_SERVER['HTTP_HOST']) {
	case 'local.view.jqueryui.com':
	case 'view.jqueryui.com':
		$rawUrl = 'https://raw.github.com/jquery/jquery-ui/';
		$gitRepository = 'jquery-ui';
		break;

	case 'view.jquery.com':
	default:
		$rawUrl = 'https://raw.github.com/jquery/jquery/';
		$gitRepository = 'jquery';
		break;
}

/*
header('Content-type: text/plain');
echo 'raw: ' . $rawUrl . "\n";
echo 'url: ' . $url . "\n";
exit;
*/

// Do we have a raw request? (There's a file extension)
if ( preg_match('/\.[a-z0-9]+$/i', $url) ) {
	require_once('mime.php');
	noHotlink($_SERVER['SCRIPT_URL']);
	header ('Content-type: ' . getMimeType($rawUrl . $url) );
	echo proxyUrl($rawUrl . $url);
} else {
	// We have a directory listing
	require_once('git-proxy.php');

	$git = new GitProxy($gitUser, $gitRepository);
	$parts = explode('/', $url);

	// Pull the first empty item off the array
	array_shift($parts);

	if ( $parts[0] == 'branches' ) {
		$branches = $git->listBranches();
		if ( $branches ) {
			echo '<ul>';
			foreach ($branches AS $name => $sha) {
				echo '<li><a href="/' . $sha . '">' . $name . '</a></li>';
			}
			echo '</ul>';
		}
	} else {
		header('Content-type: text/plain');
		$tree = $git->tree( join('/', $parts) );
		echo '<ul>';
		if ( !empty( $tree ) ) {
		  foreach ($tree AS $obj) {
  			echo '<li><a href="' . $parts[0] . '">' . $name . '</a></li>';
  		}
		}
		echo '</ul>';
		print_r( $git->tree( $parts[0] ) );
	}
}
