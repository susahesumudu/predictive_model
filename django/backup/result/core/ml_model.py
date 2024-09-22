import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from .models import Student, Submission, Attendance

def prepare_data():
    students = Student.objects.all()
    data = []
    for student in students:
        attendance = Attendance.objects.filter(student=student).count()
        submissions = Submission.objects.filter(student=student)
        avg_grade = submissions.aggregate(models.Avg('grade'))['grade__avg'] or 0
        data.append({'attendance': attendance, 'avg_grade': avg_grade, 'result': 1 if avg_grade >= 50 else 0})
    
    df = pd.DataFrame(data)
    return df

def train_model():
    df = prepare_data()
    X = df[['attendance', 'avg_grade']]
    y = df['result']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    return model, accuracy

def predict_pass_fail(student_id):
    model, _ = train_model()
    student = Student.objects.get(id=student_id)
    attendance = Attendance.objects.filter(student=student).count()
    avg_grade = Submission.objects.filter(student=student).aggregate(models.Avg('grade'))['grade__avg'] or 0
    
    prediction = model.predict([[attendance, avg_grade]])
    return 'Pass' if prediction[0] == 1 else 'Fail'

