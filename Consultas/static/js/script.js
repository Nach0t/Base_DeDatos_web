function addEvaluation() {
    const evaluationsDiv = document.getElementById('evaluations');
    const newEvaluation = document.createElement('div');
    newEvaluation.className = 'evaluation';
    newEvaluation.innerHTML = `
        <input type="text" name="eval_name" placeholder="Nombre de la Evaluación" required>
        <input type="number" name="eval_percentage" placeholder="Porcentaje" min="0" max="100" required oninput="updateTotalPercentage()">
    `;
    evaluationsDiv.appendChild(newEvaluation);
    updateTotalPercentage();
}

function removeEvaluation() {
    const evaluationsDiv = document.getElementById('evaluations');
    if (evaluationsDiv.children.length > 1) {
        evaluationsDiv.removeChild(evaluationsDiv.lastElementChild);
    }
    updateTotalPercentage();
}

function updateTotalPercentage() {
    const percentageInputs = document.querySelectorAll('input[name="eval_percentage"]');
    let total = 0;
    percentageInputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });
    document.getElementById('total-percentage').innerText = total;
}

function validateTotalPercentage() {
    const totalPercentage = parseFloat(document.getElementById('total-percentage').innerText);
    if (totalPercentage !== 100) {
        alert('El porcentaje total debe ser exactamente 100%. Por favor, ajuste los valores.');
        return false;
    }
    return true;
}
