<?php
// copies the latest data from the ewi to the defaults file

copy("/home/aron/ewi/data/ewidata.txt","/home/aron/ewi/data/defaults.txt");
header("Location:reload.php");

?>
