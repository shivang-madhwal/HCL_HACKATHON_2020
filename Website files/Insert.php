<?php
$name = $_POST['name'];
$dob = $_POST['dob'];
$gender = $_POST['gender'];
$phone = $_POST['phone']
$username = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];

if (!empty($name) || !empty($dob) || !empty($gender) || !empty($phone) || !empty($username) || !empty($email) || !empty($password)) {
 $host = "localhost";
    $dbusername = "root";
    $dbemail = "";
    $dbname = "Lottery";
    //create connection
    $conn = new mysqli($host, $dbusername, $dbemail, $dbname);
    if (mysqli_connect_error()) {
     die('Connect Error('. mysqli_connect_errno().')'. mysqli_connect_error());
    } else {
     $SELECT = "SELECT username From register Where username = ? Limit 1";
     $INSERT = "INSERT Into register (name, dob, gender, phone, username, email, password) values(?, ?, ?, ?, ?, ?, ?)";
     //Prepare statement
     $stmt = $conn->prepare($SELECT);
     $stmt->bind_param("s", $email);
     $stmt->execute();
     $stmt->bind_result($email);
     $stmt->store_result();
     $rnum = $stmt->num_rows;
     if ($rnum==0) {
      $stmt->close();
      $stmt = $conn->prepare($INSERT);
      $stmt->bind_param("sssisss", $name, $dob, $gender, $phone, $username, $email, $password);
      $stmt->execute();
      echo "New record inserted sucessfully";
     } else {
      echo "Someone already register using this username";
     }
     $stmt->close();
     $conn->close();
    }
} else {
 echo "All field are required";
 die();
}
?>