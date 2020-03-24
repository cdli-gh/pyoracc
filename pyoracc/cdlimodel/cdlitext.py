from mako.template import Template
import os
import pkg_resources

resource_package = __name__  # Could be any module/package name


class CDLIText(object):
    template = Template("""&${code} = ${description}
#project: ${project}
#atf: lang ${language}
% for child in children:
${child.serialize()}
% endfor""")

    def __init__(self):
        # CDLI Parameters
        self.ValidPnumbersfilepath = pkg_resources.resource_filename(
            __name__, 'support_files/ValidPnumbers.txt')
        self.PnumberMapfilepath = pkg_resources.resource_filename(
            __name__, 'support_files/PnumberMap.txt')
        self.pList = None
        self.oldPlist = None
        self.newPlist = None
        self.newtext_status = True

    def __str__(self):
        return CDLIText.template.render_unicode(**vars(self))

    def serialize(self):
        return CDLIText.template.render_unicode(**vars(self))

    # CDLI Methods
    def ReadPnumbers(self):
        pfile = open(self.ValidPnumbersfilepath, 'r')
        plist = pfile.readlines()
        pfile.close()
        content = [x.strip() for x in plist]
        formatContent = self.FormatPnumber(content)
        return formatContent

    def FormatPnumber(self, plist):
        formatPlist = []
        for pnumber in plist:
            stringBuilder = "P"
            length = len(pnumber)
            for i in range(1, 7 - length):
                stringBuilder = stringBuilder + "0"

            stringBuilder = stringBuilder + pnumber
            formatPlist.append(stringBuilder)

        return formatPlist

    def CheckPnumber(self, pnumber):
        self.pList = self.ReadPnumbers()
        if pnumber in self.pList:
            return True
        else:
            return False

    def ReadPMap(self):
        temp = []
        oldPlist = []
        newPlist = []

        with open(self.PnumberMapfilepath) as file:
            for line in file:
                temp = line.split()
                oldPlist.append(temp[0].strip())
                newPlist.append(temp[1].strip())
        file.close()

        return oldPlist, newPlist

    def CheckPMap(self, pnumber):
        self.oldPlist, self.newPlist = self.ReadPMap()

        foundMap = False

        if pnumber in self.oldPlist:
            foundMap = True

        if foundMap:
            index = self.oldPlist.index(pnumber)
            temp = "Replace Old Pnumber : " + pnumber + \
                " with New Pnumber : " + self.newPlist[index]
            return self.newPlist[index], True, temp
        else:
            if self.CheckPnumber(pnumber):
                return pnumber, True, None
            else:
                return pnumber, False, None
