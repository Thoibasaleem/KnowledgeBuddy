from django.db import models

class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    semester = models.IntegerField()
    
    weakest_subjects = models.TextField(help_text="Comma-separated values")
    easiest_subjects = models.TextField(help_text="Comma-separated values")
    
    LEARNING_STYLES = [
        ('Visual', 'Visual'),
        ('Auditory', 'Auditory'),
        ('Kinesthetic', 'Kinesthetic'),
    ]
    preferred_learning_style = models.CharField(max_length=20, choices=LEARNING_STYLES)

    study_goal = models.CharField(max_length=255)
    available_study_hours = models.JSONField()  # Stores days as JSON (e.g., {"Monday": True, "Tuesday": False})
    
    PERSONALITY_TYPES = [
        ('Introvert', 'Introvert'),
        ('Extrovert', 'Extrovert'),
        ('Ambivert', 'Ambivert'),
    ]
    personality_type = models.CharField(max_length=20, choices=PERSONALITY_TYPES)

    primary_language = models.CharField(max_length=50)
    preferred_collaboration_tools = models.TextField(help_text="Comma-separated values")
    preferred_study_environment = models.CharField(max_length=100)

    geographical_proximity = models.CharField(max_length=50, blank=True, null=True)
    communication_style = models.CharField(max_length=50)
    
    MOTIVATION_LEVELS = [
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low'),
    ]
    motivational_level = models.CharField(max_length=20, choices=MOTIVATION_LEVELS)

    preferred_study_time = models.CharField(max_length=50)

    def __str__(self):
        return self.name
