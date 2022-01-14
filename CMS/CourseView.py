from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from . import pool

@xframe_options_exempt
def CourseInterface(request):
    try:
        row=request.session['ADMIN']
        return render(request,"Course.html")
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitCourse(request):
    try:
        db,cmd=pool.ConnectionPooling()
        coursename=request.GET['coursename']
        q="insert into course (coursename) values('{0}')".format(coursename)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"Course.html",{'status':True})
    except Exception as e:
        print("Error.....",e)
        return render(request,"Course.html",{'status':False})

@xframe_options_exempt
def DisplayAllCourse(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from course"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row=request.session['ADMIN']
        return render(request,"DisplayAllCourse.html",{'rows':rows})
    except Exception as e:
        print("Error..",e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def CourseById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        cid=request.GET['cid']
        q="select * from course where courseid={}".format(cid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.commit()
        db.close()
        srow=request.session['ADMIN']
        return render(request,"CourseById.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def EditDeleteCourse(request):
    try:
        db,cmd=pool.ConnectionPooling()
        btn=request.GET['btn']
        if(btn=="edit"):
            courseid = request.GET['courseid']
            coursename = request.GET['coursename']
            q = "update course set coursesname='{0}' wherer courseid={1}".format(coursename, courseid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="delete"):
            courseid=request.GET['courseid']
            q="delete from course where courseid={}".format(courseid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request,"CourseById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"CourseById.html",{'status':False})

@xframe_options_exempt
def DisplayAllCourseJSON(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from course"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse([],safe=False)

