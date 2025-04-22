import logging
from django.db import models
from datetime import date
from accounts.models import Athlete

# Create your models here.

class ExerciseDefinition(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    video = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class ExercisePrescription(models.Model):
    athlete_program_assignment = models.ForeignKey(
        "AthleteProgramAssignment", on_delete=models.deletion.DO_NOTHING, null=True
    )
 
    exercise_definition = models.ForeignKey(
        ExerciseDefinition, on_delete=models.CASCADE
    )
    sets = models.TextField(null=True, blank=True)
    reps = models.TextField(null=True, blank=True)
    load = models.TextField(null=True, blank=True)
    duration = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.routine}: {self.exercise_definition}"


class ExerciseLog(models.Model):
    date = models.DateField(default=date.today)
    exercise_prescription = models.ForeignKey(
        ExercisePrescription, on_delete=models.CASCADE, null=True
    )
    athlete = models.ForeignKey(Athlete, models.CASCADE, default=None)

    completed = models.BooleanField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    sets = models.TextField(null=True, blank=True)
    reps = models.TextField(null=True, blank=True)
    load = models.TextField(null=True, blank=True)
    duration = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.exercise_prescription}"