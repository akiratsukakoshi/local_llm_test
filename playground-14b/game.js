const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const player = {
  x: canvas.width / 2,
  y: canvas.height - 50,
  width: 50,
  height: 20,
  speed: 5,
  color: '#0f0'
};

const invaders = [];
const invaderWidth = 30;
const invaderHeight = 20;
const invaderSpeed = 2;
const rows = 3;
const cols = 10;

for (let row = 0; row < rows; row++) {
  for (let col = 0; col < cols; col++) {
    invaders.push({
      x: col * (invaderWidth + 10) + 20,
      y: row * (invaderHeight + 10) + 20,
      width: invaderWidth,
      height: invaderHeight,
      color: '#f00'
    });
  }
}

const bullets = [];
const bulletSpeed = 5;

function drawPlayer() {
  ctx.fillStyle = player.color;
  ctx.fillRect(player.x, player.y, player.width, player.height);
}

function drawInvaders() {
  invaders.forEach(invader => {
    ctx.fillStyle = invader.color;
    ctx.fillRect(invader.x, invader.y, invader.width, invader.height);
  });
}

function drawBullets() {
  bullets.forEach(bullet => {
    ctx.fillStyle = '#0ff';
    ctx.fillRect(bullet.x, bullet.y, 5, 10);
  });
}

function updateInvaders() {
  invaders.forEach(invader => {
    invader.x += invaderSpeed;
    if (invader.x + invader.width > canvas.width || invader.x < 0) {
      invaderSpeed *= -1;
      invaders.forEach(invader => invader.y += invaderHeight + 10);
    }
  });
}

function updateBullets() {
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
        bullet.x < invader.x + invader.width &&
        bullet.x + 5 > invader.x &&
        bullet.y < invader.y + invader.height &&
        bullet.y + 10 > invader.y
      ) {
        bullets.splice(bulletIndex, 1);
        invaders.splice(invaderIndex, 1);
      }
    });
  });
}

function gameLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawPlayer();
  drawInvaders();
  drawBullets();
  updateInvaders();
  updateBullets();
  checkCollisions();
  requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft' && player.x > 0) {
    player.x -= player.speed;
  } else if (e.key === 'ArrowRight' && player.x < canvas.width - player.width) {
    player.x += player.speed;
  } else if (e.key === ' ') {
    bullets.push({ x: player.x + player.width / 2 - 2.5, y: player.y });
  }
});

document.addEventListener('keyup', (e) => {
  // This event listener is not strictly necessary for movement, but it can be used for other purposes
});

gameLoop();
