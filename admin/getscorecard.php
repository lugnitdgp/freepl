<?php
session_start();
if(!(isset($_SESSION['adminlogged']) && isset($_SESSION['adminname']))){
	header("Location:../index.php");
}
if(isset($_POST['url'])){
	require('../phpquery/phpQuery.php');
	//echo $url;
	$url = $_POST['url'];
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
		include '../connect.php';
		include '../day.php';
		$doc = phpQuery::newDocumentHTML($data);
		phpQuery::selectDocument($doc);
		$batinnings1 = pq("#inningsBat1 .inningsRow");
		if(count($batinnings1) == 0){
			die("error");
		}
		$players = array();
		$dismissallists = array();
		foreach($batinnings1 as $bat){
			$score = 0;
			$tempplayer = array();
			if(pq($bat)->find(".playerName a")->html() != ""){
			$name =  pq($bat)->find(".playerName a")->html();
			
			//echo $name;
			$dismissal = pq($bat)->find(".battingDismissal")->html();
			//echo $dismissal;
			$runs = intval(pq($bat)->find(".battingRuns")->html());
			$strikerate = floatval(pq($bat)->find(".battingDetails:last")->html());

			$score = floor($runs*$strikerate/100);
			//echo "|$runs|$score";
			if($runs >= 100){
				$score += 15;
			}
			else if($runs >=50){
				$score += 10;
			}
			$players[$name] = $score;
			
			array_push($dismissallists,$dismissal);
			
			//echo "<br/>";
			}
		}
		
		//echo "<br/>";
		$bowlinnings1 = pq("#inningsBowl1 .inningsRow");
		
		foreach($bowlinnings1 as $bowl){
			
			$score = 0;
			$name = pq($bowl)->find(".playerName a")->html();
			$econ = floatval(pq($bowl)->find(".bowlingDetails:eq(4)")->html());
			if($econ<1){
				$econ = 1;
			}
			$wickets = intval(pq($bowl)->find(".bowlingDetails:eq(3)")->html());
			$score = intval(100*$wickets/$econ);
			//echo "$name|$wickets|$econ|$score";
			if($wickets >= 5){
				$score+= 15;
			}
			else if($wickets >=3){
				$score+= 10;
			}
			$players[$name] = $score;
			//echo "<br/>";
		}
		
		$batinnings2 = pq("#inningsBat2 .inningsRow");
		foreach($batinnings2 as $bat){
			$score = 0;
			$tempplayer = array();
			if(pq($bat)->find(".playerName a")->html() != ""){
				$name =  pq($bat)->find(".playerName a")->html();
					
				//echo $name;
				$dismissal = pq($bat)->find(".battingDismissal")->html();
				//echo $dismissal;
				$runs = intval(pq($bat)->find(".battingRuns")->html());
				$strikerate = floatval(pq($bat)->find(".battingDetails:last")->html());
			
				$score = floor($runs*$strikerate/100);
				//echo "|$runs|$score";
				if($runs >= 100){
				$score += 15;
				}
				else if($runs >=50){
				$score += 10;
				}
				if(array_key_exists($name,$players)){
					$players[$name]+=$score;
				}
				else{
					$players[$name] = $score;
				}
				
					
				array_push($dismissallists,$dismissal);
					
				//echo "<br/>";
			}
		}
		//echo "<br/>";
		//echo "<br/>";
		$bowlinnings2 = pq("#inningsBowl2 .inningsRow");
		
		foreach($bowlinnings2 as $bowl){
				
			$score = 0;
			$name = pq($bowl)->find(".playerName a")->html();
			$econ = floatval(pq($bowl)->find(".bowlingDetails:eq(4)")->html());
			if($econ<1){
				$econ = 1;
			}
			$wickets = intval(pq($bowl)->find(".bowlingDetails:eq(3)")->html());
			$score = intval(100*$wickets/$econ);
			//echo "$name|$wickets|$econ|$score";
			if($wickets >= 5){
			$score+= 15;
			}
			else if($wickets >=3){
			$score+= 10;
			}
			if(array_key_exists($name,$players)){
				$players[$name]+=$score;
			}
			else{
				$players[$name] = $score;
			}
			//echo "<br/>";
		}
		foreach(pq(".notesTable:first .notesRow") as $tablerow){
			$tablehead = pq($tablerow)->find("td:first b")->html();
			if($tablehead == "Player of the match"){
				foreach($players as $player=>$score){
					$tablename = pq($tablerow)->find("td:first")->html();
					if(strpos($tablename, $player) !== false){
						$players[$player]+=50;
						echo "MOM".$tablename."<br/>";
					}
				}
			} 
		}
		
		$query = "";
		foreach ($players as $player=>$score){
			echo "$player|$score<br/>";
			$query .= "UPDATE freepl_players SET day$day = '$score',totalscore= totalscore + $score  WHERE player_code_name LIKE '%$player%';";
		}
		echo "<br/><br/><br/><br/>$query";
		$stmt = $pdo->prepare($query);
		$stmt->execute();
		
		
		
	}
}
else{
	?>
		<form method = "POST" action = "">
			<textarea name = "url" rows = "12" cols = "50"></textarea><br/>
			<input type = "submit" value = "submit"/>
		</form>
	<?php 
}

?>