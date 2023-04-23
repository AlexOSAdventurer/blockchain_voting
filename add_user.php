<?php
//declare(strict_types=1);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

function get_all_data() {
  $all_data = array("username" => $_GET["username"], "public_key" => $_GET["public_key"], "response" => True);
  return $all_data;
}

header("Content-Type: application/json");
echo json_encode(get_all_data());
?>
