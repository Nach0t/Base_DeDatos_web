// faq.js

// Función para mostrar/ocultar la respuesta
function toggleAnswer(element) {
  const answer = element.nextElementSibling;
  const arrow = element.querySelector('.arrow');

  if (answer.style.display === "block") {
    answer.style.display = "none";
    arrow.textContent = "▼"; // Flecha hacia abajo
  } else {
    answer.style.display = "block";
    arrow.textContent = "▲"; // Flecha hacia arriba
  }
}
