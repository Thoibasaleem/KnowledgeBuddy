from django.db import models
from django.contrib.auth.models import User


def default_study_hours():
    return {
        "Monday": False,
        "Tuesday": False,
        "Wednesday": False,
        "Thursday": False,
        "Friday": False,
        "Saturday": False,
        "Sunday": False
    }

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username

class Semester(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="semesters")
    semester_number = models.IntegerField()
    subjects = models.JSONField()  # Store subject marks as JSON
    backlogs = models.JSONField(default=list)  # Store backlog subjects

    def __str__(self):
        return f"Semester {self.semester_number} - {self.student.user.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    semester_marks = models.JSONField(default=dict)
    weakest_subjects = models.JSONField(default=list)
    easiest_subjects = models.JSONField(default=list)
    preferred_learning_style = models.CharField(max_length=50)
    study_goal = models.CharField(max_length=100)
    available_study_hours = models.JSONField(default=default_study_hours)
    personality_type = models.CharField(max_length=50)
    primary_language = models.CharField(max_length=50)
    preferred_collaboration_tools = models.JSONField(default=list)
    preferred_study_environment = models.CharField(max_length=50)
    geographical_proximity = models.CharField(max_length=50, blank=True, null=True)
    communication_style = models.CharField(max_length=50)
    motivational_level = models.CharField(max_length=50)
    preferred_study_time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - Profile"

class MatchHistory(models.Model):
    student_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matches_initiated'
    )
    student_b = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matches_received'
    )
    success_score = models.FloatField(
        default=0.0,
        help_text="Match effectiveness rating (0.0-1.0)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['student_a', 'student_b']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_a} ↔ {self.student_b} ({self.success_score})"
    
class MatchResult(models.Model):
    student_id_1 = models.IntegerField(default=1)  # Set a valid default value
    student_id_2 = models.IntegerField(default=1)
    match_probability = models.FloatField()
    
    def __str__(self):
        return f"Match: {self.student_id_1} - {self.student_id_2} ({self.match_probability}%)"

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    student1 = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="chat_room_1")
    student2 = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="chat_room_2")

    def __str__(self):
        return f"ChatRoom: {self.room_name}"
class VoiceMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='voice_messages/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VoiceMessage from {self.sender.username} at {self.timestamp}"