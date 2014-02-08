<?php
session_start();
if(!(isset($_SESSION['adminlogged']) && isset($_SESSION['adminname']))){
	header("Location:../index.php");
}
	include '../connect.php';
	require('../phpquery/phpQuery.php');
// 	$team = array(1,2,3,5,6,8);
	$team = array(4);
	$len = count($team);
	for($i = 0; $i < $len; $i++){
		$teamid = $team[$i];
		$url = "http://www.espncricinfo.com/india/content/player/country.html?country=$teamid";
		$ch = curl_init();
		$timeout = 20;
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
		$data = curl_exec($ch);
		curl_close($ch);
		if(!$data){
			die("Unable to open url");
		}
		else{
			$doc = phpQuery::newDocumentHTML($data);
			phpQuery::selectDocument($doc);
			$players = pq("#rectPlyr_Playerlistodi .playersTable td a");
			$country = pq(".ciGblSectionHead:eq(0)")->html();
			$countryarray = explode(":", $country);
			$country = $countryarray[1];
			echo $country;
			foreach($players as $player){
				$name = pq($player)->html();
				$playerlink = "http://www.espncricinfo.com".pq($player)->attr("href");
				echo $playerlink."<br/>";
				$ch = curl_init();
				$timeout = 20;
				curl_setopt($ch, CURLOPT_URL, $playerlink);
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
				curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
				$playerdata = curl_exec($ch);
				if(!$playerdata){
					die("unable to open url");
				}
				else{
					$doc1 = phpQuery::newDocumentHTML($playerdata);
					phpQuery::selectDocument($doc1);
					$fullname = pq(".ciPlayernametxt:eq(0)")->text();
					$countryname = pq(".ciPlayernametxt:eq(0) a")->html();
					$fullname = str_replace($countryname,"", $fullname);
					$fullname = str_replace($country,"",$fullname);
					$matches = pq(".engineTable:eq(0)")->find(".data1:eq(1)")->find("td:eq(1)")->html();
					$runs = pq(".engineTable:eq(0)")->find(".data1:eq(1)")->find("td:eq(4)")->html();
					if($runs == "-"){
						$runs = 0;
					}
					$battingavg = pq(".engineTable:eq(0)")->find(".data1:eq(1)")->find("td:eq(6)")->html();
					if($battingavg == "-")
					$battingavg = 0;
					$info = pq(".ciPlayerinformationtxt");
					foreach($info as $information){
						$infotitle = pq($information)->find("b")->html();
						if($infotitle == "Playing role"){
							$role = pq($information)->find("span")->html();
							break;
						}
					}
					
					$catches = pq(".engineTable")->eq(0)->find(".data1")->eq(1)->find("td")->eq(13)->html();
					$wickets = pq(".engineTable")->eq(1)->find(".data1")->eq(1)->find("td")->eq(5)->html();
					$bowlavg = pq(".engineTable")->eq(1)->find(".data1")->eq(1)->find("td")->eq(8)->html();
					
					if($bowlavg == "-"){
						$bowlavg = 0;
					}
					echo "$name|$fullname|$country|$matches|$battingavg|$bowlavg|$catches|$wickets|$runs|$role<br/>";
					$query = "INSERT INTO freepl_players(player_code_name,player_full_name,player_country,player_role,player_bat_avg,player_matches,player_runs,player_wickets,player_bowl_avg,player_catches,player_cost) ".
							"VALUES('$name','$fullname','$country','$role','$battingavg','$matches','$runs','$wickets','$bowlavg','$catches','0')";
					$result = mysql_query($query);
					if(!$result){
						die("Unable to insert into database");
					}
				}
			}
		}
	}
?>