<?php
require'db_conn.php';

$sql = 'select agent_id, agent_name from Agents';
$result = $conn->query($sql); 

$agents = [];
if ($result->num_rows > 0) { 
    while ($row = $result->fetch_assoc()) {
        $agents[$row['agent_id']] = $row['agent_name'];
    }
} 
$conn->close();

echo json_encode($agents);

?>
