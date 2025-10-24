const homeEditButton = document.getElementById('home-edit-button');

const displayHomeEdit = () => {
    let homeEditItems = document.querySelectorAll('.home-edit-display');
    homeEditItems.forEach((item) => {
        if (item.style.display === 'block') {
            item.style.display = 'none';
        } else {
            item.style.display = 'block';
        }
    });
};

homeEditButton.addEventListener("click", displayHomeEdit);
