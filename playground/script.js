const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 600;

class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 50;
        this.height = 20;
        this.color = '#0f0';
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    moveLeft() {
        this.x -= 5;
    }

    moveRight() {
        this.x += 5;
    }
}

class Enemy {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 40;
        this.height = 20;
        this.color = '#f00';
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    moveDown() {
        this.y += 5;
    }

    resetPosition() {
        this.x = Math.random() * (canvas.width - this.width);
        this.y = 30;
    }
}

class Bullet {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 5;
        this.height = 10;
        this.color = '#0ff';
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    moveUp() {
        this.y -= 5;
    }
}

const player = new Player(canvas.width / 2 - 25, canvas.height - 30);
let enemies = [];
let bullets = [];

for (let i = 0; i < 5; i++) {
    enemies.push(new Enemy(i * 70 + 30, 30));
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    player.draw();

    enemies.forEach((enemy, index) => {
        enemy.draw();
        enemy.moveDown();

        if (enemy.y > canvas.height) {
            enemies.splice(index, 1);
            enemies.push(new Enemy(Math.random() * (canvas.width - enemy.width), 30));
        }
    });

    bullets.forEach((bullet, index) => {
        bullet.draw();
        bullet.moveUp();

        if (bullet.y < 0) {
            bullets.splice(index, 1);
        }
    });
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        player.moveLeft();
    } else if (e.key === 'ArrowRight') {
        player.moveRight();
    } else if (e.key === ' ') {
        bullets.push(new Bullet(player.x + player.width / 2 - 2.5, player.y));
    }
});

setInterval(draw, 1000 / 60);
