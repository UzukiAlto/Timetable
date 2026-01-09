// カスタムプロパティ編集用のルート要素
const rootElement = document.documentElement;
// 編集ボタンを取得
const homeEditButton = document.getElementById('home-edit-button');

// htmlの<body>にあるdata属性からデータを取得
// 現在の編集モード
let isEditing = document.body.dataset.isEditing === "true";
// 時間割の行・列数
let timetableRow = parseInt(document.body.dataset.timetableRow);
const timetableRowMax = 8;
let timetableColumn = parseInt(document.body.dataset.timetableColumn);
const timetableColumnMax = 7;

rootElement.style.setProperty('--template-rows-count', timetableRow);
rootElement.style.setProperty('--template-columns-count', timetableColumn);

// 編集用の要素を表示
const enableEditContents = () => {
    document.body.classList.add('edit-mode');
};

// 編集用の要素を非表示
const disableEditContents = () => {
    
    document.body.classList.remove('edit-mode');
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
        homeEditButton.textContent = "完了";
        enableEditContents();

    } else {
        // ボタンのテキストを切り替え
        homeEditButton.textContent = "編集";
        disableEditContents();
    }
};

// 編集ボタンにクリックイベントを追加
homeEditButton.addEventListener("click", displayHomeEdit);

// 各時間枠のフォームに変更があったとき、自動で送信してデータを更新
document.querySelectorAll('.time-frame-form').forEach((form) => {
    form.addEventListener("change", async (event) => {
        try {
            form = event.currentTarget;
            // formが全て入力済みかチェック
            if (!form.checkValidity()) {
                return;
            }
            const response = await fetch('/edit/time_frame/', {
                method: 'POST',
                body: new FormData(form)
            })
            const data = await response.json();
            if (data.status === 'success') {
                const formId = Number(form.dataset.id);
                const timeFrameText = document.getElementById(`time-frame-text-${formId}`);
                timeFrameText.innerText = `${data.new_start_time} - ${data.new_end_time}`;
            } else {
                console.error('Error: ', data.message);
            }
        } catch(error) {
            console.error('Error:', error);
        }
    })
})
