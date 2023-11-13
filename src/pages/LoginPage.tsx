import React, { FormEvent } from "react";

export function LoginPage() {
    return (
        <div className="container text-center form-login-reg">
            <h2>Вход</h2>
            <form method="post">
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" name="email" required />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль:</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <div className="form-group">
                    <span id="message" style={{ color: "red" }}> </span>
                </div>
                <div className="form-group">
                    <button type="submit">Войти</button>
                </div>
            </form>
        </div>
    );
}
