<?php
	// get argument
	$sc_runset_id = $_GET["sc_runset_id"]; // replace it
	$sc_model_id = $_GET["sc_model_id"];
	$sc_reference_id = "usgsgagesstage";   // replace it
	
	// constants
	global $imgs_url, $imgs_folder, $imgs_format, $pois_csv_file_path;
	$imgs_subfolder = "andre/model_3_1/".$sc_runset_id."/repres_displayed/".$sc_model_id."/hydroforecast_".$sc_reference_id."/";
	$imgs_url = "http://s-iihr50.iihr.uiowa.edu/".$imgs_subfolder;
	$imgs_folder = "/local/iihr/".$imgs_subfolder;
	$imgs_format = ".png";
	$pois_csv_file_path = "/local/iihr/demir/test1/modelplus_3_1_git/frontend/viewer_3_1/pois_sensors.csv";
	

	function endsWith($haystack, $needle){
		// auxiliar function for string processing
		return $needle === '' || substr_compare($haystack, $needle, -strlen($needle)) === 0;
	}
	
	function list_files($sc_model_id){
		// list files from folder - function
		//  $sc_model_id:
		$return_file_names = array();
		$all_file_names = scandir($GLOBALS['imgs_folder']);
		foreach($all_file_names as $cur_file_name){
			if (!endsWith($cur_file_name, $GLOBALS['imgs_format'])){ continue; }
			$return_file_names[] = $cur_file_name;
		}
		return($return_file_names);
	}
	
	function file_list_to_js_array($files_list, $sc_model_id){
		// Return array of arrays with format:
		//  [   0   ,    1   ,       2        ,    3     ,     4    ]
		//  [ifis_id, link_id, poi_description, image_url, timestamp]
		
		$ret_array = array();
		foreach($files_list as $cur_file_name){
			// echo("Exploded '".basename($cur_file_name, $GLOBALS['imgs_format'])."' into ".explode("_", basename($cur_file_name, $GLOBALS['imgs_format']))."<br />");
			$splited_filename = explode("_", basename($cur_file_name, $GLOBALS['imgs_format']));
			$cur_img_url = $GLOBALS['imgs_url']."/".$cur_file_name;
			$cur_array = array($splited_filename[1], $splited_filename[1], "'TODO - desc'", "'".$cur_img_url."'", $splited_filename[0]);
			$ret_array[] = "[".implode(",", $cur_array)."]";
		}
		// print_r($ret_array);
		// print_r("[".implode(", ", $ret_array)."]");
		return("[".implode(", ", $ret_array)."]");
	}
	
	function pois_desc_to_js_array(){
		// read CSV file and return a string as JS array
		$ret_array = array();
		$csv_file = fopen($GLOBALS['pois_csv_file_path'], "r");
		fgetcsv($csv_file);  // ignoring header
		while(($cur_csv_line = fgetcsv($csv_file)) !== false){
			$cur_array = array($cur_csv_line[0], $cur_csv_line[1], '"'.$cur_csv_line[2].'"', '"'.$cur_csv_line[3].'"');
			$ret_array[] = "[".implode(", ", $cur_array)."]";
		}
		fclose($csv_file);
		return("[".implode(", ", $ret_array)."]");
	}
	
	// list files from folder - call
	$files_matrix = list_files($sc_model_id);
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
	<title>Hydroforecasts</title>
	
	<script src="http://code.jquery.com/jquery-3.1.0.min.js" 
			integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s=" 
			crossorigin="anonymous">
	</script>
	
	<script type="text/javascript">
		var all_files = <?php echo(file_list_to_js_array($files_matrix, $sc_model_id)); ?>;
		var images_general_url = "<?php echo($imgs_folder); ?>";
		var sc_model_id = "<?php echo($sc_model_id); ?>";
		var all_pois = <?php echo(pois_desc_to_js_array()); ?>;
		var tst = "the test";
		
		function load_csv_line(ifis_id){
			for(var i=0; i<all_pois.length; i++){
				if(all_pois[i][1]==ifis_id){
					return(all_pois[i]);
				}
			}
			return(null);
		}
		
		function fill_table(){
			var cur_ifis_id;
			var cur_img_url;
			var cur_sub_html;
			
			for(var i = 0; i < all_files.length; i++){
				cur_ifis_id = all_files[i][0];
				cur_timestamp = all_files[i][4];
				cur_img_url = all_files[i][3];
				cur_tr_obj = $('<tr ></tr>');
				cur_linkid_str = "Link id:<br />&nbsp;&nbsp;"+cur_ifis_id;
				cur_date = new Date(cur_timestamp * 1000);
				cur_date_str = "Created:<br />&nbsp;&nbsp;";
				cur_date_str = cur_date_str + (cur_date.getMonth()+1) + "/" + cur_date.getDate() + "/" + cur_date.getFullYear();
				cur_th1_obj = $('<th class="ifis_id">'+cur_linkid_str+'<br />'+cur_date_str+'</th>');
				cur_csv_line = load_csv_line(cur_ifis_id);
				if (cur_csv_line == null){
					cur_desc = "No desc";
				} else {
					cur_desc = cur_csv_line[3];
				}
				cur_a_obj = $('<a class="show" id="show_img_'+cur_ifis_id+'" >'+cur_desc+'</a>');
				cur_a_obj.click(function(){
					th_obj = $(this).parent();
					a_obj = th_obj.find('a.hide');
					img_obj = th_obj.find('img');
					if(img_obj.length == 0){
						hid_obj = th_obj.find('input');
						img_obj = $("<img src='"+hid_obj.val()+"' />");
						th_obj.append(img_obj);
					} else {
						img_obj.show();
					}
					a_obj.show();
					// $(this).hide();
				});
				
				cur_a_hide_obj = $('<a id="hide_img_'+cur_ifis_id+'" style="display:none" class="hide">(-)</a>');
				cur_a_hide_obj.click(function(){
					th_obj = $(this).parent();
					a_obj = th_obj.find('a.show');
					img_obj = th_obj.find('img');
					img_obj.hide();
					a_obj.show();
					$(this).hide();
				});
				
				cur_hid_obj = $('<input type="hidden" value="'+cur_img_url+'" />');
				cur_th2_obj = $('<th class="image"></th>');
				cur_th2_obj.append(cur_a_obj);
				cur_th2_obj.append(cur_a_hide_obj);
				cur_th2_obj.append(cur_hid_obj);
				
				// build TH objects
				cur_tr_obj.append(cur_th1_obj);
				cur_tr_obj.append(cur_th2_obj); 
				
				$('#hydroforecast_table > tbody:last-child').append(cur_tr_obj);
			}
		}
		
		function show_all_images(){
			var cur_ifis_id, cur_a_id, cur_img_obj;
			
			for(var i = 0; i < all_files.length; i++){
				cur_ifis_id = all_files[i][0];
				cur_a_id = "#show_img_" + cur_ifis_id;
				cur_img_obj = $(cur_a_id);
				if(cur_img_obj.length != 0){
					cur_img_obj.click();
				}
			}
		}
		
		function hide_all_images(){
			var cur_ifis_id, cur_a_id, cur_img_obj;
			
			for(var i = 0; i < all_files.length; i++){
				cur_ifis_id = all_files[i][0];
				cur_a_id = "#hide_img_" + cur_ifis_id;
				cur_img_obj = $(cur_a_id);
				if(cur_img_obj.length != 0){
					cur_img_obj.click();
				}
			}
		}
	</script>
	
	<style>
	
		body{
			font-family: monospace;
		}
	
		thead tr th{
			background-color: #2222ee;
			color: #ddddff;
		}
	
		thead tr th.ifis_id{
			width: 100px;
		}
		
		thead tr th.image{
			width: 1256px;
		}
		
		tbody tr th.ifis_id{
			background-color: #dfefff;
		}
		
		tbody tr th.ifis_id{
			text-align: left;
		}
		
		tbody tr th.image{
			text-align: left;
		}
		
		tbody tr th img,a{
			display: inline;
		}
		
		a:hover{
			color: #aaaaff;
			text-decoration: underline;
			cursor:pointer;
		}
	</style>
	
	</head>
	
	<body onload="fill_table();">
		<table id="hydroforecast_table">
			<thead>
				<tr>
					<th class="ifis_id">INFO</th>
					<th class="image">Hydroforecast graph</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<th class="ifis_id">&nbsp;</th>
					<th>
						<a id="show_img_all" onclick="show_all_images()" >View all</a>
						&nbsp;/&nbsp;
						<a id="hide_img_all" onclick="hide_all_images()" >Hide all</a>
					</th>
				</tr>
			</tbody>
		</table>
		
		<?php file_list_to_js_array($files_matrix, $sc_model_id); ?>
	</body>
</html>