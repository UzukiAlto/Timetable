function toggleComplete(element) {
    const homeworkId = element.dataset.id;
    const currentStatus = element.dataset.isFinished === 'true';
    const newStatus = !currentStatus;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/update/homework/finish/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            id: homeworkId,
            is_finished: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            if (data.is_finished) {
                element.classList.add('completed');
                element.dataset.isFinished = 'true';
                element.parentNode.appendChild(element);
            } else {
                element.classList.remove('completed');
                element.dataset.isFinished = 'false';
                element.parentNode.prepend(element);
            }
        } else {
            console.error('Error:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('toggle-completed').addEventListener('change', function() {
    if (this.checked) {
        document.body.classList.remove('hide-completed');
    } else {
        document.body.classList.add('hide-completed');
    }
});
