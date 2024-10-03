document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  const body = document.body;

  // Determine the base path for the images
  // Adjust basePath for static files served by Flask
  const basePath = '/static/PICTURE/symbols/';

  // Load the saved theme preference from localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    const isDarkMode = savedTheme === 'dark';
    body.classList.toggle('dark-mode', isDarkMode);
    toggle.checked = isDarkMode;
    icon.src = isDarkMode ? `${basePath}mon.png` : `${basePath}sun.png`;
  }

  toggle.addEventListener('change', () => {
    const isDarkMode = toggle.checked;
    body.classList.toggle('dark-mode', isDarkMode);
    icon.src = isDarkMode ? `${basePath}mon.png` : `${basePath}sun.png`;
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  });
});
