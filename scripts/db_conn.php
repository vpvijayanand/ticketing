<?php
require 'db_config.php';
global $sql_details;
// Create connection
$conn = new mysqli($sql_details['host'], $sql_details['user'], $sql_details['pass'], $sql_details['db'], $sql_details['port']);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>