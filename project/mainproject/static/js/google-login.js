function handleCredentialResponse(response) {
    // 新しいライブラリでは response.credential にIDトークンが入っています
    var id_token = response.credential;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '{% url "google_login" %}');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.location.href = '{% url "app:index" %}';
        } else {
            console.log('Login failed: ' + xhr.responseText);
        }
    };
    xhr.send('idtoken=' + encodeURIComponent(id_token));
}