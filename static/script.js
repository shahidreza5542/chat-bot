let currentUrl = '';

function addMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addLoadingAnimation() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<span></span><span></span><span></span>';
    loadingDiv.id = 'loadingAnimation';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeLoadingAnimation() {
    const loadingDiv = document.getElementById('loadingAnimation');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message
    addMessage(message, true);
    
    // Clear input
    userInput.value = '';
    
    // Add loading animation
    addLoadingAnimation();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            }),
        });

        const data = await response.json();
        
        // Remove loading animation
        removeLoadingAnimation();
        
        // Add bot response
        addMessage(data.response, false);
    } catch (error) {
        removeLoadingAnimation();
        addMessage('Sorry, something went wrong. Please try again.', false);
    }
}

// Add enter key listener for input field
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
