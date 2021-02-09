const $form = $("#word-form");
const $scoreBox = $("#score-div");
const $timer = $("#timer-div");

let seconds_left = 60;

const game = new Game()
// let score = 0;

// let game_over = false;
// const wordList = [];

function get_html_msg(word, result) {
    const messages = {
        'ok': `${word}: ${word.length} points`,
        'not-word': `${word} is not a valid word`,
        'not-on-board': `${word} is not on this board`,
        'duplicate': `${word} has already been found`
    }
    return `<p>${messages[result]}</p>`;
}

function update_score_box(word, result, game_over) {
    $scoreBox.empty();
    let msg;
    const score_msg = `<h3>Score: ${game.score}</h3>`;
    if (game_over) {
        msg = 'Game over!';
    } else {
        msg = get_html_msg(word, result);
    }
    $scoreBox.append(score_msg + msg);
}

function update_data(word, result) {
    if (result === 'ok' && !game.wordList.includes(word)) {
        game.score += word.length;
        game.wordList.push(word);
    }
}

async function handleWord(e) {
    e.preventDefault();
    const word = $("#word").val();
    const result = await Game.get_verdict(word);
    let res_str = result.data.result;
    if (res_str === 'ok' && game.wordList.includes(word)) {
        res_str = 'duplicate';
    }
    update_data(word, res_str);
    update_score_box(word, res_str);
    $("#word").val('');
    $("#word").focus();
}

$form.on("submit", handleWord);

async function handle_end_game() {
    $("#word").attr("disabled", "disabled");
    game.game_over = true;
    update_score_box("", "", game.game_over);
    const response = await game.get_final_info();
    $form.hide();
    $timer.hide();
    const {congrats, count, high_score} = response.data;
    if (congrats) {
        $scoreBox.append(`<h2>New High Score!!</h2>`);
    } else {
        $scoreBox.append(`<p>Your high score is ${high_score}</p>`);
    }
    $scoreBox.append(`<p>You have completed ${count} games</p>`);
    $scoreBox.append(`<p>Refresh the page to play again</p>`);
}

function update_timer() {
    seconds_left--;
    if (seconds_left < 0) {
        clearInterval(interval);
        handle_end_game();
    } else {
        $("#timer").text(seconds_left);
    }
}

const interval = setInterval(update_timer, 1000);