from django.urls import path
from . import views

app_name = 'TestScripts'

urlpatterns = [
    path('ScriptList/', views.scriptList.as_view(), name='ScriptList'),
    path('ScriptUpload/', views.scriptUpload.as_view(), name='ScriptUpload'),
    path('ScriptUpload/Done/', views.scriptUploadDone.as_view(), name='ScriptUploadDone'),
    path('ScriptRun/', views.scriptRun.as_view(), name='ScriptRun'),
    path('ReportList/<int:scriptId>/', views.reportList.as_view(), name='ReportList'),
    path('ReportDownload/', views.reportDownload.as_view(), name='ReportDownload'),
    path('ScriptDelete/', views.scriptDelete.as_view(), name='ScriptDelete'),
    path('ReportDelete/', views.reportDelete.as_view(), name='ReportDelete'),

]
