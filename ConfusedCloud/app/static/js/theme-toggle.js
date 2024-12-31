// ConfusedCloud Theme Toggle
(function() {
  const body = document.body;
  const toggleBtn = document.getElementById('themeToggle');
  const THEME_KEY = 'cc-theme';

  function setTheme(theme) {
    if (theme === 'light') {
      body.classList.add('light-theme');
      localStorage.setItem(THEME_KEY, 'light');
    } else {
      body.classList.remove('light-theme');
      localStorage.setItem(THEME_KEY, 'dark');
    }
  }

  function toggleTheme() {
    if (body.classList.contains('light-theme')) {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  }

  // Initial theme
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === 'light') setTheme('light');
  else setTheme('dark');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleTheme);
  }
})(); 