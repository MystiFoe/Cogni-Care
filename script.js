var counter = 0;
    var numberA;
    var numberB;
    var result;
    var timer;
 
    var problem = document.querySelector(".problem");
    var answers = document.querySelector(".answers").children;
    var remaining = document.querySelector(".remaining");
    var score = document.querySelector(".score");
    var button = document.querySelector('.pfc');
 
    var randomNum = function(max, min) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    };
 
    var countdown = function() {
        var increment = 99;
            timer = setInterval(function(){
            remaining.style.width = increment + "%";
            increment -= 1;
            if (remaining.style.width === "0%") {
                alert("Game over!");
                newGame();
            }
        }, 1000);
    };
 
 
    var placeNumbers = function(){
        problem.innerHTML = numberA + " x " + numberB;
        answers[randomNum(3, 0)].innerHTML = result;
        for (var i = 0; i < answers.length; i++) {
            if (answers[i].innerHTML === "") {
                if (result > 100) {
                    answers[i].innerHTML = result + i + 10;
                } else {
                    answers[i].innerHTML = result + i + 1;
                }
            }
        }
    };
 
    var newGame = function() {
        clearInterval(timer);
        problem.innerHTML = "";
        for (var i = 0; i < answers.length; i++) {
            answers[i].innerHTML = "";
        }
        button.disabled = false;
        alert("Your score is " + counter);
        remaining.style.width = "100%";
        score.innerHTML = "Score: 0";
        counter = 0;
    }
 
    var click = function(e) {
        if (e.target.innerHTML == result) {
            for (var i = 0; i < answers.length; i++) {
                answers[i].innerHTML = "";
            }
            counter++;
            score.innerHTML = "Score: " + counter;
            generateNumber();
        } else {
            alert("You lost!");
            newGame();
        }
    };
 
 
    var generateNumber = function(){
        button.disabled = true;
 
        for (var i = 0; i < answers.length; i++) {
            answers[i].addEventListener("click", click, false);
        }
 
        if (counter < 8) {
            numberA = randomNum(9, 2);
            numberB = randomNum(9, 2);
            result = numberA * numberB;
            placeNumbers();
 
        } else if (counter < 15) {
            numberA = randomNum(15, 5);
            numberB = randomNum(15, 5);
            result = numberA * numberB;
            placeNumbers();
 
        } else if (counter < 20) {
            numberA = randomNum(25, 7);
            numberB = randomNum(25, 7);
            result = numberA * numberB;
            placeNumbers();
 
        } else {
            numberA = randomNum(35, 15);
            numberB = randomNum(35, 15);
            result = numberA * numberB;
            placeNumbers();
        }
    };
 
 
    button.addEventListener("click", function(){
        countdown();
        generateNumber();
    });