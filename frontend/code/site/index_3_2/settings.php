<!DOCTYPE html>

<?php
	// PHP session for checking if user is logged in
	session_start();
	
	if((!isset($_SESSION['user_role']))||($_SESSION['user_role'] != "admin")){
		header('Location: login.html');
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
	<script type="text/javascript" src="settings.js"></script>
	<link rel="stylesheet" href="main.css" media="screen" />
	<link rel="stylesheet" href="settings.css" media="screen" />
  </head>
  <body id="central">
    <div id="wrapper">
      <div id="doc">
		<div id="header">
			<!-- keep empty -->
		</div>
		<div id="main-feature">
			<div style="width:920px; height:340px display:block; margin:auto; padding-top:10px; position:relative;">
			  <div id="tabs" >
				<div class="tab">
					&nbsp;<a href="javascript:replace_runsets()" >Runsets</a>&nbsp;
				</div>
				<div class="tab">
					&nbsp;<a href="javascript:replace_evaluations()" >Evaluations</a>&nbsp;
				</div>
				<div class="tab_back">
					&nbsp;<a href="../" >Back</a>&nbsp;
				</div>
			  </div> <!-- div:tabs -->
			  <div id="folder_content" >
				<div id="the_content">
					<!-- keep empty -->
				</div>
				<div id="the_info">
					<!-- keep empty -->
				</div>
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
