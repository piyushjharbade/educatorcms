from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from . import pool
@xframe_options_exempt
def AdminLogin(request):
    try:
        row=request.session['ADMIN']
        return render(request, "Dashboard.html", {'row': row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})
@xframe_options_exempt
def AdminLogout(request):
    del request.session['ADMIN']
    return render(request, "AdminLogin.html", {'msg': ""})

@xframe_options_exempt
def CheckLogin(request):
    try:
        db,cmd=pool.ConnectionPooling()
        emailid=request.POST['emailid']
        password=request.POST['password']
        q="select * from cmsadmin where emailid='{}' and password='{}'".format(emailid,password)
        cmd.execute(q)
        row=cmd.fetchone()
        c="select * from course"
        cmd.execute(c)
        crow=cmd.fetchall()
        d="select * from department"
        cmd.execute(d)
        drow=cmd.fetchall()
        s="select * from teacher"
        cmd.execute(s)
        srow=cmd.fetchall()
        st="select * from student"
        cmd.execute(st)
        strow=cmd.fetchall()
        if(row):
            request.session['ADMIN']=row
            return render(request, "Dashboard.html", {'row':row, 'crow':len(crow), 'drow':len(drow), 'srow':len(srow), 'strow':len(strow)})
        else:
            return render(request,"AdminLogin.html",{'msg':'Please Input Valid Emailid/Password'})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':'Server error.....'})

@xframe_options_exempt
def News(request):
    try:
        row=request.session['ADMIN']
        return render(request,"news.html",{'row':row})
    except Exception as e:
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def SubmitNews(request):
    try:
        db,cmd=pool.ConnectionPooling()
        teachername=(request.POST['teachername'])
        t=request.POST['time']
        day=request.POST['day']
        date=request.POST['date']
        news=request.POST['news']
        q="insert into news (teachername, time, day, date, news) values('{0}','{1}','{2}','{3}','{4}')".format(teachername, t, day, date, news)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"news.html",{'status':True})
    except Exception as e:
        print('error',e)
        return render(request,"news.html",{'status':False})


@xframe_options_exempt
def DisplayAllNews(request):
    try:
        db,cmd=pool.ConnectionPooling()
        q="select * from news"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        row=request.session['ADMIN']
        return render(request,"DisplayAllNews.html",{'rows':rows})
    except Exception as e:
        print('errrr:',e)
        return render(request,"AdminLogin.html",{'msg':""})

@xframe_options_exempt
def NewsById(request):
    try:
        db,cmd=pool.ConnectionPooling()
        nid=request.GET['nid']
        q="select * from news where newsno={}".format(nid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        srow=request.session['ADMIN']
        return render(request,"NewsById.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"AdminLogin.html",{'msg':""})


@xframe_options_exempt
def EditDeleteNews(request):
    try:
        btn=request.POST['btn']
        nid=request.POST['nid']
        db,cmd=pool.ConnectionPooling()
        if(btn=="Edit"):
            teachername = request.POST['teachername']
            t = request.POST['time']
            day = request.POST['day']
            date = request.POST['date']
            news = request.POST['news']
            q="update news set teachername='{}',time='{}',day='{}',date='{}',news='{}' where newsno={}".format(teachername,t,day,date,news,nid)
            cmd.execute(q)
            db.commit()
            db.close()
        elif(btn=="Delete"):
            q="delete from news where newsno={}".format(nid)
            cmd.execute(q)
            db.commit()
            db.close()
        return render(request, "NewsById.html", {'status': True})
    except Exception as e:
        print('errror:',e)
        return render(request, "NewsById.html", {'status': False})