// Get button elements
const upButton = document.getElementById('up');
const downButton = document.getElementById('down');
const leftButton = document.getElementById('left');
const rightButton = document.getElementById('right');

// API endpoint
const API_URL = 'http://192.168.1.3:5000/button-press';

// Function to send button press to API
async function sendButtonPress(direction) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ direction: direction })
        });
        
        const data = await response.json();
        console.log('API Response:', data);
    } catch (error) {
        console.error('Error sending button press:', error);
    }
}

// Add event listeners
upButton.addEventListener('click', () => {
    console.log('Up button clicked');
    sendButtonPress('up');
});

downButton.addEventListener('click', () => {
    console.log('Down button clicked');
    sendButtonPress('down');
});

leftButton.addEventListener('click', () => {
    console.log('Left button clicked');
    sendButtonPress('left');
});

rightButton.addEventListener('click', () => {
    console.log('Right button clicked');
    sendButtonPress('right');
});
