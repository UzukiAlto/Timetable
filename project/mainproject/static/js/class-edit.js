const homeworkForm = document.getElementById('homework-form');
const buttonHomeworkForm = document.getElementById('btn-add-homework');
const memoForm = document.getElementById('memo-form');
const buttonMemoForm = document.getElementById('btn-add-memo');

const buttonEditMemo = document.querySelectorAll('.btn-edit-memo');
const buttonDeleteMemo = document.querySelectorAll('.btn-delete-memo');

const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

buttonHomeworkForm.addEventListener('click', () => {
    homeworkForm.classList.toggle('is-open');
    buttonHomeworkForm.textContent = homeworkForm.classList.contains('is-open') ? '-' : '+';
})

buttonMemoForm.addEventListener('click', () => {
    memoForm.classList.toggle('is-open');
    buttonMemoForm.textContent = memoForm.classList.contains('is-open') ? '-' : '+';
})

function toggleEditMemo(memoId) {

    const textElement = document.getElementById(`memo-${memoId}-text`);
    const formElement = document.getElementById(`edit-form-memo-${memoId}`);
    const button = document.getElementById(`edit-memo-${memoId}`);

    button.querySelector('.bi-pencil').classList.toggle('hide-content');
    button.querySelector('.bi-arrow-counterclockwise').classList.toggle('hide-content');
    textElement.classList.toggle('hide-content');
    formElement.classList.toggle('hide-content');
}

function updateMemo(event, memoId) {
    // フォーム送信をキャンセルして割り込む
    event.preventDefault();

    const formElement = document.getElementById(`edit-form-memo-${memoId}`);

    const formData = new FormData(formElement);
    const content = formData.get('content');

    fetch(`/update/memo/${memoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        // データをjson化
        body: JSON.stringify({ content: content})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const memoText = document.getElementById(`memo-${memoId}-text`);
            memoText.innerText = data.new_content;

            toggleEditMemo(memoId);
        } else {
            alert('Error:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteMemo(memoId) {
    const confirmResult = confirm('この操作は取り消せません。削除しますか？');
    if (!confirmResult) return;
    fetch('/delete/memo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ memo_id: memoId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const memoContainer = document.getElementById(`memo-${memoId}`);
            memoContainer.classList.add('hide-content');
        } else {
            alert('Error:' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    })

}