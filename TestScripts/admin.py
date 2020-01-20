from django.contrib import admin
from .models import testFile, testScript, testReport, testSuite


# Register your models here.
@admin.register(testFile)
class testFileAdmin(admin.ModelAdmin):
    list_display = ['uploader', 'fileName', 'zipFile', 'unzipFile', 'uploadTime', 'isDelete']


@admin.register(testScript)
class testScriptAdmin(admin.ModelAdmin):
    list_display = ['testFile', 'scriptName', 'scriptFile', 'runTimes', 'status',
                    'lastRunTime', 'isDelete', 'createTime']


@admin.register(testReport)
class testReportAdmin(admin.ModelAdmin):
    list_display = ['testScript', 'reportName', 'reportFile', 'reportZip', 'isDelete', 'createTime']


@admin.register(testSuite)
class testSuiteAdmin(admin.ModelAdmin):
    list_display = ['suiteName', 'runTimes', 'status', 'lastRunTime', 'isDelete', 'createTime']
