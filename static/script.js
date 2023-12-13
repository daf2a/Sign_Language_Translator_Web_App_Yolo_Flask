//Updating Frames in Image tag to Show Video Stream
window.addEventListener('load', function () {
    console.log("Window UP")
    // document.getElementById("videoElement").src = "/video_feed"
    // clearTerminal();
    // stopProcess("");
});
var show_ad = false;

$(document).ready(function () {


    $("#banner2").hide();
    $("#closeAd").click(function () {
        $("#banner2").hide(1000);
    });
});

function startCamera() {
    var url = '0';
    $('#urlForm').attr('action', '/index'); // Set the form action to /index
    $('#urlForm').attr('method', 'POST'); // Set the form method to POST
    $('#urlForm').find('#url').val(url); // Set the URL value in the form
    $('#urlForm').submit(); // Submit the form
}

function startVideo() {
    var url = $('#url').val();
    $('#urlForm').attr('action', '/index'); // Set the form action to /index
    $('#urlForm').attr('method', 'POST'); // Set the form method to POST
    $('#urlForm').find('#url').val(url); // Set the URL value in the form
    $('#urlForm').submit(); // Submit the form
}

function stopProcess(message) {
    console.log("Stop BUTTON");
    const terminalData = document.getElementById('terminal').innerHTML;
    document.getElementById('terminal').innerHTML = terminalData + "<br><br><center>" + message + "</center><br><br>";
    fetch('/stop_process')
        .then(response => response.text())
        .then(message => {
            console.log(message);
            // Redirect to homepage after stopping the process
            window.location.href = '/';
        })
        .catch(error => console.error(error));
}


//This Code is used to Communicate b/w Client & Server via SOCKETIO
var socket = io.connect('http://127.0.0.1:5000/');

// Variabel untuk menyimpan kata-kata berturut-turut
let consecutiveWords = [];
let finalSentence = "";
let wordCounter = 0;

function appendToTerminal(message) {
    var terminal = document.getElementById("terminal");
    var p = document.createElement("p");
    p.innerHTML = `<table class="table table-striped text-center" style="border: none;">
                    <tr class="row">
                        <td class="col-md-6" style="color: #01ECEC; border: none;">${message[0]}</td>
                        <td class="col-md-6" style="color: #01ECEC; border: none;">${message[1]}</td>
                    </tr>
                </table>`;
    terminal.appendChild(p);
    terminal.scrollTop = terminal.scrollHeight;

    if (consecutiveWords.length === 0 || consecutiveWords[consecutiveWords.length - 1] === message[0]) {
        consecutiveWords.push(message[0]);
        wordCounter++; // Menambah jumlah kemunculan kata yang sama
    } else {
        consecutiveWords = [message[0]];
        wordCounter = 1; // Mengatur ulang jumlah kemunculan kata yang sama
    }

    if (wordCounter >= 10) {
        finalSentence += (finalSentence.length > 0 ? " " : "") + consecutiveWords[0];
        document.getElementById("finalSentencePara").innerText = finalSentence;
        consecutiveWords = [];
        wordCounter = 0;
    }

    if (show_ad) {
        let className = message[0];
        $('#banner2').show(1000);
        $("#spanTxt").text(className);
        $(".no-link").prop("href", "https://www.amazon.com/s?k=" + className);
    }
}

//Updating Terminal with Detected Objects
socket.on("label", (data) => {
    appendToTerminal(data);
});

//Code For All Switches
function toggleHSwitch() {
    var switchElement = $("#flip-horizontal");
    var switchIsOn = switchElement.is(":checked");

    if (switchIsOn) {
        console.log("SWITCH ON")
        $.getJSON("/request_flipH_switch", function (data) {
            console.log("Switch on request sent.");
        });
    } else {
        console.log("SWITCH OFF")
        $.getJSON("/request_flipH_switch", function (data) {
            console.log("Switch off request sent.");
        });
    }
}

function toggleMediaPipeSwitch() {
    var switchElement = $("#mediapipe");
    var switchIsOn = switchElement.is(":checked");

    if (switchIsOn) {
        console.log("SWITCH ON")
        $.getJSON("/request_mediapipe_switch", function (data) {
            console.log("Switch on request sent.");
        });
    } else {
        console.log("SWITCH OFF")
        $.getJSON("/request_mediapipe_switch", function (data) {
            console.log("Switch off request sent.");
        });
    }
}

function toggleDetSwitch() {

    var switchElement = $("#run_detection");
    var switchIsOn = switchElement.is(":checked");

    if (switchIsOn) {
        console.log("SWITCH ON")
        $.getJSON("/request_run_model_switch", function (data) {
            console.log("Switch on request sent.");
        });
    } else {
        console.log("SWITCH OFF")
        $.getJSON("/request_run_model_switch", function (data) {
            console.log("Switch off request sent.");
        });
    }
}

function toggleOffSwitch() {
    var switchElement = $("#turn_off");
    var switchIsOn = switchElement.is(":checked");

    if (switchIsOn) {
        console.log("Camera ON")
        $.getJSON("/request_preview_switch", function (data) {
            console.log("Switch on request sent.");
        });
    } else {
        console.log("Camera OFF")
        $.getJSON("/request_preview_switch", function (data) {
            console.log("Switch off request sent.");
        });
    }
}

$(document).ready(function () {
    // Get the slider element
    var slider = $('#slider');

    // Attach the event listener to the slider element
    slider.on('input', function () {
        // Get the value of the slider
        var sliderValue = slider.val();

        // Call the updateSliderValue() function and pass in the slider value
        updateSliderValue(sliderValue);
    });
});


function updateSliderValue(sliderValue) {
    console.log(sliderValue)
    $.ajax({
        type: 'POST',
        url: '/update_slider_value',
        data: {'sliderValue': sliderValue},
        success: function () {
            console.log('Slider value updated successfully!');
        },
        error: function () {
            console.log('Error updating slider value!');
        }
    });
    document.getElementById("conf_display").innerHTML = sliderValue
}

function toggleTheme() {
    if (document.body.classList.contains("dark"))
        document.body.classList.remove("dark");
    else
        document.body.classList.add("dark");
}