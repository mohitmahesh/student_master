from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import StudentDetails
from .models import TeacherDetails
from .models import Term1
from .models import Term2
from .models import Finals
from .models import User
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.hashers import make_password

def base(request):
    return render(request, 'base.html')

def login_s(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        student = authenticate(username=username,password=password)
        if student is None:
            return redirect('login')
        else:
            login(request,student)
            return redirect('home')
    return render(request,"login.html")

def login_t(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        teacher = authenticate(username=username,password=password)
        if teacher is None:
            print("EH DOG")
            return redirect('teacherlogin')
        else:
            login(request,teacher)
            teacher_user_object = User.objects.get(username=username)
            teacher_details = TeacherDetails.objects.get(teacher=teacher_user_object)
            print(teacher_details.is_principal)
            if teacher_details.is_principal == True:
                return redirect('principalhome')
            else:
                return redirect('teacherhome')
    return render(request,"teacherlogin.html")


def logout(request):
    logout(request)
    return redirect('base')
    
@login_required
def principalhome(request):
    if request.method == "POST":
        if 'addteacher' in request.POST.keys():
            username = request.POST['username']
            password = request.POST['password']
            subject = request.POST['subject']
            password_hashed = make_password(password)
            teacher_user_object = User(username=username, password=password_hashed)
            teacher_user_object.save()
            teacher_user_object = User.objects.get(username=username)
            teacher_details = TeacherDetails(teacher=teacher_user_object, subject=subject)
            teacher_details.save()
            return redirect('principalhome')
        elif 'removeteacher' in request.POST.keys():
            teacher_user_id = request.POST['teacherid']
            teacher_user_object = User.objects.get(id=teacher_user_id)
            teacher_user_object.delete()
            return redirect('principalhome')
    else:
        teachers = TeacherDetails.objects.all().filter(is_principal=False)
        return render(request, 'principalhome.html', {'teachers':teachers})

@login_required  
def teacherhome(request):
    if request.method == 'POST':
        teacher = request.user
        teacher_profile = TeacherDetails.objects.get(teacher=teacher)
        teacher_subject = teacher_profile.subject
        data = request.POST
        if 'add-student' in data.keys():
            username = data['username']
            password = data['password']
            hashed_password = make_password(password)
            new_student = User(username=username,password=hashed_password)
            new_student.save()
            new_student = User.objects.get(username=username)
            f_name = data['f-name']
            m_name = data['m-name']
            rollno = data['rollno']
            dob = data['dob']
            new_student_profile = StudentDetails(user=new_student,rollno=rollno,fname=f_name,mname=m_name,dob=dob)
            new_student_profile.save()
        if 'change-marks' in data.keys():
            student_username = data['student']
            student = User.objects.get(username=student_username)
            student_profile = StudentDetails.objects.get(user=student)
            exam = data['exam']
            marks = data['marks']
            if exam == 'Term1':
                exam_marks = Term1.objects.get(user=student_profile)
                if teacher_subject == 'phy':
                    exam_marks.phy = marks
                    exam_marks.save()
                if teacher_subject == 'chem':
                    exam_marks.chem = marks
                    exam_marks.save()
                if teacher_subject == 'math':
                    exam_marks.math = marks
                    exam_marks.save()
                if teacher_subject == 'comp':
                    exam_marks.comp = marks
                    exam_marks.save()
                if teacher_subject == 'eng':
                    exam_marks.eng = marks
                    exam_marks.save()
            if exam == 'Term2':
                exam_marks = Term2.objects.get(user=student_profile)
                if teacher_subject == 'phy':
                    exam_marks.phy = marks
                    exam_marks.save()
                if teacher_subject == 'chem':
                    exam_marks.chem = marks
                    exam_marks.save()
                if teacher_subject == 'math':
                    exam_marks.math = marks
                    exam_marks.save()
                if teacher_subject == 'comp':
                    exam_marks.comp = marks
                    exam_marks.save()
                if teacher_subject == 'eng':
                    exam_marks.eng = marks
                    exam_marks.save()
            if exam == 'Finals':
                exam_marks = Finals.objects.get(user=student_profile)
                if teacher_subject == 'phy':
                    exam_marks.phy = marks
                    exam_marks.save()
                if teacher_subject == 'chem':
                    exam_marks.chem = marks
                    exam_marks.save()
                if teacher_subject == 'math':
                    exam_marks.math = marks
                    exam_marks.save()
                if teacher_subject == 'comp':
                    exam_marks.comp = marks
                    exam_marks.save()
                if teacher_subject == 'eng':
                    exam_marks.eng = marks
                    exam_marks.save()
        return redirect('teacherhome')
    else:
        students = StudentDetails.objects.all().order_by('rollno')
        return render(request,'teacherhome.html', {'students':students})
    

def home(request):
    user = request.user
    student_id = user.id
    #username=form.cleaned_data.get('username')
    student_object = User.objects.get(id=student_id)
    student_details = StudentDetails.objects.get(user=student_object)
    return render(request,'home.html',{'student':student_details})
    
@login_required(login_url='s_manage:login')
def logout_view(request):
    logout(request)
    return redirect('myaccounts:home')


@login_required    
def term1(request):
    student = request.user
    student_id = student.id
    student_object = User.objects.get(id=student_id)
    student_details = StudentDetails.objects.get(user=student_object)
    term1_marks = Term1.objects.get(user=student_details)
    return render(request, 'marks.html', {'marks':term1_marks})
@login_required
def term2(request):
    student = request.user
    student_id = student.id
    student_object = User.objects.get(id=student_id)
    student_details = StudentDetails.objects.get(user=student_object)
    term2_marks = Term2.objects.get(user=student_details)
    return render(request, 'marks.html', {'marks':term2_marks})
@login_required
def finals(request):
    student = request.user
    student_id = student.id
    student_object = User.objects.get(id=student_id)
    student_details = StudentDetails.objects.get(user=student_object)
    finals_marks = Finals.objects.get(user=student_details)
    return render(request, 'marks.html', {'marks':finals_marks})

@login_required
def reportcard(request):
    student = request.user
    student_id = student.id
    student_object = User.objects.get(id=student_id)
    student_details = StudentDetails.objects.get(user=student_object)
    term1_marks = Term1.objects.get(user=student_details)
    term2_marks = Term2.objects.get(user=student_details)
    finals_marks = Finals.objects.get(user=student_details)
    return render(request,'reportcard.html', {'term1_marks':term1_marks,'term2_marks':term2_marks,'finals_marks':finals_marks})

