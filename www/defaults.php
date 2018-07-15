<?php
// takes the data from the defaults file, replaces the initial string
// with a loading string and loads the data to the EWI
$F = fopen("/home/aron/ewi/data/defaults.txt","r");
$BANK0 = "F0 47 7F 6D 00 00 06".substr(fgets($F),20);
$BANK2 = "F0 47 7F 6D 02 00 0B".substr(fgets($F),20);
fclose($F);

// fixed default settings below - superseded by user settable ones
//$BANK0 = "F0 47 7F 6D 00 00 06 7F 1A 00 00 06 7F F7";
//$BANK2 = "F0 47 7F 6D 02 00 0B 0A 01 40 7F 0B 2B 00 7C 00 7F 7F F7";

// write the data to the send file
file_put_contents("/home/aron/ewi/data/sendewidata.txt",$BANK0 . $BANK2 . "\n");

// write the data to the ewi
$OUTPUT = exec("/home/aron/ewi/scripts/setewidata.sh");
sleep(4);

header("Location:reload.php");

?>

