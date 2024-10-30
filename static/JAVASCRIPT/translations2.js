document.addEventListener('DOMContentLoaded', () => {
    console.log("Cargando idioma predeterminado...");
    loadTranslations('en');
});

function loadTranslations(language) {
    // Construir la URL para el archivo JSON
    const url = `/static/JSON/language/about/${language}.json`;

    console.log(`Intentando cargar traducciones desde: ${url}`);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el archivo JSON: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos de traducción cargados correctamente:", data);

            // Cargar los textos en los elementos de la página About
            document.getElementById('aboutTitle').textContent = data.title || 'About Us';
            document.getElementById('description').textContent = data.description || 'We are a group of Computer Science students from University San Sebastian, Chile.';
            document.getElementById('teamTitle').textContent = data.teamTitle || 'Our Team:';
            
            // Primer miembro del equipo
            document.getElementById('teamMember1').textContent = data.team.member1?.name || 'Ignacio Rehbein';
            document.getElementById('teamExpertise1').textContent = data.team.member1?.expertise || 'Expert in web design.';
            
            // Segundo miembro del equipo
            document.getElementById('teamMember2').textContent = data.team.member2?.name || 'Claudio Diaz';
            document.getElementById('teamExpertise2').textContent = data.team.member2?.expertise || 'Expert in Flask logic.';
            
            // Tercer miembro del equipo
            document.getElementById('teamMember3').textContent = data.team.member3?.name || 'Vicente Quintanilla';
            document.getElementById('teamExpertise3').textContent = data.team.member3?.expertise || 'Expert in database management.';
            
            // Pie de página
            document.getElementById('footer').innerHTML = data.footer || '&copy; <span id="currentYear"></span> Chuequito Company. All rights reserved.';
            
            // Actualiza el año actual en el pie de página
            document.getElementById('currentYear').textContent = new Date().getFullYear();
        })
        .catch(error => {
            console.error('Error al cargar traducciones:', error);
            document.getElementById('footer').textContent = 'Error loading translations. Please try again later.';
        });
}

function changeLanguage(language) {
    console.log(`Cambiando el idioma a: ${language}`);
    loadTranslations(language);
}
