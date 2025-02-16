from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponse


# ------------- Login ------------------
def q_login(req):
    if 'user' in req.session:
        return redirect(userpro)
    if 'quiz' in req.session:
        return redirect(adpro)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['quiz']=uname
                return redirect(adhome)
            else:
                login(req,data)
                req.session['user']=uname
                req.session['user1']= data.id
                return redirect(home)
        else:
            messages.warning(req,"Invalid uname or password")
            return redirect(q_login)
    else:
        return render(req,'login.html')

def q_logout(req):
    req.session.flush()          
    logout(req)
    return redirect(home)


def register(req):
    if req.method == 'POST':
        fname = req.POST['fname']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['fname'] = fname
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp_reg')
    return render(req, 'register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        fname = req.session.get('fname')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=fname,email=email,password=password,username=email)
            player=Player.objects.create(user=user,name=fname,email=email)
            user.is_verified = True
            user.save()    
            player.save()  
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Bookmart', settings.EMAIL_HOST_USER, [email])
            return redirect('login')
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'verify_oto_reg.html')

def resend_otp_reg(req):
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        
        send_mail(
            'Your New OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP resent to your email")
    
    return redirect('verify_otp_reg')
        
def forgetpassword(req):
    if req.method == 'POST':
        email = req.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.warning(req, "Email not found")
            return redirect('forgetpassword')
    return render(req, 'forgetpassword.html')

def verify_otp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session.get('otp'):
            return redirect('resetpassword')
        else:
            messages.warning(req, "Invalid OTP")
            return redirect('verify_otp')
    return render(req, 'verify_otp.html')

def resend_otp(req):  
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
        messages.success(req, "OTP resent to your email")
    return redirect('verify_otp')

def resetpassword(req):
    if req.method == 'POST':
        password = req.POST['password']  
        email = req.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(req, "Password reset successfully")
            return redirect('login')
        except User.DoesNotExist:
            messages.warning(req, "Error resetting password")
            return redirect('resetpassword')
    return render(req, 'resetpassword.html')



# ----------------Admin-----------------

def adhome(req):
    if req.method == 'POST':
        text = req.POST.get('text')
        option_a = req.POST.get('option_a')
        option_b = req.POST.get('option_b')
        option_c = req.POST.get('option_c')
        option_d = req.POST.get('option_d')
        correct_answer = req.POST.get('correct_answer')
        difficulty = req.POST.get('difficulty')
        time = req.POST.get('time')
        if text and option_a and option_b and option_c and option_d and correct_answer:
            question = Question(
                text=text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                difficulty=difficulty,
                time=time
            )
            question.save()
            return redirect('adhome')  
        else:
            return HttpResponse("Please fill out all fields.", status=400)
    else:
         return render(req,'admin/adhome.html')
    
def viewqst(request):
    difficulty = request.GET.get('difficulty', None)
    if difficulty:
        questions = Question.objects.filter(difficulty=difficulty)
    else:
        questions = Question.objects.all()
    return render(request, 'admin/viewqs.html', {'questions': questions, 'difficulty': difficulty})

def editqst(request, question_id):
    question = get_object_or_404(Question, id=question_id)    
    if request.method == 'POST':
        question.text = request.POST.get('text')
        question.option_a = request.POST.get('option_a')
        question.option_b = request.POST.get('option_b')
        question.option_c = request.POST.get('option_c')
        question.option_d = request.POST.get('option_d')
        question.correct_answer = request.POST.get('correct_answer')
        question.difficulty = request.POST.get('difficulty')
        question.time = request.POST.get('time')
        question.save()
        return redirect('viewqst')
    return render(request, 'admin/editqst.html', {'question': question})
   

def adpro(req):
    return render(req,'admin/adpro.html')

def player_list(request):
    players = Player.objects.all()  
    return render(request, 'admin/viewplayer.html', {'players': players})

def adleaderboard(req):
    players = Player.objects.all().order_by('-score') 
    return render(req, 'admin/leaders.html', {'players': players})

# -------------- Users -------------------
def home(req):
    return render(req, 'user/index.html')

def userpro(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Player.objects.filter(user=user)
        return render(req,'user/userpro.html',{'data':data})
    else:
        return redirect('login')

def edit_player(req,id):
    player = get_object_or_404(Player, pk=id)
    if req.method == 'POST':
        player.name = req.POST.get('name')
        player.dob = req.POST.get('dob')
        player.save()
        messages.success(req, "Player details have been updated successfully.")
        return redirect(userpro)  
    return render(req, 'user/editpro.html', {'player': player})

def select_level(req):
    return render(req, 'user/selectlvl.html')

def start_quiz(req):
    if 'user1' in req.session:
        req.session['score'] = 0
        req.session['lives'] = 3
        level = req.GET.get('level')  
        if level == 'easy':
            questions = Question.objects.filter(difficulty=1)
            timer_duration = 60
        elif level == 'medium':
            questions = Question.objects.filter(difficulty=2)
            timer_duration = 30
        elif level == 'hard':
            questions = Question.objects.filter(difficulty=3)
            timer_duration = 15
        else:
            questions = Question.objects.all()
            timer_duration = 60  
        if not questions:
            return render(req, 'user/noqst.html')
        question = random.choice(questions)
        req.session['level'] = level
        return render(req, 'user/quiz.html', {'question': question, 'timer_duration': timer_duration})
    else:
        return redirect('login')

def question(req):
    if req.session.get('lives', 3) <= 0:
        return redirect('game_over')
    if 'level' not in req.session:
        return redirect('select_level')
    level = req.session['level']
    if level == 'easy':
        questions = Question.objects.filter(difficulty=1)
    elif level == 'medium':
        questions = Question.objects.filter(difficulty=2)
    elif level == 'hard':
        questions = Question.objects.filter(difficulty=3)
    else:
        questions = Question.objects.all() 
    if not questions:
        return render(req, 'quiz/no_questions.html')
    question = random.choice(questions)
    req.session['current_question_id'] = question.id
    req.session.modified = True
    return render(req, 'user/quiz.html', {'question': question})

def check_answer(req):
    if 'score' not in req.session:
        req.session['score'] = 0
    if 'lives' not in req.session:
        req.session['lives'] = 3

    if req.method == 'POST':
        selected_answer = req.POST.get('answer')
        question_id = req.POST.get('question_id')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            messages.error(req, "Question not found.")
            return redirect('question')
        if selected_answer.upper() == question.correct_answer:
            req.session['score'] += 5 
            feedback = {
                'message': 'Correct!',
                'class': 'alert-success'
            }
        else:
            req.session['lives'] -= 1  
            feedback = {
                'message': 'Incorrect!',
                'class': 'alert-danger'
            }
        req.session.modified = True
        if req.user.is_authenticated:
            user = req.user
            try:
                player = Player.objects.get(user=user)

                if req.session['score'] > player.score:
                    player.score = req.session['score']
                    player.save()
            except Player.DoesNotExist:
                Player.objects.create(user=user, score=req.session['score'])
        if req.session['lives'] <= 0:
            return redirect('game_over')
        next_question = Question.objects.order_by('?').first()
        req.session['current_question_id'] = next_question.id
        req.session.modified = True
        return render(req, 'user/quiz.html', {
            'question': next_question,
            'feedback': feedback
        })
def game_over(req):
    score = req.session.get('score', 0)
    return render(req, 'user/gameover.html', {'score': score})

def leaderboard(req):
    players = Player.objects.all().order_by('-score')  
    return render(req, 'user/leaders.html', {'players': players})