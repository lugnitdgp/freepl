<?php
	session_start();
	if(isset($_POST['admin_username']) && isset($_POST['admin_password'])){
		$username = $_POST['admin_username'];
		$pass = $_POST['admin_password'];
		if($username == "freepladmin123" && $password = "freepl123!@#"){
			$_SESSION['adminlogged'] = true;
			$_SESSION['adminname'] = "Arjun";
			header("Location:index12.php");
		}
		header("Location:index12.php");
	}
?>