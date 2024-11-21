document.addEventListener('DOMContentLoaded', function () {
    // Calls updateTotalPercentage when the page loads to display the correct initial percentage
    updateTotalPercentage();
});

function addEvaluation() {
    const evaluationsDiv = document.getElementById('evaluations');
    const newEvaluation = document.createElement('div');
    newEvaluation.className = 'evaluation-row';

    newEvaluation.innerHTML = `
        <input type="text" name="eval_name" class="input-field" placeholder="Evaluation Name" required>
        <input type="number" name="eval_percentage" class="input-field" placeholder="Percentage" min="0" max="100" required oninput="updateTotalPercentage()">
        <button type="button" class="delete-button" onclick="removeEvaluation(this)">-</button>
    `;

    evaluationsDiv.appendChild(newEvaluation);
    updateTotalPercentage();
}

function removeEvaluation(button) {
    const evaluationDiv = button.parentElement;
    evaluationDiv.remove();
    updateTotalPercentage();
}

function updateTotalPercentage() {
    const percentageInputs = document.querySelectorAll('input[name="eval_percentage"]');
    let total = 0;

    // Calculate the total percentage by summing the values of the inputs
    percentageInputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });

    document.getElementById('total-percentage').innerText = total;

    // Show error message if the total is not equal to 100%
    const errorMessage = document.getElementById('error-message');
    if (total !== 100) {
        errorMessage.style.display = 'block';
    } else {
        errorMessage.style.display = 'none';
    }
}

function validateTotalPercentage() {
    const totalPercentage = parseFloat(document.getElementById('total-percentage').innerText);
    if (totalPercentage !== 100) {
        alert('The total percentage must be exactly 100%. Please adjust the values.');
        return false;
    }
    return true;
}

function addProfessor() {
    const professorsSection = document.getElementById('professors-section');
    const newProfessorRow = document.createElement('div');
    newProfessorRow.className = 'professor-row';

    newProfessorRow.innerHTML = `
        <div class="input-group">
            <label for="professor_name" class="input-label">Professor Name:</label>
            <input type="text" name="professor_name" class="input-field" placeholder="Professor Name" required />
            <button type="button" class="delete-button" onclick="removeProfessor(this)">-</button>
        </div>
    `;

    professorsSection.appendChild(newProfessorRow);
}

function removeProfessor(button) {
    const professorRow = button.parentElement.parentElement; // Go up one level to remove the entire professor container
    professorRow.remove();
}
