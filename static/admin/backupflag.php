<?php
session_start();
if(!(isset($_SESSION['adminlogged']) && isset($_SESSION['adminname']))){
	header("Location:../index.php");
}
include '../connect.php';
$query = "SELECT team_user_id FROM freepl_teams";
$result = mysql_query($query);
if(!$result){
	die("Unable to query");
}
else{
	while($temp = mysql_fetch_assoc($result)){
		$teamid = $temp['team_user_id'];
		$query2 = "UPDATE user_team_$teamid SET user_flag1 = user_flag";
		$result2 = mysql_query($query2);
		if(!$result2){
			die("unable to update flags");
		}
		else{
			echo "<br/>flags updated for team with id: $teamid<br/>";
		}
	}
}