from flask import Flask, render_template,request,session
from flask import jsonify, redirect,url_for
from db import connection,cursor
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from gemini_helper import get_ai_insights
from AI_CHAT.chat_engine import get_ai_reply
import os
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


model = joblib.load(
    "model/productivity_model.pkl"
)

gender_encoder = joblib.load(
    "model/gender_encoder.pkl"
)

# helper function for db of assessment

def get_latest_assessment(user_id):

    cursor.execute(""" SELECT * FROM assessments WHERE user_id = %s ORDER BY assessment_id DESC LIMIT 1""", (user_id,))

    return cursor.fetchone()

# signup routing to n fro db
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        full_name = request.form["fullname"]

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            
            return render_template("signup.html",error="Passwords do not match!")
        
        hashed_password = generate_password_hash(password)

        cursor.execute("INSERT INTO users (full_name, username, email, password) VALUES (%s,%s,%s,%s)",(full_name, username, email, hashed_password))
        
        connection.commit()

        
        return redirect(url_for("login"))

       

    return render_template("signup.html")

# login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        cursor.execute(

            "SELECT * FROM users WHERE username = %s",

            (username,)

        )

        user = cursor.fetchone()

        if user is None:

            return render_template("login.html",error="Invalid Username!")

        if not check_password_hash(user["password"], password):

            return render_template("login.html",error="Incorrect Password!")
        
        session["user_id"] = user["id"]

        session["username"] = user["username"]

        return redirect(url_for("assessment"))

    return render_template("login.html")



# routings

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/assessment")
def assessment():
    if "user_id" not in session:

        return redirect(url_for("login"))
     
    return render_template("assessment.html")   


# we r doing this so that when analysed button is clicked it fetches everyhing with help of predict route so dashboard has got nothing
# thats why we are making dashboard also to get data from user so that it can be independent from predict

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    assessment = get_latest_assessment(session["user_id"])

    if assessment is None:
        return redirect(url_for("assessment"))

    study_score = round((assessment["study_hours"] / 12) * 100, 0)

    sleep_score = round((assessment["sleep_hours"] / 10) * 100, 0)

    focus_score = assessment["focus"]

    attendance_score = assessment["attendance_percentage"]

    stress_score = round((assessment["stress"] / 10) * 100, 0)

    exercise_score = round(
        min((assessment["exercise_minutes"] / 120) * 100, 100), 0
    )

    return render_template(

        "dashboard.html",

        productivity_score=assessment["productivity_score"],

        productivity_status=assessment["productivity_status"],

        wellness_score=assessment["wellness_score"],

        burnout_risk=assessment["burnout_risk"],

        burnout_status=assessment["burnout_status"],

        distraction_index=assessment["distraction_index"],

        distraction_status=assessment["distraction_status"],

        study_score=study_score,

        sleep_score=sleep_score,

        focus_score=focus_score,

        attendance_score=attendance_score,

        stress_score=stress_score,

        exercise_score=exercise_score,

        focus_leakage=assessment["focus_leakage"],

        digital_profile=assessment["digital_profile"],

        top_source=assessment["top_source"],

        potential_gain=assessment["potential_gain"],

        potential_productivity=assessment["potential_productivity"],

        strongest_attribute=assessment["strongest_attribute"]

    )

# chatbot route

@app.route("/ai_coach")
def ai_coach():

    return render_template("ai_coach.html")

# Route to handle chat messages sent from the AI Coach page
@app.route("/chat", methods=["POST"])
def chat():

    # Get JSON data sent from JavaScript
    data = request.get_json()

    # Extract only the user's message
    user_message = data["message"]

    # Get latest assessment from database
    assessment = get_latest_assessment(session["user_id"])

    # Student profile from latest assessment

    student_profile = f"""

    Age : {assessment["age"]}

    Study Hours : {assessment["study_hours"]}

    Sleep Hours : {assessment["sleep_hours"]}

    Phone Usage : {assessment["phone_usage_hours"]}

    Exercise Minutes : {assessment["exercise_minutes"]}

    Attendance : {assessment["attendance_percentage"]}

    Stress Level : {assessment["stress"]}

    Focus Score : {assessment["focus"]}

    Final Grade : {assessment["final_grade"]}

    Productivity Score : {assessment["productivity_score"]}

    Wellness Score : {assessment["wellness_score"]}

    Burnout Risk : {assessment["burnout_risk"]}

    Distraction Index : {assessment["distraction_index"]}

    Strongest Attribute : {assessment["strongest_attribute"]}

"""

    # Send the user's message to the AI engine and also students questionaire so that AI can gove personalised answers
    ai_reply = get_ai_reply(user_message, student_profile)

    # Send AI reply back to JavaScript
    return jsonify({"reply": ai_reply})

    # "jsonify() converts the Python response into JSON so JavaScript can read it easily."

    # print(user_message)

# improvement page
@app.route("/improvement")
def improvement():

    if "user_id" not in session:
        return redirect(url_for("login"))

    assessment = get_latest_assessment(session["user_id"])

    if assessment is None:
        return redirect(url_for("assessment"))

    return render_template(

        "improvement.html",

        current_productivity=assessment["productivity_score"],

        sleep_hours=assessment["sleep_hours"],

        study_hours=assessment["study_hours"],

        exercise_minutes=assessment["exercise_minutes"],

        phone_usage_hours=assessment["phone_usage_hours"],

        focus=assessment["focus"]

    )
    



@app.route("/simulate", methods=["POST"])
def simulate():

    if "user_id" not in session:
        return {"predicted_score": 0}

    assessment = get_latest_assessment(session["user_id"])

    data = request.get_json()

    sleep_hours = float(data["sleep_hours"])
    study_hours = float(data["study_hours"])
    exercise_minutes = float(data["exercise_minutes"])
    phone_usage_hours = float(data["phone_usage_hours"])
    focus = float(data["focus"])

    features = [[

        float(assessment["age"]),
        int(assessment["gender"]),

        study_hours,
        sleep_hours,
        phone_usage_hours,

        float(assessment["social_media"]),
        float(assessment["youtube"]),
        float(assessment["gaming"]),

        float(assessment["breaks_per_day"]),
        float(assessment["coffee"]),

        exercise_minutes,

        float(assessment["assignments_completed"]),
        float(assessment["attendance_percentage"]),
        float(assessment["stress"]),

        focus,

        float(assessment["final_grade"])

    ]]

    predicted_score = round(
        model.predict(features)[0],
        2
    )

    return {
        "predicted_score": predicted_score
    }

# this is for generating ai insights and roadmap only if the buttons are clicked so that tokens wont be wasted
@app.route("/generate_insights", methods=["POST"])
def generate_insights():

    assessment = get_latest_assessment(session["user_id"])

    student_context = f"""

    AGE:
    {assessment["age"]}

    PRODUCTIVITY SCORE:
    {assessment["productivity_score"]}

    STUDY HOURS:
    {assessment["study_hours"]}

    ATTENDANCE:
    {assessment["attendance_percentage"]}

    ASSIGNMENTS COMPLETED:
    {assessment["assignments_completed"]}

    FINAL GRADE:
    {assessment["final_grade"]}

    FOCUS SCORE:
    {assessment["focus"]}

    SLEEP HOURS:
    {assessment["sleep_hours"]}

    STRESS LEVEL:
    {assessment["stress"]}

    EXERCISE MINUTES:
    {assessment["exercise_minutes"]}

    PHONE USAGE:
    {assessment["phone_usage_hours"]}

    SOCIAL MEDIA:
    {assessment["social_media"]}

    YOUTUBE:
    {assessment["youtube"]}

    GAMING:
    {assessment["gaming"]}

    WELLNESS SCORE:
    {assessment["wellness_score"]}

    BURNOUT RISK:
    {assessment["burnout_risk"]}

    DISTRACTION INDEX:
    {assessment["distraction_index"]}

    STRONGEST ATTRIBUTE:
    {assessment["strongest_attribute"]}

    """

    ai_prompt = """

    Analyze the student profile.

    Give output exactly in this format:
    <strong>🎯 STRONGEST HABIT</strong>

    <p>Your explanation here(1 short sentence)</p>

    <strong>⚠ BIGGEST BLOCKER</strong>

    <p>Your explanation here(1 short sentence)</p>

    <strong>💡 HIDDEN INSIGHT</strong>

    <p>Your explanation here(1 short sentence)</p>

    <strong>🚀 NEXT STEP</strong>

    <p>Your explanation here(1 short sentence)</p>

    <strong>🔥 MOTIVATION</strong>

    <p>Your explanation here(1 short sentence)</p>

    Use HTML tags exactly.

    Rules:

    - Keep each explanation to 1-2 lines.
    - Leave one blank line after every heading.
    - Use the exact heading format shown above.
    - Do NOT use markdown symbols like **.
    - Do NOT use bullet points.
    - Do NOT use long paragraphs.
    - Use simple student-friendly language.
    - Maximum 100 words.
    - Make the insights feel personalized and intelligent.

    """

    try:

        ai_response = get_ai_insights(
            student_context + ai_prompt
        )

        return {
            "response": ai_response
        }

    except Exception:

        return {
            "response":
            "⚠ AI service temporarily unavailable. Please try again later."
        }

# roadmap works only if button clicked
@app.route("/generate_roadmap", methods=["POST"])
def generate_roadmap():

    assessment = get_latest_assessment(session["user_id"])

    student_context = f"""

    PRODUCTIVITY SCORE:
    {assessment["productivity_score"]}

    STUDY HOURS:
    {assessment["study_hours"]}

    ATTENDANCE:
    {assessment["attendance_percentage"]}

    FOCUS:
    {assessment["focus"]}

    SLEEP:
    {assessment["sleep_hours"]}

    STRESS:
    {assessment["stress"]}

    EXERCISE:
    {assessment["exercise_minutes"]}

    PHONE USAGE:
    {assessment["phone_usage_hours"]}

    WELLNESS SCORE:
    {assessment["wellness_score"]}

    BURNOUT RISK:
    {assessment["burnout_risk"]}

    DISTRACTION INDEX:
    {assessment["distraction_index"]}

    STRONGEST ATTRIBUTE:
    {assessment["strongest_attribute"]}

    """
    roadmap_prompt = """

    Create a personalized student success roadmap.

    Return output exactly in this format:
    

    📅 WEEK 1

    - Action 1

    - Action 2

    📅 WEEK 2

    - Action 1

    - Action 2

    📅 WEEK 3

    - Action 1

    - Action 2

    📅 WEEK 4

    - Action 1

    - Action 2

    ❤️ RECOVERY PLAN

    - Recovery tip

    - Recovery tip

    🎯 EXPECTED OUTCOME

    (1 short sentence)

    Rules:

    - Leave one blank line after every heading.
    - Use the exact heading format shown above.
    - Do NOT use markdown symbols like **.
    - Keep every action short and practical.
    - Maximum 120 words.
    - Student friendly.
    - Easy to read.
    - No long paragraphs.
    - Sound like a personal AI mentor.
    -Do NOT generate any HTML tags such as <strong>, <b>, <p>, or <br>.
     Return plain text only.

    """

    
    try:

        roadmap_response = get_ai_insights(
            student_context + roadmap_prompt
        )

        return {
            "response": roadmap_response
        }

    except Exception:

        return {
            "response":
            "⚠ AI roadmap currently unavailable."
        }






# this redirects form after clicking analyze button to dashboard html
# shows res like age etc in terminal
@app.route("/predict", methods=["POST"])
def predict():

    
    age = request.form["age"]

    gender = request.form["gender"]

    study_hours = request.form["study_hours"]

    assignments_completed = request.form["assignments_completed"]

    attendance = request.form["attendance_percentage"]

    grade = request.form["grade"]

    sleep_hours = request.form["sleep_hours"]

    stress = request.form["stress"]

    focus = request.form["focus"]

    phone_usage_hours = request.form["phone_usage_hours"]

    social_media = request.form["social_media"]

    youtube = request.form["youtube"]

    gaming = request.form["gaming"]

    breaks_per_day = request.form["breaks_per_day"]

    exercise_minutes = request.form["exercise_minutes"]

    coffee = request.form["coffee"]


    # mappings for gender,coffee,finalscore aka prev sem res
    gender = gender_encoder.transform([gender])[0]
    # final score
    grade_map = {
    "Poor": 50,
    "Average": 65,
    "Good": 80,
    "Excellent": 95
    }

    final_grade = grade_map[grade]
    # coffee
    coffee_map = {
    "None": 0,
    "Low": 125,
    "Moderate": 250,
    "High": 375,
    "Very High": 499
    }

    coffee = coffee_map[coffee]

    # features
    features = [[
    float(age),
    gender,
    float(study_hours),
    float(sleep_hours),
    float(phone_usage_hours),
    float(social_media),
    float(youtube),
    float(gaming),
    float(breaks_per_day),
    float(coffee),
    float(exercise_minutes),
    float(assignments_completed),
    float(attendance),
    float(stress),
    float(focus),
    float(final_grade)
    ]]

    prediction = model.predict(features)[0]


    # classifying the output as range for better UI

    if prediction <= 25:
        productivity_status = "Poor"

    elif prediction <= 50:
        productivity_status = "Average"

    elif prediction <= 75:
        productivity_status = "Good"

    else:
        productivity_status = "Excellent"

    # Wellness Score

    sleep_score = (float(sleep_hours) / 8) * 25

    exercise_score = (float(exercise_minutes) / 60) * 20

    focus_score = float(focus)

    attendance_score = float(attendance)

    focus_score_part = (float(focus) / 100) * 25

    stress_score = ((10 - float(stress)) / 10) * 20

    phone_score = ((10 - float(phone_usage_hours)) / 10) * 10

    wellness_score = (
                        sleep_score +
                        exercise_score +
                        focus_score_part +
                        stress_score +
                        phone_score
                    )

    wellness_score = min(round(wellness_score),100)


    # burnout calculations
    

    burnout_risk = (

        (float(stress) * 4) +

        (float(phone_usage_hours) * 3) +

        (float(social_media) * 2) +

        (float(youtube) * 2) +

        (float(gaming) * 2)

    ) - (

        (float(sleep_hours) * 3) +

        (float(exercise_minutes) / 10)

    )

    burnout_risk = max(0,min(round(burnout_risk),100))

    print("Burnout Risk:", burnout_risk)

    if burnout_risk <= 30:
        burnout_status = "Low Risk"

    elif burnout_risk <= 60:
        burnout_status = "Moderate Risk"

    else:
        burnout_status = "High Risk"


    # distraction index calculation

    distraction_index = (

        (float(phone_usage_hours) * 4) +

        (float(social_media) * 4) +

        (float(youtube) * 3) +

        (float(gaming) * 3)

    )

    distraction_index = max(0,min(round(distraction_index),100))

    if distraction_index <= 30:
        distraction_status = "Well Managed"

    elif distraction_index <= 60:
        distraction_status = "Needs Control"

    else:
        distraction_status = "Highly Distracted"

    # Digital Distraction Analysis

    focus_leakage = distraction_index
    # Digital Behavior Profile

    if distraction_index < 20:

        digital_profile = "Highly Disciplined"

    elif distraction_index < 40:

        digital_profile = "Balanced Digital User"

    elif distraction_index < 60:

        digital_profile = "Social Media Centric"

    elif distraction_index < 80:

        digital_profile = "High Distraction Risk"

    else:

        digital_profile = "Severely Distracted"


    # Top Distraction Source

    distractions = {

        "Phone Usage": float(phone_usage_hours),

        "Social Media": float(social_media),

        "YouTube": float(youtube),

        "Gaming": float(gaming)

    }

    top_source = max(distractions,key=distractions.get)
    # Focus Recovery Potential

    potential_gain = round(distraction_index * 0.2)

    potential_productivity = min(round(prediction + potential_gain),100)


    # Strongest Attribute

    strengths = {

        "Focus": float(focus),

        "Attendance": float(attendance),

        "Sleep Discipline": (float(sleep_hours) / 10) * 100,

        "Study Consistency": (float(study_hours) / 12) * 100,

        "Physical Activity": min((float(exercise_minutes) / 120) * 100,100)

    }

    strongest_attribute = max(
        strengths,
        key=strengths.get
    )

    # Store AI data for Gemini (AI integration)

 # db for assessment table
    cursor.execute("""

        INSERT INTO assessments (

        user_id,

        age,
        gender,

        study_hours,
        assignments_completed,
        attendance_percentage,
        final_grade,

        sleep_hours,
        stress,
        focus,

        phone_usage_hours,
        social_media,
        youtube,
        gaming,

        breaks_per_day,
        exercise_minutes,
        coffee,

        productivity_score,
        productivity_status,

        wellness_score,

        burnout_risk,
        burnout_status,

        distraction_index,  
        distraction_status,

        focus_leakage,

        digital_profile,

        top_source,

        potential_gain,
        potential_productivity,

        strongest_attribute

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """, (

        session["user_id"],

        int(age),
        int(gender),

        float(study_hours),
        int(assignments_completed),
        float(attendance),
        int(final_grade),

        float(sleep_hours),
        float(stress),
        float(focus),

        float(phone_usage_hours),
        float(social_media),
        float(youtube),
        float(gaming),

        int(breaks_per_day),
        int(exercise_minutes),
        int(coffee),

        round(prediction,2),
        productivity_status,

        wellness_score,

        burnout_risk,
        burnout_status,

        distraction_index,
        distraction_status,

        focus_leakage,

        digital_profile,

        top_source,

        potential_gain,
        potential_productivity,

        strongest_attribute

        ))

    connection.commit()


    return redirect(url_for("dashboard"))

# logout for ending a session
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)