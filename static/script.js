let time = 25 * 60;

let timerRunning = false;

let interval;

function updateDisplay() {

    const timer = document.getElementById("timer");

    let minutes = Math.floor(time / 60);
    let seconds = time % 60;

    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    timer.innerText = `${minutes}:${seconds}`;
}

function startTimer() {

    if (timerRunning) {
        return;
    }

    timerRunning = true;

    interval = setInterval(() => {

        time--;

        updateDisplay();

        if (time <= 0) {

            clearInterval(interval);

            document.getElementById("timer").innerText = "Selesai!";

            timerRunning = false;

            time = 25 * 60;
        }

    }, 1000);
}

function pauseTimer() {

    clearInterval(interval);

    timerRunning = false;
}

updateDisplay();