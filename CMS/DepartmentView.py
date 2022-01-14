from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import pymysql as MYSQL
from . import pool
import os

@xframe_options_exempt
def DepartmentInterface(request):
    try:
        row=request.session['ADMIN']
        return render(request,"Department.html")
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitDepartment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        courseid=request.GET['courseid']
        departmentname=request.GET['departmentname']
        q="insert into department (courseid,departmentname) values({0},'{1}')".format(courseid,departmentname)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"Department.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"Department.html",{'status':False})

@xframe_options_exempt
def DisplayAllDepartment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select D.*,(select C.coursename from course C where C.courseid=D.courseid) from department D"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row=request.session['ADMIN']
        return render(request, "DisplayAllDepartment.html",{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def DepartmentById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        did=request.GET['did']
        q = "select D.*,(select C.coursename from course C where C.courseid=D.courseid) from department D where D.departmentid={0}".format(did)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        srow=request.session['ADMIN']
        return render(request,"DepartmentById.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def EditDeleteDepartment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        btn=request.GET['btn']
        if(btn=="edit"):
            departmentid=request.GET['departmentid']
            courseid=request.GET['courseid']
            departmentname=request.GET['departmentname']
            q="update department set courseid={0},departmentname='{1}' where departmentid={2}".format(courseid,departmentname,departmentid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="delete"):
            departmentid=request.GET['departmentid']
            q="delete from department where departmentid={}".format(departmentid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request,"DepartmentById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"DepartmentById.html",{'status':False})

@xframe_options_exempt
def DisplayAllDepartmentJSON(request):
    try:
        db,cmd=pool.ConnectionPooling()
        cid=request.GET['cid']
        q="select * from department where courseid={}".format(cid)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse([],safe=False)