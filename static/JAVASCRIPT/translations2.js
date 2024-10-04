document.addEventListener('DOMContentLoaded', () => {
    // Cargar el idioma predeterminado (en este caso, inglés)
    loadTranslations('en');
});

function loadTranslations(language) {
    // Construir la URL para el archivo JSON
    const url = `/static/JSONS/language/about/${language}.json`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Cargar los textos en los elementos de la página About
            
            // Título de la página About
            document.getElementById('aboutTitle').textContent = data.title || 'About Us';

            // Descripción general del equipo
            document.getElementById('description').textContent = data.description || 'We are a group of Computer Science students from University San Sebastian, Chile.';

            // Sección de equipo
            document.getElementById('teamTitle').textContent = data.teamTitle || 'Our Team:';
            
            // Primer miembro del equipo
            document.getElementById('teamMember1').textContent = data.team.member1?.name || 'Ignacio Rehbein';
            document.getElementById('teamExpertise1').textContent = data.team.member1?.expertise || 'Expert in .';
            
            // Segundo miembro del equipo
            document.getElementById('teamMember2').textContent = data.team.member2?.name || 'Claudio Diaz';
            document.getElementById('teamExpertise2').textContent = data.team.member2?.expertise || 'Expert in .';

            // Tercer miembro del equipo
            document.getElementById('teamMember3').textContent = data.team.member3?.name || 'Vicente Quintanilla';
            document.getElementById('teamExpertise3').textContent = data.team.member3?.expertise || 'No, I´ll win.';

            // Pie de página
            document.getElementById('footer').innerHTML = data.footer || '&copy; <span id="currentYear"></span> Chuequito Company. All rights reserved.';
            
            // Actualiza el año actual en el pie de página
            document.getElementById('currentYear').textContent = new Date().getFullYear();
        })
        .catch(error => {
            console.error('Error loading translations:', error);
            // Mensaje de error amigable
            document.getElementById('footer').textContent = 'Error loading translations. Please try again later.';
        });
}

function changeLanguage(language) {
    // Cambiar el idioma dinámicamente
    loadTranslations(language);
}
