<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<style>
input[type='text'] { font-size: 50px; text-align:center; }
input[type='number'] { font-size: 50px; width: 200px; text-align:center; }
input[type='decimal'] { font-size: 50px; text-align:center; }
button[type='button'] { width: 230px; height: 90px; font-size:25px; }
input[type='submit'] { width: 230px; height: 90px; font-size:25px; }
input[type='range'] { width: 400px;  }
input[type='checkbox'] { text-align:left; transform: scale(4);  }
select { font-size: 50px; text-align:center; }
</style>

<style>
/*----- Tabs -----*/
.tabs {
    width:100%;
    display:inline-block;
}

    /*----- Tab Links -----*/
    /* Clearfix */
    .tab-links:after {
        display:block;
        clear:both;
        content:'';
    }

    .tab-links li {
        margin:0px 5px;
        float:left;
        list-style:none;
    }

        .tab-links a {
            padding:9px 15px;
            display:inline-block;
            border-radius:3px 3px 0px 0px;
            background:#7FB5DA;
            font-size:30px;
	    font-family:arial;
            font-weight:600;
            color:#4c4c4c;
            transition:all linear 0.15s;
        }

        .tab-links a:hover {
            background:#a7cce5;
            text-decoration:none;
        }

    li.active a, li.active a:hover {
        background:#fff;
        color:#4c4c4c;
    }

    /*----- Content of Tabs -----*/
    .tab-content {
        padding:15px;
        border-radius:3px;
        box-shadow:-1px 1px 1px rgba(0,0,0,0.15);
        background:#fff;
    }

        .tab {
            display:none;
        }

        .tab.active {
            display:block;
        }
	</style>
<title>
EWI-USB - Configuration
</title>
</head>

<?php

// interrogate the EWI to find out what it is currently set to
$OUTPUT = exec("/home/aron/ewi/scripts/getewidata.sh");

// while we're waiting for the ewi to respond, get the other settings


$F = fopen("/home/aron/ewi/data/status.txt","r");
$STATUS = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/mode.txt","r");
$MODE = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/btaddress.txt","r");
$BTADDRESS = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/synthport.txt","r");
$SYNTHPORT = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/noteoff.txt","r");
$NOTEOFF = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/buttons.txt","r");
$BUTTONS = fgets($F);
fclose($F);

$F = fopen("/home/aron/ewi/data/finetune.txt","r");
$FINETUNE = fgets($F);
fclose($F);



// wait for EWI response file to be created
if ($STATUS == "RUN")
	{
	for ($N = 0; $N < 10; $N++) {
		if (!file_exists("/home/aron/ewi/data/ewidata.txt"))
			{
			sleep(1);
			}
		}

// if the file hasn't appeared yet, there's a problem - raise an alert
	if (!file_exists("/home/aron/ewi/data/ewidata.txt"))
		{
		print "<script language=\"javascript\">";
		print "alert('The EWI did not respond.... Try reloading the page')";
		print "</script>";
		}

// wait a bit more for info to actually arrive in file
	sleep(2);
	$F = fopen("/home/aron/ewi/data/ewidata.txt","r");
	$BANK0 = explode(' ', fgets($F));
	$BANK2 = explode(' ', fgets($F));
	fclose($F);
	}

// configure the formats for the table cells
$FORMATLABEL = "valign=\"middle\" align=\"left\" style=\"font-family:Arial; font-size:40px; height:90px; border-top: none; border-bottom: none; border-left: none; border-right: none; padding-top: 0.1cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm\"";
$FORMATVALUE = "valign=\"middle\" align=\"center\" style=\"font-family:Arial;font-size:40px; height:90px; border-top: none; border-bottom: none; border-left: none; border-right: none; padding-top: 0.1cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm\"";

?>

<body>
<form method="post" action="handler.php">

<!--  Header Table  with control buttons -------------------------------------->
<table width="940px" cellpadding="4" cellspacing="1">
	<tr>
	        <td>
                <button type="button" style="background: pink;" onclick="window.location='poweroffpage.php'">POWER OFF</button>
                </td>

                <td>
		<button type="button"  onclick="window.location='defaults.php'">Load Defaults</button>
                </td>

                <td>
		<button type="button"  onclick="window.location='startrouterpage.php'">START</button>
                </td>

                <td>
		<button type="button"  onclick="window.location='reload.php'">Reload Page</button>
                </td>
	</tr>
	<tr>
                <?php
	                if (exec("pgrep router.py")) {
                        print("<td colspan=\"4\" align=\"center\" style=\"background-color:green;font-family:arial; font-size:40px\">".$VALUE."Router Running");
                        } else {
                        print("<td colspan=\"4\" align=\"center\" style=\"background-color:red;font-family:arial; font-size:40px\">".$VALUE."Router Stopped");
                        }
		?>
                </td>
</tr>
	<tr>
                <td>
                
                </td>

                <td>
                <button type="button"  onclick="window.location='makedefaults.php'">Save as Defaults</button>
                </td>

                <td>
		<button type="button"  onclick="window.location='stoprouterpage.php'">STOP</button>
                </td>

                <td><input type="submit" value="Save to EWI" />
                </td>

	</tr>
</table>
<br><br>

<!-- now start the tabs --------------------------------------------->

<div class="tabs">
    <ul class="tab-links">
        <li class="active"><a href="#Performance">Performance</a></li>
	<li><a href="#Presets">Presets</a></li>
        <li><a href="#Settings">Settings</a></li>
        <li><a href="#Controllers">Controllers</a></li>
        <li><a href="#Router">Router</a></li>
    </ul>

<!-- Performance Tab --------------------------------------------------->

    <div class="tab-content">
        <div id="Performance" class="tab active">
	<table width="900px" cellpadding="4" cellspacing="1">
	<tr>
	<td colspan="4" style="font-family:Arial; font-size:40px;">
	=== Performance Settings ===
	</td>
	</tr>
	<tr>
	        <td>
                <button type="button"  onclick="window.location='loadpreset1.php'">PRESET 1</button>
                </td>

                <td>
				<button type="button"  onclick="window.location='loadpreset2.php'">PRESET 2</button>
                </td>

                <td>
				<button type="button"  onclick="window.location='loadpreset3.php'">PRESET 3</button>
                </td>

                <td>
				<button type="button"  onclick="window.location='loadpreset4.php'">PRESET 4</button>
                </td>
	</tr>
	</table>
	<table width="900px" cellpadding="4" cellspacing="1">
	<col width="35%">

        <tr>
                <td <?php echo $FORMATLABEL?>>Midi Channel</td>
                <td <?php echo $FORMATVALUE?>>
                        <select  name="midichannel">
				<option value="0"  <?php echo ( hexdec($BANK2[7]) == 0 )  ? "selected='selected'" : ""?>>1  Default</option>
				<option value="1"  <?php echo ( hexdec($BANK2[7]) == 1 )  ? "selected='selected'" : ""?>>2</option>
				<option value="2"  <?php echo ( hexdec($BANK2[7]) == 2 )  ? "selected='selected'" : ""?>>3</option>
				<option value="3"  <?php echo ( hexdec($BANK2[7]) == 3 )  ? "selected='selected'" : ""?>>4</option>
				<option value="4"  <?php echo ( hexdec($BANK2[7]) == 4 )  ? "selected='selected'" : ""?>>5</option>
				<option value="5"  <?php echo ( hexdec($BANK2[7]) == 5 )  ? "selected='selected'" : ""?>>6</option>
				<option value="6"  <?php echo ( hexdec($BANK2[7]) == 6 )  ? "selected='selected'" : ""?>>7</option>
				<option value="7"  <?php echo ( hexdec($BANK2[7]) == 7 )  ? "selected='selected'" : ""?>>8</option>
				<option value="8"  <?php echo ( hexdec($BANK2[7]) == 8 )  ? "selected='selected'" : ""?>>9</option>
				<option value="9"  <?php echo ( hexdec($BANK2[7]) == 9 )  ? "selected='selected'" : ""?>>10</option>
				<option value="10" <?php echo ( hexdec($BANK2[7]) == 10 ) ? "selected='selected'" : ""?>>11</option>
				<option value="11" <?php echo ( hexdec($BANK2[7]) == 11 ) ? "selected='selected'" : ""?>>12</option>
				<option value="12" <?php echo ( hexdec($BANK2[7]) == 12 ) ? "selected='selected'" : ""?>>13</option>
				<option value="13" <?php echo ( hexdec($BANK2[7]) == 13 ) ? "selected='selected'" : ""?>>14</option>
				<option value="14" <?php echo ( hexdec($BANK2[7]) == 14 ) ? "selected='selected'" : ""?>>15</option>
				<option value="15" <?php echo ( hexdec($BANK2[7]) == 15 ) ? "selected='selected'" : ""?>>16</option>
				</select>
                </td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Transpose</td>
                <td <?php echo $FORMATVALUE?>>
			<select  name="transpose">
						<option value="76" <?php echo ( hexdec($BANK2[9]) == 76 ) ? "selected='selected'" : ""?>>76 5C</option>
                                                <option value="74" <?php echo ( hexdec($BANK2[9]) == 74 ) ? "selected='selected'" : ""?>>74 Bb</option>
						<option value="67" <?php echo ( hexdec($BANK2[9]) == 67 ) ? "selected='selected'" : ""?>>67 Eb</option>
						<option value="66" <?php echo ( hexdec($BANK2[9]) == 66 ) ? "selected='selected'" : ""?>>66 D</option>
						<option value="65" <?php echo ( hexdec($BANK2[9]) == 65 ) ? "selected='selected'" : ""?>>65 C#</option>
						<option value="64" <?php echo ( hexdec($BANK2[9]) == 64 ) ? "selected='selected'" : ""?>>64 4C - Default</option>
						<option value="63" <?php echo ( hexdec($BANK2[9]) == 63 ) ? "selected='selected'" : ""?>>63 B</option>
						<option value="62" <?php echo ( hexdec($BANK2[9]) == 62 ) ? "selected='selected'" : ""?>>62 Bb</option>
						<option value="61" <?php echo ( hexdec($BANK2[9]) == 61 ) ? "selected='selected'" : ""?>>61 A</option>
						<option value="60" <?php echo ( hexdec($BANK2[9]) == 60 ) ? "selected='selected'" : ""?>>60 Ab</option>
						<option value="59" <?php echo ( hexdec($BANK2[9]) == 59 ) ? "selected='selected'" : ""?>>59 G</option>
						<option value="58" <?php echo ( hexdec($BANK2[9]) == 58 ) ? "selected='selected'" : ""?>>58 F#</option>
						<option value="57" <?php echo ( hexdec($BANK2[9]) == 57 ) ? "selected='selected'" : ""?>>57 F</option>
						<option value="56" <?php echo ( hexdec($BANK2[9]) == 56 ) ? "selected='selected'" : ""?>>56 E</option>
						<option value="55" <?php echo ( hexdec($BANK2[9]) == 55 ) ? "selected='selected'" : ""?>>55 Eb</option>
                                                <option value="54" <?php echo ( hexdec($BANK2[9]) == 54 ) ? "selected='selected'" : ""?>>54 D</option>
                                                <option value="53" <?php echo ( hexdec($BANK2[9]) == 53 ) ? "selected='selected'" : ""?>>53 C#</option>
						<option value="52" <?php echo ( hexdec($BANK2[9]) == 52 ) ? "selected='selected'" : ""?>>52 3C</option>
						<option value="50" <?php echo ( hexdec($BANK2[9]) == 50 ) ? "selected='selected'" : ""?>>50 Bb</option>
						<option value="43" <?php echo ( hexdec($BANK2[9]) == 43 ) ? "selected='selected'" : ""?>>43 Eb</option>
						<option value="40" <?php echo ( hexdec($BANK2[9]) == 40 ) ? "selected='selected'" : ""?>>40 2C</option>
						</select>
                </td>
		
        </tr>
		<tr>
                <td <?php echo $FORMATLABEL?>>Fine Tuning</td>
	
		<td <?php echo $FORMATVALUE?>>
			<select  name="finetune">
						<option value="96" <?php echo ( $FINETUNE == 96 ) ? "selected='selected'" : ""?>>+50 cents</option>
						<option value="90" <?php echo ( $FINETUNE == 90 ) ? "selected='selected'" : ""?>>+40 cents</option>
						<option value="83" <?php echo ( $FINETUNE == 83 ) ? "selected='selected'" : ""?>>+30 cents</option>
						<option value="77" <?php echo ( $FINETUNE == 77 ) ? "selected='selected'" : ""?>>+20 cents</option>
						<option value="70" <?php echo ( $FINETUNE == 70 ) ? "selected='selected'" : ""?>>+10 cents</option>
						<option value="64" <?php echo ( $FINETUNE == 64 ) ? "selected='selected'" : ""?>>0 cents</option>
						<option value="58" <?php echo ( $FINETUNE == 58 ) ? "selected='selected'" : ""?>>-10 cents</option>
						<option value="51" <?php echo ( $FINETUNE == 51 ) ? "selected='selected'" : ""?>>-20 cents</option>
						<option value="45" <?php echo ( $FINETUNE == 45 ) ? "selected='selected'" : ""?>>-30 cents</option>
						<option value="38" <?php echo ( $FINETUNE == 38 ) ? "selected='selected'" : ""?>>-40 cents</option>
						<option value="32" <?php echo ( $FINETUNE == 32 ) ? "selected='selected'" : ""?>>-50 cents</option>
						</select>
		</td>
	</tr>

	</table>



        </div>

<!-- Presets Tab ------------------------------------------------------------>


        <div id="Presets" class="tab">
	<table width="900px" cellpadding="4" cellspacing="1">
	<td colspan="4" style="font-family:Arial; font-size:40px;">
	=== Presets for EWI ===
	</td>
	</tr>
	<tr>
	        <td>
                <button type="button" onclick="window.location='makepreset1.php'">Save current as Preset 1</button>
                </td>
	        <td>
                <button type="button" onclick="window.location='makepreset2.php'">Save current as Preset 2</button>
                </td>
	        <td>
                <button type="button" onclick="window.location='makepreset3.php'">Save current as Preset 3</button>
                </td>
	        <td>
                <button type="button" onclick="window.location='makepreset4.php'">Save current as Preset 4</button>
                </td>
	</tr>




	</table>

        </div>

<!-- Settings Tab ----------------------------------------------------------------------->

        <div id="Settings" class="tab">
	<table width="900px" cellpadding="4" cellspacing="1">
		<col width="35%">
	<tr>
	<td colspan="2" style="font-family:Arial; font-size:40px;">
	=== EWI Settings ===
	</td>
	</tr>
        <tr>
                <td <?php echo $FORMATLABEL?>>Breath Gain</td>
      
	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="breathgain" value="<?php echo hexdec($BANK0[7])?>" min="0" max="127" step="1"
				oninput="breathgaina.value=breathgain.value"	>
			<output name="breathgaina" for="breathgaina"><?php echo hexdec($BANK0[7])?></output>
		</td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Velocity</td>
	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="velocity" value="<?php echo hexdec($BANK2[10])?>" min="0" max="127" step="1"
				oninput="velocitya.value=velocity.value"	>
			<output name="velocitya" for="velocitya"><?php echo hexdec($BANK2[10])?></output>
		</td>


        </tr>
	
       <tr>
                <td <?php echo $FORMATLABEL?>>Bite Gain</td>

	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="bitegain" value="<?php echo hexdec($BANK0[8])?>" min="0" max="127" step="1"
				oninput="bitegaina.value=bitegain.value"	>
			<output name="bitegaina" for="bitegaina"><?php echo hexdec($BANK0[8])?></output>
		</td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Bite AC Gain</td>

	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="biteacgain" value="<?php echo hexdec($BANK0[9])?>" min="0" max="127" step="1"
				oninput="biteacgaina.value=biteacgain.value"	>
			<output name="biteacgaina" for="biteacgaina"><?php echo hexdec($BANK0[9])?></output>
		</td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Pitch Bend Gain</td>

	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="pitchbendgain" value="<?php echo hexdec($BANK0[10])?>" min="0" max="127" step="1"
				oninput="pitchbendgaina.value=pitchbendgain.value"	>
			<output name="pitchbendgaina" for="pitchbendgaina"><?php echo hexdec($BANK0[10])?></output>
		</td>
        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Key Delay</td>

	<td <?php echo $FORMATVALUE?>>
			<input type="range" 
				name="keydelay" value="<?php echo hexdec($BANK0[11])?>" min="0" max="15" step="1"
				oninput="keydelaya.value=keydelay.value"	>
			<output name="keydelaya" for="keydelaya"><?php echo hexdec($BANK0[11])?></output>
		</td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Fingering</td>
                <td <?php echo $FORMATVALUE?>>
                        <select  name="fingering">
                                <option value="0" <?php echo ( hexdec($BANK2[8]) == 0 ) ? "selected='selected'" : ""?>>0 EWI</option>
                                <option value="1" <?php echo ( hexdec($BANK2[8]) == 1 ) ? "selected='selected'" : ""?>>1 Saxophone</option>
                                <option value="2" <?php echo ( hexdec($BANK2[8]) == 2 ) ? "selected='selected'" : ""?>>2 Flute</option>
                                <option value="3" <?php echo ( hexdec($BANK2[8]) == 3 ) ? "selected='selected'" : ""?>>3 Oboe</option>
                                <option value="4" <?php echo ( hexdec($BANK2[8]) == 4 ) ? "selected='selected'" : ""?>>4 EVI normal</option>
                                <option value="5" <?php echo ( hexdec($BANK2[8]) == 5 ) ? "selected='selected'" : ""?>>5 EVI reverse</option>
                                </select>
                </td>
                <td>
                </td>

        </tr>

	</table>


        </div>

<!-- Controllers Tab -------------------------------------------------------->

        <div id="Controllers" class="tab">
	<table width="900px" cellpadding="4" cellspacing="1">
		<col width="45%">
	<tr>
	<td colspan="2" style="font-family:Arial; font-size:40px;">
	=== EWI Controllers ===
	</td>
	</tr>
        <tr>
                <td <?php echo $FORMATLABEL?>>Breath CC1</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="breathcc1" value="<?php echo hexdec($BANK2[11])?>">
                </td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Breath CC2</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="breathcc2" value="<?php echo hexdec($BANK2[12])?>">
                </td>

        </tr>
 	
       <tr>
                <td <?php echo $FORMATLABEL?>>Bite CC1</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="bitecc1" value="<?php echo hexdec($BANK2[14])?>">
                </td>
        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Bite CC2</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="bitecc2" value="<?php echo hexdec($BANK2[15])?>">
                </td>

        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Pitch Bend Up</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="pitchbendup" value="<?php echo hexdec($BANK2[16])?>">
                </td>
        </tr>
	
        <tr>
                <td <?php echo $FORMATLABEL?>>Pitch Bend Down</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="number" size="4"  pattern="[0-9]{3}" min="0" max="127" name="pitchbenddown" value="<?php echo hexdec($BANK2[17])?>">
                </td>

        </tr>
	</table>
        </div>

<!-- Router Tab -------------------------------------------------------------->

        <div id="Router" class="tab">
	<table width="900px" cellpadding="4" cellspacing="1">
		<col width="55%">
	<tr>
	<td colspan="2" style="font-family:Arial; font-size:40px;">
	=== Router Settings ===
	</td>
	</tr>
	<tr>
                <td <?php echo $FORMATLABEL?>>EWI Connection Mode</td>
	
		<td <?php echo $FORMATVALUE?>>
			<select  name="mode">
						<option value="BT" <?php echo ( $MODE == "BT" ) ? "selected='selected'" : ""?>>Bluetooth</option>
						<option value="USB" <?php echo ( $MODE == "USB" ) ? "selected='selected'" : ""?>>USB</option>
						</select>
		</td>
	</tr>
	
	<tr>
                <td <?php echo $FORMATLABEL?>>UD-BT01 Bluetooth Address</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="text" size="14"    name="btaddress" value="<?php echo $BTADDRESS?>">
                </td>
	</tr>
	
	
	<tr>
                <td <?php echo $FORMATLABEL?>>Synth port name (part only)</td>
                <td <?php echo $FORMATVALUE?>>
                        <input type="text" size="8"    name="synthport" value="<?php echo $SYNTHPORT?>">
                </td>
	</tr>
	
 	<tr>
                <td <?php echo $FORMATLABEL?>>Note-off function</td>
	
		<td <?php echo $FORMATVALUE?>>
			<select  name="noteoff">
						<option value="RUN" <?php echo ( $NOTEOFF == "RUN" ) ? "selected='selected'" : ""?>>RUN</option>
						<option value="STOP" <?php echo ( $NOTEOFF == "STOP" ) ? "selected='selected'" : ""?>>STOP</option>
						</select>
		</td>
	</tr>
	 	<tr>
                <td <?php echo $FORMATLABEL?>>GPIO Buttons</td>
	
		<td <?php echo $FORMATVALUE?>>
			<select  name="buttons">
						<option value="RUN" <?php echo ( $BUTTONS == "RUN" ) ? "selected='selected'" : ""?>>RUN</option>
						<option value="STOP" <?php echo ( $BUTTONS == "STOP" ) ? "selected='selected'" : ""?>>STOP</option>
						</select>
		</td>
	</tr>
</table>
	</div>

</div>

<!-- Jquery script for the tabs --------------------------------------->
</form>
<script src="jquery.js"></script>
<script>
jQuery(document).ready(function() {
    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');

        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();

        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

        e.preventDefault();
    });
});
</script>

</body>
</html>
