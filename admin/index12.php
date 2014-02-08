<?php
	session_start();
	if(isset($_SESSION['adminlogged']) && isset($_SESSION['adminname'])){
		?>
			<!DOCTYPE html>
			<html>
				<head></head>
				<body>
					<h1>Select Your action</h1>
					<a href = "getscorecard.php" style = "margin-bottom:100px">Get Scorecard</a><br/>
					<br/><br/><br/><br/><br/><br/>
					<a href = "backupflag.php" style = "margin-top:100px">Backup Teams</a>
					<br/><br/><br/><br/><br/><br/>
					<a href = "updatescores.php" style = "margin-top:100px">Update Teams</a>
				</body>
			</html>
		<?php 
	}
	else{
		?>
		
			<html>
				<head></head>
				<body>
					<form action = "adminlogin.php" method = "POST">
					<label>Username</label>
					<input type = "text" name = "admin_username"/><br/>
					<label>Password</label>
					<input type = "password" name = "admin_password"/><br/>
					<input type = "submit" value = "submit"/>
					</form>
				</body>
			</html>
		<?php 
	}
?>