from collective.grok import gs
from reddplusid.missionreport import MessageFactory as _

@gs.importstep(
    name=u'reddplusid.missionreport', 
    title=_('reddplusid.missionreport import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('reddplusid.missionreport.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
