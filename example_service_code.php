
<?php

 if (get_query_var('ox_token')) {

  print "<BR><BR><HR><h1>Got an access token from our Hello World App</h1>Ready to authenticate against OX AppSuite backend...";


        $client = urlencode("PHP-Redeem-Client-v0.1");
        $uuid = urlencode(md5(uniqid()));
        $secret = urlencode("THE-SECRET-IN-THE-FILE-tokenlogin-secrets");
        $url_encoded_string_params = "token=".$ox_token."&client=".$client."&authId=".$uuid."&secret=".$secret;
        $post = file_get_contents('http://OX_APPSUITE_URL/ajax/login?action=redeemToken',null,stream_context_create(array(
            'http' => array(
                'protocol_version' => 1.1,
                'user_agent'       => 'PHP Redeem Client v0.1',
                'method'           => 'POST',
                'header'           => "Content-type: application/x-www-form-urlencoded\r\n".
                                      "Connection: close\r\n" .
                                      "Content-length: " . strlen($url_encoded_string_params) . "\r\n",
                'content'          => $url_encoded_string_params,
            ),
        )));

        if ($post) {
            echo "<h2>OX AppSuite Middleware Response:</h2>";
            echo $post;
        } else {
            echo "POST failed";
        }


 }

?>
