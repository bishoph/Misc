<?php

/**
 * Simple PHP example script
 * Author: Martin Kauss
 * 2015-03-03
 */

function getData($value) {

   $items = [
        [
        "id" => 1,
        "content" => "This is just a simple JSON response from the server",
        "value" => $value
        ]
   ];

   return $items;

}

if (isset($_GET['name'])) {
 $value = $_GET['name'];
 $items = getData($value);
 if ($items) {
    header('Content-Type: application/json');
    print json_encode($items);
 } else {
     print "<h1>Nothing to send!</h1>";
 }
} else {
    print "<h1>We got no name/value pair!</h1>";
}

?>