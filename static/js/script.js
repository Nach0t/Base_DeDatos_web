document.addEventListener('DOMContentLoaded', function () {
    // Automatically populate initial percentages and update the total percentage
    populateTotalPercentage();
});

// Function to add a new dynamic evaluation row
function addDynamicEvaluation() {
    const evaluationsDiv = document.getElementById('evaluations');
    if (!evaluationsDiv) {
        console.error("The evaluations container was not found.");
        return;
    }

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

// Function to remove an evaluation row
function removeEvaluation(button) {
    const evaluationRow = button.parentElement; // Elimina la fila completa
    evaluationRow.remove();
    updateTotalPercentage();
}

// Function to update the total percentage based on evaluation percentages
function updateTotalPercentage() {
    const percentageInputs = document.querySelectorAll('input[name="eval_percentage"]');
    let total = 0;

    // Calculate the total percentage by summing the values of the inputs
    percentageInputs.forEach(input => {
        const value = parseFloat(input.value);
        if (!isNaN(value)) {
            total += value;
        }
    });

    // Update the total percentage on the page
    document.getElementById('total-percentage').innerText = total;

    // Show an error message if the total percentage is not 100%
    const errorMessage = document.getElementById('error-message');
    if (total !== 100) {
        errorMessage.style.display = 'block';
    } else {
        errorMessage.style.display = 'none';
    }
}

// Function to validate that the total percentage is exactly 100% before submission
function validateTotalPercentage() {
    const totalPercentage = parseFloat(document.getElementById('total-percentage').innerText);
    const evaluationNames = document.querySelectorAll('input[name="eval_name"]');
    const evaluationPercentages = document.querySelectorAll('input[name="eval_percentage"]');

    // Check for empty names or invalid percentages
    for (let i = 0; i < evaluationNames.length; i++) {
        if (evaluationNames[i].value.trim() === "") {
            alert('Evaluation name cannot be empty.');
            return false;
        }

        if (evaluationPercentages[i].value.trim() === "" || isNaN(evaluationPercentages[i].value)) {
            alert('Evaluation percentage must be a valid number.');
            return false;
        }
    }

    if (totalPercentage !== 100) {
        alert('The total percentage must be exactly 100%. Please adjust the values.');
        return false;
    }
    return true;
}

// Automatically populate and update initial percentages
function populateTotalPercentage() {
    const percentageInputs = document.querySelectorAll('input[name="eval_percentage"]');
    let total = 0;

    percentageInputs.forEach(input => {
        const value = parseFloat(input.value);
        if (!isNaN(value)) {
            total += value;
        }
    });

    // Update the total percentage displayed
    document.getElementById('total-percentage').innerText = total;
    updateTotalPercentage();
}
