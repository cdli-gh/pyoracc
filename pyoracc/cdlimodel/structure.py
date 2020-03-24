from mako.template import Template
import re


class Structure(object):
    template = Template("""&${code} = ${description}
#project: ${project}
#atf: lang ${language}
% for child in children:
${child.serialize()}
% endfor""")

    def __init__(self):
        self.newtext_status = True
        self.surfaceList = list()
        self.objectType = ""
        self.errorText = ""
        self.columnCounter = 0
        self.pnumber = ""

    def __str__(self):
        return Structure.template.render_unicode(**vars(self))

    def serialize(self):
        return Structure.template.render_unicode(**vars(self))

    def IncrementColumnCounter(self):
        self.columnCounter = self.columnCounter + 1

    def ResetColumnCounter(self):
        self.columnCounter = 0

    def UpdatePnumber(self, pnumber):
        self.pnumber = pnumber

    def SetObjectType(self, roughType):
        if "@tablet" in roughType:
            self.objectType = "TABLET"
        elif "bulla" in roughType:
            self.objectType = "BULLA"
        elif "prism" in roughType:
            self.objectType = "PRISM"
        elif "barrel" in roughType:
            self.objectType = "BARREL"
        elif "cylinder" in roughType:
            self.objectType = "CYLINDER"
        elif "brick" in roughType:
            self.objectType = "BRICK"
        elif "cone" in roughType:
            self.objectType = "CONE"
        elif "sealing" in roughType:
            self.objectType = "SEALING"
        elif "seal" in roughType:
            self.objectType = "SEAL"
        elif "composite" in roughType:
            self.objectType = "COMPOSITE"

    def SetSurface(self, surfaceType):
        self.surfaceList.append(surfaceType.rstrip())

    def ClearData(self):
        self.surfaceList = list()
        self.errorText = ""
        self.objectType = ""
        self.pnumber = ""

    def CheckSurfaceRules(self):
        surfaceRegex = re.compile("@surface")
        specificSurfaceRegex = re.compile(
            "@(obverse|reverse|top|bottom|left|right)")
        faceSurfaceRegex = re.compile("@face")
        sealRegex = re.compile("@seal")

        surfaceList = filter(surfaceRegex.match, self.surfaceList)
        specificSurfaceList = filter(
            specificSurfaceRegex.match, self.surfaceList)
        faceSurfaceList = filter(faceSurfaceRegex.match, self.surfaceList)
        sealList = filter(sealRegex.match, self.surfaceList)

        print(self.objectType)

        if len(faceSurfaceList) > 0:
            self.errorText += "%s: General Warning:\
                 Surface Type: face is not supported anymore.\n" % self.pnumber

        if self.objectType == "BULLA":
            if len(surfaceList) > 0 and len(specificSurfaceList) > 0:
                self.errorText += "%s: Bulla Warning: \
                Both Generic Surface type (ex. @surface) and \
                Specific Surface type (ex. @obverse), cannot \
                be used together.\n" % self.pnumber
        elif self.objectType == "PRISM":
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Prism Warning: Specific Surface type \
                (ex. @obverse) are not allowed.\n" % self.pnumber
        elif self.objectType == "BARREL":
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Barrel Warning:\
                Specific Surface type (ex. @obverse) are not allowed.\n"\
                % self.pnumber
        elif self.objectType == "CYLINDER":
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Cylinder Warning: Specific Surface type\
                (ex. @obverse) are not allowed.\n" % self.pnumber
        elif self.objectType == "BRICK":
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Brick Warning: Specific Surface type\
                (ex. @obverse) are not allowed.\n" % self.pnumber
        elif self.objectType == "CONE":
            if len(surfaceList) > 2:
                self.errorText += "%s: Cone Warning: More than 2 Generic \
                Surfaces are not allowed.\n" % self.pnumber
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Cone Warning: Specific Surface type \
                (ex. @obverse) are not allowed.\n" % self.pnumber
        elif self.objectType == "SEALING":
            if len(surfaceList) > 1:
                self.errorText += "%s: Sealing Warning: More than 1 Generic \
                Surfaces are not allowed.\n" % self.pnumber
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Sealing Warning: Specific Surface \
                type (ex. @obverse) are not allowed.\n" % self.pnumber
            if len(sealList) < 1:
                self.errorText += "%s: Sealing Warning: There should atleast \
                be one Seal impression.\n" % self.pnumber
        elif self.objectType == "SEAL":
            if len(surfaceList) > 1:
                self.errorText += "%s: Seal Warning: More than 1 Generic \
                Surfaces are not allowed.\n" % self.pnumber
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Seal Warning: Specific Surface type \
                (ex. @obverse) are not allowed.\n" % self.pnumber
            if len(sealList) > 0:
                self.errorText += "%s: Seal Warning: \
                There shouldn't be any Seal.\n" % self.pnumber
        elif self.objectType == "COMPOSITE":
            if len(surfaceList) > 1:
                self.errorText += "%s: Composite Warning: More than 1 Generic \
                Surfaces are not allowed.\n" % self.pnumber
            if len(specificSurfaceList) > 0:
                self.errorText += "%s: Composite Warning: Specific Surface \
                type (ex. @obverse) are not allowed.\n" % self.pnumber
            if len(sealList) > 0:
                self.errorText += "%s: Composite Warning: \
                    There shouldn't be any Seal.\n" % self.pnumber
            if self.columnCounter > 0:
                self.errorText += "%s: Composite Warning: \
                Columns are not allowed.\n" % self.pnumber

    def PrintResults(self):
        if not self.errorText == "":
            print(self.errorText)
