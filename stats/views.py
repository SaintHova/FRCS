import csv
from math import floor
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teams.models import Team
from .models import Pit_stats, Game_stats, Match
from .forms import pit_scout_form, game_scout_form, pit_correct_form
from django.views.generic import (
        ListView,
        DetailView,
)
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from users.models import Profile, CustomUser
from random import randint
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings

@login_required
def scouthub(request):
    if(Pit_stats.objects.all().exists()):
        context = {
            #*checks to see if there is data scouted for team
            'team_count': Team.objects.filter(team_users__isnull=True).count(),

            'sub_count': (Match.objects.all().count() - Match.objects.filter(match_number__isnull=True).count()) + Pit_stats.objects.all().count(),
            'teams': Game_stats.objects.all(),

            'pit_stats_vision_yes':  Pit_stats.objects.filter(robot_vision_implement='Yes').count(),
            'pit_stats_vision_no':  Pit_stats.objects.filter(robot_vision_implement='No').count(),
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

            'pit_stats_climb_none':  Pit_stats.objects.filter(robot_climb='None').count(),
            'pit_stats_climb_lower':  Pit_stats.objects.filter(robot_climb='Lower Rung').count(),
            'pit_stats_climb_middle':  Pit_stats.objects.filter(robot_climb='Middle Rung').count(),
            'pit_stats_climb_upper':  Pit_stats.objects.filter(robot_climb='Upper Rung').count(),
            'pit_stats_climb_traversal':  Pit_stats.objects.filter(robot_climb='Traversal Rung').count(),
            
            'pit_stats_shot_high':  Pit_stats.objects.filter(robot_goal_height='Lower Hub').count(),
            'pit_stats_shot_low':  Pit_stats.objects.filter(robot_goal_height='Upper Hub').count(),
            'pit_stats_shot_both':  Pit_stats.objects.filter(robot_goal_height='Both Lower and Upper Hub').count(),
            
            'pit_stats_weight': (int(Pit_stats.objects.all().aggregate(Avg('robot_weight'))['robot_weight__avg'])),
            'pit_stats_width': (int(Pit_stats.objects.all().aggregate(Avg('robot_frame_width'))['robot_frame_width__avg'])),
            'pit_stats_length': (int(Pit_stats.objects.all().aggregate(Avg('robot_frame_length'))['robot_frame_length__avg'])),
            'pit_stats_vision_usage': (int(Pit_stats.objects.all().aggregate(Avg('robot_vision_implement'))['robot_vision_implement__avg']*100)),
        }
    else:
        context = {
        'team_count': Team.objects.filter(team_users__isnull=True).count(),
        'sub_count': Game_stats.objects.all().count(),
        'teams': Game_stats.objects.all(),
        }
        

    return render(request, 'stats/scout-hub.html', context)


def returnVal(stats, id):
    data = []
    for i in stats.match_set.all().values_list(id, flat = True).filter(updatingEntry=False):
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

@login_required
def ScoutDetail(request, id):
    
    stats = get_object_or_404(Game_stats, id=id)
    data = {}
    for i in Match._meta.get_fields():
        data[i.name] = returnVal(stats, i.name)
        
    #Percentages for special data
    context = {
        'stat': stats, 
        'data': data,
        'score': Profile.objects.get(user=request.user).relativeScoring,
        'averageDefense': Match.objects.all()
    }
    return render(request, 'stats/game_stats_detail.html', context)

class ScoutListView(ListView):
    model = Game_stats
    template_name = 'stats/game_stats_list'
    context_object_name = 'stats'
    ordering = ['-id']
    paginate_by = 20
    
    def get_context_data(self, *args, **kwargs):          
        context = super(ScoutListView, self).get_context_data(*args, **kwargs)
        new_context_entry = Match.objects.values_list('team_num', flat=True).distinct()
        context["team"] = new_context_entry
        return context
    

class PitListView(ListView):
    
    model = Pit_stats
    template_name = 'stats/pit_stats_list'
    context_object_name = 'teams'
    ordering = ['-id']
    paginate_by = 20

@login_required
def PitDetail(request, stat_id):
    return render(request, 'stats/pit_stats_detail.html', {'object': Pit_stats.objects.get(stat_id=stat_id)})


def randomIDGenerator():
    range_start = 10**(15-1)
    range_end = (10**15)-1
    return randint(range_start, range_end)

@login_required
def pit_scout(request):
    form = pit_scout_form(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            
            obj = form.save(commit=False)
            
            
            team_num = form.cleaned_data['team_num']
            
            obj.is_incorrect = False
            stat_gen = randomIDGenerator()
            
            obj.scout = Profile.objects.get(user=request.user)
            
            obj.stat_id = stat_gen
            while Pit_stats.objects.filter(stat_id=stat_gen).exists():
                obj.stat_id = randomIDGenerator()
            
            if not Team.objects.filter(team_num = team_num).exists():
                Team.objects.create(team_num = team_num)

            if Pit_stats.objects.filter(team_num = team_num).exists():
                
                    pk = Pit_stats.objects.get(team_num=team_num).pk
                    return redirect('pitdata-view', pk=pk)
        
            form.save()
            messages.success(request, "Pit entry submitted, Thank You")
            return redirect('pitscout-view')
        else:
    
            messages.error(request, "Form invalid, Try submitting data again properly")
            return redirect('pitscout-view')
    return render(request, 'stats/pit-scout.html', {'form': form})

    
@login_required
def scout(request):
    form = game_scout_form(request.POST)
    if request.method == 'POST':
        obj = form.save(commit=False)
        if form.is_valid() and not Match.objects.filter(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).exists():
            #Saving team number of user to Game_stats object
            
            obj.scout = CustomUser.objects.get(username=request.user)
            #Gathering data
            team_num = form.cleaned_data['team_num']
            obj.score = 0
            #Creating new team if necessary
            if not Team.objects.filter(team_num = team_num).exists():
                Team.objects.create(team_num = team_num)
            # if not Game_stats.objects.filter(team = team_num).exists():
            #     Game_stats.objects.create(team = Team.objects.get(team_num = team_num), rank=0)
            
            # if(Match.objects.filter(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False)):
            #     Match.objects.filter(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).update(
            #         auto_lower =  floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).auto_lower)) + int(obj.auto_lower) / 2),
            #         auto_upper = floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).auto_upper)) + int(obj.auto_upper) / 2),
            #         lower = floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).lower)) + int(obj.lower) / 2),
            #         upper = floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).upper)) + int(obj.upper) / 2),
            #         opposite_color = floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).opposite_color)) + int(obj.opposite_color) / 2),
            #         defense_percentage = floor((int(Match.objects.get(match_number = obj.match_number, team_num=obj.team_num, updatingEntry=False).defense_percentage)) + int(obj.defense_percentage) / 2),
            #     )
            #     obj.updatingEntry = True


            #Finally, add Game_stats object to the team
            obj.stat = Team.objects.get(team_num = team_num).game_stats
            form.save()
            return redirect('home-view')
        else:
            messages.error(request, "Data already scouted for this team during this match")
            return redirect('scout-view')
    return render(request, 'stats/scout.html', {'form': form})


@login_required
def pitFlag(request, stat_id):
    instance = get_object_or_404(Pit_stats, stat_id=stat_id)
    form = pit_correct_form(instance=instance)
    # subject = 'Thank you for registering to our site'
    # message = 'it means a world to us '
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['jtyler03@optonline.net',]
    # send_mail( subject, message, email_from, recipient_list )
    if request.method == 'POST':
        form = pit_correct_form(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_incorrect = True
            instance.save()
            return redirect('/profile')
    context = {
        'form': form
    }
    return render(request, 'stats/pit-flag.html', context)

@login_required
def archiveWarning(request, id):
    context = {'id': id}
    return render(request, 'stats/warning.html', context)

@login_required
def downloadGameData(request, id):
    stats = Match.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=match_data.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Team Number', 'Competition', 'Match Number', 'Left Tarmac', 'Auto Lower', 'Auto Upper', 'Lower', 'Upper', 'Climb', 'Defense Percentage', 'Notes'])
    stat = stats.values_list('id','team_num', 'competition', 'match_number', 'left_tarmac', 'auto_lower', 'auto_upper', 'lower', 'upper', 'robot_climb', 'defense_percentage', 'notes')
    for std in stat:
        writer.writerow(std)
    if(Match.objects.filter(team_num=request.user.team_num).count() > 0):
        for i in Match.objects.filter(team_num=request.user.team_num):
            i.delete()
    return response


