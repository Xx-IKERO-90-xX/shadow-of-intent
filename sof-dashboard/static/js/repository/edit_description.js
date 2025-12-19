let openEditBtn = document.getElementById('open-edit-description');
let editBtn = document.getElementById('edit-btn');
let cancelBtn = document.getElementById('cancel-btn');

openEditBtn.addEventListener('click', () => {
    openEditBtn.classList.add('off');
    editBtn.classList.remove('off');
    cancelBtn.classList.remove('off');

    const descriptionTextarea = document.getElementById('description-text');
    descriptionTextarea.removeAttribute('readonly');
});

cancelBtn.addEventListener('click', () => {
    openEditBtn.classList.remove('off');
    editBtn.classList.add('off');
    cancelBtn.classList.add('off');

    const descriptionTextarea = document.getElementById('description-text');
    descriptionTextarea.setAttribute('readonly', true);
});