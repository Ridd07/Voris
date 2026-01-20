$(document).ready(function () {
    console.log("Document ready - initializing components...");

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
        eel.allCommands()()
        
    });
});