import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div class="jumbotron text-center main">
        <h1></h1>
        <p>Сервис корпоративного питания для сотрудников СберБанка</p>
        <a href="#" class="btn btn-primary btn-lg">Личный кабинет</a>
      </div>
      <section class="container py-5">
        <div class="text-center">
          <h2>Помощь</h2>
          <p class="lead">by NovaDev</p>
          <ul class="list-inline">
            <li class="list-inline-item"><a href="https://vk.com/artyomjk">VK</a></li>
            <li class="list-inline-item"><a href="https://github.com/artemgoncarov">Github</a></li>
            <li class="list-inline-item"><a href="https://t.me/artyomjk">Telegram</a></li>
          </ul>
        </div>
      </section>
    </div>
  );
}

export default App;
