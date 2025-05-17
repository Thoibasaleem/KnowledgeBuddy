import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from itertools import combinations
import random
from .models import Student, StudentProfile
import json

def convert_grades_to_numeric(semester_marks):
    grade_mapping = {'A+': 10, 'A': 9, 'B+': 8, 'B': 7, 'C': 6, 'D': 5, 'E': 4, 'F': 0}
    numeric_marks = []
    
    def extract_grades(data):
        """Recursively extract grades from different formats (dicts, lists)"""
        if isinstance(data, dict):
            for value in data.values():
                extract_grades(value)
        elif isinstance(data, list):
            for item in data:
                extract_grades(item)
        elif isinstance(data, str):
            numeric_marks.append(grade_mapping.get(data.strip(), 0))
    
    extract_grades(semester_marks)
    
    return np.mean(numeric_marks) if numeric_marks else 0

def train_and_predict():
    students = Student.objects.all()
    data = []
    
    for student in students:
        # Use get_or_create to ensure a StudentProfile exists for each student
        profile, created = StudentProfile.objects.get_or_create(
            user=student.user,
            defaults={
                'semester_marks': {},
                'weakest_subjects': [],
                'easiest_subjects': [],
                'preferred_learning_style': '',
                'study_goal': '',
                'available_study_hours': {day: False for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                'personality_type': '',
                'primary_language': '',
                'preferred_collaboration_tools': [],
                'preferred_study_environment': '',
                'geographical_proximity': '',
                'communication_style': '',
                'motivational_level': '',
                'preferred_study_time': ''
            }
        )
        semester_marks = convert_grades_to_numeric(profile.semester_marks)
        data.append({
            'student_id': student.id,
            'username': student.user.username,
            'learning_style': profile.preferred_learning_style,
            'study_goal': profile.study_goal,
            'personality_type': profile.personality_type,
            'language': profile.primary_language,
            'collaboration_tools': profile.preferred_collaboration_tools or "Unknown",
            'study_environment': profile.preferred_study_environment,
            'geographical_proximity': profile.geographical_proximity,
            'communication_style': profile.communication_style,
            'motivation_level': profile.motivational_level,
            'study_time': profile.preferred_study_time,
            'semester_marks': semester_marks
        })

    df = pd.DataFrame(data)
    print("Initial DataFrame:")
    print(df.head())

    df['semester_marks'] = pd.to_numeric(df['semester_marks'], errors='coerce').fillna(0)

    mapping_dicts = {
        'learning_style': {'Visual': 0, 'Auditory': 1, 'Reading/Writing': 2, 'Kinesthetic': 3},
        'study_goal': {'Grade Improvement': 0, 'Understanding Concepts': 1, 'Exam Preparation': 2, 'Project/Assignment Help': 3},
        'personality_type': {'Introvert': 0, 'Extrovert': 1, 'Ambivert': 2},
        'language': {'English': 0, 'Spanish': 1, 'French': 2, 'German': 3, 'Chinese': 4},
        'collaboration_tools': {'Zoom': 0, 'Slack': 1, 'Google Meet': 2, 'Microsoft Teams': 3, 'Google Docs': 4},
        'study_environment': {'Quiet': 0, 'Background Music': 1, 'Library': 2, 'Home': 3},
        'geographical_proximity': {'Local': 0, 'Regional': 1, 'National': 2, 'International': 3},
        'communication_style': {'Email': 0, 'Chat': 1, 'Video Call': 2, 'Phone Call': 3, 'Direct': 4, 'Casual': 5},
        'motivation_level': {'High': 0, 'Medium': 1, 'Low': 2},
        'study_time': {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
    }

    for column, mapping in mapping_dicts.items():
        if column in df:
            print(f"Mapping column: {column}")
            if column == 'collaboration_tools':
                df[column] = df[column].apply(lambda x: [mapping.get(tool.strip(), -1) for tool in x] if isinstance(x, list) else [mapping.get(x.strip(), -1)])
                df[column] = df[column].apply(lambda x: max(x))  
            else:
                df[column] = df[column].map(mapping).fillna(-1).astype(int)

    features = list(mapping_dicts.keys()) + ['semester_marks']

    def create_student_pairs(df, features, sample_size=1000):
        pairs = []
        labels = []
        student_pairs = list(combinations(range(len(df)), 2))
        sampled_pairs = random.sample(student_pairs, min(sample_size, len(student_pairs)))

        for (i, j) in sampled_pairs:
            pair = np.abs(df[features].iloc[i].astype(float) - df[features].iloc[j].astype(float))
            pairs.append(pair)
            label = 1 if sum(pair) < 5 else 0
            labels.append(label)
        return np.array(pairs), np.array(labels)

    pairs, labels = create_student_pairs(df, features)
    
    X_train, X_test, y_train, y_test = train_test_split(pairs, labels, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division=0))

    def predict_match(i, j):
        pair = np.abs(df[features].iloc[i].astype(float) - df[features].iloc[j].astype(float))
        probability = clf.predict_proba([pair])[0][1]
        return {
            'student_id_1': int(df['student_id'].iloc[i]),
            'student_name_1': Student.objects.get(id=int(df['student_id'].iloc[i])).user.first_name or df['username'].iloc[i],
            'student_id_2': int(df['student_id'].iloc[j]),
            'student_name_2': Student.objects.get(id=int(df['student_id'].iloc[j])).user.first_name or df['username'].iloc[j],
            'match_probability': probability * 100
        }

    prediction_pairs = list(combinations(range(len(df)), 2))
    results = [predict_match(i, j) for (i, j) in prediction_pairs]

    grouped_results = {}

    for result in results:
        student_id_1 = result['student_id_1']
        student_id_2 = result['student_id_2']

        if student_id_1 == student_id_2:
            continue  

        if student_id_1 not in grouped_results:
            grouped_results[student_id_1] = []

        grouped_results[student_id_1].append(result)

    for student_id in grouped_results:
        grouped_results[student_id] = sorted(
            grouped_results[student_id], 
            key=lambda x: x['match_probability'], 
            reverse=True
        )[:5]  

    print("✅ Final Matches (Sent to Frontend):")
    print(json.dumps(grouped_results, indent=4))  

    return grouped_results

if __name__ == "__main__":
    train_and_predict()