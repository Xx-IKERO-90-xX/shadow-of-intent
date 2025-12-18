import { createErrorAlert } from "/static/js/alerts/alerts.js";
import { addAlert } from "/static/js/main.js";

let formAddRepo = document.getElementById("add_repository_form");

const TXT_REGEX = /^https?:\/\/([a-zA-Z0-9]([a-zA-Z0-9\-].*[a-zA-Z0-9])?\.)+[a-zA-Z].*\.txt$/;
const JSON_REGEX = /^https?:\/\/([a-zA-Z0-9]([a-zA-Z0-9\-].*[a-zA-Z0-9])?\.)+[a-zA-Z].*\.json$/;

formAddRepo.addEventListener("submit", (event) => {
    let urlInput = document.getElementById("repo_url");
    let typeInput = document.getElementById("repo_type");

    let url = urlInput.value;
    let type = typeInput.value;

    if (type === "txt" && !TXT_REGEX.test(url)) {
        event.preventDefault();
        let message = "La URL no coincide con el tipo 'txt'. Debe terminar en .txt";
        let errorAlert = createErrorAlert(message);
        let alert = addAlert(errorAlert);
        addAlert(alert);
        
        return;
    }

    if (type === "json" && !JSON_REGEX.test(url)) {
        event.preventDefault();
        let message = "La URL no coincide con el tipo 'json'. Debe terminar en .json";
        let errorAlert = createErrorAlert(message);
        let alert = addAlert(errorAlert);
        addAlert(alert);

        return;
    }
});



