/**
 * Example code to authenticate against an Open-Xchange middleware based on
 * http://oxpedia.org/wiki/index.php?title=HTTP_API#Module_.22token.22_.28since_7.4.0.29
 * and request capabilities from the newly created session
 * http://oxpedia.org/wiki/index.php?title=HTTP_API#Module_.22capabilities.22_.28available_with_v7.4.2.29
 */

<?php

  if (isset($_GET['ox_token'])) {

        $ox_token = $_GET['ox_token'];
        print "<h1>Hello World Service</h1>";

        $client = urlencode("PHP-Redeem-Client-v0.1");
        $uuid = urlencode(md5(uniqid()));
        $secret = urlencode("THE-SECRET-IN-THE-FILE-tokenlogin-secrets");
        $url_encoded_string_params = "token=".$ox_token."&client=".$client."&authId=".$uuid."&secret=".$secret;

        $ox_server_domain = "PUT_YOUR_SERVER_DOMAIN_HERE";

        $context = stream_context_create(array(
            'http' => array(
                'protocol_version' => 1.1,
                'user_agent'       => $client,
                'method'           => 'POST',
                'header'           => "Content-type: application/x-www-form-urlencoded\r\n".
                                      "Connection: close\r\n" .
                                      "Content-length: " . strlen($url_encoded_string_params) . "\r\n",
                'content'          => $url_encoded_string_params,
            ),
        ));

        $post = file_get_contents('http://'.$ox_server_domain.'/ajax/login?action=redeemToken',null,$context);
        if ($post) {

                $post = utf8_encode($post);
                $json_obj = json_decode($post, true);

                if (array_key_exists("error", $json_obj)) {
                        // An error occurred, we show the reason as given in the response and within the related attributes
                        print "<h2>Error</h2>".$json_obj['error']."<BR>".$json_obj['error_desc'];
                } else {
                        if (array_key_exists("session", $json_obj)) {
                                $ox_sessionid = $json_obj['session'];
                                print "<h2>Got a session from OX AppSuite middleware</h2>";
                                print "Session ID: ".$ox_sessionid;

                                 // Manually extracting cookies...maybe we should use a function that covers that for us. Feel free to optimize ;)
                                 $cookies = array();
                                 foreach ($http_response_header as $hdr) {
                                    if (preg_match('/^Set-Cookie:\s*([^;]+)/', $hdr, $matches)) {
                                                parse_str($matches[1], $tmp);
                                                $cookies += $tmp;
                                    }
                                 }
                                 // Building cookie string together. This is important for the authentication as we must send all cookies back!
                                 $ox_cookies = "";
                                 $count = 1;
                                 foreach ($cookies as $key => $value) {
                                        $ox_cookie = $key."=".$value;
                                        if ($count == 1) {
                                                $ox_cookies = $ox_cookies . $ox_cookie;
                                        } else {
                                                $ox_cookies = $ox_cookies . "; " . $ox_cookie;
                                        }
                                        $count = $count + 1;
                                 }

                                 // Get request to fetch the capabilities from the middleware
                                 $opts = array(
                                        'http'=>array(
                                        'method'=>"GET",
                                        'header'=>"Accept-language: en\r\n" .
                                                  "User-Agent: " . $client . "\r\n" .
                                                  "Cookie: " . $ox_cookies . "\r\n"
                                        )
                                 );

                                 $url = 'http://'.$ox_server_domain.'/ajax/capabilities?action=all&session='.$ox_sessionid;

                                 $context = stream_context_create($opts);
                                 $capabilities = file_get_contents($url, false, $context);
                                 print "<h2>Got capabilities</h2>";
                                 print $capabilities;
                        } else {
                                print $post;
                        }
                }


        } else {
            echo "POST failed";
        }

 }

?>
