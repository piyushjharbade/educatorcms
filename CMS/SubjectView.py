from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from . import pool
import os
@xframe_options_exempt
def SubjectInterface(request):
    try:
        row=request.session['ADMIN']
        return render(request, "Subject.html", {'row': row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitSubject(request):
    try:
        db,cmd=pool.ConnectionPooling()
        courseid=request.POST['courseid']
        departmentid=request.POST['departmentid']
        subjectname=(request.POST['subjectname']).upper()
        icon=request.FILES['icon']
        q="insert into subject (courseid,departmentid,subjectname,icon) values({0},{1},'{2}','{3}')".format(courseid,departmentid,subjectname,icon.name)
        cmd.execute(q)
        db.commit()
        I=open("D:/CMS/assets/subjecticons/"+icon.name,"wb")
        for chunk in icon.chunks():
            I.write(chunk)
        I.close()
        db.close()
        return render(request,"Subject.html",{'status':True})
    except Exception as e:
        print('error',e)
        return render(request,"Subject.html",{'status':False})

@xframe_options_exempt
def DisplayAllSubject(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D where D.departmentid=S.departmentid) from subject S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row = request.session['ADMIN']
        return  render(request,"DisplayAllSubject.html",{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubjectById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        sid=request.GET['sid']
        q="select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D where D.departmentid=S.departmentid) from subject S where subjectid={}".format(sid)
        cmd.execute(q)
        rows=cmd.fetchone()
        db.close()
        srow = request.session['ADMIN']
        return render(request,"SubjectById.html",{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def EditDeleteSubject(request):
    try:
        db,cmd=pool.ConnectionPooling()
        btn=request.GET['btn']
        if(btn=="edit"):
            subjectid=request.GET['subjectid']
            courseid=request.GET['courseid']
            departmentid=request.GET['departmentid']
            subjectname=request.GET['subjectname']
            q="update subject set courseid={0},departmentid={1},subjectname='{2}' where subjectid={3}".format(courseid,departmentid,subjectname,subjectid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="delete"):
            subjectid=request.GET['subjectid']
            q="delete from subject where subjectid={}".format(subjectid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request,"SubjectById.html",{'status':True})
    except Exception as e:
        return render(request,"SubjectById.html",{'status':False})

@xframe_options_exempt
def EditIcon(request):
    try:
        db,cmd=pool.ConnectionPooling()
        sid=request.POST['sid']
        icon=request.FILES['icon']
        oldicon=request.POST['oldicon']
        q="update subject set icon='{0}'where subjectid={1}".format(icon.name,sid)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/subjecticons/"+icon.name,"wb")
        for chunk in icon.chunks():
            P.write(chunk)
        P.close()
        os.remove("D:/CMS/assets/subjecticons/"+oldicon)
        db.close()
        return render(request,"SubjectById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"SubjectById.html",{'status':False})

@xframe_options_exempt
def DisplayAllSubjectJSON(request):
    try:
        db,cmd=pool.ConnectionPooling()
        did=request.GET['did']
        q="select * from subject where departmentid={}".format(did)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return  JsonResponse(rows,safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse([],safe=False)