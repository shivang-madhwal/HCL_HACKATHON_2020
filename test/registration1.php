<!DOCTYPE html>
<html>
<head>
	<title>Register Form</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="login1.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <style>
        body {
            background-color: #303641;
        }
    </style>
</head>
<body>
	<div>
	<?php
	if (isset($_POST['create'])) {
		echo "User Submitted";

        $name = $_POST['name'];
        $dob = $_POST['dob'];
        $gender = $_POST['gender'];
        $phone = $_POST['phone']
        $username = $_POST['username'];
        $email = $_POST['email'];
        $password = $_POST['password'];

        echo $name " " $dob " " $gender " " $phone " " $username " " $email " " $password;
	?>	
	</div>
<div id="register-box">
        <div id="title" style="color: white;">
            Register
        </div>

        <form action="registration1.php" method="POST">
                    <div class="input" >
                        <div class="input-box" style=" color: #949494;
                        margin: 0;
                        background-color: #373b3d;
                        border: 1px solid #373b3d;
                        padding: 6px 0px;
                        border-radius: 3px;">
                            <i class="material-icons">face</i>
                        </div>
                        <input id="name" placeholder="Full name" type="text" required class="validate" autocomplete="off" >
                    </div>

                    <div class="clearfix"></div>

                    <div class="input">
                        <div class="input-box">
                            <i class="material-icons">calendar_today</i>
                        </div>
                        <input id="dob" placeholder="DD-MM-YYYY" type="date" required class="validate" autocomplete="off">
                    </div>

                    <div class="clearfix"></div>

                     <div class="input" >
                        <div class="input-box" style=" color: #949494;
                        margin: 0;
                        background-color: #373b3d;
                        border: 1px solid #373b3d;
                        padding: 6px 0px;
                        border-radius: 3px;">
                            <i class="material-icons">person</i>
                        </div>
                        <input id="gender" placeholder="Gender(M/F)" type="text" required class="validate" autocomplete="off" >
                    </div>


                    <div class="clearfix"></div>

                    <div class="input">
                        <div class="input-box" style="color: #949494;
                        margin: 0;
                        background-color: #373b3d;
                        border: 1px solid #373b3d;
                        padding: 2px 0px;
                        border-radius: 3px;">
                            <i class="material-icons">phone</i>
                        </div>
                        <input id="phone" placeholder="Mobile No." type="number" required class="validate" autocomplete="off" style="background-color: #373b3d; border: 1px solid #373b3d; color: #949494;">
                    </div>

                    <div class="clearfix"></div>

                    <div class="input">
                        <div class="input-box" style="color: #949494;
                        margin: 0;
                        background-color: #373b3d;
                        border: 1px solid #373b3d;
                        padding: 6px 0px;
                        border-radius: 3px;">
                            <i class="material-icons">account_circle</i>
                        </div>
                        <input id="username" placeholder="Username" type="text" required class="validate" autocomplete="off">
                    </div>

                    <div class="clearfix"></div>

                    <div class="input">
                        <div class="input-box" style="  color: #949494;
                            margin: 0;
                            background-color: #373b3d;
                            border: 1px solid #373b3d;
                            padding: 6px 0px;
                            border-radius: 3px;">
                            <i class="material-icons">email</i>
                        </div>
                        <input id="email" placeholder="E-mail" type="email" required class="validate" autocomplete="off">
                    </div>

                    <div class="clearfix"></div>

                    <div class="input">
                        <div class="input-box" style=" color: #949494;
                        margin: 0;
                        background-color: #373b3d;
                        border: 1px solid #373b3d;
                        padding: 6px 0px;
                        border-radius: 3px;">
                            <i class="material-icons">vpn_key</i>
                        </div>
                        <input id="password" placeholder="Password" type="password" required class="validate" autocomplete="off" style=" color: #949494; margin: 0; background-color: #373b3d; border: 1px solid #373b3d; padding: 6px 0px; border-radius: 3px;">
                    </div>

                    <div class="remember-me">
                        <input type="checkbox" >
                        <span style="color: #DDD">I accept Terms of Service</span>
                    </div>

                    <input type="submit" name="create" value="Register" />
                </form>

                <div class="register" style="color: white;">
                    Already have an account?
                    <a href="login.html" target="_self"><button id="register-link">Log In here</button></a>
                </div>  
    </div>
</body>
</html>