
document.addEventListener('DOMContentLoaded', () => {

    // =====================================
    // LOGIN FORM
    // =====================================

    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: new FormData(loginForm)
                });

                const result = await response.json();

                if (result.success) {
                    window.location.href = '/browse';
                } else {
                    alert('Login failed: ' + result.message);
                }

            } catch (error) {
                alert('Login error: ' + error.message);
            }
        });
    }


    // =====================================
    // SIGNUP FORM
    // =====================================

    const signupForm = document.getElementById('signupForm');

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            try {
                const response = await fetch('/signup', {
                    method: 'POST',
                    body: new FormData(signupForm)
                });

                const result = await response.json();

                if (result.success) {
                    window.location.href = '/login';
                } else {
                    alert('Signup failed: ' + result.message);
                }

            } catch (error) {
                alert('Signup error: ' + error.message);
            }
        });
    }


    // =====================================
    // STUDY MATERIALS
    // =====================================

    const materialsList = document.getElementById('materialsList');

    if (materialsList) {

        fetch('/api/materials')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Could not load materials.');
                }
                return response.json();
            })
            .then(data => {

                materialsList.replaceChildren();

                data.forEach(material => {

                    const card = document.createElement('div');
                    card.className = 'material-item';

                    const title = document.createElement('h3');
                    title.textContent = material.title || 'Untitled';

                    const description = document.createElement('p');
                    description.textContent =
                        material.description || 'No description';

                    const link = document.createElement('a');
                    link.href =
                        '/download/' + encodeURIComponent(material.filename);

                    link.className = 'download-btn';
                    link.textContent = 'Download';

                    card.append(title, description, link);
                    materialsList.appendChild(card);
                });

            })
            .catch(error => {
                console.error('Materials error:', error);
            });
    }


    // =====================================
    // NEXORA AI CHAT
    // =====================================

    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-btn');
    const chatSection = document.querySelector('.chat-section');
    const welcomeSection = document.querySelector('.welcome-section');
    const inputContainer = document.querySelector('.input-container');

    const researchButton =
        document.getElementById('research-toggle');


    if (chatInput && sendButton && chatSection && inputContainer) {

        // =====================================
        // MESSAGE CONTAINER
        // =====================================

        const messagesContainer = document.createElement('div');

        messagesContainer.id = 'chat-messages';
        messagesContainer.style.display = 'none';

        chatSection.insertBefore(
            messagesContainer,
            inputContainer
        );


        // =====================================
        // SEARCH RESULTS CONTAINER
        // =====================================

        const searchResults = document.createElement('div');

        searchResults.id = 'search-results';

        searchResults.style.padding = '15px';
        searchResults.style.margin = '15px 0';
        searchResults.style.color = '#ffffff';

        chatSection.insertBefore(
            searchResults,
            inputContainer
        );


        // =====================================
        // SEARCH MODE
        // =====================================

        let searchMode = false;


        function updateSearchButton() {

            if (!researchButton) return;

            researchButton.setAttribute(
                'aria-pressed',
                String(searchMode)
            );

            if (searchMode) {

                researchButton.textContent = '🌐 Search ON';

                researchButton.style.background = '#293b67';
                researchButton.style.color = '#ffffff';
                researchButton.style.border = '1px solid #718cff';

            } else {

                researchButton.textContent = '🌐 Search';

                researchButton.style.background = '';
                researchButton.style.color = '';
                researchButton.style.border = '';

            }
        }


        // TOGGLE SEARCH ON/OFF

        if (researchButton) {

            researchButton.addEventListener('click', () => {

                searchMode = !searchMode;

                updateSearchButton();

                chatInput.focus();

            });
        }


        // =====================================
        // ADD CHAT MESSAGE
        // =====================================

        function addMessage(text, sender) {

            const message = document.createElement('div');

            message.className =
                sender === 'user' ? 'user-message' : 'ai-message';

            message.textContent = text;

            message.style.padding = '14px';
            message.style.margin = '12px 0';
            message.style.borderRadius = '12px';
            message.style.whiteSpace = 'pre-wrap';
            message.style.overflowWrap = 'anywhere';

            if (sender === 'user') {

                message.style.background = '#252b40';
                message.style.marginLeft = '15%';

            } else {

                message.style.background = '#151c2e';
                message.style.marginRight = '15%';

            }

            messagesContainer.appendChild(message);

            messagesContainer.scrollTop =
                messagesContainer.scrollHeight;
        }


        // =====================================
        // DISPLAY SEARCH RESULTS
        // =====================================

        function displaySearchResults(results) {

            searchResults.replaceChildren();

            const heading = document.createElement('h3');

            heading.textContent = 'Internet Search Results';

            searchResults.appendChild(heading);


            if (!results || results.length === 0) {

                const emptyMessage = document.createElement('p');

                emptyMessage.textContent = 'No results found.';

                searchResults.appendChild(emptyMessage);

                return;
            }


            results.forEach(item => {

                const card = document.createElement('div');

                card.style.padding = '15px';
                card.style.margin = '12px 0';
                card.style.background = '#151c2e';
                card.style.borderRadius = '10px';


                const title = document.createElement('h4');

                title.textContent = item.title || 'Untitled';


                const description = document.createElement('p');

                description.textContent =
                    item.description || 'No description available.';

                description.style.lineHeight = '1.6';


                card.appendChild(title);
                card.appendChild(description);


                // Validate website URL

                try {

                    const url = new URL(item.url);

                    if (
                        url.protocol === 'https:' ||
                        url.protocol === 'http:'
                    ) {

                        const link = document.createElement('a');

                        link.textContent = 'Visit Website →';

                        link.href = url.href;

                        link.target = '_blank';

                        link.rel = 'noopener noreferrer';

                        link.style.color = '#8b9cff';

                        card.appendChild(link);
                    }

                } catch (error) {
                    // Ignore invalid URLs
                }


                searchResults.appendChild(card);

            });
        }


        // =====================================
        // INTERNET SEARCH FUNCTION
        // =====================================

        async function performSearch(query) {

            searchResults.replaceChildren();

            const loading = document.createElement('p');

            loading.textContent = 'Searching the internet...';

            searchResults.appendChild(loading);


            try {

                const response = await fetch('/api/search', {

                    method: 'POST',

                    headers: {
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify({
                        query: query
                    })

                });


                const data = await response.json();

                if (!response.ok) {

                    throw new Error(
                        data.error || 'Search failed'
                    );
                }


                displaySearchResults(data.results);

            } catch (error) {

                searchResults.replaceChildren();

                const errorMessage = document.createElement('p');

                errorMessage.textContent =
                    'Search Error: ' + error.message;

                searchResults.appendChild(errorMessage);

            }
        }


        // =====================================
        // NORMAL AI CHAT FUNCTION
        // =====================================

        async function performChat(message) {

            const loadingMessage = document.createElement('div');

            loadingMessage.textContent = 'NEXORA is thinking...';

            loadingMessage.style.padding = '14px';

            messagesContainer.appendChild(loadingMessage);


            try {

                const response = await fetch('/api/chat', {

                    method: 'POST',

                    headers: {
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify({
                        message: message
                    })

                });


                const result = await response.json();

                loadingMessage.remove();


                if (!response.ok) {

                    throw new Error(
                        result.error || 'Server error'
                    );
                }


                const reply =
                    result.reply ||
                    result.response ||
                    result.message;

                addMessage(
                    reply || 'AI did not return a response.',
                    'ai'
                );


            } catch (error) {

                loadingMessage.remove();

                addMessage(
                    'Error: ' + error.message,
                    'ai'
                );

            }
        }


        // =====================================
        // SEND MESSAGE
        // =====================================

        async function sendMessage() {

            const message = chatInput.value.trim();

            if (!message) return;


            if (welcomeSection) {
                welcomeSection.style.display = 'none';
            }


            messagesContainer.style.display = 'block';

            addMessage(message, 'user');

            chatInput.value = '';

            sendButton.disabled = true;

            if (researchButton) {
                researchButton.disabled = true;
            }


            try {

                // SEARCH MODE ON

                if (searchMode) {

                    await performSearch(message);

                }

                // SEARCH MODE OFF

                else {

                    await performChat(message);

                }

            } finally {

                sendButton.disabled = false;

                if (researchButton) {
                    researchButton.disabled = false;
                }

                chatInput.focus();

            }
        }


        // =====================================
        // SEND BUTTON CLICK
        // =====================================

        sendButton.addEventListener('click', sendMessage);


        // =====================================
        // ENTER TO SEND
        // =====================================

        chatInput.addEventListener('keydown', (e) => {

            if (e.key === 'Enter' && !e.shiftKey) {

                e.preventDefault();

                sendMessage();

            }

        });

    }

});