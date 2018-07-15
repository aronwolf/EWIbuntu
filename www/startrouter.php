<?php

file_put_contents("/home/aron/ewi/data/status.txt", "RUN");
sleep(4);
header("Location:reload.php");

?>

