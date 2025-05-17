from rest_framework import serializers
from .models import StudentProfile, Semester, Student

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    semesters = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def get_semesters(self, obj):
        """Fetch semesters related to the student linked to this profile."""
        try:
            student = Student.objects.get(user=obj.user)
            semesters = Semester.objects.filter(student=student)
            return SemesterSerializer(semesters, many=True).data
        except Student.DoesNotExist:
            return []
