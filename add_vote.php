<?php
//declare(strict_types=1);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

function get_all_data() {
	$node_root = $_GET["node_name"];
	$location = $node_root."/add_vote?";
	$args = array("name" => $_GET["name"], "username" => $_GET["username"], "vote" => $_GET["vote"], "signature" => $_GET["signature"]);
	$url_query = $location . http_build_query($args);
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_URL, $url_query);
	$result = curl_exec($ch);

	return json_decode($result);
}

header("Content-Type: application/json");
echo json_encode(get_all_data());
?>
