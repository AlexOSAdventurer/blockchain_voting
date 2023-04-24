<?php
//declare(strict_types=1);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);


/*function get_all_data() {
	$user1 = array("name" => "abad", "public_key" => "asdfasdf");
	$user2 = array("name" => "abd", "public_key" => "adsfasdg");
	$user3 = array("name" => "ab3rd", "public_key" => "dhjkhh");
	$user4 = array("name" => "aba3", "public_key" => "dsgjilgr");
	return [$user1, $user2, $user3, $user4];
}
}*/

function get_all_data() {
	$node_root = $_GET["node_name"];
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_URL, $node_root."/get_users");
	$result = curl_exec($ch);

	return json_decode($result);
}

header("Content-Type: application/json");
echo json_encode(get_all_data());
?>
