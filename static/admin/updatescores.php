<?php
session_start();
if(!(isset($_SESSION['adminlogged']) && isset($_SESSION['adminname']))){
	header("Location:../index.php");
}

include '../day.php';
include '../connect.php';
$query = "SELECT DISTINCT(team_user_id) FROM freepl_teams";
$result = mysql_query($query);
if(!$result){
	die("Unable to query");
}
else{
	while($tempdata = mysql_fetch_assoc($result)){
		$teamid = $tempdata['team_user_id'];
		echo "<br/> Fetching for teamid: $teamid";
		$query2 = "SELECT DISTINCT(user_player_id) FROM user_team_$teamid WHERE user_flag1 = '1'";
		$result2 = mysql_query($query2);
		if(!$result2){
			die("Unable to update");
		}
		if(mysql_num_rows($result2) == 0){
			continue;
		}
		$players = "(";
		while($temp2 = mysql_fetch_assoc($result2)){
			$players.=$temp2['user_player_id'].",";
		}
		$players = substr($players, 0, -1).")";
		echo "<br/>Player ids : $players<br/>";
		$query2 = "SELECT SUM(day$day) AS sum FROM freepl_players WHERE player_id IN $players AND day$day <> -1";
		$result2 = mysql_query($query2);
		if(!$result2){
			die("Unable to get total scores");
		} 
		$tempscore = mysql_fetch_assoc($result2);
		$score = $tempscore['sum'];
		$query2 = "UPDATE freepl_teams SET day$day=$score, team_totalscore = team_totalscore+$score WHERE team_user_id = '$teamid'";
		echo "<br/>$query2<br/>";
		$result2 = mysql_query($query2);
		if(!$result2){
			die("Unable to update");
		}
	}
	
}
?>