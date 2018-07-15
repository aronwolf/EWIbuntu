<?php
// This program writes the midi channel info to file 

// The format is required for use in a fluidsynth config file
 
$CHANNELS = array(10, 11, 12, 13, 14, 15);

$F=fopen("/home/aron/ewi/data/channels.txt","w");

fputs($F, "#This file is created automatically  - DO NOT EDIT"."\r\n");

fputs($F, "load ".$_POST["sfont"]."\r\n");

foreach ($CHANNELS as $CH) {
		fputs($F, "#".($CH+1)." ".$_POST["name".$CH]."\r\n");
		if ($_POST["prog".$CH]  == "") {
			fputs($F, "prog ".$CH." "."0"."\r\n");
		} elseif ( intval($_POST["prog".$CH] ) <=0) {
			fputs($F, "prog ".$CH." "."0"."\r\n");		
		} elseif ( intval($_POST["prog".$CH] ) > 127) {
			fputs($F, "prog ".$CH." "."0"."\r\n");		
		} else  {			
			fputs($F, "prog ".$CH." ".$_POST["prog".$CH]."\r\n");
		}
		}

fclose($F);

header("Location:reload.php");

?>

