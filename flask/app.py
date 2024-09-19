from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




migrate = Migrate(app, db)

# Create a model for storing exercise data
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    exercise_title = db.Column(db.String(100), nullable=False)
    submission_deadline = db.Column(db.DateTime, nullable=False)  # Track the deadline
    submission_time = db.Column(db.DateTime, nullable=True)  # Track when the exercise was submitted
    completed_on_time = db.Column(db.String(20), nullable=False)  # On Time, Late, etc.
    level_of_completion = db.Column(db.String(20), nullable=False)
    quality_of_work = db.Column(db.Integer, nullable=False)
    learning_outcome = db.Column(db.Text, nullable=False)
    challenges = db.Column(db.Text)
    teacher_feedback = db.Column(db.Text)
    grade = db.Column(db.Integer, nullable=True)  # Grade given by teacher
    status = db.Column(db.String(20), default='Pending')  # Status of review
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        student_name = request.form.get('student_name')
        exercise_title = request.form.get('exercise_title')
        submission_deadline = request.form.get('submission_deadline')
        level_of_completion = request.form.get('level_of_completion')
        quality_of_work = request.form.get('quality_of_work')
        learning_outcome = request.form.get('learning_outcome')
        challenges = request.form.get('challenges', '')

        submission_time = datetime.utcnow()  # Automatically capture submission time
        deadline = datetime.strptime(submission_deadline, "%Y-%m-%dT%H:%M")

        # Determine if the submission is on time or late
        if submission_time > deadline:
            completed_on_time = "Late"
        else:
            completed_on_time = "On Time"

        # Create a new exercise submission
        new_exercise = Exercise(
            student_name=student_name,
            exercise_title=exercise_title,
            submission_deadline=deadline,
            submission_time=submission_time,
            completed_on_time=completed_on_time,
            level_of_completion=level_of_completion,
            quality_of_work=quality_of_work,
            learning_outcome=learning_outcome,
            challenges=challenges,
            status='Pending'  # Initially set status to Pending
        )

        db.session.add(new_exercise)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('index.html')



@app.route("/teacher")
def teacher_view():
    exercises = Exercise.query.filter_by(status="Pending").all()
    return render_template('teacher.html', exercises=exercises)

@app.route("/review/<int:id>", methods=["GET", "POST"])
def review_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    if request.method == "POST":
        exercise.teacher_feedback = request.form['teacher_feedback']
        exercise.grade = request.form['grade']
        exercise.status = 'Reviewed'
        db.session.commit()
        return redirect('/teacher')

    return render_template('review.html', exercise=exercise)




@app.route("/student/status")
def student_status():
    student_name = request.args.get('student_name')  # For simplicity, pass student name as a query parameter
    exercises = Exercise.query.filter_by(student_name=student_name).all()
    return render_template('student_status.html', exercises=exercises)




# Route to display stored exercise data
@app.route("/results")
def results():
    exercises = Exercise.query.order_by(Exercise.date_created).all()
    return render_template('results.html', exercises=exercises)

@app.cli.command('init-db')
def init_db():
    """Create all database tables."""
    db.create_all()
    print("Database initialized!")



if __name__ == "__main__":
    app.run(debug=True)

