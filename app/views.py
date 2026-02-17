from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .forms import RegistrationForm,LoginForm
from .models import Category,Question,Score
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import make_password
import win32com.client
import pythoncom

# Create your views here.
def homepage(request):
    pythoncom.CoInitialize()
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak("Welcome to Quiz Zone")
    finally:
        pythoncom.CoUninitialize()

    return render(request,'index.html')


class Registration(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'registration.html',{'form':form})
    def post(self,request):
        form =RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation User Registration successfully')
            form = RegistrationForm()
        else:
            messages.error(request, 'Invalid input Data')
        return render(request, 'registration.html', {'form':form})

class Login(View):
    def get(self,request):
        form = LoginForm()
        return render(request , "login.html",{'form':form})
    def post(self,request):
        form = LoginForm(request ,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,'Login Successfully')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request , "login.html",{'form':form})

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def aboutpage(request):

    pythoncom.CoInitialize()
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(
            "Welcome to the About page of Quiz Zone. "
            "Quiz Zone is designed for IT and Computer Science students "
            "to practice and improve their technical knowledge."
        )
    finally:
        pythoncom.CoUninitialize()

    return render(request,'about.html')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_list(request):
    categories = Category.objects.all()
    return render(request,'categories.html',{'categories':categories})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def quiz_view(request, category_id, q_no):

    questions = Question.objects.filter(category_id=category_id).order_by('level')
    
    paginator = Paginator(questions, 2)
    pagenumber = request.GET.get('page', 1)
    finalpage = paginator.get_page(pagenumber)
    totalpage = finalpage.paginator.num_pages

    total_questions = questions.count() 

    if q_no > questions.count():
         return redirect('result', category_id=category_id, solved=total_questions)


    question = questions[q_no - 1]

    if request.method == "POST":
        selected = request.POST.get("answer")
        if selected is None:
            return render(request, "quizz.html", {"question": question})

        selected = int(selected)

        if selected == question.correct_option:
            return redirect('quiz', category_id=category_id, q_no=q_no+1)
        else:
            return redirect('gameover', category_id=category_id, solved=q_no-1)


    return render(request, "quizz.html", {
        "question": question,
        "q_no": q_no,
        "finalpage": finalpage,
        "lastpage": totalpage
    })

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def result_view(request, category_id, solved):
    if request.user.is_authenticated:
        Score.objects.update_or_create(
            user=request.user,
            category_id=category_id,
            defaults={'score': solved}
        )
        text = f"Congratulations {request.user.username}. You have successfully completed {solved} questions. Keep learning and keep growing."

        pythoncom.CoInitialize()
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        finally:
            pythoncom.CoUninitialize()

    return render(request, "result.html", {"solved": solved})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def gameover_view(request, category_id, solved):

    if request.user.is_authenticated:

        Score.objects.update_or_create(
            user=request.user,
            category_id=category_id,
            defaults={'score': solved}
        )

        text = f"Sorry {request.user.username}, the game is over. You solved {solved} questions. Better luck next time!"

        pythoncom.CoInitialize()
        try:
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        finally:
            pythoncom.CoUninitialize()

    return render(request, "gameover.html", {"solved": solved})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def leaderboard(request):
    categories = Category.objects.all()
    users = User.objects.all()

    search = request.GET.get('search')

    if search:
        users = users.filter(username__icontains=search)

    user_scores = {}
    for user in users:
        scores_dict = {}
        for cat in categories:
            score_obj = Score.objects.filter(user=user, category=cat).first()
            scores_dict[cat] = score_obj.score if score_obj else 0
        user_scores[user] = scores_dict

    return render(request, 'leaderboard.html', {
        'categories': categories,
        'user_scores': user_scores,
        'search': search
    })

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_view(request):
    user = request.user
    
    scores = Score.objects.filter(user=user)
    total_score = sum(score.score for score in scores)
    total_attempts = scores.count()

    pythoncom.CoInitialize()
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(f"Welcome {user.username}. This is your profile page.")
    finally:
        pythoncom.CoUninitialize()

    context = {
        "user": user,
        "scores": scores,
        "total_score": total_score,
        "total_attempts": total_attempts,
    }

    return render(request, "profile.html", context)

def user_logout(request):
    logout(request)
    return redirect('login')



def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            messages.success(request, f"Confirmation: Password reset link ready for {user.username}")
            return redirect('reset_password', user_id=user.id)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')
    

def reset_password(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")
        
        if password != confirm:
            messages.error(request, "Passwords do not match")
        else:
            user.password = make_password(password)
            user.save()
            messages.success(request, "Password changed successfully. You can now login.")
            return redirect('login')

    return render(request, 'reset_password.html', {"user": user})
