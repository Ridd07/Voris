$(document).ready(function () {
    console.log("Document ready - initializing components...");

    eel.init()()
    // Standard text animation
    $(".text").textillate({
        loop: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" },
    });

    // Siri message animation
    $(".siri-message").textillate({
        loop: true,
        sync: false,
        in: {
            effect: "fadeInUp",
            delay: 50,
        },
        out: {
            effect: "fadeOutUp",
            delay: 50,
        },
    });

    // Siri Wave initialization with error handling
    try {
        const siriContainer = document.getElementById("siri-container");

        if (!siriContainer) {
            console.error("Error: siri-container element not found!");
            return;
        }

        if (typeof SiriWave === 'undefined') {
            console.error("Error: SiriWave library not loaded!");
            return;
        }

        console.log("Initializing SiriWave...");
        const siriWave = new SiriWave({
            container: siriContainer,
            width: 800,
            height: 200,
            style: "ios9",
            amplitude: 1.5,
            speed: 0.2,
            autostart: true
        });

        console.log("SiriWave initialized successfully!", siriWave);

    } catch (error) {
        console.error("Error initializing SiriWave:", error);
    }

    //mic button click event
    $("#MicBtn").click(function () {
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);

        // Clear previous message immediately
        $(".siri-message .texts li").text("Listening...");
        $('.siri-message').textillate('start');

        eel.allCommands()()

    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the  same time

        if (e.key.toLowerCase() === 'v' && e.ctrlKey && e.shiftKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            $("#SiriWave").show();

            // Clear previous message immediately
            $(".siri-message .texts li").text("Listening...");
            $('.siri-message').textillate('start');

            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message)();
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#sendBtn").attr('hidden', true);
        }
    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#sendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#sendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    });

    $("#sendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)
    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }

    });
});