from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from . import pool
import os
import random

@xframe_options_exempt
def StudentInterface(request):
    try:
        row = request.session['ADMIN']
        return render(request, "Student.html")
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def DisplayAllBranchJSON(request):
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

@xframe_options_exempt
def SubmitStudent(request):
    try:
        db,cmd=pool.ConnectionPooling()
        studentname=request.POST['studentname']
        dob=request.POST['dob']
        admissionyear=request.POST['admissionyear']
        email=request.POST['email']
        address=request.POST['address']
        courseid=request.POST['courseid']
        branchid=request.POST['branchid']
        spicture=request.FILES['spicture']
        password="".join(random.sample(['1','q','8','x','6','#','@','Z'],k=7))
        q="insert into student (studentname,dob,admissionyear,email,address,courseid,branchid,spicture,password) values('{0}','{1}',{2},'{3}'," \
          "'{4}',{5},{6},'{7}','{8}')".format(studentname,dob,admissionyear,email,address,courseid,branchid,spicture.name,password)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/"+spicture.name,"wb")
        for chunk in spicture.chunks():
            P.write(chunk)
        P.close()
        db.close()
        return render(request,"Student.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"Student.html",{'status':False})

@xframe_options_exempt
def DisplayAllStudent(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D " \
          "where D.departmentid=S.branchid) from student S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row = request.session['ADMIN']
        return render(request, "DisplayAllStudent.html",{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def StudentById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        stid=request.GET['stid']
        q="select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D " \
          "where D.departmentid=S.branchid) from student S where S.studentid={}".format(stid)
        cmd.execute(q)
        rows=cmd.fetchone()
        db.close()
        row = request.session['ADMIN']
        return render(request,"StudentById.html",{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def EditDeleteStudentData(request):
    try:
        db,cmd=pool.ConnectionPooling()
        btn=request.GET['btn']
        if(btn=="edit"):
            studentid=request.GET['studentid']
            studentname=request.GET['studentname']
            dob=request.GET['dob']
            admissionyear=request.GET['admissionyear']
            email=request.GET['email']
            address=request.GET['address']
            courseid=request.GET['courseid']
            branchid=request.GET['branchid']
            q="update student set studentname='{0}',dob='{1}',admissionyear={2},email='{3}',address='{4}',courseid={5},branchid={6} where studentid={7}" \
              "".format(studentname,dob,admissionyear,email,address,courseid,branchid,studentid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="delete"):
            studentid=request.GET['studentid']
            q="delete from student where studentid={}".format(studentid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request,"StudentById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"StudentById.html",{'status':False})

@xframe_options_exempt
def EditPicture(request):
    try:
        db,cmd=pool.ConnectionPooling()
        studentid=request.POST['studentid']
        filename1=request.POST['filename1']
        spicture=request.FILES['spicture']
        q="update student set spicture='{0}'where studentid={1}".format(spicture.name,studentid)
        cmd.execute(q)
        db.commit()
        S=open("D:/CMS/assets/"+spicture.name,"wb")
        for chunk in spicture.chunks():
            S.write(chunk)
        S.close()
        os.remove("D:/CMS/assets/"+filename1)
        db.close()
        return render(request,"StudentById.html",{'status':True})
    except Exception as e:
        print('errror:',e)
        return render(request,"StudentById.html",{'status':False})


    #Student Frontend

def StudentView(request):
    return render(request,"StudentView.html")
def StudentLogin(request):
    return render(request,"StudentLogin.html",{'msg':""})

def CheckStudent(request):
    try:
        db,cmd=pool.ConnectionPooling()
        studentid=request.POST['studentid']
        password=request.POST['password']
        q="select * from student where studentid={} and password='{}'".format(studentid,password)
        p = "select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select T.icon from teacher T where T.teacherid=E.teacherid)," \
            "(select S.subjectname from subject S where S.subjectid=E.subjectid) from enrollstudent E where E.studentid".format(studentid)
        cmd.execute(q)
        row=cmd.fetchone()
        cmd.execute(p)
        prow=cmd.fetchall()
        r="select * from news"
        cmd.execute(r)
        nrow=cmd.fetchall()
        db.close()
        if(row and prow):
            return render(request,"StudentView.html",{'row':row,'prow':prow,'nrow':nrow})
        else:
            return render(request,"Slogin.html",{'msg':"Please Input Valid Id/Password..."})
    except Exception as e:
        print('error:',e)
        return render(request,"Slogin.html",{'msg':"Server Error..."})

def StudentCourse(request):
        try:
            db, cmd = pool.ConnectionPooling()
            subid = request.GET['subid']
            tid = request.GET['tid']
            sid=request.GET['sid']
            q = "select * from subject where subjectid={}".format(subid)
            p = "select * from teacher where teacherid={}".format(tid)
            s="select * from student where studentid={}".format(sid)
            r = "select * from enrollstudent where teacherid={} and subjectid={} and studentid={}".format(tid, subid,sid)
            cmd.execute(q)
            srow = cmd.fetchone()
            cmd.execute(p)
            trow = cmd.fetchone()
            cmd.execute(r)
            rrow = len(cmd.fetchall())
            cmd.execute(s)
            strow=cmd.fetchone()
            db.close()
            return render(request, "StudentCourse.html", {'srow': srow, 'trow': trow, 'rrow': rrow,'strow':strow})
        except Exception as e:
            print('error:', e)
            return render(request, "StudentCourse.html", {'srow': [], 'trow': [], 'rrow': 0,'strow':[]})

    # Student Profile
def StudentProfile(request):
        try:
            db, cmd = pool.ConnectionPooling()
            sid = request.GET['sid']
            p = "select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D where D.departmentid=S.branchid) from student S where S.studentid={}".format(sid)
            cmd.execute(p)
            trow = cmd.fetchone()
            db.close()
            return render(request, "StudentProfile.html", {'trow': trow})
        except Exception as e:
            print('error:', e)
            return render(request, "StudentProfile.html", {'trow': []})

     #Student Course Material

def StudentCourseMaterail(requesst):
    try:
        db,cmd=pool.ConnectionPooling()
        subid=requesst.GET['subid']
        tid=requesst.GET['tid']
        sid=requesst.GET['sid']
        q="select * from subject where subjectid={}".format(subid)
        r="select * from teacher where teacherid={}".format(tid)
        s="select * from teachercoursematerial where subjectid={} and teacherid={}".format(subid,tid)
        t="select * from student where studentid={}".format(sid)
        p = "select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select T.icon from teacher T where T.teacherid=E.teacherid)," \
            "(select S.subjectname from subject S where S.subjectid=E.subjectid) from enrollstudent E where E.studentid".format(sid)
        cmd.execute(p)
        prow=cmd.fetchall()
        cmd.execute(q)
        srow=cmd.fetchone()
        cmd.execute(r)
        trow=cmd.fetchone()
        cmd.execute(s)
        smrow=cmd.fetchall()
        cmd.execute(t)
        strow=cmd.fetchone()
        db.close()
        return render(requesst,"StudentCourseMaterial.html",{'prow':prow,'srow':srow,'trow':trow,'smrow':smrow,'strow':strow})
    except Exception as e:
        print('error:',e)
        return render(requesst,"StudentCourseMaterial.html",{'prow':[],'srow':[],'trow':[],'smrow':[],'strow':[]})

    #Student Lectures

def StudentLecture(requesst):
    try:
        db,cmd=pool.ConnectionPooling()
        subid=requesst.GET['subid']
        tid=requesst.GET['tid']
        sid=requesst.GET['sid']
        q="select * from subject where subjectid={}".format(subid)
        r="select * from teacher where teacherid={}".format(tid)
        s="select * from lecture where subjectid={} and teacherid={}".format(subid,tid)
        t="select * from student where studentid={}".format(sid)
        p = "select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select T.icon from teacher T where T.teacherid=E.teacherid)," \
            "(select S.subjectname from subject S where S.subjectid=E.subjectid) from enrollstudent E where E.studentid".format(sid)
        cmd.execute(p)
        prow=cmd.fetchall()
        cmd.execute(q)
        srow=cmd.fetchone()
        cmd.execute(r)
        trow=cmd.fetchone()
        cmd.execute(s)
        smrow=cmd.fetchall()
        cmd.execute(t)
        strow=cmd.fetchone()
        db.close()
        return render(requesst,"StudentLectures.html",{'prow':prow,'srow':srow,'trow':trow,'smrow':smrow,'strow':strow})
    except Exception as e:
        print('error:',e)
        return render(requesst,"StudentLectures.html",{'prow':[],'srow':[],'trow':[],'smrow':[],'strow':[]})