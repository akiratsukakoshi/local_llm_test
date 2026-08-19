const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 600;

const invaderWidth = 40;
const invaderHeight = 30;
const invaderPadding = 10;
const invaderOffsetX = 50;
const invaderOffsetY = 50;
const invaderRowCount = 5;
const invaderColumnCount = 10;
const invaders = [];

let invaderSpeed = 2;
let currentDirection = 1; // 1 for right, -1 for left

function createInvaders() {
    for (let row = 0; row < invaderRowCount; row++) {
        invaders[row] = [];
        for (let col = 0; col < invaderColumnCount; col++) {
            invaders[row][col] = {
                x: 0,
                y: 0,
                status: 1
            };
        }
    }
}

function drawInvaders() {
    for (let row = 0; row < invaderRowCount; row++) {
        for (let col = 0; col < invaderColumnCount; col++) {
            if (invaders[row][col].status === 1) {
                const x = col * (invaderWidth + invaderPadding) + invaderOffsetX;
                const y = row * (invaderHeight + invaderPadding) + invaderOffsetY;
                invaders[row][col].x = x;
                invaders[row][col].y = y;
                ctx.fillStyle = 'green';
                ctx.fillRect(x, y, invaderWidth, invaderHeight);
            }
        }
    }
}

function updateInvaders() {
    let edgeHit = false;

    for (let row = 0; row < invaderRowCount; row++) {
        for (let col = 0; col < invaderColumnCount; col++) {
            const invader = invaders[row][col];
            if (invader.status === 1) {
                if (invader.x + invaderWidth >= canvas.width || invader.x <= 0) {
                    edgeHit = true;
                }
            }
        }
    }

    if (edgeHit) {
        currentDirection *= -1;
        for (let row = 0; row < invaderRowCount; row++) {
            for (let col = 0; col < invaderColumnCount; col++) {
                const invader = invaders[row][col];
                if (invader.status === 1) {
                    invader.y += invaderHeight + invaderPadding;
                }
            }
        }
    }

    for (let row = 0; row < invaderRowCount; row++) {
        for (let col = 0; col < invaderColumnCount; col++) {
            const invader = invaders[row][col];
            if (invader.status === 1) {
                invader.x += invaderSpeed * currentDirection;
            }
        }
    }
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawInvaders();
    updateInvaders();
    requestAnimationFrame(gameLoop);
}

createInvaders();
gameLoop();
