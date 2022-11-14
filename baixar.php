<?php
if(!empty($_GET["url"]) && isset($_GET["url"]) && !empty($_GET["title"])){
    $url = $_GET["url"];
    $title = $_GET["title"];

    echo "<strong>Download Link: </strong><a download=\"$title.html\" href=\"";
    system("python3 wattscript.py $url $title");
    echo "\">Download</a>";

    echo file_get_contents("$title.html");
}
