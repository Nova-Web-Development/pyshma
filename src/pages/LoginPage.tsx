import React, { FormEvent, useState } from "react";
// import axios from 'axios';

export const LoginPage: React.FC = () => {
    // const sendRequest = (url: string, params: object = {}) => {
    //     axios.get(url)
    // }

    const [formData, setFormData] = useState({
        email: '',
        password: '',
      });
    
      const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };
    
      const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Ваш код обработки формы
        console.log('Отправка данных:', formData);
      };
    
    return (
        <div className="container text-center form-login-reg">
            <h2>Вход</h2>
            <form method="post" onSubmit={handleSubmit}>
                <div className="form-group">
                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль:</label>
                    <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    />
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