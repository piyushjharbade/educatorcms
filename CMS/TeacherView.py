from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from . import pool
import os
import random

@xframe_options_exempt
def TeacherInterface(request):
    try:
        row=request.session['ADMIN']
        return render(request,"Teacher.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitTeacher(request):
    try:
        db,cmd=pool.ConnectionPooling()
        teachername=(request.POST['teachername']).upper()
        email=request.POST['email']
        address=request.POST['address']
        picture=request.FILES['picture']
        icon=request.FILES['icon']
        password="".join(random.sample(['1','q','8','x','6','#','@','Z'],k=7))
        q="insert into teacher (teachername,email,address,picture,icon,password) values('{0}','{1}','{2}','{3}','{4}','{5}')".format(teachername,email,address,picture.name,icon.name,password)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/" + picture.name,"wb")
        for chunk in picture.chunks():
            P.write(chunk)
        P.close()
        P=open("D:/CMS/assets/cardImages/" + icon.name,"wb")
        for chunk in icon.chunks():
            P.write(chunk)
        P.close()
        db.close()
        return render(request,"Teacher.html",{'status':True})
    except Exception as e:
        print('error',e)
        return render(request,"Teacher.html",{'status':False})

@xframe_options_exempt
def EnrollTeacher(request):
    try:
        row=request.session['ADMIN']
        return render(request,"EnrollTeacher.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitTeacherEnroll(request):
    try:
        db,cmd=pool.ConnectionPooling()
        teacherid=request.GET['teacherid']
        courseid=request.GET['courseid']
        departmentid=request.GET['departmentid']
        subjectid=request.GET['subjectid']
        q="insert into enrollteacher (teacherid, courseid, departmentid, subjectid) values({},{},{},{})".format(teacherid, courseid, departmentid, subjectid)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"EnrollTeacher.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"EnrollTeacher.html",{'status':False})


@xframe_options_exempt
def FetchAllTeacher(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from teacher"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error:',e)
        return JsonResponse([],safe=False)

@xframe_options_exempt
def DisplayAllTeacher(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from teacher"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row = request.session['ADMIN']
        return render(request, "DisplayAllTeacher.html",{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def DisplayTeacherEnrollment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select C.coursename from course C where C.courseid=E.courseid)," \
          "(select D.departmentname from department D where D.departmentid=E.departmentid),(select S.subjectname from subject S where S.subjectid=E.subjectid) from enrollteacher E"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row = request.session['ADMIN']
        return render(request,"DisplayTeacherEnrollment.html",{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def TeacherById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        tid=request.GET['tid']
        q="select * from teacher where teacherid={}".format(tid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        srow = request.session['ADMIN']
        return render(request,"TeacherById.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def UpadateTeacherEnrollment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        en=request.GET['en']
        q = "select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select C.coursename from course C where C.courseid=E.courseid)," \
            "(select D.departmentname from department D where D.departmentid=E.departmentid),(select S.subjectname from subject S where S.subjectid=E.subjectid) from enrollteacher E where E.enrollnumber".format(en)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        srow = request.session['ADMIN']
        return render(request,"UpdateTeacherEnrollment.html",{'row':row})
    except Exception as e:
        print('error',e)
        return render(request,"AdminLogin.html",{'msg':""})


@xframe_options_exempt
def EditDeleteTeacherEnrollment(request):
    try:
        btn=request.GET['btn']
        en=request.GET['en']
        db,cmd=pool.ConnectionPooling()
        if(btn=="Edit"):
           teacherid = request.GET['teacherid']
           courseid = request.GET['courseid']
           departmentid = request.GET['departmentid']
           subjectid = request.GET['subjectid']
           q="update enrollteacher set teacherid={},courseid={},departmentid={},subjectid={} where enrollnumber={}".format(teacherid,courseid,departmentid,subjectid,en)
           cmd.execute(q)
           db.commit()
           db.close()
        elif(btn=="Delete"):
            q="delete from enrollteacher where enrollnumber={}".format(en)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request, "UpdateTeacherEnrollment.html", {'status': True})
    except Exception as e:
        print('errror:',e)
        return render(request, "UpdateTeacherEnrollment.html", {'status': False})




@xframe_options_exempt
def EditDeleteTeacherData(request):
    try:
        db,cmd=pool.ConnectionPooling()
        btn=request.GET['btn']
        tid=request.GET['tid']
        if(btn=="Edit"):
            teachername=request.GET['teachername']
            email=request.GET['email']
            address=request.GET['address']
            # courseid=request.GET['courseid']
            # departmentid=request.GET['departmentid']
            # subjectid=request.GET['subjectid']
            q="update teacher set teachername='{}',email='{}',address='{}' where teacherid={}".format(teachername,email,address,tid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="Delete"):
            q="delete from teacher where teacherid={}".format(tid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request,"TeacherById.html",{'status':True})
    except Exception as e:
        print('errror:',e)
        return render(request,"TeacherById.html",{'status':False})

@xframe_options_exempt
def EditPicture(request):
    try:
        db,cmd=pool.ConnectionPooling()
        tid=request.POST['tid']
        picture=request.FILES['picture']
        oldpicture=request.POST['oldpicture']
        q="update teacher set picture='{0}'where teacherid={1}".format(picture.name,tid)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/"+picture.name,"wb")
        for chunk in picture.chunks():
            P.write(chunk)
        P.close()
        os.remove("D:/CMS/assets/"+oldpicture)
        db.close()
        return render(request,"TeacherById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"TeacherById.html",{'status':False})


@xframe_options_exempt
def EditIcon(request):
    try:
        db,cmd=pool.ConnectionPooling()
        tid=request.POST['tid']
        icon=request.FILES['icon']
        oldicon=request.POST['oldicon']
        q="update teacher set icon='{0}'where teacherid={1}".format(icon.name,tid)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/cardImages/"+icon.name,"wb")
        for chunk in icon.chunks():
            P.write(chunk)
        P.close()
        os.remove("D:/CMS/assets/cardImages/"+oldicon)
        db.close()
        return render(request,"TeacherById.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"TeacherById.html",{'status':False})


       #ENROLL STUDENT

def EnrollStudent(request):
    return render(request,"EnrollStudent.html")

@xframe_options_exempt
def FetchAllStudent(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select S.*,(select C.coursename from course C where C.courseid=S.courseid),(select D.departmentname from department D where D.departmentid=S.branchid) from student S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error:',e)
        return JsonResponse([],safe=False)

@xframe_options_exempt
def FetchAllSubject(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from subject"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error:',e)
        return JsonResponse([],safe=False)

@xframe_options_exempt
def DisplayAllSubjectJSON(request):
    try:
        db,cmd=pool.ConnectionPooling()
        subid=request.GET['subjectid']
        q="select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollteacher E  where E.subjectid={}".format(subid)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return  JsonResponse(rows,safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse([],safe=False)


def SubjectTeacherData(request):
   try:
    db,cmd=pool.ConnectionPooling()
    subid=request.GET['subid']
    tid=request.GET['tid']
    q="select * from subject where subjectid={}".format(subid)
    p="select * from teacher where teacherid={}".format(tid)
    cmd.execute(q)
    srow=cmd.fetchone()
    cmd.execute(p)
    trow=cmd.fetchone()
    r = "select E.*,(select s.studentname from student s where s.studentid=E.studentid),(select S.subjectname from subject S where S.subjectid=E.subjectid)," \
        "(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollstudent E where subjectid={} and teacherid={}".format(subid,tid)
    cmd.execute(r)
    rows = cmd.fetchall()
    db.close()
    return render(request,"EnrollStudent2.html",{'srow':srow,'trow':trow,'rows':rows})
   except Exception as e:
       print('error:',e)
       return render(request, "EnrollStudent2.html", {'srow': [], 'trow': [],'rows':[]})

def SubmitEnrollStudent(request):
    try:
        db,cmd=pool.ConnectionPooling()
        studentid=request.GET['studentid']
        subjectid=request.GET['subid']
        teacherid=request.GET['tid']
        print(subjectid,teacherid)
        q="insert into enrollstudent (studentid, subjectid, teacherid) values({},{},{})".format( studentid, subjectid, teacherid)
        cmd.execute(q)
        db.commit()
        r = "select E.*,(select s.studentname from student s where s.studentid=E.studentid),(select S.subjectname from subject S where S.subjectid=E.subjectid)," \
            "(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollstudent E where subjectid={} and teacherid={}".format(subjectid,teacherid)
        cmd.execute(r)
        rows = cmd.fetchall()
        db.close()
        return render(request,"EnrollStudent2.html",{'status':True,'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,"EnrollStudent2.html",{'status':False,'rows':[]})
#
# def DisplayStudentEnrollment(request):
#     try:
#         db,cmd=pool.ConnectionPooling()
#         q="select E.*,(select s.studentname from student s where s.studentid=E.studentid),(select S.subjectname from subject S where S.subjectid=E.subjectid)," \
#           "(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollstudent E"
#         cmd.execute(q)
#         rows=cmd.fetchall()
#         db.close()
#         return render(request,"EnrollStudent2.html",{'rows':rows})
#     except Exception as e:
#         print('error:',e)
#         return render(request,"EnrollStudent2.html",{'rows':[]})

def UpdateStudentEnrollment(request):
    try:
        db,cmd=pool.ConnectionPooling()
        en=request.GET['en']
        q="select E.*,(select s.studentname from student s where s.studentid=E.studentid),(select S.subjectname from subject S where S.subjectid=E.subjectid)," \
          "(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollstudent E where E.enrollnumber={}".format(en)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request,"UpdateStudentEnrollment.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"UpdateStudentEnrollment.html",{'row':[]})

def EditDeleteStudentEnroll(request):
    try:
        db,cmd=pool.ConnectionPooling()
        en=request.GET['en']
        q="delete from enrollstudent where enrollnumber={}".format(en)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"EnrollStudent2.html")
    except Exception as e:
        print('error:',e)
        return render(request,"EnrollStudent2.html")

     #Upload Marks

def SubmitMarks(request):
    try:
         db,cmd=pool.ConnectionPooling()
         subid=request.GET['subid']
         tid=request.GET['tid']
         examname=request.GET['examname']
         studentid=request.GET['studentid']
         marks=request.GET['marks']
         print(subid,tid,examname,studentid,marks)
         q="insert into marks (subjectid, teacherid, examname, studentid, marks) values({},{},'{}',{},'{}')".format(subid,tid,examname,studentid,marks)
         cmd.execute(q)
         db.commit()
         db.close()
         return render(request,"Marks.html")
    except Exception as e:
        print('error:',e)
        return render(request,"Marks.html")


def SubjectTeacherData2(request):
        try:
            db, cmd = pool.ConnectionPooling()
            subid = request.GET['subid']
            tid = request.GET['tid']
            q = "select * from subject where subjectid={}".format(subid)
            p = "select * from teacher where teacherid={}".format(tid)
            cmd.execute(q)
            srow = cmd.fetchone()
            cmd.execute(p)
            trow = cmd.fetchone()
            r = "select E.*,(select s.studentname from student s where s.studentid=E.studentid),(select S.subjectname from subject S where S.subjectid=E.subjectid)," \
                "(select T.teachername from teacher T where T.teacherid=E.teacherid) from enrollstudent E where subjectid={} and teacherid={}".format(
                subid, tid)
            cmd.execute(r)
            rows = cmd.fetchall()
            db.close()
            return render(request, "Marks.html", {'srow': srow, 'trow': trow, 'rows': rows})
        except Exception as e:
            print('error:', e)
            return render(request, "Marks.html", {'srow': [], 'trow': [], 'rows': []})


        #Upload Course Material

def SubjectTeacherData3(request):
        try:
            db, cmd = pool.ConnectionPooling()
            subid = request.GET['subid']
            tid = request.GET['tid']
            q = "select * from subject where subjectid={}".format(subid)
            p = "select * from teacher where teacherid={}".format(tid)
            cmd.execute(q)
            srow = cmd.fetchone()
            cmd.execute(p)
            trow = cmd.fetchone()
            r="select * from teachercoursematerial where subjectid={} and teacherid={}".format(subid,tid)
            cmd.execute(r)
            rows = cmd.fetchall()
            db.close()
            return render(request, "TeacherCourseMaterial.html", {'srow': srow, 'trow': trow, 'rows': rows})
        except Exception as e:
            print('error:', e)
            return render(request, "TeacherCourseMaterial.html", {'srow': [], 'trow': [], 'rows': []})


def UplaodCourseMaterial(request):
    try:
        db,cmd=pool.ConnectionPooling()
        subid=request.POST['subid']
        tid=request.POST['tid']
        coursematerial=request.FILES['coursematerial']
        t=request.POST['time']
        day=request.POST['day']
        date=request.POST['date']
        q="insert into teachercoursematerial (subjectid, teacherid, coursematerial, time,day,date) values({},{},'{}','{}','{}','{}')".format(subid,tid, coursematerial.name,t,day,date)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/coursematerial/"+coursematerial.name,"wb")
        for chunk in coursematerial.chunks():
            P.write(chunk)
        P.close()
        db.close()
        return render(request,"TeacherCourseMaterial.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"TeacherCourseMaterial.html",{'status':False})

def DeleteCourseMaterial(request):
    try:
        db,cmd=pool.ConnectionPooling()
        cmno=request.GET['cmno']
        filename=request.GET['filename']
        subid=request.GET['subid']
        tid=request.GET['tid']
        q="delete from teachercoursematerial where coursematerialno={}".format(cmno)
        cmd.execute(q)
        r = "select * from teachercoursematerial where subjectid={} and teacherid={}".format(subid, tid)
        cmd.execute(r)
        rows = cmd.fetchall()
        db.commit()
        os.remove("D:/CMS/assets/coursematerial/"+filename)
        db.close()
        return render(request,"TeacherCourseMaterial.html",{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,"TeacherCourseMaterial.html",{'rows':[]})

    # Teacher Profile
def TeacherProfile(request):
        try:
            db, cmd = pool.ConnectionPooling()
            tid = request.GET['tid']
            p = "select * from teacher where teacherid={}".format(tid)
            r = "select E.*,(select D.departmentname from department D where D.departmentid=E.departmentid) from enrollteacher E where E.teacherid={}".format(
                tid)
            cmd.execute(p)
            trow = cmd.fetchone()
            cmd.execute(r)
            rrow = cmd.fetchone()
            db.close()
            return render(request, "TeacherProfile.html", {'trow': trow, 'rrow': rrow})
        except Exception as e:
            print('error:', e)
            return render(request, "TeacherProfile.html", {'trow': [], 'rrow': 0})

def UpdateTeacherProfile(request):
    try:
        db, cmd = pool.ConnectionPooling()
        btn = request.GET['btn']
        tid = request.GET['tid']
        if (btn == "Edit"):
            teachername = request.GET['teachername']
            email = request.GET['email']
            address = request.GET['address']
            q = "update teacher set teachername='{}',email='{}',address='{}' where teacherid={}".format(teachername,
                                                                                                        email, address,
                                                                                                        tid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request, "TeacherProfile.html")
    except Exception as e:
        print('errror:', e)
        return render(request, "TeacherProfile.html")

    #Upload Lectures
def SubjectTeacherData4(request):
        try:
            db, cmd = pool.ConnectionPooling()
            subid = request.GET['subid']
            tid = request.GET['tid']
            q = "select * from subject where subjectid={}".format(subid)
            p = "select * from teacher where teacherid={}".format(tid)
            cmd.execute(q)
            srow = cmd.fetchone()
            cmd.execute(p)
            trow = cmd.fetchone()
            r = "select * from lecture where subjectid={} and teacherid={}".format(subid, tid)
            cmd.execute(r)
            rows = cmd.fetchall()
            db.close()
            return render(request, "TeacherLectures.html", {'srow': srow, 'trow': trow, 'rows': rows})
        except Exception as e:
            print('error:', e)
            return render(request, "TeacherLectures.html", {'srow': [], 'trow': [], 'rows': []})

def UplaodLecture(request):
    try:
        db,cmd=pool.ConnectionPooling()
        subid=request.POST['subid']
        tid=request.POST['tid']
        lecture=request.FILES['lecture']
        t=request.POST['time']
        day=request.POST['day']
        date=request.POST['date']
        q="insert into lecture (subjectid, teacherid, lectureurl, time, day, date) values({},{},'{}','{}','{}','{}')".format(subid,tid, lecture.name,t,day,date)
        cmd.execute(q)
        db.commit()
        P=open("D:/CMS/assets/lectures/"+lecture.name,"wb")
        for chunk in lecture.chunks():
            P.write(chunk)
        P.close()
        db.close()
        return render(request,"TeacherLectures.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"TeacherLectures.html",{'status':False})

def DeleteLecture(request):
        try:
            db, cmd = pool.ConnectionPooling()
            lno = request.GET['lno']
            filename = request.GET['filename']
            subid = request.GET['subid']
            tid = request.GET['tid']
            q = "delete from lecture where lectureno={}".format(lno)
            cmd.execute(q)
            r = "select * from lecture where subjectid={} and teacherid={}".format(subid, tid)
            cmd.execute(r)
            rows = cmd.fetchall()
            db.commit()
            os.remove("D:/CMS/assets/lectures/" + filename)
            db.close()
            return render(request, "TeacherCourseMaterial.html", {'rows': rows})
        except Exception as e:
            print('error:', e)
            return render(request, "TeacherCourseMaterial.html", {'rows': []})

      #Teacher Frontent

def TeacherLogin(request):
    return render(request,"TeacherLogin.html",{'msg':""})
def CheckTeacher(request):
    try:
        db,cmd=pool.ConnectionPooling()
        teacherid=request.POST['teacherid']
        password=request.POST['password']
        q="select * from teacher where teacherid={} and password='{}'".format(teacherid,password)
        p = "select E.*,(select T.teachername from teacher T where T.teacherid=E.teacherid),(select C.coursename from course C where C.courseid=E.courseid)," \
            "(select D.departmentname from department D where D.departmentid=E.departmentid),(select S.subjectname from subject S where S.subjectid=E.subjectid),(select S.icon from subject S where S.subjectid=E.subjectid) from enrollteacher E where E.teacherid".format(teacherid)
        cmd.execute(q)
        row=cmd.fetchone()
        cmd.execute(p)
        prow=cmd.fetchall()
        r="select * from news"
        cmd.execute(r)
        nrow=cmd.fetchall()
        if(row and prow):
            return render(request,"TeacherView.html",{'row':row,'prow':prow,'nrow':nrow})
        else:
            return render(request,"Login.html",{'msg':"Please Input Valid Id/Password..."})
    except Exception as e:
        print('error:',e)
        return render(request,"Login.html",{'msg':"Server Error..."})


def TeacherView(request):
    return render(request,"TeacherView.html")

def TeacherCourse(request):
   try:
    db,cmd=pool.ConnectionPooling()
    subid=request.GET['subid']
    tid=request.GET['tid']
    q="select * from subject where subjectid={}".format(subid)
    p="select * from teacher where teacherid={}".format(tid)
    r="select * from enrollstudent where teacherid={} and subjectid={}".format(tid,subid)
    cmd.execute(q)
    srow=cmd.fetchone()
    cmd.execute(p)
    trow=cmd.fetchone()
    cmd.execute(r)
    rrow=len(cmd.fetchall())
    db.close()
    return render(request,"TeacherCourse.html",{'srow':srow,'trow':trow,'rrow':rrow})
   except Exception as e:
       print('error:',e)
       return render(request, "TeacherCourse.html", {'srow': [], 'trow': [],'rrow':0})



def EnrollStudent2(request):
    return render(request,"EnrollStudent2.html")
def Marks(request):
    return render(request,"Marks.html")
def TeacherCourseMaterial(request):
    return render(request,"TeacherCourseMaterial.html")
