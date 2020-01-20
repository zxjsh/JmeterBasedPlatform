from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.http import FileResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
from .forms import uploadFileForms, runScriptForms, downloadReportForms, deleteReportForms, deleteScriptForms
from .models import testScript, testFile, testReport
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, View
from .myfunction import zipManage, jmxManage
import time
import os


# Create your views here.

class scriptList(ListView):
    template_name = 'TestScripts/ScriptList.html'
    context_object_name = 'testScriptList'
    paginate_by = 10

    def get_queryset(self):
        return testScript.objects.filter(testFile__uploader=self.request.user, isDelete=0).order_by('-createTime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scriptRunForm'] = runScriptForms()
        context['scriptDeleteForm'] = deleteScriptForms()
        return context


class scriptUpload(CreateView):
    template_name = 'TestScripts/Upload.html'
    form_class = uploadFileForms

    def form_valid(self, form):
        zm = zipManage()
        jm = jmxManage()

        newFile = form.save(commit=False)
        newFile.uploader = self.request.user
        newFile.fileName = form.cleaned_data['zipFile'].name
        unzipFilePath = os.path.join(settings.MEDIA_ROOT, "unzipfiles", time.strftime('%Y'), time.strftime('%m'),
                                     time.strftime('%d'))
        newFile.unzipFile = zm.getUnzipFile(newFile.zipFile, newFile.fileName, unzipFilePath)
        newFile.save()

        globList = jm.getJmxList(newFile.unzipFile)
        for jmxFile in globList:
            jmxName = os.path.splitext(os.path.split(jmxFile)[-1])[0]
            testScript.objects.create(testFile=newFile, scriptName=jmxName, scriptFile=jmxFile)

        # return super().form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('TestScripts:ScriptUploadDone')


class scriptUploadDone(View):
    def get(self, request):
        return render(request, 'TestScripts/UploadDone.html', None)


class scriptRun(FormView):
    # template_name = 'TestScripts/ScriptList.html'
    form_class = runScriptForms

    def form_valid(self, form):
        zm = zipManage()
        jm = jmxManage()

        scriptId = form.cleaned_data['scriptId']
        suffix = time.strftime('%Y%m%d%H%M%S')
        script = get_object_or_404(testScript, testFile__uploader=self.request.user, id=scriptId, isDelete=0)
        reportFilePath = os.path.join(settings.MEDIA_ROOT, "reportfiles", time.strftime('%Y'), time.strftime('%m'),
                                      time.strftime('%d'))

        reportDir = jm.runJmx(script.scriptName, script.scriptFile, reportFilePath, suffix)
        reportName = '%s_%s' % (script.scriptName, suffix)

        reportZip = reportName + '.zip'
        reportZipPath = os.path.join(settings.MEDIA_ROOT, "reportzipfiles", reportZip)

        zm.getZipFile(reportDir, reportZipPath)
        reportFile = os.path.join(reportDir, 'index.html')

        testReport.objects.create(testScript=script, reportName=reportName, reportFile=reportFile,
                                  reportZip=reportZipPath)

        script.runTimes = script.runTimes + 1
        script.save()

        # return super().form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('TestScripts:ScriptList')


class reportList(ListView):
    template_name = 'TestScripts/ReportList.html'
    context_object_name = 'reportList'
    paginate_by = 10

    def get_queryset(self):
        return testReport.objects.filter(testScript__testFile__uploader=self.request.user, isDelete=0,
                                         testScript=self.kwargs.get('scriptId')).order_by('-createTime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportDownloadForm'] = downloadReportForms()
        context['reportDeleteForm'] = deleteReportForms()
        return context


class reportDownload(View):
    def post(self, request):
        reportId = request.POST.get('reportId')
        report = get_object_or_404(testReport, testScript__testFile__uploader=self.request.user, id=reportId,
                                   isDelete=0)
        with open(report.reportZip, 'rb') as file:
            wrapper = FileWrapper(file)
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(report.reportZip)
            return response


class scriptDelete(FormView):
    template_name = 'TestScripts/ScriptList.html'
    form_class = deleteScriptForms

    def form_valid(self, form):
        scriptId = form.cleaned_data['scriptId']
        testScript.objects.filter(id=scriptId).update(isDelete=1)
        # return super().form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('TestScripts:ScriptList')


class reportDelete(FormView):
    template_name = 'TestScripts/ReportList.html'
    form_class = deleteReportForms

    def form_valid(self, form):
        reportId = form.cleaned_data['reportId']
        testReport.objects.filter(id=reportId).update(isDelete=1)
        # return super().form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('TestScripts:ScriptList')
        # return reverse_lazy('TestScripts:ReportDelete')
