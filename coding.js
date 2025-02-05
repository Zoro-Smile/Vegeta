function appendNumber(number) {
    const screen = document.getElementById('screen');
    screen.value += number;
}

function appendOperator(operator) {
    const screen = document.getElementById('screen');
    screen.value += ' ' + operator + ' ';
}

function clearScreen() {
    const screen = document.getElementById('screen');
    screen.value = '';
}

function calculate() {
    const screen = document.getElementById('screen');
    try {
        screen.value = eval(screen.value);
    } catch (error) {
        screen.value = 'Error';
    }
}