<?php
require 'db_conn.php';

if($_POST){
    $ticket_id = $_POST['ticket_id'];
    $solution_comments = $_POST['solution_comments'];
    $new_category = $_POST['new_category'];
    $status = $_POST['status'];

    
    // Prepare the SQL update statement
    $sql = "UPDATE ticket_details SET solution_comments = ?, new_category = ?, ticket_status = ? WHERE ticket_id = ?";
    $stmt = $conn->prepare($sql);

    // Check if the statement was prepared correctly
    if ($stmt === false) {
        die("Prepare failed: " . $conn->error);
    }

    // Bind parameters
    $stmt->bind_param("sssi",$solution_comments, $new_category, $status, $ticket_id); // "ssi" means string, string, integer

    // Execute the statement
    if ($stmt->execute()) {
        echo "1";
    } else {
        echo "Error updating record: " . $stmt->error;
    }

    // Close the statement
    $stmt->close();
}

?>