/** 要素を更新する関数の引数として渡すクラス */
class ElementUpdateParams{
    /**
     * @param {Object} param - 引数をまとめたもの
     * @param {SubmitEvent} param.event - フォームの送信イベント
     * @param {string} param.elementType - 要素の種類（例：homework, memo）
     * @param {number} param.id - 要素のID
     * @param {string[]} param.contents - 更新する内容の配列(例：['deadline', 'content'] )
     */
    constructor({event, elementType, id, contents}){
        /** @type {SubmitEvent} */
        this.event = event;
        /** @type {string} */
        this.elementType = elementType;
        /** @type {number} */
        this.id = id;
        /** @type {string[]} */
        this.contents = contents;
    }
}

/** 要素を削除する関数の引数として渡すクラス */
class ElementDeleteParams{
    /**
     * @param {Object} param - 引数をまとめたもの
     * @param {string} param.elementType - 要素の種類（例：homework, memo）
     * @param {number} param.id - 要素のID
     */
    constructor({elementType, id}){
        /** @type {string} */
        this.elementType = elementType;
        /** @type {number} */
        this.id = id;
    }
}

/** 要素の種類としてクラスに入れる */
const elementTypes = Object.freeze({
    classBasicInfo: 'class-basic-info',
    homework: 'homework',
    memo: 'memo',
})

const buttonHomeworkForm = document.getElementById('btn-add-homework');
const buttonMemoForm = document.getElementById('btn-add-memo');


// CSRFトークンの取得
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


buttonHomeworkForm.addEventListener('click', () => {
    const homeworkForm = document.getElementById('homework-form');
    homeworkForm.classList.toggle('is-open');
    buttonHomeworkForm.textContent = homeworkForm.classList.contains('is-open') ? '-' : '+';
})

buttonMemoForm.addEventListener('click', () => {
    const memoForm = document.getElementById('memo-form');
    memoForm.classList.toggle('is-open');
    buttonMemoForm.textContent = memoForm.classList.contains('is-open') ? '-' : '+';
})


/** @param {ElementUpdateParams} elementUpdateParams */
async function updateData(elementUpdateParams) {
    if(!(elementUpdateParams instanceof ElementUpdateParams)){
        console.error(elementUpdateParams + "は想定外のデータ型です。");
        return
    }

    // フォーム送信をキャンセルして割り込む
    elementUpdateParams.event.preventDefault();
    const formElement = document.getElementById(`edit-form-${elementUpdateParams.elementType}-${elementUpdateParams.id}`);
    const formData = new FormData(formElement);
    // jsonとして送るデータ
    const body = { id: elementUpdateParams.id };
    elementUpdateParams.contents.forEach((content) => {
        body[content] = formData.get(content);
    });

    try{
        const response = await fetch(`/update/${elementUpdateParams.elementType.split('-').join('_')}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }, 
            // データをjson化
            body: JSON.stringify(body)
        });
        const data = await response.json();
        if (data.status === 'success') {
            elementUpdateParams.contents.forEach((content) => {
                document.getElementById(`${elementUpdateParams.elementType.split('_').join('-')}-${elementUpdateParams.id}-${content.split('_').join('-')}`).innerText = data[`new_${content}`];
            });

            toggleEditClass(elementUpdateParams.elementType, elementUpdateParams.id);
        } else {
            alert('Error:'+ data.message);
        }
    } catch(error) {
        console.error('Error:', error);
    }
}

/** @param {ElementDeleteParams} elementDeleteParams */
async function deleteData(elementDeleteParams) {
    // 画面に確認ダイアログを表示
    const confirmResult = confirm('この操作は取り消せません。削除しますか？');
    if (!confirmResult) return;

    try{
        const response = await fetch(`/delete/${elementDeleteParams.elementType.split('-').join('_')}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ id: elementDeleteParams.id })
        });
        const data = await response.json();
        if (data.status === 'success') {
            const container = document.getElementById(`${elementDeleteParams.elementType}-${elementDeleteParams.id}`);
            container.classList.add('hide-content');
        } else {
            alert('Error:' + data.message);
        }

    } catch (error) {
        console.error('Error:', error);
    }

}

async function updateClassBasicInfo(event, classId) {
    const classBasicInfoParam = new ElementUpdateParams({
        event: event,
        elementType: elementTypes.classBasicInfo,
        id: classId,
        contents: ['class_name', 'classroom_name', 'professor_name']
    })
    updateData(classBasicInfoParam);
}

/**
 * 編集時にフォーム等の表示を切り替える関数
 * @param {string} elementType 
 * @param {number} elementId 
 */
function toggleEditClass(elementType, elementId) {
    document.querySelectorAll(`.js-display-${elementType}-${elementId}`).forEach(element => {
        element.classList.toggle('hide-content');
    });
}

function updateMemo(event, memoId) {
    const memoUpdateParams = new ElementUpdateParams({
        event: event,
        elementType: elementTypes.memo,
        id: memoId,
        contents: ["content"]
    });
    updateData(memoUpdateParams);
}

function deleteMemo(memoId) {
    const memoDeleteParam = new ElementDeleteParams({
        elementType: elementTypes.memo,
        id: memoId
    });
    deleteData(memoDeleteParam);
}

async function updateHomework(event, homeworkId) {
    const homeworkUpdateParam = new ElementUpdateParams({
        event: event,
        elementType: elementTypes.homework,
        id: homeworkId,
        contents: ['deadline', 'content']
    });
    updateData(homeworkUpdateParam);
}

async function deleteHomework(homeworkId) {
    const homeworkDeleteParam = new ElementDeleteParams({
        elementType: elementTypes.homework,
        id: homeworkId
    })
    deleteData(homeworkDeleteParam);
}