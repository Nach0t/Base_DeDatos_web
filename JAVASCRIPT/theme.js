// JavaScript to handle theme switching
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  const body = document.body;

  // Determine the base path for the images
  const basePath = window.location.pathname.includes('HTML') ? '../PICTURE/symbols/' : 'PICTURE/symbols/';

  // Load the saved theme preference from localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    body.classList.toggle('dark-mode', savedTheme === 'dark');
    toggle.checked = savedTheme === 'dark';
    icon.src = savedTheme === 'dark' ? `${basePath}mon.png` : `${basePath}sun.png`;
  }

  toggle.addEventListener('change', () => {
    const isDarkMode = toggle.checked;
    body.classList.toggle('dark-mode', isDarkMode);
    icon.src = isDarkMode ? `${basePath}mon.png` : `${basePath}sun.png`;
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  });
});
