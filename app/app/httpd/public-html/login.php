<?php
  $username = $_POST['username'];
  $password = $_POST['password'];
?>

<!doctype html>
<html lang="ko">
  <head>
  <meta charset="utf-8">
    <title>HTML</title>
    <style>
      * {
        font-size: 16px;
        font-family: Consolas, sans-serif;
      }
    </style>
  </head>
  <body>
    <p>User Name is <?php echo $username ?>.</p>
    <p>Password is <?php echo $password ?>.</p>
  </body>
</html>