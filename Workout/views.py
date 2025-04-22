from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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