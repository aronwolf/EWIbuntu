<?php
// sends a dummy command to the router to set a preset

$OUTPUT = exec("/home/aron/ewi/scripts/setewidata.sh 4");
sleep(4);
header("Location:reload.php");

?>

