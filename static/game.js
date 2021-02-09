/** Game class tracks valid words and total score */
class Game {

    constructor() {
        this.wordList = [];
        this.score = 0;
        this.game_over = false;
    }

    async get_final_info() {
        const response = await axios({
            url: '/final-score',
            method: 'POST',
            data: {score: this.score}
        });

        return response;
    }

    static async get_verdict(word) {
        const response = await axios({
            url: `/check-word/${word}`,
            method: "GET"
        })
        return response;
    }

}