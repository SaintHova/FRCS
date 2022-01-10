from django.db import models
from teams.models import Team 
from users.models import CustomUser, Profile
from django.utils import timezone
from django_random_id_model import RandomIDModel
import uuid

# Create your models here.

class Pit_stats(RandomIDModel):
    date_entered = models.DateTimeField(default=timezone.now())
    team_num = models.IntegerField(null = True)
    competition = models.CharField(max_length = 100, null = True)
    scout = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True)
    scouting_team = models.CharField(max_length=100, null = True)
    robot_weight = models.DecimalField(max_digits=5, decimal_places = 2, null = True)
    robot_frame_length = models.DecimalField(max_digits=5, decimal_places = 2, null = True)
    robot_frame_width = models.DecimalField(max_digits=5, decimal_places = 2, null = True)
    robot_drivetrain_type = models.CharField(max_length=100, null = True)
    robot_vision_type = models.CharField(max_length=100, null = True)
    robot_vision_implement = models.CharField(max_length=100, null = True)
    robot_goal_height = models.CharField(max_length=100, null = True)
    robot_autonomous = models.CharField(max_length=100, null = True)
    robot_climb = models.CharField(max_length=100, null = True)
    #robot_buddy_climb = models.CharField(max_length=100, null = True)
    
    customOne = models.CharField(max_length=100, null = True, blank = True)
    customTwo = models.CharField(max_length=100, null = True, blank = True)
    customThree = models.CharField(max_length=100, null = True, blank = True)
    
    answerOne = models.CharField(max_length=100, null = True, blank = True)
    answerTwo = models.CharField(max_length=100, null = True, blank = True)
    answerThree = models.CharField(max_length=100, null = True, blank = True)
    
    notes = models.TextField(max_length=100, null = True)
    is_incorrect = models.BooleanField()
    incorrect_selection = models.CharField(max_length=100)
    is_hidden = models.BooleanField(default=False)
    
    # custom_questions = models.ForeignKey(CustomPitQuestions, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return f'{self.team_num} Pit Stats'
class Stat:
    pass

class Game_stats(models.Model):
    team = models.OneToOneField(Team, on_delete = models.CASCADE) #TAKE NULL = TRUE OUT IN PROD
    rank = models.IntegerField(null = True)
    

    def __str__(self):
       return f'{self.team} Game Stat List'

class Match(models.Model):
    
    
    stat = models.ForeignKey(Game_stats, on_delete = models.CASCADE, null = True)
    team_num = models.IntegerField(null = True)
    scout = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True, related_name='scouter')
    # competition = models.CharField(max_length=100, null = True)
    match_number = models.IntegerField(null = True, blank=True)

    left_tarmac = models.CharField(max_length=100, null = True, blank=True)
    auto_lower = models.CharField(max_length=100, null = True, blank=True)
    auto_upper = models.CharField(max_length=100, null = True, blank=True)
    
    lower = models.CharField(max_length=100, null = True, blank=True)
    upper = models.CharField(max_length=100, null = True, blank=True)
    opposite_color = models.CharField(max_length=100, null = True, blank=True)
    
    robot_climb = models.CharField(max_length=100, null = True, blank=True)
    # robot_climb_help = models.CharField(max_length=100, null = True)
    
    defense_percentage = models.IntegerField(null = True, blank=True)

    notes = models.TextField(max_length=100, null = True, blank=True)

    score = models.IntegerField(null = True, blank=True)

    def __str__(self):
        return f'{self.team_num} - {self.match_number}'


