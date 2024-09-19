# A simple prediction function based on fixed rules
def predict_performance(attendance_rate, assignment_score, exercise_completion, engagement):
    # Very simple logic: if attendance and scores are above 70%, the student will pass
    if attendance_rate > 0.7 and assignment_score > 70 and exercise_completion > 0.7 and engagement > 0.7:
        return "Pass"
    else:
        return "Fail"

