<!DOCTYPE html>

<?php
	include_once("login_lib.php");

	$url_main = "index.html";
	$url_login = "login.html";
	
	include_once("login_lib.php");
	
	$message = "";
	$url_back = "";

	// basic check
	if(!isset($_GET['user_id'])){
		$message = "Missing 'Login' data.";
		$url_back = $url_login;
	} elseif (!isset($_GET['user_pass'])){
		$message = "Missing 'Password' data.";
		$url_back = $url_login;
	} else {
	
		// get data and start session
		$user_id = $_GET['user_id'];
		$user_pass = $_GET['user_pass'];
		session_start();
		
		// make login
		if (DatabaseDefs::check_access($user_id, $user_pass)){
			$_SESSION['user_role'] = "admin";
			$message = "Logged as <strong>admin</strong> !";
			$message .= "<br />";
			$message .= "Go to <a href='settings.php'>settings page</a>.";
			$url_back = $url_main;
		} else {
			unset($_SESSION['user_role']);
			$message = "Invalid user/password !";
			$url_back = $url_login;
		}
	}
?>

<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=960" />
    <meta charset="UTF-8" />
    <title>IFC MODEL PLUS - IFIS SPECIAL CASE</title>
	<script type="text/javascript" src="jquery-3.1.1.min.js"></script>
	<script type="text/javascript" src="scripts/modelplus.url.js"></script>
	<script type="text/javascript" src="base_lib.js"></script>
	<link rel="stylesheet" href="main.css" media="screen" />
	<link rel="stylesheet" href="login.css" media="screen" />
  </head>
  <body id="central">
    <div id="wrapper">
      <div id="doc">
		<div id="header">
		  <!-- keep empty -->
		</div>
		<div id="main-feature">
		  <div id="subheader" >
			Login
		    <span style="float:right">
		      &nbsp;<a href="login.html" >Back</a>&nbsp;
		    </span>
		  </div>
		  <div id="middle_form" >
		    <div class="simple_line" >
			  <?php echo($message); ?>
			</div>
		  </div>
		</div>
		<div id="footer">
			<!-- keep empty -->
		</div>
	  </div> <!-- doc -->
	</div>   <!-- wrapper -->
  </body>
</html>
