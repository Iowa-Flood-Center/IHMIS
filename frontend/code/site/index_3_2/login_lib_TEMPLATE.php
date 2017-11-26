<?php
	
	class DatabaseDefs {
		const USER_ID = "YOUR_ID";
		const USER_PASS = "YOUR_PASS";
		
		public static function check_access($user_id, $user_pass){
			if (($user_id == DatabaseDefs::USER_ID)&&($user_pass == DatabaseDefs::USER_PASS)){
				return(true);
			} else {
				return(false);
			}
		}
	}

?>