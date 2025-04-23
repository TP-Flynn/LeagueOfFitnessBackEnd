from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Workout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@api_view(["POST"])
def log_workout(request):
    # Logic to log a workout
    pass

@api_view(["GET"])
def workout_history(request):
    # Logic to get workout history
    pass

# Create your views here.
@api_view(["POST"])
@csrf_exempt
def create_exercise_definition(request):
    data = request.data

    name = data["name"] or None
    type_of_exercise = data["type_of_exercise"] or None
    video = data["video"] or None

    if ExerciseDefinition.objects.filter(name=name).exists():
        return Response(status=status.HTTP_412_PRECONDITION_FAILED,
                        data={"reason": "An exercise definition with this name already exists."})

    try:
        ExerciseDefinition.objects.create(
            name=name, type_of_exercise=type_of_exercise, video=video
        ).save()
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"reason": f"Could not create exercise defintion: {str(e)}"})

    return Response(status=status.HTTP_201_CREATED)
