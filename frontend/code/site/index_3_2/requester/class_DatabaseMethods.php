<?php

	include_once("class_DatabaseDefs.php");

	class DatabaseMethods {
		
		/**
		 * CONSTANTS
		 */
		const DB_PREC_NAME = "precipitation";
		const DB_PREC_FLAG = 1;
		const DB_OUTP_NAME = "model_backtime";
		const DB_OUTP_FLAG = 2;
		const DB_RSRV_NAME = "reservoir_historical";
		const DB_RSRV_FLAG = 3;
		const RSRV_MAX_DIST_SEC = 3000;
		
		/**
		 *
		 * $database_flag : One of DatabaseDefs::DB_...._FLAG values
		 * RETURN : Open connection object
		 */
		public static function open_db_connection($database_flag){
			
			$database_name = DatabaseMethods::get_database_name($database_flag);
			
			$conn_string = "host=".DatabaseDefs::DB_HOST." port=".DatabaseDefs::DB_PORT." ";
			$conn_string .= "dbname=".$database_name." user=".DatabaseDefs::USER_DB." ";
			$conn_string .= "password=".DatabaseDefs::PASS_DB;
			
			$db_conn = pg_connect($conn_string);
			return($db_conn);
		}
		
		/**
		 *
		 * $precipitation_source_id : 
		 * $timestamp_ini : 
		 * $timestamp_end : 
		 * $db_conn : Database connection
		 * RETURN : Boolean. True if entire interval is available, False otherwise
		 */
		public static function is_interval_available($precipitation_source_id, $timestamp_ini, 
													 $timestamp_end, $db_conn){
			
			// estimate expected timestamps present on mapping
			$delta_timestamp = $timestamp_end - $timestamp_ini;
			$expct_count = ($delta_timestamp / (60 * 60)) + 1;
			
			// basic check
			if($expct_count <= 0){
				// echo("NEGT: ".$expct_count);
				return(False); 
			}
			
			// build select query
			$schema_name = DatabaseMethods::get_schema_name($precipitation_source_id);
			switch($precipitation_source_id){
				case "st4":
					$sql_select = "SELECT COUNT(*) AS C FROM ".$schema_name.".map_index WHERE ";
					$sql_select .= " unix_time >= ".$timestamp_ini." AND";
					$sql_select .= " unix_time <= ".$timestamp_end;
					break;
				case "mrms":
					// TODO - implement
					return(False);
				case "ifc":
					// TODO - implement
					return(False);
				default:
					// echo("What: '".$precipitation_source_id."'. ");
					return(False);
			}
			
			// execute query
			$result = pg_query($db_conn, $sql_select);
			if(!$result){
				// echo("Fail: '".$sql_select."'. ");
				return(False);
			}
			
			// compare expected with obtained
			$line = pg_fetch_assoc($result);
			if ($line['c'] == $expct_count) {
				// echo("Equal: ".$line['c']." and ".$expct_count.". ");
				return(true);
			} else {
				// echo("Diff: ".$line['c']." and ".$expct_count.". ");
				return(false);
			}
		}
		
		/**
		 *
		 * $timestamp_ini
		 * $timestamp_end
		 * $db_conn
		 * RETURN : String.
		 */
		public static function get_available_reservoirs($timestamp_ini, 
													    $timestamp_end, 
														$db_conn){
			
			// build select query
			$sql_select =  "WITH time_dist_ini AS (";
			$sql_select .= "  SELECT ";
			$sql_select .= "    MIN(ABS(unix_time - ".$timestamp_ini.")) dist_time_ini, link_id";
			$sql_select .= "  FROM";
			$sql_select .= "    usgs_streamgages.link_discharge";
			$sql_select .= "  GROUP BY";
			$sql_select .= "    link_id";
			$sql_select .= "), time_dist_end AS (";
			$sql_select .= "  SELECT";
			$sql_select .= "    MIN(ABS(unix_time - ".$timestamp_end.")) dist_time_end, link_id";
			$sql_select .= "  FROM";
			$sql_select .= "    usgs_streamgages.link_discharge";
			$sql_select .= "  GROUP BY";
			$sql_select .= "    link_id";
			$sql_select .= ")";
			$sql_select .= "SELECT";
			$sql_select .= "  time_dist_ini.dist_time_ini,";
			$sql_select .= "  time_dist_end.dist_time_end,";
			$sql_select .= "  time_dist_end.link_id ";
			$sql_select .= "FROM ";
			$sql_select .= "  time_dist_ini, time_dist_end ";
			$sql_select .= "WHERE";
			$sql_select .= "  time_dist_ini.link_id = time_dist_end.link_id";
															
			// execute query
			$result = pg_query($db_conn, $sql_select);
			if(!$result){
				// echo("Fail: '".$sql_select."'. ");
				return(False);
			}
			
			// retrieve accepted link ids
			$return_array = array();
			while ($cur_db_line = pg_fetch_array($result)) {
				if (($cur_db_line["dist_time_ini"] < DatabaseMethods::RSRV_MAX_DIST_SEC) && 
						($cur_db_line["dist_time_end"] < DatabaseMethods::RSRV_MAX_DIST_SEC)){
					array_push($return_array, $cur_db_line["link_id"]);
				}
			}
			
			return($return_array);
		}
		
		/**
		 *
		 * $precipitation_source_id :
		 * RETURN : String.
		 */
		private static function get_schema_name($precipitation_source_id){
			switch($precipitation_source_id){
				case "st4":
					return("stage4");
				case "mrms":
					// TODO - return something usefull
				case "ifc":
					// TODO - return something usefull
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $database_flag : One of DatabaseDefs::DB_...._FLAG values
		 * RETURN : String.
		 */
		private static function get_database_name($database_flag){
			switch($database_flag){
				case DatabaseMethods::DB_PREC_FLAG:
					return (DatabaseMethods::DB_PREC_NAME);
				case DatabaseMethods::DB_OUTP_FLAG:
					return (DatabaseMethods::DB_OUTP_NAME);
				case DatabaseMethods::DB_RSRV_FLAG:
					return (DatabaseMethods::DB_RSRV_NAME);
				default:
					return (null);
			}
		}
		
	}
?>