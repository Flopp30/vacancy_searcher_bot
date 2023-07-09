function makeMessage(message, tag) {
    const messagesContainer = document.getElementById('messages-container');

    const messageElement = document.createElement('div');

    messageElement.classList.add('alert', `alert-${tag}`, 'fade', 'show');

    const closeButton = document.createElement('button');
    closeButton.setAttribute('type', 'button');
    closeButton.classList.add('close');
    closeButton.setAttribute('data-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');
    closeButton.innerHTML = '&#215;';
    closeButton.addEventListener('click', function () {
        messageElement.remove();
    });

    const messageText = document.createElement('span');
    messageText.textContent = message;

    messageElement.appendChild(closeButton);
    messageElement.appendChild(messageText);
    messagesContainer.appendChild(messageElement);
    setTimeout(() => {
        messageElement.classList.remove("show");
        setTimeout(() => {
            messageElement.remove();
        }, 700);
    }, 5000);
}

window.onload = function () {
    const profileForm = document.getElementById("edit-profile-form");
    profileForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(profileForm);
        const jsonFormData = JSON.stringify(Object.fromEntries(formData));

        try {
            const response = await fetch(profileForm.action, {
                method: "POST",
                body: jsonFormData,
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                const body = await response.text();
                makeMessage(body, "success");
            } else {
                const body = await response.text();
                makeMessage(body, "warning");
            }
        } catch (error) {
            console.error("Произошла ошибка при отправке данных:", error);
        }
    });
};
