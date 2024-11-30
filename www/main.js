$(document).ready(function () {
    // Initialize text animation
    $('.text').textillate({
        loop: true,
        minDisplayTime: 2000,
        initialDelay: 1000,
        in: {
            effect: "bounceIn",
            delayScale: 1.5,
            delay: 50
        },
        out: {
            effect: "bounceOut",
            delayScale: 1.5,
            delay: 50,
            sync: true
        },
        autoStart: true
    });

    // SiriWave configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    // Siri message text animation
    $('.siri-message').textillate({
        loop: true,
        minDisplayTime: 2000,
        initialDelay: 1000,
        in: {
            effect: "fadeIn",
            delayScale: 0.5,
            delay: 10,
            sync: true
        },
        out: {
            effect: "fadeOut",
            delayScale: 0.5,
            delay: 10,
            sync: true
        },
        autoStart: true
    });

    // Mic button click event
    $("#MicBtn").click(function () {
        eel.playAssetSound('start_sound');  // Play sound
        $("#Oval").attr("hidden", true);
        $("#Siri-Wave").attr("hidden", false);
        eel.allCommands();  // Start voice commands
    });

    // Keyup event for Ctrl + B
    function doc_keyUp(e) {
        console.log("Key pressed:", e.key);  // Log key press for debugging

        // Check if Windows key + B is pressed
        if (e.key === 'b' && e.getModifierState('Meta')) {  // 'Meta' represents the Windows key in JavaScript
            console.log("Win + B pressed");
            eel.playAssistantSound();  // Play sound when Win + B is pressed
            $("#Oval").attr("hidden", true);
            $("#Siri-Wave").attr("hidden", false);
            eel.allCommands();  // Trigger the allCommands function in Python
        }
    }

    function PlayAssistant(message) {
        if (message != "") {
            $("#Oval").attr("hidden", true);
            $("#Siri-Wave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#Sendbtn").attr('hidden', true);  // Corrected to 'Sendbtn'
        }
    }

    // Toggle function to hide and display mic and send button
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#Sendbtn").attr('hidden', true);  // Corrected to 'Sendbtn'
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#Sendbtn").attr('hidden', false);  // Corrected to 'Sendbtn'
        }
    }

    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // Send button event handler
    $("#Sendbtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // Enter press event handler on chatbox
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {  // Enter key is pressed
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    // Add the keyup event listener for Ctrl + B
    document.addEventListener('keyup', doc_keyUp, false);
});
