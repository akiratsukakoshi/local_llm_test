const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const playerWidth = 50;
const playerHeight = 10;
const playerSpeed = 5;
let playerX = (canvas.width - playerWidth) / 2;

const invaderWidth = 30;
const invaderHeight = 30;
const invaderSpeed = 2;
let invaders = [];
let invaderDirection = 1;

const bulletWidth = 5;
const bulletHeight = 10;
const bulletSpeed = 5;
let bullets = [];

function drawPlayer() {
    ctx.fillStyle = '#00f';
    ctx.fillRect(playerX, canvas.height - playerHeight, playerWidth, playerHeight);
}

function drawInvaders() {
    ctx.fillStyle = '#f00';
    invaders.forEach(invader => {
        ctx.fillRect(invader.x, invader.y, invaderWidth, invaderHeight);
    });
}

function drawBullets() {
    ctx.fillStyle = '#ff0';
    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bulletWidth, bulletHeight);
    });
}

function movePlayer(event) {
    if (event.key === 'ArrowLeft') {
        playerX -= playerSpeed;
        if (playerX < 0) playerX = 0;
    } else if (event.key === 'ArrowRight') {
        playerX += playerSpeed;
        if (playerX + playerWidth > canvas.width) playerX = canvas.width - playerWidth;
    }
}

function shootBullet(event) {
    if (event.key === ' ') {
        bullets.push({ x: playerX + playerWidth / 2 - bulletWidth / 2, y: canvas.height - playerHeight - bulletHeight });
    }
}

function moveInvaders() {
    invaders.forEach(invader => {
        invader.x += invaderSpeed * invaderDirection;
    });

    const rightmostInvader = Math.max(...invaders.map(invader => invader.x + invaderWidth));
    const leftmostInvader = Math.min(...invaders.map(invader => invader.x));

    if (rightmostInvader >= canvas.width || leftmostInvader <= 0) {
        invaderDirection *= -1;
        invaders.forEach(invader => invader.y += invaderHeight);
    }
}

function moveBullets() {
    bullets.forEach((bullet, index) => {
        bullet.y -= bulletSpeed;
        if (bullet.y < 0) {
            bullets.splice(index, 1);
        }
    });
}

function checkCollisions() {
    bullets.forEach((bullet, bulletIndex) => {
        invaders.forEach((invader, invaderIndex) => {
            if (
                bullet.x < invader.x + invaderWidth &&
                bullet.x + bulletWidth > invader.x &&
                bullet.y < invader.y + invaderHeight &&
                bullet.y + bulletHeight > invader.y
            ) {
                bullets.splice(bulletIndex, 1);
                invaders.splice(invaderIndex, 1);
            }
        });
    });
}

function initInvaders() {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 10; col++) {
            invaders.push({
                x: col * (invaderWidth + 10) + 50,
                y: row * (invaderHeight + 10) + 50
            });
        }
    }
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPlayer();
    drawInvaders();
    drawBullets();
    moveInvaders();
    moveBullets();
    checkCollisions();
    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', movePlayer);
document.addEventListener('keydown', shootBullet);

initInvaders();
gameLoop();
