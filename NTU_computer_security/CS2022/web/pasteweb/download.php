<?php
  session_start();
  if(!isset($_SESSION['name'])){
    header("Location: /");
    die();
  }

	$sandbox = './sandbox/'.md5($_SESSION['name']).'/';
	if (!file_exists($sandbox)){
		mkdir($sandbox);
	}
	chdir($sandbox);

  header("Content-Disposition: attachment; filename=download.tar");
  shell_exec("tar -cvf download.tar *");
  readfile("download.tar");
  shell_exec("rm download.tar");
  die();
?>
