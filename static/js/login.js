const loginForm = document.getElementById("loginForm")

loginForm.addEventListener("submit", (event) => {
    event.preventDefault()
    
    const btn = loginForm.querySelector("button[type='submit']")
    btn.classList.add("disabled")
    const endpoint = "http://127.0.0.1:8000/v1/api/user-authenticate/"

    fetch(endpoint, {
        method: "POST",
        body: new FormData(loginForm)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const { isLogged, message } = data

        if(isLogged) {
            window.location.href = "/"
        } else {
            error = document.getElementById("error")
            error.innerHTML = `<div class="error">${message}</div>`
        }
    }).finally(() => {
        btn.classList.remove("disabled")
    })
})