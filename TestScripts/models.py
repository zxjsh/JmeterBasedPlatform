from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.

class testFile(models.Model):
    delete_choices = ((0, 'undelete'), (1, 'delete'))

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploader')
    fileName = models.CharField(max_length=50)
    zipFile = models.FileField(upload_to='zipfiles/%Y/%m/%d')
    unzipFile = models.CharField(max_length=250, blank=True)
    uploadTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=0, choices=delete_choices)

    def __str__(self):
        return self.fileName


class testScript(models.Model):
    status_choices = ((0, 'wait'), (1, 'running'), (2, 'complete'))
    result_choices = ((0, 'pass'), (1, 'fail'))
    delete_choices = ((0, 'undelete'), (1, 'delete'))

    testFile = models.ForeignKey(testFile, on_delete=models.CASCADE, verbose_name='testFile')
    scriptName = models.CharField(max_length=50)
    scriptFile = models.CharField(max_length=250, blank=True)
    runTimes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='wait')
    lastRunTime = models.DateTimeField(auto_now=True)
    createTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=0, choices=delete_choices)

    def __str__(self):
        return self.scriptName


class testReport(models.Model):
    result_choices = ((0, 'pass'), (1, 'fail'))
    delete_choices = ((0, 'undelete'), (1, 'delete'))

    testScript = models.ForeignKey(testScript, on_delete=models.CASCADE, verbose_name='testScript')
    reportName = models.CharField(max_length=50, blank=True)
    reportFile = models.CharField(max_length=250, blank=True)
    reportZip = models.CharField(max_length=250, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=0, choices=delete_choices)
