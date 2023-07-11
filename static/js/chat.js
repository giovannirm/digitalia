const chatForm = document.getElementById("csvForm")
chatForm.addEventListener("submit", (event) => {
    event.preventDefault()
    
    const btn = loginForm.querySelector("button[type='submit']")
    btn.classList.add("disabled")
    const endpoint = "http://127.0.0.1:8000/v1/api/upload-csv/"

    const response = fetch(endpoint, {
        method: "POST",
        body: new FormData(chatForm)
    })
    .then(response => response.json())
    .then(data => {
        const chatHistory = document.getElementById("chatHistory")
        console.log(data)
        const { messages } = data

        if(!messages) return alert("Ingresa una clave API válida de OpenAI")
        chatHistory.innerHTML = messages.map(message => {
            const { role, content } = message
            const  classes = {
                assistant: 'assist',
                customer: 'defect',
                system: 'system'
            }[role]

            return `
            <div class="card ${classes}">
                <div class="card-body">
                <strong>${ role }:</strong> ${content}
                </div>
            </div>`
        }).join('')

    }).finally(() => {
        btn.classList.remove("disabled")
    })
})