import React, { FormEvent } from "react";

function verifyPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); // Prevents the form from submitting by default

    var pw1 = (document.getElementById("password1") as HTMLInputElement).value;
    var pw2 = (document.getElementById("password2") as HTMLInputElement).value;

    // check empty password field
    if (pw1 !== pw2) {
        document.getElementById("message")!.innerHTML = "Пароли различаются!";
        return false;
    }

    // minimum password length validation
    if (pw1.length < 8) {
        document.getElementById("message")!.innerHTML = "Пароль должен содержать не менее 8 символов!";
        return false;
    }

    return true; // Allows form submission when password verification passes
}

export function RegisterPage() {
    return (
        <div>
            <div className="container text-center form-login-reg">
                <h2>Регистрация</h2>
                <form onSubmit={verifyPassword} method="post">
                    <div className="form-group">
                        <label htmlFor="username">Имя пользователя:</label>
                        <input type="text" id="username" name="username" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email:</label>
                        <input type="email" id="email" name="email" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password1">Пароль:</label>
                        <input type="password" id="password1" name="password1" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password2">Подтвердите пароль:</label>
                        <input type="password" id="password2" name="password2" required />
                    </div>
                    <div className="form-group">
                        <span id="message" style={{ color: "red" }}> </span>
                    </div>
                    <div className="form-group">
                        <button type="submit">Зарегистрироваться</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
