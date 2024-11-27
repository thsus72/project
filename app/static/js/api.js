// static/js/api.js
const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrf_access_token='))
    ?.split('=')[1];

fetch('/protected', {
    method: 'GET',
    headers: {
        'X-CSRF-TOKEN': csrfToken // CSRF 토큰 추가
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
