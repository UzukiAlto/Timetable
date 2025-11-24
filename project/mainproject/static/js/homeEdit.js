// タブを切り替えるボタン
const tabButtons = document.querySelectorAll('.nav-link');
// 授業新規追加画面に表示する要素
const classForm = document.querySelectorAll('.class-form');
// 既存授業から追加する画面に表示する要素
const scheduleForm = document.querySelectorAll('.schedule-form');

// 初期表示は授業新規追加フォームを表示
classForm.forEach ((item) => {
    item.classList.remove('hide-content');
});
scheduleForm.forEach ((item) => {
    item.classList.add('hide-content');
});

const changeTab = () => {
    classForm.forEach ((item) => {
        changeActiveItem(item);
    });
    scheduleForm.forEach ((item) => {
        changeActiveItem(item);
    });
}

const changeActiveItem = (item) => {
    if (item.classList.contains('hide-content')){
        item.classList.remove('hide-content');
    } else {
        item.classList.add('hide-content');
    }
}

tabButtons.forEach((button) => {
    button.addEventListener('click', changeTab);
});
