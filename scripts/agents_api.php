<?php
require'db_conn.php';

$sql = 'select id, agent_name from Agents';
$result = $conn->query($sql); 

$agents = [];
if ($result->num_rows > 0) { 
    while ($row = $result->fetch_assoc()) {
        $agents[$row['id']] = $row['agent_name'];
    }
} 
$conn->close();

echo json_encode($agents);

?>
