<?php

// handles the settings obtained from the index.php web page
$BANK0 = "F0 47 7F 6D 00 00 06";
$BANK0 .= " " . str_pad(dechex($_POST["breathgain"]),2,"0",STR_PAD_LEFT);
$BANK0 .= " " . str_pad(dechex($_POST["bitegain"]),2,"0",STR_PAD_LEFT);
$BANK0 .= " " . str_pad(dechex($_POST["biteacgain"]),2,"0",STR_PAD_LEFT);
$BANK0 .= " " . str_pad(dechex($_POST["pitchbendgain"]),2,"0",STR_PAD_LEFT);
$BANK0 .= " " . str_pad(dechex($_POST["keydelay"]),2,"0",STR_PAD_LEFT);
$BANK0 .= " 7F F7";
$BANK0 = strtoupper($BANK0);

$BANK2 = "F0 47 7F 6D 02 00 0B";
$BANK2 .= " " . str_pad(dechex($_POST["midichannel"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["fingering"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["transpose"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["velocity"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["breathcc1"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["breathcc2"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " 00";
$BANK2 .= " " . str_pad(dechex($_POST["bitecc1"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["bitecc2"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["pitchbendup"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " " . str_pad(dechex($_POST["pitchbenddown"]),2,"0",STR_PAD_LEFT);
$BANK2 .= " F7";
$BANK2 = strtoupper($BANK2);

// write data to the file to send to the EWI
file_put_contents("/home/aron/ewi/data/sendewidata.txt",$BANK0 . "\n" . $BANK2 . "\n");

// write the settings to the EWI
$OUTPUT = exec("/home/aron/ewi/scripts/setewidata.sh 0");

// write the other config settings
file_put_contents("/home/aron/ewi/data/mode.txt", $_POST["mode"]);
file_put_contents("/home/aron/ewi/data/btaddress.txt", $_POST["btaddress"]);
file_put_contents("/home/aron/ewi/data/runsynth.txt", $_POST["runsynth"]);
file_put_contents("/home/aron/ewi/data/synthport.txt", $_POST["synthport"]);
file_put_contents("/home/aron/ewi/data/noteoff.txt", $_POST["noteoff"]);
file_put_contents("/home/aron/ewi/data/buttons.txt", $_POST["buttons"]);
file_put_contents("/home/aron/ewi/data/finetune.txt", $_POST["finetune"]);




header("Location:reload.php");

?>

