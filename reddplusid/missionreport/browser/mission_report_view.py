from five import grok
from plone.directives import dexterity, form
from reddplusid.missionreport.content.mission_report import IMissionReport

from Acquisition import aq_parent

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionReport)
    grok.require('zope2.View')
    grok.template('mission_report_view')
    grok.name('view')

    def mission(self):
        return aq_parent(self.context)
