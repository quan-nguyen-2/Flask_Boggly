const submittedWords = [];

document.querySelector('#submit').addEventListener('click', function(e){
    e.preventDefault();
    const word = document.querySelector('#word').value;
    document.querySelector('#word').value = ""
    checkDuplo(word);
});

function checkDuplo(word){
    if (submittedWords.includes(word)){
        let msg = `${word} already used`;
        const p = document.querySelector('#result');
        p.innerText = msg;
        return false;
    } else {
        sendWord(word);
    }
}

async function sendWord(word){
    const result = await axios.get('/submission', {params: {word: word}});
    handleResult(result, word);
}

async function sendScore(){
    await axios.post('/endgame', {score: score});
}

function handleResult(result, word){
    postMessage(result, word);
    if (result.data.result === "ok"){
        submittedWords.push(word);
        postScore(word);
    }
}

function postMessage(result, word){
    const accepted = result.data.result;
    let msg = ''
    if (accepted === "ok"){
        msg = `${word} accepted!`;
    } else if (accepted === "not-on-board"){
        msg = `${word} is not on the board`;
    } else {
        msg = `${word} is not a word`;
    }
    const p = document.querySelector('#result');
    p.innerText = msg;
}

let score = 0

function postScore(word){
    const newScore = word.length;
    score += newScore;
    document.querySelector('#score').innerText = score;
}

document.querySelector('#start').addEventListener('click', function(e){
    $('.row').css('display', 'table-row');
    e.target.remove();
    count = setInterval(countdown, 1000);
})

let clock = 60;

function countdown(){
    clock --;
    document.querySelector('#time').innerText = clock;
    if (clock === 0){
        document.querySelector('#submit').disabled = true;
        clearInterval(count);
        alert("Time is up!");
        sendScore();
    }
}