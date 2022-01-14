"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import CourseView
from . import SubjectView
from . import DepartmentView
from . import TeacherView
from . import StudentView
from . import AdminView
from . import CollageView
urlpatterns = [
    path('admin/', admin.site.urls),

#Admin
    path('adminlogin/',AdminView.AdminLogin),
    path('adminlogout/',AdminView.AdminLogout),
    path('checklogin',AdminView.CheckLogin),
    path('news/', AdminView.News),
    path('submitnews',AdminView.SubmitNews),
    path('displayallnews/',AdminView.DisplayAllNews),
    path('newsbyid/',AdminView.NewsById),
    path('editdeletenews',AdminView.EditDeleteNews),

# Course
    path('course/',CourseView.CourseInterface),
    path('submitcourse/',CourseView.SubmitCourse),
    path('displayallcourse/',CourseView.DisplayAllCourse),
    path('coursebyid/',CourseView.CourseById),
    path('editdeletecourse/',CourseView.EditDeleteCourse),
    path('displayallcoursejson/',CourseView.DisplayAllCourseJSON),

#Subject
    path('subject/',SubjectView.SubjectInterface),
    path('submitsubject',SubjectView.SubmitSubject),
    path('displayallsubject/',SubjectView.DisplayAllSubject),
    path('subjectbyid/',SubjectView.SubjectById),
    path('editdeletesubject/',SubjectView.EditDeleteSubject),
    path('displayallsubjectjson/',SubjectView.DisplayAllSubjectJSON),
    path('editsubjecticon',SubjectView.EditIcon),

#Department
    path('department/',DepartmentView.DepartmentInterface),
    path('submitdepartment/',DepartmentView.SubmitDepartment),
    path('displayalldepartment/',DepartmentView.DisplayAllDepartment),
    path('departmentbyid/',DepartmentView.DepartmentById),
    path('editdeletedepartment/',DepartmentView.EditDeleteDepartment),
    path('displayalldepartmentjson/',DepartmentView.DisplayAllDepartmentJSON),

 #Teacher
    path('teacher/',TeacherView.TeacherInterface),
    path('submitteacher',TeacherView.SubmitTeacher),
    path('displayallteacher/',TeacherView.DisplayAllTeacher),
    path('teacherbyid/',TeacherView.TeacherById),
    path('editdeleteteacherdata/',TeacherView.EditDeleteTeacherData),
    path('editteacherpicture',TeacherView.EditPicture),
    path('editteachericon',TeacherView.EditIcon),
    path('enrollteacher/',TeacherView.EnrollTeacher),
    path('fetchallteacher/',TeacherView.FetchAllTeacher),
    path('sumbitteacherenroll/',TeacherView.SubmitTeacherEnroll),
    path('displayteacherenrollment/', TeacherView.DisplayTeacherEnrollment),
    path('updateteacherenrollment/',TeacherView.UpadateTeacherEnrollment),
    path('editdeleteteacherenrollment/',TeacherView.EditDeleteTeacherEnrollment),
    path('enrollstudent/',TeacherView.EnrollStudent),
    path('fetchallstudent/',TeacherView.FetchAllStudent),
    path('fetchallsubject/',TeacherView.FetchAllSubject),
    path('enrollstudentjson/',TeacherView.DisplayAllSubjectJSON),
    path('submitstudentenroll/',TeacherView.SubmitEnrollStudent),
    path('subjectteacherdata/',TeacherView.SubjectTeacherData),
    path('updatestudentenrollment/',TeacherView.UpdateStudentEnrollment),
    path('editdeletestudentenroll/',TeacherView.EditDeleteStudentEnroll),
    path('submitmarks/',TeacherView.SubmitMarks),
    path('subjectteacherdata2/', TeacherView.SubjectTeacherData2),
    path('teacherlogin/',TeacherView.TeacherLogin),
    path('checkteacher',TeacherView.CheckTeacher),
    path('teacherview/',TeacherView.TeacherView),
    path('teachercourse/',TeacherView.TeacherCourse),
    path('enrollstudent2/',TeacherView.EnrollStudent2),
    path('marks/',TeacherView.Marks),
    path('teachercoursematerial/',TeacherView.TeacherCourseMaterial),
    path('subjectteacherdata3/', TeacherView.SubjectTeacherData3),
    path('uploadcoursematerial',TeacherView.UplaodCourseMaterial),
    path('deletecoursematerial/',TeacherView.DeleteCourseMaterial),
    path('teacherprofile/',TeacherView.TeacherProfile),
    path('updateteacherprofile/',TeacherView.UpdateTeacherProfile),
    path('subjectteacherdata4/', TeacherView.SubjectTeacherData4),
    path('uploadlecture', TeacherView.UplaodLecture),
    path('deletelecture/', TeacherView.DeleteLecture),

    #Student
    path('student/',StudentView.StudentInterface),
    path('displayallbranchjson/',StudentView.DisplayAllBranchJSON),
    path('submitstudent',StudentView.SubmitStudent),
    path('displayallstudent/', StudentView.DisplayAllStudent),
    path('studentbyid',StudentView.StudentById),
    path('editdeletestudentdata/',StudentView.EditDeleteStudentData),
    path('editstudentpicture',StudentView.EditPicture),
    #Student Frontend
    path('studentview/',StudentView.StudentView),
    path('studentlogin/',StudentView.StudentLogin),
    path('checkstudent',StudentView.CheckStudent),
    path('studentcourse/',StudentView.StudentCourse),
    path('studentprofile/',StudentView.StudentProfile),
    path('studentcoursematerial/',StudentView.StudentCourseMaterail),
    path('studentlecture/', StudentView.StudentLecture),

    #Collage
    path('collageinterface/',CollageView.CollageInterface),
    path('about/',CollageView.About),
    path('blog/',CollageView.Blog),
    path('collagecourse/',CollageView.Course),
    path('contact/',CollageView.Contact),
    path('login/',CollageView.Login),
    path('slogin/',CollageView.SLogin),


]
