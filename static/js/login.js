const loginForm = document.getElementById("loginForm")

loginForm.addEventListener("submit", (event) => {
    event.preventDefault()
    
    const btn = loginForm.querySelector("button[type='submit']")
    btn.classList.add("disabled")
    const endpoint = "http://127.0.0.1:8000/v1/api/authenticate-login/"

    fetch(endpoint, {
        method: "POST",
        body: new FormData(loginForm)
    })
    .then(response => response.json())
    .then(data => {
        const chatHistory = document.getElementById("chatHistory")
        console.log(data)
        const { isLogged } = data

        if(isLogged) {
            window.location.href = "/home/"
        }

        else {
            alert("Invalid credentials")
        }

    }).finally(() => {
        btn.classList.remove("disabled")
    })
})