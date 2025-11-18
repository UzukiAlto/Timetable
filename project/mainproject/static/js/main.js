// 編集ボタンを取得
const homeEditButton = document.getElementById('home-edit-button');
// 時間割グリッドの要素を取得
const timetableGrid = document.querySelector('.timetable-grid');
// 編集ボタンを押したときに表示・非表示を切り替える要素を取得
let homeEditItems = document.querySelectorAll('.home-edit-display');

let classContentItems = document.querySelectorAll('.class-content.card-body.btn');

// htmlの<body>にあるdata属性からデータを取得
// 現在の編集モード
let isEditing = document.body.dataset.isEditing === "true";
// 時間割の行・列数
let timetableRow = parseInt(document.body.dataset.timetableRow);
let timetableColumn = parseInt(document.body.dataset.timetableColumn);

const enableEditContents = () => {
    // 編集用の要素を表示
    homeEditItems.forEach((item) => {
        item.style.display = 'block';
    });
    classContentItems.forEach((item) => {
        item.classList.add('btn-disabled');
    });
    timetableGrid.style.gridTemplateRows = `60px repeat(8, 1fr)`;
    timetableGrid.style.gridTemplateColumns = `repeat(7, 1fr)`;
};

const disableEditContents = () => {
    
    // 初期表示時のグリッド設定
    timetableGrid.style.gridTemplateRows = `60px repeat(${timetableRow}, 1fr)`;
    timetableGrid.style.gridTemplateColumns = `repeat(${timetableColumn}, 1fr)`;
    
    homeEditItems.forEach((item) => {
        item.style.display = 'none';
    });
    classContentItems.forEach((item) => {
        item.classList.remove('btn-disabled');
    });
};




// 初期表示時に編集モードかどうかを判定
if (isEditing) {
    enableEditContents();
}else {
    disableEditContents();
}

// 編集ボタンがクリックされたときに要素の表示とグリッドの設定を切り替える
const displayHomeEdit = () => {
    isEditing = !isEditing;
    if (isEditing == true){
        // ボタンのテキストを切り替え
        homeEditButton.textContent = "編集完了";
        enableEditContents();

    } else {
        // ボタンのテキストを切り替え
        homeEditButton.textContent = "授業編集";
        disableEditContents();
    }
};

// 編集ボタンにクリックイベントを追加
homeEditButton.addEventListener("click", displayHomeEdit);
