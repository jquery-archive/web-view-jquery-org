<?php
$debug = false;

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

function proxyUrl( $url ) {
  if ( $debug ) {
    echo "URL: $url\n";
  }
	$ch = curl_init();
	curl_setopt( $ch, CURLOPT_URL, $url );
	curl_setopt( $ch, CURLOPT_HEADER, 0 );
	curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
	curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, false );
	$response = curl_exec( $ch );
	$statusCode = curl_getinfo( $ch, CURLINFO_HTTP_CODE );
	curl_close( $ch );
	if ( $statusCode == '404' ) {
		echo "404 occurred: $url\n";
		return false;
	}
	if ( $debug ) {
	  echo "STATUS: $statusCode\n";
	}
	return $response;
}

$url = $_REQUEST[ 'q' ]; //use local .htaccess if available
if ( !$url ) {
  $url = $_SERVER[ 'SCRIPT_NAME' ]; // use server config (workaround for now)
} 
$url = preg_replace( '/^\//', '', $url ); // kill the first '/'



// Select our repository based upon hostname
$gitUser = 'jquery';
$gitUrl = "https://raw.github.com/jquery";
$gitRepository = 'jquery';
if ( $_SERVER[ 'HTTP_HOST'] == 'local.view.jqueryui.com' || $_SERVER[ 'HTTP_HOST' ] == 'view.jqueryui.com' ) {
  $gitRepository = 'jquery-ui';
}
// create our starting url depending on desired repo
$rawUrl = $gitUrl . '/' . $gitRepository . '/';


// Do we have a raw request? (There's a file extension and it ain't .php)
if ( !preg_match( '/\.php/', $url ) && preg_match('/\.[a-z0-9]+$/i', $url) ) {
	require_once('mime.php');
	noHotlink($_SERVER['SCRIPT_URL']);
	header ('Content-type: ' . getMimeType($rawUrl . $url) );
	echo proxyUrl($rawUrl . $url);
	// proxyUrl handles showing the file, bail.
	exit;
} 

// Did we ask to create a url from github's?
if ( isset( $_REQUEST[ 'url' ] ) && !empty( $_REQUEST[ 'url' ] ) ) {
  $url = trim( $_REQUEST[ 'url' ] );
  $output = $error = false;
  preg_match( '/github.com\/jquery\/([^\/]+)\/(blob\/)?(.*)$/', $url, $matches );
  if ( !empty( $matches ) && !empty( $matches[3] ) ) {
    if ( $matches[1] === "jquery" ) {
      $output = "http://view.jquery.org/" . $matches[3];
    }
    if ( $matches[1] === "jquery-ui" ) {
      $output = "http://view.jqueryui.com/" . $matches[3];
    }
  }
  if ( $output ) {
    header( 'Location: ' . $output );
  }else {
    $error = "Error creating link.";
  }
}
?>
<!DoctypE html>
<html>
<head>
  <title>jQuery Git Proxy</title>
  <style>
    body {
      font-family: Arial;
    }
    input[type="text"] {
      width:500px;
      border:1px solid #555;
      padding:5px;
      font-size:1.2em;
    }
    input[type="submit"] {
      border:1px solid #555;
      cursor: pointer;
      background: #CCC;
      font-size:1.2em;
      padding:5px;
    }
    #error {
      margin:10px;
      padding:10px;
      font-size:1.2em;
      color:#FF0000;
    }
  </style>
</head>
<body>
  <?php if ( !empty( $error ) ): ?>
    <div id="error">
      <?php echo $error; ?>
    </div>
  <?php endif; ?>
  <form method="POST">
    <h1>Paste in github file-uri to proxy</h1>
    <p>Examples:
      <ul>
        <li>https://github.com/jquery/jquery-ui/blob/master/demos/accordion/index.html</li>
        <li>https://github.com/jquery/jquery/blob/master/src/ajax.js</a>
      </ul>
    <p>
    <input type="text" name="url" size="30" autofocus />
    <input type="submit" name="submit" value="Go" />
  </form>
</body>
</html>
 
