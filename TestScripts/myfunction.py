import zipfile
import time
import glob
import os


class zipManage():
    def getZipFile(slef, dirpath, outFullName):
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            fpath = path.replace(dirpath, '')

            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()

    def getUnzipFile(slef, file, fileName, path):
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

        baseName = fileName.replace('.zip', '')
        unzipPath = os.path.join(path, baseName)

        isZipFile = zipfile.is_zipfile(file)
        if isZipFile:
            with zipfile.ZipFile(file) as zf:
                zf.extractall(unzipPath)
        else:
            print('This is not zip')

        return unzipPath


class jmxManage():
    def runJmx(slef, jmxName, jmxFile, path, suffix):
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

        reportPath = '%s\%s_%s' % (path, jmxName, suffix)
        os.system(r'jmeter -n -t %s -l %s\%s_%s_result.jtl -e -o %s' % (jmxFile, path, jmxName, suffix, reportPath))

        return reportPath

    def getJmxList(slef, path):
        globList = glob.glob(pathname=r'%s/*.jmx' % path)
        # jmxList = [os.path.splitext(os.path.split(jmx)[-1])[0] for jmx in globList]
        return globList
