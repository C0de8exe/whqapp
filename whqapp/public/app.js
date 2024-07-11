document.addEventListener('DOMContentLoaded', () => {
  const registerButton = document.querySelector('.register-button');
  const comingSoonElement = document.querySelector('.coming-soon');
  const modal = document.getElementById('modal');
  const claimButton = document.querySelector('.claim-button');

  registerButton.addEventListener('click', async () => {
    const telegram = window.Telegram.WebApp;
    const chatId = telegram.initDataUnsafe.user.id;
    const username = telegram.initDataUnsafe.user.username;

    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chatId, username }),
      });
      const result = await response.json();
      if (result.success) {
        modal.style.display = 'none';
        registerButton.disabled = true;
        registerButton.innerHTML = 'Registered';
        registerButton.classList.remove('register-button');
        registerButton.classList.add('registered-text');
        registerButton.style.backgroundColor = 'transparent';
        registerButton.style.color = '#00ff00';
        registerButton.style.border = 'none';
        registerButton.querySelector('img').style.display = 'none';
      } else {
        alert(result.message || 'Ошибка при регистрации.');
      }
    } catch (error) {
      console.error('Ошибка при регистрации:', error);
      alert('Ошибка при регистрации.');
    }
  });

  const symbols = ['?', '7', '+', ':', '=', 'I', '~'];

  function createSymbol() {
    const symbol = document.createElement('div');
    symbol.className = 'symbol';
    symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
    symbol.style.setProperty('--random-x', `${Math.random() * 300 - 150}px`);
    symbol.style.setProperty('--random-y', `${Math.random() * 300 - 150}px`);
    symbol.style.setProperty('--random-scale', `${Math.random() * 1 + 0.5}`);
    symbol.style.top = `${Math.random() * 100}vh`;
    symbol.style.left = `${Math.random() * 100}vw`;
    symbol.style.animationDelay = `${Math.random() * 5}s`;
    document.getElementById('background').appendChild(symbol);
  }

  for (let i = 0; i < 200; i++) {
    createSymbol();
  }
});
