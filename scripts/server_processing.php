<?php
 
/*
 * DataTables example server-side processing script.
 *
 * Please note that this script is intentionally extremely simple to show how
 * server-side processing can be implemented, and probably shouldn't be used as
 * the basis for a large complex system. It is suitable for simple use cases as
 * for learning.
 *
 * See https://datatables.net/usage/server-side for full details on the server-
 * side processing requirements of DataTables.
 *
 * @license MIT - https://datatables.net/license_mit
 */
 
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Easy set variables
 */
 
// DB table to use
$table = 'ticket_details';

ini_set("display_errors",1);
error_reporting(E_ALL);
 
// Table's primary key
$primaryKey = 'ticket_id';
 
// Array of database columns which should be read and sent back to DataTables.
// The `db` parameter represents the column name in the database, while the `dt`
// parameter represents the DataTables column identifier. In this case simple
// indexes
$columns = array(
    array( 'db' => 'ticket_id', 'dt' => 0 ),
    array( 'db' => 'category',  'dt' => 1 ),
    array( 'db' => 'problem_description',   'dt' => 2 ),
    array( 'db' => 'Language',     'dt' => 3 ),
    array( 'db' => 'severity',     'dt' => 4 ),
    array( 'db' => 'agent_name',     'dt' => 5 ),
    array( 'db' => 'solution_comments',     'dt' => 6 ),
    array( 'db' => 'new_category',     'dt' => 7 ),
    array( 'db' => 'ticket_status',     'dt' => 8 ),
    array( 'db' => 'esclation_flag',     'dt' => 9 ),
);
 
require 'db_config.php';
global $sql_details;
 

 
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * If you just want to use the basic configuration for DataTables with PHP
 * server-side, there is no need to edit below this line.
 */
 
require( 'ssp.class.php' );
 
echo json_encode(
    SSP::simple( $_GET, $sql_details, $table, $primaryKey, $columns )
);
 