<?php
    if(isset($_GET['sc']) && ($_GET['sc'] == 'open')){

		if ($_SERVER['SERVER_NAME']=='s-iihr50.iihr.uiowa.edu') {
			include_once "/local/iihr/ifis.iowawis.org/sc/inc_config.php";
			if (strpos($_SERVER[REQUEST_URI], "/dst/")){
				// for local distribution
				IFIS_Init(1, 'IFIS MODEL 3.2', 'test1/ihmis/dst/viewer_3_2', 1); 
			} else {
				// for local development
				IFIS_Init(1, 'IFIS MODEL 3.2', 'test1/ihmis/dev/frontend/code/site/viewer_3_2', 1); 
			}
		} else {
			// for release
			include_once "../inc_config.php"; 
			IFIS_Init(1, 'IFIS MODEL 3.2', 'modelplus/viewer_3_2', 1);
		}

	} else {
?>

<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=960" />
    <meta charset="UTF-8" />
    <title>IHMIS - Iowa Hydrologic Model Information System</title>
    
    <script type="text/javascript" src="common/vendor/jquery-3.1.1.min.js"></script>
	<script type="text/javascript" src="common/scripts/modelplus.util.js"></script>
    <script type="text/javascript" src="common/scripts/modelplus.url.js"></script>
    <script type="text/javascript" src="common/scripts/modelplus.api.js"></script>
    <script type="text/javascript" src="index_3_2/base_lib.js"></script>
    <script type="text/javascript" src="modelplus.index.js"></script>
    <script type="text/javascript">
      // update landing image after page is loaded
      window.addEventListener('load', function() {
    	modelplus.index.update_landing_image({
          dom_img_id: null,
          dom_label_id: null,
          sc_runset_id: 'realtime',
		  sc_model_id: 'fc254mrm01da',
          sc_result_id: 'dcufldicupd',
          sc_result_title: null
		});
      });
    </script>

    <link rel="stylesheet" href="index_3_2/main.css" media="screen" />
	
  </head>
  <body id="central">
    <div id="wrapper">
      <div id="doc">
		<div id="header">
		  <!-- keep empty -->
		</div>
	    <div id="main-feature">
		  <div id="launchifis">
            <div class="intro_maps_div" >
			  <img src="index_3_2/imgs/launchviewer_background.png" alt="Background Map of Iowa-USA" class="background" id="intro_map_background" />
			  <img src="index_3_2/imgs/icons/loading.gif" alt="Loading gif" id="intro_map_loading" class="loadingicon" />
			  <img src="" alt="State Map of Iowa-USA" id="intro_map_view" class="frontmap" />
			</div>
			<div id="intro_date_view"></div>
			<br />
			<a href="index.php?sc=open" class="btnmain btnwht">
			  &nbsp;&nbsp;&nbsp;Viewer&nbsp;&nbsp;&nbsp;
			</a>
          </div>
		  <div id="slogan">
		    ModelPlus is a web tool for observing, comparing and evaluating hidrological models outputs for the State of Iowa.<br />
		    It is originally designed for HLM-Asynch (Hillslope-Link Model) results, but can be easily extended to accept results from other models when conversion of outputs into hillslope-scale segmentation is feasible.<br />
		    The main tool is the <strong>Viewer</strong>, in which real-time simulations and forecasts can be observed, as do as results from isolated events runs.<br />
		    To request a new model run, a different interface was provided named <strong>Requester</strong>.
		  </div>
          <div id="banner" style="width:100%; height:200px; display:block" >
			<div style="width:900px; display:block-inline; text-align:left">
				<img src="index_3_2/imgs/img_request.png"  style="width:128px; height:128px; padding-left:60px" />
				<img src="index_3_2/imgs/img_question.png" style="width:128px; height:128px; padding-left:100px" />
				<img src="index_3_2/imgs/img_config.png"   style="width:128px; height:128px; padding-left:90px" />
				<img src="index_3_2/imgs/img_report.png"   style="width:128px; height:128px; padding-left:90px" />
			</div>
			<div style="width:900px; display:block-inline; text-align:left">
				<div class="video" onclick="location.href='index_3_2/requester.html'">
					Requester
				</div>
				<div class="video" onclick="location.href='index_3_2/about.html';">
					About
				</div>
				<div class="video" onclick="location.href='index_3_2/settings.php';">
					Settings
				</div>
				<div class="video" onclick="location.href='index_3_2/report.html'">
					Report
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

<?php
	}
?>

