import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="jumbotron text-center main">
        <h1></h1>
        <p>Сервис корпоративного питания для сотрудников СберБанка</p>
        <a href="#" className="btn btn-primary btn-lg">Личный кабинет</a>
      </div>
      <section className="container py-5">
        <div className="text-center">
          <h2>Помощь</h2>
          <p className="lead">by NovaDev</p>
          <ul className="list-inline">
            <li className="list-inline-item"><a href="https://vk.com/artyomjk">VK</a></li>
            <li className="list-inline-item"><a href="https://github.com/artemgoncarov">Github</a></li>
            <li className="list-inline-item"><a href="https://t.me/artyomjk">Telegram</a></li>
          </ul>
        </div>
      </section>
    </div>
  );
}

export default App;
