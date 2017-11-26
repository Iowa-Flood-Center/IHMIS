<?
include_once("../common/class_FoldersDefs.php");

/*
* get_file.php
*
* Script for validating a request through a secret token, passing a file
* to the user, and ensuring the token can not be used again.
*
*/

/* Retrive the given token: */
$token = $_GET['q'];
$timestamp = $_GET['timestamp'];

if(strlen($token)<32)
    die("Invalid token!");

/* Define the secret file: */
$secretfile = FoldersDefs::TEMP_FOLDERPATH.$timestamp.".tar.gz"; //timestamp.tar.gz

/* This variable is used to determine if the token is valid or not: */
$valid = 0;


/* Define what file holds the ids. */
$file = FoldersDefs::TEMP_FOLDERPATH."md5s.txt";

/* Read the whole token-file into the variable $lines: */
$lines = file($file);

/* Truncate the token-file, and open it for writing: */
if( !($fd = fopen(FoldersDefs::TEMP_FOLDERPATH."md5s.txt","w")) )
        die("Could not open $file for writing!");

/* Aquire exclusive lock on $file. */
if( !(flock($fd,LOCK_EX)) )
        die("Could not equire exclusive lock on $file!");

/* Loop through all tokens in the token-file: */
//for( $i = 0; $lines[$i]; $i++ )
//	for ($i=0;i<(count($lines)-1); $i++)
//{
        /* Is the current token the same as the one defined in $token? */
        if( $token == rtrim($lines[0]) )
        {
                $valid = 1;
        }
        /* The code below will only get executed if $token does NOT match the
           current token in the token file. The result of this will be that
           a valid token will not be written to the token file, and will
           therefore only be valid once. */
        else
        {
                fwrite($fd,$lines[0]);
        }
//}

/* We're done writing to $file, so it's safe release the lock. */
if( !(flock($fd,LOCK_UN)) )
        die("Could not release lock on $file!");

/* Save and close the token file: */
if( !(fclose($fd)) )
        die("Could not close file pointer for $file!");

/* If there was a valid token in $token, output the secret file: */
if( $valid )
{
        readfile($secretfile);
}
else
{
        print "Invalid URL!";
}

?>
