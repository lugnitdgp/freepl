<?php
	include 'connect.php';
	$query = "SELECT user_email FROM freepl_users WHERE user_verified = 1";
	$result = mysql_query($query);
	if(!$result){
		die("unable to query");
	}
	else{
		while($temp = mysql_fetch_assoc($result)){
			echo "$email<br/>";
			$email = $temp['user_email'];
			$subject = "[FreePL] Score Update";
			$message = "Scores for the South Africa New Zealand match has been updated.\n\n --\nFreePL Team";
			$header = "FROM: FreePL <no-reply@freepl.mkti.in> \r\n".
					'Reply-To: no-reply@freepl.mkti.in' . "\r\n" .
					'X-Mailer: PHP/' . phpversion();
			mail($email, $subject, $message,$header); 
		}
	}
?> 