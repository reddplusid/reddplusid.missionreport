from five import grok
from plone.app.content.interfaces import INameFromTitle
from reddplusid.missionreport.content.mission_report import IMissionReport


class MissionReportTitle(grok.Adapter):

    grok.implements(INameFromTitle)
    grok.context(IMissionReport)

    def __new__(cls, context):
        '''
        This sets the title for naming purposes, but Mission Reports
        title are indexed as the same value as the parent mission.
        missionreport.title is never displayed in template or indexed.
        '''
        
        instance = super(MissionReportTitle, cls).__new__(cls)
        instance.title = u'Mission Report'
        return instance
