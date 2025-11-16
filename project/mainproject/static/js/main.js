const homeEditButton = document.getElementById('home-edit-button');
const timetableGrid = document.querySelector('.timetable-grid');
let homeEditItems = document.querySelectorAll('.home-edit-display');

let isEditing = document.body.dataset.isEditing === "true";
let timetableRow = parseInt(document.body.dataset.timetableRow);
let timetableColumn = parseInt(document.body.dataset.timetableColumn);
if (isEditing) {
    homeEditItems.forEach((item) => {
        item.style.display = 'block';
    });
}
const displayHomeEdit = () => {
    isEditing = !isEditing;
    homeEditButton.textContent = isEditing ? "編集完了" : "授業編集";
    if (isEditing == true){
        timetableGrid.style.gridTemplateRows = `60px repeat(8, 1fr)`;
        timetableGrid.style.gridTemplateColumns = `repeat(7, 1fr)`;
        console.log("set to normal");
    } else {
        timetableGrid.style.gridTemplateRows = `60px repeat(${timetableRow}, 1fr)`;
        timetableGrid.style.gridTemplateColumns = `repeat(${timetableColumn}, 1fr)`;
        console.log("set to edit");
    }
    homeEditItems.forEach((item) => {
        if (item.style.display === 'block') {
            item.style.display = 'none';
        } else {
            item.style.display = 'block';
        }
    });
};

homeEditButton.addEventListener("click", displayHomeEdit);


