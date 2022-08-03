<?php
  $username = $_PUT['username'];
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
    <p>You forgot password.</p>
    <p>User Name is <?php echo $username ?>.</p>
  </body>
</html>