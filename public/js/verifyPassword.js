function verifyPassword() {
    var pw1 = document.getElementById("password1").value;
    var pw2 = document.getElementById("password2").value;

    // check empty password field
    if (pw1 !== pw2) {
        document.getElementById("message").innerHTML = "Пароли различаются!";
        return false;
    }

    // minimum password length validation
    if (pw1.length < 8) {
        document.getElementById("message").innerHTML = "Пароль должен содержать не менее 8 символов!";
        return false;
    }

    console.log(123);

    return true; // Added to allow form submission when password verification passes
}