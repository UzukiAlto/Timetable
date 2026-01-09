// タブを切り替えるボタン
const tabButtons = document.querySelectorAll('.nav-link');
// 授業新規追加画面に表示する要素
const classFormItem = document.querySelector('.tab-item.class-form');
const classFormButton = document.querySelector('.nav-link.class-form');
// 既存授業から追加する画面に表示する要素
const scheduleFormItem = document.querySelector('.tab-item.schedule-form');
const scheduleFormButton = document.querySelector('.nav-link.schedule-form');

// 初期表示は授業新規追加フォームを表示
classFormItem.classList.add('active');
classFormItem.classList.remove('fading-out');
classFormButton.classList.add('active');

scheduleFormItem.classList.remove('active');
scheduleFormItem.classList.add('fading-out');
scheduleFormButton.classList.remove('active');


const changeActiveItem = (item) => {
    if (item.classList.contains('active')){
        item.addEventListener('transitionend', () => {
            item.classList.remove('active');
        }, { once: true});
        item.classList.add('fading-out');
    } else {
        item.classList.remove('fading-out');
        item.classList.add('active');

    }
}

classFormButton.addEventListener('click', () => {
    if (classFormButton.classList.contains('active')) return;

    scheduleFormButton.classList.remove('active');
    changeActiveItem(scheduleFormItem);
    scheduleFormItem.addEventListener('transitionend', () => {
    classFormButton.classList.add('active');
    changeActiveItem(classFormItem);
    }, { once: true });
    
});
scheduleFormButton.addEventListener('click', () => {
    if (scheduleFormButton.classList.contains('active')) return;
    classFormButton.classList.remove('active');
    changeActiveItem(classFormItem);
    classFormItem.addEventListener('transitionend', () => {
        scheduleFormButton.classList.add('active');
        changeActiveItem(scheduleFormItem);
    }, { once: true });
});
