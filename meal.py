


import openai
import json
import os
import streamlit as st
import requests





OPENAI_API_KEY = ""

model_id = "678d8d099274c680fd67445f"



st.title("Healthy Heart, Happy You! Welcome to your Happy Heart Meal Planner!")
st.write("Welcome! This app will generate a personalized weekly meal plan based on your preferences! Get ready for happiness and healthiness!")

# basic user inputs
age = st.number_input("Enter your age:", min_value=18, max_value=100, step=1)

gender = st.selectbox("Select gender:", options=["Male", "Female"])
gender_value = 1 if gender == "Male" else 0

diet_preference = st.text_input("Enter your diet preference(s) (separate by commas) (ex: Mediterranean, Gujarati, South Indian, Punjabi, Southern US, Chinese, Mexican, no preference, etc.) (restrictions like vegetarian, vegan, lactose-intolerant will be asked for later):")

ethnicity = st.text_input("Enter your ethnicity or ethnicities (separate with commas) (this helps us determine risk factors for CVD that are often higher for certain ethnic groups):")
height = st.number_input("Enter your height (in inches):")
weight = st.number_input("Enter your weight (in pounds (lbs)):")
location = st.text_input("Do you have access to a supermarket (like Trader Joe's, Walmart, Kroger, Publix, Dollar General Market, Target, etc. where you can find a wide variety of fresh foods? Respond with yes or no, yes if there is an accessible supermarket where you typically shop):")
smoker = st.number_input("Cigarettes per day:", min_value=0, max_value=100, step=1)
shopping = st.selectbox("How often do you grocery shop?", ["Once a week", "Twice a week", "Every two weeks", "Every three weeks", "Every month", "Every single day", "Three times a week", "Four times a week", "Five times a week", "Six times a week"])



# time to cook for each day of the week (allows for more personalization)
st.subheader("Time to cook for each day and each meal of the week (in minutes):")
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
meals = ["breakfast", "lunch", "dinner"]
cook_times = {}

for day in days:
	with st.expander(f"{day}"):
		cook_times[day] = {}
		for meal in meals:
			cook_times[day][meal] = st.number_input(f"{day} {meal}", min_value=0, max_value=300, step=1)


# more info about health
st.subheader("Health details")
allergies = st.text_input("Enter any allergies you have (separate by commas) (ex: peanuts, tree-nuts, lactose intolerant, gluten-free, eggs, etc.):", key="allergies")
dietary_restrictions = st.text_input("Enter your dietary restrictions (separate by commas) (ex: egg-free, vegetarian, lacto-vegetarian, pescatarian, keto, no red meat):", key="dietary_restrictions")
diabetes = st.selectbox("Do you have diabetes?", options=["Yes", "No"])
bpmeds = st.selectbox("Are you on blood pressure medication?", options=["Yes", "No"])
BMI = st.number_input("Enter your Body Mass Index:", min_value=0.0, max_value=100.0, step=0.01)
prevalentStroke = st.selectbox("Have you had a stroke?", options=["Yes", "No"])
prevalentHyp = st.selectbox("Do you have hypertension (high blood pressure)?", options=["Yes", "No"])
currentSmoker = st.selectbox("Are you a current smoker?", options=["Yes", "No"])


# specifics about health (if user has this input)
st.subheader("Please enter more specific data regarding your health (this information can usually be found from your regular examinations with your physician. If you don't have this info, that is fine as well, and you will need to input 0 for questions you don't have data for):")
glucose = st.number_input("Enter your fasting glucose level (mg/dL):", min_value=0, step=1)
total_cholesterol = st.number_input("Enter your total cholesterol (mg/dL):", min_value=0, step=1)
hdl_cholesterol = st.number_input("Enter your HDL cholesterol (mg/dL):", min_value=0, step=1)
ldl_cholesterol = st.number_input("Enter your LDL cholesterol (mg/dL):", min_value=0, step=1)
triglycerides = st.number_input("Enter your triglyceride level (mg/dL):", min_value=0, step=1)
systolic_bp = st.number_input("Enter your systolic blood pressure (mmHg):", min_value=0, step=1)
diastolic_bp = st.number_input("Enter your diastolic blood pressure (mmHg):", min_value=0, step=1)
iron = st.number_input("Enter your iron level (ferritin) (ng/mL):", min_value=0, step=1)
protein = st.number_input("Enter your total protein level (g/dL):", min_value=0.0, step=0.1)
hemoglobin = st.number_input("Enter your hemoglobin level (g/dL):", min_value=0.0, step=0.1)
creatinine = st.number_input("Enter your creatinine level (mg/dL):", min_value=0.0, step=0.1)
bun = st.number_input("Enter your BUN level (Blood Urea Nitrogen) (mg/dL):", min_value=0.0, step=0.1)
vitamin_d = st.number_input("Enter your Vitamin D level (ng/mL):", min_value=0.0, step=0.1)
sodium = st.number_input("Enter your sodium level (mEq/L):", min_value=0.0, step=0.1)
potassium = st.number_input("Enter your potassium level (mEq/L):", min_value=0.0, step=0.1)
calcium = st.number_input("Enter your calcium level (mg/dL):", min_value=0.0, step=0.1)


# Display all user inputs (for user review)
st.write("Here's what you've entered:")
st.write(f"Age: {age}")
st.write(f"Gender: {gender}")
st.write(f"Diet Preferences: {diet_preference}")
st.write(f"Ethnicity: {ethnicity}")
st.write(f"Height: {height} inches")
st.write(f"Weight: {weight} lbs")
st.write(f"Location Access: {location}")
st.write(f"Smoker: {smoker} cigarettes per day")
st.subheader("Time to cook each meal:")
for day in days:
	for meal in meals:
		meal_key = f"{day}_{meal}"
		time_to_cook = cook_times[day][meal]
		st.write(f"{day} {meal.capitalize()}: {time_to_cook} minutes")
st.write(f"Allergies: {allergies}")
st.write(f"Dietary Restrictions: {dietary_restrictions}")
st.write(f"Diabetes: {diabetes}")
st.write(f"BP Medicine: {bpmeds}")
st.write(f"BMI: {BMI}")
st.write(f"Prevalent Stroke: {prevalentStroke}")
st.write(f"Hypertension: {prevalentHyp}")
st.write(f"Current Smoker: {currentSmoker}")
st.write(f"Fasting Glucose: {glucose} mg/dL")
st.write(f"Total Cholesterol: {total_cholesterol} mg/dL")
st.write(f"HDL Cholesterol: {hdl_cholesterol} mg/dL")
st.write(f"LDL Cholesterol: {ldl_cholesterol} mg/dL")
st.write(f"Triglycerides: {triglycerides} mg/dL")
st.write(f"Systolic BP: {systolic_bp} mmHg")
st.write(f"Diastolic BP: {diastolic_bp} mmHg")
st.write(f"Iron Level: {iron} ng/mL")
st.write(f"Protein Level: {protein} g/dL")
st.write(f"Hemoglobin Level: {hemoglobin} g/dL")
st.write(f"Creatinine Level: {creatinine} mg/dL")
st.write(f"BUN Level: {bun} mg/dL")
st.write(f"Vitamin D: {vitamin_d} ng/mL")
st.write(f"Sodium Level: {sodium} mEq/L")
st.write(f"Potassium Level: {potassium} mEq/L")
st.write(f"Calcium Level: {calcium} mg/dL")


st.title("Heart Disease Risk Prediction")

if st.button("Predict"):
    input_data = {
        "age": age,
        "male": gender,
        "cigsPerDay": smoker,
        "glucose": glucose,
        "totChol": total_cholesterol, 
        "SysBP": systolic_bp,
        "DiaBP": diastolic_bp,
        "diabetes": diabetes,
        "BPMeds": bpmeds,
        "prevalentStroke": prevalentStroke,
        "prevalentHyp": prevalentHyp,
        "currentSmoker": currentSmoker,
    }


prediction = api.create_prediction(model_id, input_data)

print(prediction['object']['output'])

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
	data = request.get_json()  
	return jsonify({"message": "Meal plan generated", "data": {data}})
    # Extracting relevant data from the input (e.g., age, gender, allergies)
    
    # Make the OpenAI API call here to generate meal plans
	response = openai.Completion.create(
      #  model="gpt-4", 
      #  prompt=f"Generate a meal plan for a {age}-year-old {gender} who weighs {weight} pounds and is {height} inches tall. They have these allergies: {allergies}. Their dietary restrictions are: {dietary_restrictions}. Their dietary preferences are: {diet_preference}. Their ethnicity is {ethnicity}. Their height is {height} inches, and they weigh {weight} pounds. Do they have access to a supermarket for groceries: {location}. They shop {shopping} for groceries. Do they have diabetes: {diabetes}. Do they take Blood pressure medicine: {bpmeds}. Their BMI is {BMI}. Have they had a prevalent stroke: {prevalentStroke}. Do they have hypertension: {prevalentHyp}. Are they a current smoker: {currentSmoker}. And they smoke {smoker} cigarettes per day. Their health metrics are: glucose: {glucose} mg/dL, total cholesterol: {total_cholesterol} mg/dL, hdl cholesterol: {hdl_cholesterol} mg/dL, ldl cholesterol: {ldl_cholesterol} mg/dL, triglycerides: {triglycerides} mg/dL, systolic bp: {systolic_bp} mmHg, diastolic bp: {diastolic_bp} mmHg, iron: {iron} ng/mL, protein: {protein} g/dL, hemoglobin: {hemoglobin} g/dL, creatinine: {creatinine} mg/dL, blood urea nitrogen: {bun} mg/dL, vitamin d: {vitamin_d} ng/mL, sodium: {sodium} mEq/L, potassium: {potassium} mEq/L, calcium: {calcium} mg/dL", 
      #  temperature=0.7,
      #  max_tokens=200
    )

if __name__ == '__main__':
	app.run(debug=True, port=5000)


