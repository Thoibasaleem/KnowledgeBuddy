import random
from django.core.management.base import BaseCommand
import pandas as pd
from django.contrib.auth.models import User
from students.models import Student, Semester, StudentProfile

class Command(BaseCommand):
    help = "Import student data from Excel file"

    def handle(self, *args, **kwargs):
        df = pd.read_excel('Untitled form (Responses).xlsx')

        # Define sample value pools for random fill
        study_goals = ["Crack GATE", "Excel in Semester", "Improve understanding"]
        personalities = ["INTJ", "ENFP", "ISTP", "ENTJ"]
        languages = ["English", "Malayalam", "Hindi", "Tamil"]
        tools = [["Zoom", "WhatsApp"], ["Google Meet"], ["Discord", "Telegram"]]
        environments = ["Quiet place", "Group study", "Library"]
        proximity_options = ["Nearby", "Same college", "Remote"]
        communication_styles = ["Direct", "Supportive", "Analytical"]
        motivation_levels = ["High", "Medium", "Low"]
        study_times = ["Morning", "Evening", "Night"]

        for _, row in df.iterrows():
            name = str(row["Student Name "]).strip()
            email = str(row["Email "]).strip().lower().replace(" ", "")
            semester_str = str(row["Semester "]).strip()
            semester_number = int(''.join(filter(str.isdigit, semester_str))) if semester_str else 1

    # 🔥 UPDATE HERE:
            user, _ = User.objects.get_or_create(username=email, email=email)
            user.first_name = name  # ✅ Store actual name
            user.save()

            student, _ = Student.objects.get_or_create(user=user, email=email)

            subjects = {
                "subject_1": str(row[6]).strip(),
                "subject_2": str(row[7]).strip()
            }

            weakest = [s.strip() for s in str(row["Enter your Weakest subjects"]).split(',')] if pd.notna(row["Enter your Weakest subjects"]) else []
            easiest = [s.strip() for s in str(row["Enter your Easiest subjects"]).split(',')] if pd.notna(row["Enter your Easiest subjects"]) else []
            backlogs = [s.strip() for s in str(row["  Select your backlog subjects from Semester 1  "]).split(',')] if pd.notna(row["  Select your backlog subjects from Semester 1  "]) else []

            Semester.objects.create(
                student=student,
                semester_number=semester_number,
                subjects=subjects,
                backlogs=backlogs
            )

            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    "semester_marks": {f"semester_{semester_number}": subjects},
                    "weakest_subjects": weakest,
                    "easiest_subjects": easiest,
                    "preferred_learning_style": str(row.get("preferred study Method", "")).strip(),
                    "study_goal": random.choice(study_goals),
                    "available_study_hours": {day: False for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                    "personality_type": random.choice(personalities),
                    "primary_language": random.choice(languages),
                    "preferred_collaboration_tools": random.choice(tools),
                    "preferred_study_environment": random.choice(environments),
                    "geographical_proximity": random.choice(proximity_options),
                    "communication_style": random.choice(communication_styles),
                    "motivational_level": random.choice(motivation_levels),
                    "preferred_study_time": str(row.get("Preferred Study Time", "")).strip() or random.choice(study_times)
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Students imported with random fill for missing profile fields!"))
