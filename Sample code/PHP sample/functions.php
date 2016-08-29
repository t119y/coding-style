<?php
    /*
    functions for pet social media application

    author: Yuan Tu;
    */

    // Try to connect to the databse; Inputs: servername, username, password, database name.
    $connection = mysqli_connect("127.0.0.1","root","","meetUp");
      // Test if connection succeeded
        if(mysqli_connect_errno()) {
            die("Database connection failed: " . 
                 mysqli_connect_error() . 
                 " (" . mysqli_connect_errno() . ")"
        );
      }


    /*
    ---------------------------------------------------------Functions for sidebar starts here---------------------------------------------------------
    Note: user login is currently separating from main page display
    */

    /*
    Getting the main pet types from the database and display them in a sidebar. 
    Easy for user to search for a specific pet type they want to explore. *Maybe removed later for a better web design purpose.
    */
    function getCats(){

        global $connection;

        $get_cats = "SELECT * FROM pet_categories";

        $run_cats = mysqli_query($connection,$get_cats);
        
        // Test if query runs succeeded
        if ($run_cats) {
            
            die('Invalid query: fail to get data from pet_categories');
        
        }

        // fetching run_cats query, and save data to local variable to row_cats
        while ($row_cats = mysqli_fetch_array($run_cats)){
            
            $cat_id = $row_cats['cat_id'];
            
            $cat_name = $row_cats['cat_name'];

            echo "<li><a href='#'>$cat_name</a></li>";

        }
    }


    /*
    Getting 6 friends who are in active most recently of a user from the database and display them in the sidebar. 
    Easy for users to follow their friends' activities. *Maybe removed later for a better web design purpose.
    
    */
    function getFriends(){

        global $connection;

        $get_friends = "SELECT * FROM friends order by recent_login LIMIT 0,6 ";

        $run_friends = mysqli_query($connection,$get_friends);
        
        // Test if query runs succeeded
        if ($run_friends) {
            
            die('Invalid query: fail to get data from friends');
        }

        // fetching run_friends query, and save data to local variable to row_friends
        while ($row_friends = mysqli_fetch_array($run_friends)){
            
            $friends_name = $row_friends['friends_username'];

            echo "<li><a href='#'>$friends_name</a></li>";

        }
    }


    /*
    ---------------------------------------------------------Functions for the main container starts here---------------------------------------------------------
    Note:   1.how to display comments for a post?  
            2.user login is currently separating from main page display
            3.dynamic display;  
    */

    /*
    Getting most recent 9 posts from a user, and display posts in main container.
    */
    function getMediaPost(){

        global $connection;

        $get_posts = "SELECT * FROM media order by recent_posted LIMIT 0,9";

        $run_posts = mysqli_query($connection,$get_posts);
        
        // Test if query runs succeeded
        if ($run_posts) {
            
            die('Invalid query: fail to get data from media');
        }

        // fetching run_posts query, and save data to local variable to row_posts
        while ($row_posts = mysqli_fetch_array($run_posts)){
            
            $user_name = $row_posts['user_name'];
            $media_image = $row_posts['media_image'];
            $media_title = $row_posts['media_title'];

            echo "

                <img src='.../mediaPost/media_image' width = 180, height = 180' />

                <p><b><a href='details.php; style='float:left'> $media_title </a></b></p>

                <a href='index.php'><button style='float:right'>Comments</button></a>

                ";
        }

    }


    /*
    ---------------------------------------------------------Functions for login starts here---------------------------------------------------------
    *Saved both the salt and the hash in the user's database record. 
    For more information about password hashing: https://crackstation.net/hashing-security.htm#salt
    
    Note: user login is currently separating from main page display

    */

    /*
    Function for password encryption. Encrypted the password use a standard hash function;
    Input: password;
    return: hash value of the input password;
    */
    function password_encrypt($password) {
          $hash_format = "$2y$10$";   // Tells PHP to use Blowfish with a "cost" of 10
          
          $salt_length = 22;     // Blowfish salts should be 22-characters or more
          
          $salt = generate_salt($salt_length);
          
          $format_and_salt = $hash_format . $salt;
          
          $hash = crypt($password, $format_and_salt);
        
        return $hash;
    }
    

    /*
    Helper function for password_encrypt;
    Generating salt by a given length(22). We can randomize the hashes by appending or prepending a random string, called a salt, to the password before hashing
    Input: length(int);
    Return: salt value;
    */
    function generate_salt($length) {
          // Not 100% unique, not 100% random, but good enough for a salt
          // MD5 returns 32 characters
        $unique_random_string = md5(uniqid(mt_rand(), true));
      
        // Valid characters for a salt are [a-zA-Z0-9./]
          $base64_string = base64_encode($unique_random_string);
      
        // But not '+' which is valid in base64 encoding
         $modified_base64_string = str_replace('+', '.', $base64_string);
      
        // Truncate string to the correct length
        $salt = substr($modified_base64_string, 0, $length);
      
        return $salt;
    }
    

    /*
    Check if the input password matches the user's hashed_password in database
    Input: password, hashed_password;
    Return: true - if matches; 
            false - if not.
    */
    function password_check($password, $existing_hash) {
    
        // existing hash contains format and salt at start
         
         $hash = crypt($password, $existing_hash);
          
          if ($hash === $existing_hash) {
       
               return true;
          
          } else {
       
            return false;
          }
    }


    /*
    Find user in database by his/her unique username
    Input: username;
    Return: user - if the usernmae found in database;
            null - if the username is not in database
    */
    function find_user_by_username($username) {
        global $connection;
        
        $safe_username = mysqli_real_escape_string($connection, $username);
        
        $get_user = "SELECT * FROM user_profiles WHERE username = '{$safe_username}' LIMIT 1";
        
        $user_set = mysqli_query($connection, $get_user);
        
        confirm_query($user_set);
        
        if($user = mysqli_fetch_assoc($user_set)) {
        
            return $user;
        
        } else {
        
            return null;
        }
    }


    /*
    Attempt to log current user in
    Input: username, password
    Return: user - if succeeded;
            false - if fail to log in the user
    */
    function attempt_login($username, $password) {
        $user = find_user_by_username($username);
        
        if ($user) {
        
            // found user, now check password, retrieve the user's hashed_password from the database.
            if (password_check($password, $user["hashed_password"])) {
        
                // password matches
                return $user;
        
            } else {
        
                // password does not match
                return false;
            }
        
        } else {
        
            // user not found
            return false;
        }
    }    


    /*
    Helper function for confirm_logged_in function
    */
    function logged_in() {
    
        return isset($_SESSION['user_id']);
    }
    

    /*
    Confirm the user is loggedin and redirect to main page - index.php
    */
    function confirm_logged_in() {
        
        if (!logged_in()) {
        
            redirect_to("index.php");
        }
    }




?>