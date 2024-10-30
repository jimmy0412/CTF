<?php
  session_start();
  if(isset($_GET['id']) && preg_match('/^[a-f0-9]{32}$/i', $_GET['id'])){
    $sandbox = './sandbox/'.$_GET['id'].'/';
    if (!file_exists($sandbox)){
      die("id doesn't exist!");
    }
  } else if(isset($_SESSION['name'])){
    $sandbox = './sandbox/'.md5($_SESSION['name']).'/';
  } 

	if (!file_exists($sandbox)){
    header("Location: /");
    die();
	}

	chdir($sandbox);
  $theme = isset($_GET['theme'])? str_replace('/', '', $_GET['theme']): 'default';
?>
<!DOCTYPE html>
<html>
  <head>
    <title>PasteWeb</title>
    <style>
      <?=file_get_contents($theme.'.css');?> 
    </style>
  </head>
  <body>
    <?=file_get_contents('index.html');?> 
  </body>
</html>