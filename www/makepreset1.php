<?php
// copies the latest data from the ewi to the defaults file

copy("/home/aron/ewi/data/ewidata.txt","/home/aron/ewi/data/preset1.txt");
header("Location:reload.php");

?>

