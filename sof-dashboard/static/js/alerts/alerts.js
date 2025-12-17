
function createErrorAlert(message) {
    let errorAlertTemplate = document.getElementById('error-alert-template');
    let alertClone = errorAlertTemplate.content.cloneNode(true);
    alertClone.querySelector('.alert-message').textContent = message;
    console.log (alertClone);

    return alertClone;
}

function createWarningAlert(message) {
    let warningAlertTemplate = document.getElementById('warning-alert-template');
    let alertClone = warningAlertTemplate.content.cloneNode(true);
    alertClone.querySelector('.alert-message').textContent = message
    console.log (alertClone);
    
    return alertClone;
}

export {
    createErrorAlert,
    createWarningAlert
}