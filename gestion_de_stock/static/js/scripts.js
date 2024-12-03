const themeToggle = document.getElementById('theme-toggle');
const body = document.body;
const sidebar = document.getElementById('sidebar');

// Leer el estado guardado en localStorage
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// Aplicar tema inicial
if (isDarkMode) {
  body.classList.add('dark-mode');
  sidebar.classList.add('bg-dark');
  themeToggle.textContent = '🌙 Noche';
}

// Cambiar tema y guardar en localStorage
themeToggle.addEventListener('click', () => {
  isDarkMode = !isDarkMode;
  body.classList.toggle('dark-mode', isDarkMode);
  sidebar.classList.toggle('bg-dark', isDarkMode);
  themeToggle.textContent = isDarkMode ? '🌙 Noche' : '🌞 Día';
  localStorage.setItem('darkMode', isDarkMode);
});



