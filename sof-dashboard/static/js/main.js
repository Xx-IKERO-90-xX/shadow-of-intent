
function clearAlerts() {
    const alertDiv = document.getElementById('alert-div');
    alertDiv.innerHTML = '';
}

function addAlert(alertElement) {
    const alertDiv = document.getElementById('alert-div');
    alertDiv.appendChild(alertElement);
}

export { clearAlerts, addAlert };