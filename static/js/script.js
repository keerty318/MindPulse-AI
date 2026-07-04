
// for making the forms invisible,like one behind another(cascading)





function nextStep(current, next) {

    document.getElementById(
        "step" + current
    ).style.display = "none";

    document.getElementById(
        "step" + next
    ).style.display = "block";

}


// Study Hours

const studySlider =
    document.getElementById("studyHours");
// for slider color
    updateSliderFill(studySlider);

const studyValue =
    document.getElementById("studyValue");

studySlider.addEventListener("input", function () {

    studyValue.innerText =
        this.value + " Hours";
    
    // used for slider color to grow or shrink
     updateSliderFill(this);


});


// Attendance

const attendanceSlider =
    document.getElementById("attendance");

updateSliderFill(attendanceSlider);

const attendanceValue =
    document.getElementById("attendanceValue");

attendanceSlider.addEventListener("input", function () {

    attendanceValue.innerText =
        this.value + "%";

     updateSliderFill(this);


});


// Sleep Hours

const sleepSlider =
    document.getElementById("sleepHours");
updateSliderFill(sleepSlider);

const sleepValue =
    document.getElementById("sleepValue");

sleepSlider.addEventListener("input", function () {

    sleepValue.innerText =
        this.value + " Hours";

     updateSliderFill(this);


});


// Phone Usage

const phoneSlider =
    document.getElementById("phoneUsage");
updateSliderFill(phoneSlider);

const phoneValue =
    document.getElementById("phoneValue");

phoneSlider.addEventListener("input", function () {

    phoneValue.innerText =
        this.value + " Hours";

     updateSliderFill(this);


});


// Breaks

const breakSlider =
    document.getElementById("breaks");
updateSliderFill(breakSlider);

const breakValue =
    document.getElementById("breakValue");

breakSlider.addEventListener("input", function () {

    breakValue.innerText =
        this.value + " Breaks";

     updateSliderFill(this);


});

// slider colour
function updateSliderFill(slider){

    const percentage =
    ((slider.value - slider.min) /
    (slider.max - slider.min)) * 100;

    slider.style.background =
    `linear-gradient(
        90deg,
        #4338ca 0%,
        #06b6d4 ${percentage}%,
        #e5e7eb ${percentage}%,
        #e5e7eb 100%
    )`;
}

// Stress Level

const stressSlider =
    document.getElementById("stressLevel");

updateSliderFill(stressSlider);

const stressValue =
    document.getElementById("stressValue");

stressSlider.addEventListener("input", function () {

    stressValue.innerText =
        this.value;

    updateSliderFill(this);

});


// Focus Score

const focusSlider =
    document.getElementById("focusScore");

updateSliderFill(focusSlider);

const focusValue =
    document.getElementById("focusValue");

focusSlider.addEventListener("input", function () {

    focusValue.innerText =
        this.value;

    updateSliderFill(this);

});


// Social Media Hours

const socialSlider =
    document.getElementById("socialMedia");

updateSliderFill(socialSlider);

const socialValue =
    document.getElementById("socialValue");

socialSlider.addEventListener("input", function () {

    socialValue.innerText =
        this.value + " Hours";

    updateSliderFill(this);

});


// YouTube Hours

const youtubeSlider =
    document.getElementById("youtubeHours");

updateSliderFill(youtubeSlider);

const youtubeValue =
    document.getElementById("youtubeValue");

youtubeSlider.addEventListener("input", function () {

    youtubeValue.innerText =
        this.value + " Hours";

    updateSliderFill(this);

});


// Gaming Hours

const gamingSlider =
    document.getElementById("gamingHours");

updateSliderFill(gamingSlider);

const gamingValue =
    document.getElementById("gamingValue");

gamingSlider.addEventListener("input", function () {

    gamingValue.innerText =
        this.value + " Hours";

    updateSliderFill(this);

});
