import re
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load data
training = pd.read_csv('Data/Training.csv')
testing = pd.read_csv('Data/Testing.csv')
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

reduced_data = training.groupby(training['prognosis']).max()

# Encode labels
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

# Split data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx = testing[cols]
testy = testing['prognosis']
testy = le.transform(testy)

# Train Decision Tree
clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)
scores = cross_val_score(clf, x_test, y_test, cv=3)

# Train SVM
model = SVC()
model.fit(x_train, y_train)

# Dictionaries for symptoms, severity, descriptions, and precautions
severityDictionary = {}
description_list = {}
precautionDictionary = {}
symptoms_dict = {symptom: index for index, symptom in enumerate(x)}

def getSeverityDict():
    with open('MasterData/symptom_severity.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) > 1:
                severityDictionary[row[0]] = int(row[1])

def getDescription():
    with open('MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            description_list[row[0]] = row[1]

def getprecautionDict():
    with open('MasterData/symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]

def calc_condition(exp, days):
    if not exp:  # Handle empty symptom list
        return "No additional symptoms provided. Please consult a doctor if symptoms persist."
    sum_severity = 0
    for item in exp:
        if item in severityDictionary:  # Only include valid symptoms
            sum_severity += severityDictionary[item]
        else:
            st.warning(f"Severity for symptom '{item}' not found. Skipping this symptom.")
    if (sum_severity * days) / (len(exp) + 1) > 13:
        return "You should take the consultation from doctor."
    return "It might not be that bad but you should take precautions."

def check_pattern(dis_list, inp):
    pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if len(pred_list) > 0:
        return 1, pred_list
    return 0, []

def sec_predict(symptoms_exp):
    df = pd.read_csv('Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        if item in symptoms_dict:  # Ensure symptom exists in dictionary
            input_vector[symptoms_dict[item]] = 1
    return rf_clf.predict([input_vector])

def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x: x.strip(), list(disease)))

# Streamlit app
st.title("HealthCare ChatBot")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.name = ""
    st.session_state.symptom = ""
    st.session_state.days = 0
    st.session_state.confirmed_symptom = ""
    st.session_state.symptoms_present = []
    st.session_state.symptoms_exp = []

# Load dictionaries
getSeverityDict()
getDescription()
getprecautionDict()

# Step 0: Get user name
if st.session_state.step == 0:
    st.markdown("### Welcome to the HealthCare ChatBot")
    name = st.text_input("Your Name?")
    if st.button("Submit Name"):
        if name:
            st.session_state.name = name
            st.session_state.step = 1
            st.rerun()

# Step 1: Get initial symptom
if st.session_state.step == 1:
    st.write(f"Hello, {st.session_state.name}")
    symptom_input = st.text_input("Enter the symptom you are experiencing:")
    if st.button("Submit Symptom"):
        chk_dis = cols
        conf, cnf_dis = check_pattern(chk_dis, symptom_input)
        if conf == 1:
            st.session_state.symptom = symptom_input
            st.session_state.cnf_dis = cnf_dis
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Enter a valid symptom.")

# Step 2: Confirm symptom
if st.session_state.step == 2:
    st.write("Searches related to your input:")
    for num, item in enumerate(st.session_state.cnf_dis):
        st.write(f"{num}) {item}")
    conf_inp = st.selectbox("Select the one you meant:", options=[f"{i}" for i in range(len(st.session_state.cnf_dis))])
    if st.button("Confirm Symptom"):
        st.session_state.confirmed_symptom = st.session_state.cnf_dis[int(conf_inp)]
        st.session_state.step = 3
        st.rerun()

# Step 3: Get number of days
if st.session_state.step == 3:
    days = st.number_input("For how many days have you been experiencing this symptom?", min_value=1, step=1)
    if st.button("Submit Days"):
        st.session_state.days = days
        st.session_state.step = 4
        st.rerun()

# Step 4: Process symptom and get additional symptoms
if st.session_state.step == 4:
    tree_ = clf.tree_
    feature_name = [cols[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]
    
    def recurse(node, depth):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            val = 1 if name == st.session_state.confirmed_symptom else 0
            if val <= threshold:
                return recurse(tree_.children_left[node], depth + 1)
            else:
                st.session_state.symptoms_present.append(name)
                return recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            red_cols = reduced_data.columns
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            st.write("Are you experiencing any of the following symptoms?")
            for syms in list(symptoms_given):
                if syms in severityDictionary:  # Only include symptoms with known severity
                    response = st.radio(f"{syms}?", options=["Yes", "No"], key=syms)
                    if response == "Yes":
                        st.session_state.symptoms_exp.append(syms)
            return present_disease

    present_disease = recurse(0, 1)
    if present_disease is None:
        st.error("Unable to determine a diagnosis. Please try again with different symptoms.")
        st.session_state.step = 5
    else:
        second_prediction = sec_predict(st.session_state.symptoms_exp)
        condition = calc_condition(st.session_state.symptoms_exp, st.session_state.days)
        
        if st.button("Get Diagnosis"):
            st.markdown("### Diagnosis")
            st.write(condition)
            if present_disease[0] == second_prediction[0]:
                st.write(f"You may have **{present_disease[0]}**")
                st.write(description_list[present_disease[0]])
            else:
                st.write(f"You may have **{present_disease[0]}** or **{second_prediction[0]}**")
                st.write(description_list[present_disease[0]])
                st.write(description_list[second_prediction[0]])
            
            st.markdown("### Precautions")
            precaution_list = precautionDictionary[present_disease[0]]
            for i, precaution in enumerate(precaution_list, 1):
                st.write(f"{i}) {precaution}")
            
            st.session_state.step = 5

# Step 5: End
if st.session_state.step == 5:
    if st.button("Restart"):
        st.session_state.step = 0
        st.session_state.name = ""
        st.session_state.symptom = ""
        st.session_state.days = 0
        st.session_state.confirmed_symptom = ""
        st.session_state.symptoms_present = []
        st.session_state.symptoms_exp = []
        st.rerun()

st.markdown("---")
st.write("HealthCare ChatBot - Powered by Streamlit")