from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from datetime import datetime


def student_list(request):
    students = Student.objects.all().order_by('-date')

    query = request.GET.get('q')
    status = request.GET.get('status')

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_id__icontains=query)
        )

    if status == 'present':
        students = students.filter(is_present=True)
    elif status == 'absent':
        students = students.filter(is_present=False)

    context = {
        'students': students,
        'query': query,
        'status': status
    }

    return render(request, 'index.html', context)





def add_student(request):
    if request.method == 'POST':
    
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')   
        date_str = request.POST.get('date')      
        is_present = request.POST.get('is_present') 


        is_present = True if is_present == 'present' else False

       
        new_student = Student(
            name=name,
            student_id=student_id,
            date=date_str,
            is_present=is_present
        )
        new_student.save()
        
       
        return redirect("/")

    return render(request, 'add.html')



def edit_student(request, student_id):
    
    select_student = Student.objects.get(pk=student_id)
    
    if request.method == 'POST':
        body = request.POST
        name = body.get('name')
        new_student_id = body.get('student_id')
        date = body.get('date')
        is_present = body.get('is_present') 
        
        # Match the HTML <option value="True"> logic
        is_present = True if is_present == 'True' or is_present == 'present' else False

        # Update the student object
        select_student.name = name
        select_student.student_id = new_student_id
        select_student.date = date
        select_student.is_present = is_present
        
        select_student.save()
        return redirect("/")
    
    context = {
        "student": select_student
    }
    
    return render(request, "edit.html", context)


def delete_student(request, student_id):
    if request.method == 'GET':
        select_student = Student.objects.get(pk=student_id)
        context = {
            "student": select_student
        }
    
        return render(request, "delete.html", context)
    elif request.method == 'POST':
        select_student = Student.objects.get(pk=student_id)
        select_student.delete()
        return redirect("/")
    
    


def view_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    context = {
        "student": student
    }
    
    return render(request, 'view.html', context)