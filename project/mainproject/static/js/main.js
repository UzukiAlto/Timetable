const homeEditButton = document.getElementById('home-edit-button');
let homeEditItems = document.querySelectorAll('.home-edit-display');

let isEditing = document.body.dataset.isEditing === "true";
if (isEditing) {
    homeEditItems.forEach((item) => {
        item.style.display = 'block';
    });
}
const displayHomeEdit = () => {
    isEditing = !isEditing;
    homeEditItems.forEach((item) => {
        if (item.style.display === 'block') {
            item.style.display = 'none';
        } else {
            item.style.display = 'block';
        }
    });
};

homeEditButton.addEventListener("click", displayHomeEdit);


