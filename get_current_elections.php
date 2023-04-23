<?php
//declare(strict_types=1);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);


function get_all_data() {
	$election1 = array("name" => "Penn", "prompt" => "Going in!", "user" => "abad", "yays" => 10, "nays" => 2);
	$election2 = array("name" => "Nebraska", "prompt" => "Going in 2!", "user" => "abd", "yays" => 5, "nays" => 2);
	$election3 = array("name" => "Yugo", "prompt" => "Going in 3!", "user" => "aba3", "yays" => 3, "nays" => 9);
	$election4 = array("name" => "Tenn", "prompt" => "Going in 4!", "user" => "ab3rd", "yays" => 27, "nays" => 4);

	return [$election1, $election2, $election3, $election4];
}

header("Content-Type: application/json");
echo json_encode(get_all_data());
?>
