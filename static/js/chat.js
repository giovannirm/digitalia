const chatForm = document.getElementById("csvForm")
chatForm.addEventListener("submit", (event) => {
    event.preventDefault()
    
    const btn = chatForm.querySelector("button[type='submit']")
    const btn_logout = document.querySelector("a.btn-logout")
    
    btn.classList.add("disabled")
    btn_logout.classList.add("disabled")
    const endpoint = "http://127.0.0.1:8000/v1/api/upload-csv/"

    fetch(endpoint, {
        method: "POST",
        body: new FormData(chatForm)
    })
    .then(response => response.json())
    .then(data => {
        const chatHistory = document.getElementById("chatHistory")
        console.log(data)
        const { message, messages } = data

        if(!messages) return alert(message)
        
        chatHistory.innerHTML = messages.map(message => {
            const { role, content } = message
            const  classes = {
                system: 'system',
                user: 'user',
                assistant: 'assistant'
            }[role]

            return `
            <div class="card ${classes}">
                <div class="card-body">
                <strong>${ role.toUpperCase() }:</strong> ${content}
                </div>
            </div>`
        }).join('')

    }).finally(() => {
        btn.classList.remove("disabled")
        btn_logout.classList.remove("disabled")
    })
})