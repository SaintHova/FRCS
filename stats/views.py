import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import request
from teams.models import Team
import string
from .models import Pit_stats, Game_stats, Match, Competition
from .forms import pit_scout_form, game_scout_form, pit_correct_form
from django.views.generic.edit import FormView, CreateView, UpdateView
import tbapy
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView
)
from django.contrib.auth.models import User
from users.views import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
import random
from django.contrib import messages
from users.models import Profile, CustomUser
from random import randint
from django.core.paginator import Paginator
import json
from django.db.models import Avg



def scouthub(request):
   
    context = {
    'team_count': Team.objects.all().count(),
    'sub_count': Game_stats.objects.all().count(),
    'teams': Game_stats.objects.all(),
    
    'pit_stats_vision_none':  Pit_stats.objects.filter(robot_vision_type='None').count(),
    'pit_stats_vision_limelight':  Pit_stats.objects.filter(robot_vision_type='Limelight').count(),
    'pit_stats_vision_rpi':  Pit_stats.objects.filter(robot_vision_type='Raspberry Pi').count(),
    'pit_stats_vision_other':  Pit_stats.objects.filter(robot_vision_type='Other').count(),
    
    'pit_stats_dt_4skid':  Pit_stats.objects.filter(robot_drivetrain_type='4 Wheel Skid').count(),
    'pit_stats_dt_6skid':  Pit_stats.objects.filter(robot_drivetrain_type='6 Wheel Skid').count(),
    'pit_stats_dt_8skid':  Pit_stats.objects.filter(robot_drivetrain_type='8 Wheel Skid').count(),
    'pit_stats_dt_tread':  Pit_stats.objects.filter(robot_drivetrain_type='Treads').count(),
    'pit_stats_dt_omni':  Pit_stats.objects.filter(robot_drivetrain_type='Omni').count(),
    'pit_stats_dt_swerve':  Pit_stats.objects.filter(robot_drivetrain_type='Swerve').count(),
    'pit_stats_dt_other':  Pit_stats.objects.filter(robot_drivetrain_type='Other').count(),
    
    'pit_stats_vision_yes':  Pit_stats.objects.filter(robot_vision_implement='Yes').count(),
    'pit_stats_vision_no':  Pit_stats.objects.filter(robot_vision_implement='No').count(),
    
    'pit_stats_climb_yes':  Pit_stats.objects.filter(robot_climb='Yes').count(),
    'pit_stats_climb_no':  Pit_stats.objects.filter(robot_climb='No').count(),
    
    'pit_stats_buddy_yes':  Pit_stats.objects.filter(robot_buddy_climb='Yes').count(),
    'pit_stats_buddy_no':  Pit_stats.objects.filter(robot_buddy_climb='No').count(),
    
    'pit_stats_height_short':  Pit_stats.objects.filter(robot_highlow='Low - below 28"').count(),
    'pit_stats_height_tall':  Pit_stats.objects.filter(robot_highlow='High - above 28"').count(),
    
    'pit_stats_weight': str(Pit_stats.objects.all().aggregate(Avg('robot_weight'))).split('(')[1].split(')')[0].split("'")[1],
    'pit_stats_width': str(Pit_stats.objects.all().aggregate(Avg('robot_frame_width'))).split('(')[1].split(')')[0].split("'")[1],
    'pit_stats_length': str(Pit_stats.objects.all().aggregate(Avg('robot_frame_length'))).split('(')[1].split(')')[0].split("'")[1]
    
    

    }
    

    return render(request, 'stats/scout-hub.html', context)


def returnVal(stats, id):
    data = []
    for i in stats.match_set.all().values_list(id, flat = True):
        data.append(str(i))
    return data

def getPercentage(whole, num):
    return num/whole * 100

def getPercentage(list):
    sum1 = 0
    sum2 = 0
    for i in list:
        if(i == 100):
            sum1 += 1
        else:
            sum2 += 1

    total = sum1 + sum2
    calc = [sum1/total, sum2/total]
    return calc

class ScoutDetailView(View):
    def get(self, request, *args, **kwargs):
        stats = get_object_or_404(Game_stats, pk=kwargs['pk'])
        data = {}
        for i in Match._meta.get_fields():
            data[i.name] = returnVal(stats, i.name)
        #Percentages for special data
        context = {
            'stat': stats, 
            'data': data,
            'score': Profile.objects.get(user=request.user).relativeScoring
        }
        return render(request, 'stats/game_stats_detail.html', context)

class ScoutListView(ListView):
    model = Game_stats
    template_name = 'stats/game_stats_list'  # <app>/<model>_<viewtype>.html
    context_object_name = 'stats'
    ordering = ['-id']
    paginate_by = 20


class PitListView(ListView):
    
    model = Pit_stats
    template_name = 'stats/pit_stats_list'
    context_object_name = 'teams'
    ordering = ['-id']
    paginate_by = 20


class PitDetailView(DetailView):
    model = Pit_stats
    


def test(request):
    return render(request, 'stats/test.html')

def randomIDGenerator():
    range_start = 10**(15-1)
    range_end = (10**15)-1
    return randint(range_start, range_end)

def pit_scout(request):
    form = pit_scout_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            team_num = form.cleaned_data['team_num']
            obj.scout = Profile.objects.get(user=request.user)
            
            obj.is_incorrect = False
            
            obj.scouted_team_num = request.user.team_num
            obj.stat_id = randomIDGenerator()

            if not Team.objects.filter(team_num = team_num).exists():
                Team.objects.create(team_num = team_num)

            if Pit_stats.objects.filter(team_num = team_num).exists():
                
                if Profile.objects.get(user=request.user.profile.user).viewPitResubmit:
                    pk = Pit_stats.objects.get(team_num=team_num).pk
                    return redirect('pitdata-view', pk=pk)
                else:
                    messages.error(request, "Team pit entry already exists")
                    return redirect('Pitscout-view')
            form.save()
            messages.success(request, "Pit entry submitted, Thank You")
            return redirect('Pitscout-view')

        
        else:
            messages.error(request, "Form invalid, Try submitting data again properly")
            return redirect('Pitscout-view')
    return render(request, 'stats/pit-scout.html', {'form': form})


def returnChoiceData(field):
    if(field == "100"):
        return 1
    else:
        return 0

@login_required
def scout(request):
    form = game_scout_form(request.POST)
    if request.method == 'POST':
        print(form.errors)
        print(form.non_field_errors)
        if form.is_valid():
            #Saving team number of user to Game_stats object
            obj = form.save(commit=False)
            obj.team_num = request.user.team_num
            #!SCOUTING TEAM NUMBER
            obj.scout = CustomUser.objects.get(username=request.user)
            #Gathering data
            scouted_team_num = form.cleaned_data['scouted_team_num']
            competition = form.cleaned_data['competition']
            
            randomNumber = randomIDGenerator()
            obj.match_id = randomNumber
            obj.score = returnChoiceData(form.cleaned_data.get('robot_climb')) + returnChoiceData(form.cleaned_data.get('robot_generator')) + returnChoiceData(form.cleaned_data.get('initiation_line')) + returnChoiceData(form.cleaned_data.get('control_panel_rot')) + returnChoiceData(form.cleaned_data.get('control_panel_pos')) + form.cleaned_data['auto_low_goal_scored'] + form.cleaned_data['auto_outer_goal_scored'] + form.cleaned_data['auto_inner_goal_scored'] + form.cleaned_data['inner_goal_scored'] + form.cleaned_data['outer_goal_scored'] + form.cleaned_data['inner_goal_scored']
            
           
            
            team_code = Team.objects.get(team_num=request.user.team_num).team_code
            obj.scouted_team_code = team_code
            #Creating new team if necessary
   
            
            Competition.objects.create(competition = competition)
            if not Team.objects.filter(team_num = scouted_team_num).exists():
                Team.objects.create(team_num = scouted_team_num)
            #Finally, add Game_stats object to the team
            obj.stat = Team.objects.get(team_num = scouted_team_num).game_stats
            form.save()
            return redirect('home-view')
        else:
            return redirect('scout-view')
    low_goal_scored = Match.objects.filter(team_num=810)
    print(low_goal_scored)
    return render(request, 'stats/scout.html', {'form': form})

  
def pitFlag(request, pk):
    instance = get_object_or_404(Pit_stats ,pk=pk)
    form = pit_correct_form(instance=instance)
    if request.method == 'POST':
        form = pit_correct_form(request.POST, instance=instance)
        if form.is_valid():
             instance = form.save(commit=False)
             instance.save()
             return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'stats/pit-flag.html', context)