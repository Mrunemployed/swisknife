// Get the necessary DOM elements
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const selectorContainer = document.getElementById('selectorContainer');

let startX, startY, endX, endY;
let isDrawing = false;

// Event listeners for mouse down, move, and up
canvas.addEventListener('mousedown', startDraw);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDraw);

// Start drawing function
function startDraw(e) {
    isDrawing = true;
    startX = e.clientX - selectorContainer.offsetLeft;
    startY = e.clientY - selectorContainer.offsetTop;
}

// Draw function
function draw(e) {
    if (!isDrawing) return;

    // Clear previous rectangle
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    endX = e.clientX - selectorContainer.offsetLeft;
    endY = e.clientY - selectorContainer.offsetTop;

    // Draw new rectangle
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 2;
    ctx.strokeRect(startX, startY, endX - startX, endY - startY);
}

// End drawing function
function endDraw() {
    isDrawing = false;
    // Here you can capture the selected rectangle coordinates (startX, startY, endX, endY) and perform further actions
    console.log(`Selected area: (${startX}, ${startY}, ${endY}, ${endX})`);
}
