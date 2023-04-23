<?php
//declare(strict_types=1);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

function get_all_data() {
  $all_data = ["a", "b", "c", "SAdfasdf", "sadf"];
  return $all_data;
}

header("Content-Type: application/json");
echo json_encode(get_all_data());
?>
