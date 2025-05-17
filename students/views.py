from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .models import Student, Semester, StudentProfile
from .student_match_model import train_and_predict
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
import mimetypes
from django.conf import settings
from .models import VoiceMessage
import os
from .recommendation_engine import generate_recommendations
from .models import Student  # make sure your Student model exists



def parse_list(value):
    """Utility function to safely parse a comma-separated list."""
    return value.split(',') if value else []

@csrf_exempt
def save_student(request):
    if request.method == 'POST':
        try:
            data = request.POST
            username, email = data.get('username'), data.get('email')
            
            if not username or not email:
                return JsonResponse({"error": "Username and email are required."}, status=400)
            
            user = User.objects.create_user(username=username, email=email)
            student = Student.objects.create(user=user, email=email)

            semester_marks = {}
            for i in range(1, 5):
                subjects = {f'subject_{j}': data.get(f'grade{i}_{j}', '') for j in range(1, 7)}
                backlogs = parse_list(data.get(f'backlogs{i}', ''))
                Semester.objects.create(student=student, semester_number=i, subjects=subjects, backlogs=backlogs)
                semester_marks[f'semester_{i}'] = subjects

            profile = StudentProfile.objects.create(
                user=user,
                semester_marks=semester_marks,
                weakest_subjects=parse_list(data.get('weakestSubjects')),
                easiest_subjects=parse_list(data.get('easiestSubjects')),
                preferred_learning_style=data.get('learningStyle', ''),
                study_goal=data.get('studyGoal', ''),
                available_study_hours={day: data.get(day, 'off') == 'on' for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                personality_type=data.get('personality', ''),
                primary_language=data.get('language', ''),
                preferred_collaboration_tools=parse_list(data.get('collaborationTools')),
                preferred_study_environment=data.get('studyEnvironment', ''),
                geographical_proximity=data.get('geographicalProximity', ''),
                communication_style=data.get('communicationStyle', ''),
                motivational_level=data.get('motivationLevel', ''),
                preferred_study_time=data.get('studyTime', '')
            )
            
            return JsonResponse({"message": "Student data saved successfully!", "student_id": student.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def get_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_data = [{"username": student.user.username, "email": student.email} for student in students]
        return JsonResponse({"students": student_data})
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def submit_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name, email, message = data.get("name", "").strip(), data.get("email", "").strip(), data.get("message", "").strip()

            if not name or not email or not message:
                return JsonResponse({"status": "error", "message": "All fields are required"}, status=400)
            
            return JsonResponse({"status": "success", "message": "Data submitted successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
@csrf_exempt
def train_model(request):
    if request.method == "POST":
        try:
            matching_data = train_and_predict()
            matches_list = []

            if isinstance(matching_data, dict):
                for key, value in matching_data.items():
                    matches_list.extend(value)

            return JsonResponse({"status": "success", "matches": matches_list})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@csrf_exempt
def create_chat_room(student1_id, student2_id):
    try:
        # ✅ Consistent room name order
        room_name = f"chat_{min(student1_id, student2_id)}_{max(student1_id, student2_id)}"
        chat_room, created = ChatRoom.objects.get_or_create(
            room_name=room_name,
            defaults={"student1_id": student1_id, "student2_id": student2_id}
        )
        return JsonResponse({"status": "success", "room_name": chat_room.room_name})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)




@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # 1) Save the file to 'uploads/' inside your media folder
            file_path = default_storage.save(f'uploads/{file.name}', file)

            # 2) Build the absolute file URL
            #    default_storage.url(file_path) returns '/media/uploads/<filename>'
            #    request.build_absolute_uri() converts it to a full URL
            absolute_file_url = request.build_absolute_uri(default_storage.url(file_path))

            # 3) Detect file type (application/pdf, image/png, etc.)
            file_type, _ = mimetypes.guess_type(file.name)
            file_type = file_type or 'application/octet-stream'

            return JsonResponse({
                'file_url': absolute_file_url,
                'file_type': file_type
            })
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ✅ New chat view to render chat.html
@csrf_exempt
def chat_view(request):
    student_id = request.GET.get('studentId')
    student_name = request.GET.get('studentName')

    print(f"🔎 Received student_id: {student_id}")
    print(f"🔎 Received student_name: {student_name}")

    if not student_id or not student_name:
        return HttpResponse("Error: studentId or studentName is missing!", status=400)

    try:
        partner = Student.objects.get(id=student_id)
        print(f"✅ Chat partner: {partner.user.username}")
    except Student.DoesNotExist:
        return HttpResponse("Error: Invalid studentId", status=400)

    return render(request, 'chat/chat.html', {
        'student_id': student_id,
        'student_name': student_name,
        'messages': []  # placeholder until you integrate messages
    })


    
    
@csrf_exempt
def upload_voice_message(request):
    if request.method == 'POST':
        try:
            sender_id = request.POST.get('sender_id')
            audio_file = request.FILES.get('audio_file')
            
            if not (sender_id and audio_file):
                return JsonResponse({"error": "Missing required data."}, status=400)
            
            sender = User.objects.get(id=sender_id)
            voice_msg = VoiceMessage.objects.create(
                sender=sender,
                audio_file=audio_file
            )
            
            return JsonResponse({
                "message": "Voice message uploaded successfully!",
                "voice_message_id": voice_msg.id,
                "audio_url": voice_msg.audio_file.url
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)
import json
from pathlib import Path

@csrf_exempt
def get_recommendations_page(request):
    student_id = request.GET.get("studentId")

    if not student_id:
        return HttpResponse("Missing studentId", status=400)

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return HttpResponse("Invalid studentId", status=404)

    # 📚 Get latest semester data
    latest_semester = Semester.objects.filter(student=student).order_by("-semester_number").first()
    if not latest_semester:
        return HttpResponse("No semester data found", status=404)

    semesters = Semester.objects.filter(student=student)
    if not semesters:
       return HttpResponse("No semester data found", status=404)

    backlogs = []
    for sem in semesters:
        backlogs.extend(sem.backlogs or [])

    subject_marks = {}
    for sem in semesters:
        subject_marks[f"semester_{sem.semester_number}"] = sem.subjects

    try:
        profile = StudentProfile.objects.get(user=student.user)
        weakest_subjects = profile.weakest_subjects
    except StudentProfile.DoesNotExist:
        weakest_subjects = []

    topics_to_recommend = list(set(backlogs + weakest_subjects))

    # 🔍 Load JSON file with recommendations
    json_path = Path(settings.BASE_DIR) / "students" / "recommendations.json"
    with open(json_path, "r", encoding="utf-8") as file:
        all_recommendations = json.load(file)

    # 🎯 Filter matching recommendations
    # ✅ Extract subjects from query params if provided (optional override)
    query_weak = request.GET.getlist("weak_subjects")
    query_backlogs = request.GET.getlist("backlogs")

# ✅ Combine both form + query param values
    final_weak = [s.strip().lower() for s in weakest_subjects + query_weak]
    final_back = [s.strip().lower() for s in backlogs + query_backlogs]

    topics_to_recommend = list(set(final_weak + final_back))

# 🎯 Match recommendations from JSON
    matched_recommendations = [
        rec for rec in all_recommendations
        if rec["topic"].lower().strip() in topics_to_recommend
    ]


    return render(request, "recommendations.html", {
        "student_name": student.user.username,
        "backlogs": backlogs,
        "weakest_subjects": weakest_subjects,
        "topics": topics_to_recommend,
        "recommendations": matched_recommendations  # ✅ send to template
    })
@csrf_exempt
def get_student_data(request):
    student_id = request.GET.get('studentId')
    if not student_id:
        return JsonResponse({"error": "Missing student ID"}, status=400)

    try:
        student = Student.objects.get(id=student_id)
        profile = StudentProfile.objects.get(user=student.user)
        latest_semester = Semester.objects.filter(student=student).order_by("-semester_number").first()
        return JsonResponse({
            "student_name": student.user.username,
            "weak_subjects": profile.weakest_subjects if profile else [],
            "backlogs": latest_semester.backlogs if latest_semester else []
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
