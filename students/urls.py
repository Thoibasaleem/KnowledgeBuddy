from django.urls import path
from .views import save_student, get_students, submit_data, train_model, chat_view, upload_file, upload_voice_message
from . import views  # or your app's views
from .views import get_student_data, get_recommendations_page
urlpatterns = [
    path('save-student/', save_student, name='save_student'),
    path('get-students/', get_students, name='get_students'),
    path('submit-data/', submit_data, name='submit_data'),
    path('train/', train_model, name='train_model'),
    path('chat/', chat_view, name='chat'),
    path('chat/upload/', upload_file, name='upload_file'),
    path('upload_voice_message/', upload_voice_message, name='upload_voice_message'),
    path('recommendations/', get_recommendations_page, name='recommendations'),
    path("api/get_student_data/", views.get_student_data, name="get_student_data"),
]