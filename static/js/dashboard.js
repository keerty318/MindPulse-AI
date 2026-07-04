// for meters in dashboard -prosuctivity,wellness,burnout,distraction
document.addEventListener("DOMContentLoaded", function(){

    const meters =
    document.querySelectorAll(".meter-fill");

    meters.forEach(meter => {

        const score =
        meter.dataset.score;

        meter.style.width =
        score + "%";

    });

});

// for radar chart visualization

// Radar Chart for visualizing student performance

const radarCanvas =
document.getElementById("performanceRadar");

// Create chart only if radar canvas exists

if(radarCanvas){

    new Chart(radarCanvas, {

        // Radar chart type

        type: "radar",

        data: {

            // Performance dimensions

            labels: [

                "Study",
                "Sleep",
                "Focus",
                "Attendance",
                "Stress",
                "Exercise"

            ],

            datasets: [{

                // Student performance values

                label: "Student Profile",

                data: [

                    radarCanvas.dataset.study,

                    radarCanvas.dataset.sleep,

                    radarCanvas.dataset.focus,

                    radarCanvas.dataset.attendance,

                    radarCanvas.dataset.stress,

                    radarCanvas.dataset.exercise

                ],

                // Styling for radar area

                borderColor:"#4338ca",

                backgroundColor:
                "rgba(67,56,202,0.2)",

                borderWidth:2

            }]

        },

        options: {
            maintainAspectRatio:false,
            plugins: {

                legend: {

                 display: false

                }

            },

            scales: {

                r: {

                    // Radar chart range

                    min:0,

                    max:100

                }

            }

        }

    });

}


// improvement html page
// WHAT IF SIMULATOR


const simulateBtn =
document.getElementById("simulateBtn");

if(simulateBtn){

    simulateBtn.addEventListener("click", function(){

        fetch("/simulate", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                sleep_hours:
                document.getElementById("sleepSlider").value,

                study_hours:
                document.getElementById("studySlider").value,

                exercise_minutes:
                document.getElementById("exerciseSlider").value,

                phone_usage_hours:
                document.getElementById("phoneSlider").value,

                focus:
                document.getElementById("focusSlider").value

            })

        })

        .then(response => response.json())

        .then(data => {

            console.log(data);

            document.getElementById(
                "predictedScore"
            ).innerText =
            data.predicted_score;

            const currentScore =
            parseFloat(
                document.getElementById(
                    "currentScore"
                ).innerText
            );

            const gain =
            data.predicted_score -
            currentScore;

            const improvementValue =
            document.getElementById(
                "improvementValue"
            );

            const improvementCard =
            document.querySelector(
                ".improvement-card"
            );

            if(gain >= 0){

                improvementValue.innerText =
                "+" + gain.toFixed(2);

                improvementValue.style.color =
                "#10b981";

                improvementCard.style.border =
                "2px solid #10b981";

            }
            else{

                improvementValue.innerText =
                gain.toFixed(2);

                improvementValue.style.color =
                "#ef4444";

                improvementCard.style.border =
                "2px solid #ef4444";

            }

        });

    });

}

/* =====================================
   LIVE SLIDER VALUES
===================================== */

const sleepSlider =
document.getElementById("sleepSlider");

const studySlider =
document.getElementById("studySlider");

const exerciseSlider =
document.getElementById("exerciseSlider");

const phoneSlider =
document.getElementById("phoneSlider");

const focusSlider =
document.getElementById("focusSlider");

if(sleepSlider){

    sleepSlider.addEventListener("input", () => {

        document.getElementById(
            "sleepValue"
        ).innerText =
        sleepSlider.value + " h";

    });

    studySlider.addEventListener("input", () => {

        document.getElementById(
            "studyValue"
        ).innerText =
        studySlider.value + " h";

    });

    exerciseSlider.addEventListener("input", () => {

        document.getElementById(
            "exerciseValue"
        ).innerText =
        exerciseSlider.value + " min";

    });

    phoneSlider.addEventListener("input", () => {

        document.getElementById(
            "phoneValue"
        ).innerText =
        phoneSlider.value + " h";

    });

    focusSlider.addEventListener("input", () => {

        document.getElementById(
            "focusValue"
        ).innerText =
        focusSlider.value;

    });

}


// this is for slider filler colour till thumb (round)colour comes remaining  is white
function updateSliderFill(slider){

    const percentage =
    ((slider.value - slider.min) /
    (slider.max - slider.min)) * 100;

    slider.style.background =
    `linear-gradient(
        to right,
        #4338ca 0%,
        #06b6d4 ${percentage}%,
        #e2e8f0 ${percentage}%,
        #e2e8f0 100%
    )`;
}
[
 sleepSlider,
 studySlider,
 exerciseSlider,
 phoneSlider,
 focusSlider
].forEach(slider => {

    if(slider){

        updateSliderFill(slider);

        slider.addEventListener(
            "input",
            () => updateSliderFill(slider)
        );
    }
});

// AI Insights Button

const insightBtn =
document.getElementById(
    "generateInsightsBtn"
);

if(insightBtn){

    insightBtn.addEventListener(
        "click",

        function(){

            document.getElementById(
                "aiResponse"
            ).innerText =
            "Generating AI Insights...";

            fetch(
                "/generate_insights",
                {
                    method:"POST"
                }
            )

            .then(
                response =>
                response.json()
            )

            .then(data => {

                document.getElementById(
                    "aiResponse"
                ).innerHTML =
                data.response;

            })

            .catch(error => {

                document.getElementById(
                    "aiResponse"
                ).innerText =
                "Unable to generate insights.";

                console.log(error);

            });

        }

    );

}

// AI ROADMAP BUTTON FUNC
// AI Roadmap

const roadmapBtn =
document.getElementById(
    "generateRoadmapBtn"
);

if(roadmapBtn){

    roadmapBtn.addEventListener(
        "click",

        function(){

            document.getElementById(
                "roadmapResponse"
            ).innerHTML =
            "Generating AI Roadmap...";

            fetch(
                "/generate_roadmap",
                {
                    method:"POST"
                }
            )

            .then(
                response =>
                response.json()
            )

            .then(data => {

                document.getElementById(
                    "roadmapResponse"
                ).innerText =
                data.response;

            })

            .catch(error => {

                document.getElementById(
                    "roadmapResponse"
                ).innerText =
                "Unable to generate roadmap.";

                console.log(error);

            });

        }

    );

}
// ---------------------------------------------------------------------------------------------------------------------------------------------------

// for chat bot
// AI Coach

// Get Send button
const sendBtn = document.getElementById("send-btn");

// Run only if AI Coach page is opened
if (sendBtn) {

    // Get input box and chat area
    const userInput = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");

    // Send message when button is clicked
    sendBtn.addEventListener("click", sendMessage);

    // Send message when Enter key is pressed
    userInput.addEventListener("keypress", function (event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    });

    function sendMessage() {

        // Read user's message
        const message = userInput.value.trim();

        // Don't send empty messages
        if (message === "") {

            return;

        }

        // Add user message to chat
        chatContainer.innerHTML += `
        <div class="message user-message">
            <div class="message-content">
                <p>${message}</p>
            </div>
        </div>
        `;

        // Clear input box
        userInput.value = "";

        // Scroll to latest message
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Show temporary thinking message
        chatContainer.innerHTML += `
        <div class="message ai-message" id="thinking">
            <div class="avatar">
                🤖
            </div>

            <div class="message-content">
                <h4>MindPulse AI</h4>
                <p>Thinking...</p>
            </div>
        </div>
        `;

        // Scroll again
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Send user message to Flask
        fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        })

        .then(response => response.json())

        .then(data => {

            // Remove thinking message
            document.getElementById("thinking").remove();

            // Display AI reply
            chatContainer.innerHTML += `
            <div class="message ai-message">

                <div class="avatar">
                    🤖
                </div>

                <div class="message-content">
                    <h4>MindPulse AI</h4>
                    <div>${marked.parse(data.reply)}</div>
                    
                </div>

            </div>
            `;

            // Scroll to latest message
            chatContainer.scrollTop = chatContainer.scrollHeight;

        })

        .catch(error => {

            console.log(error);

        });

    }

}
