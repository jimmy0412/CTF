<?php
  session_start();
  if(!isset($_SESSION['name'])){
    header("Location: /");
    die();
  }

	echo 'http://'.$_SERVER['HTTP_HOST'].'/view.php?id='.md5($_SESSION['name']);
?>