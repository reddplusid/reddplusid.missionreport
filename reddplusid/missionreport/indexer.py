from plone.indexer import indexer
from reddplusid.missionreport.content.mission_report import IMissionReport
from reddplusid.mission.content.mission import id_provinces
import p01.vocabulary.country 
from Acquisition import aq_parent

from five import grok

#searchable text index

@indexer(IMissionReport)
def title(obj):
    return aq_parent(obj).title

@indexer(IMissionReport)
def description(obj):
     return aq_parent(obj).description

@indexer(IMissionReport)
def index_searchable(obj):

    results = []

    results.append(obj.mission_achievements.output)
    results.append(obj.mission_achievements.output)
    results.append(obj.mission_followup.output)

    results.append(mission_searchabletext(aq_parent(obj)))
    

    return results

def mission_searchabletext(obj):

    results = []
    for attr in [
                 'mission_location',
                 ]:
        results.append(' '.join(getattr(obj, attr, []) or []))

    results.append(obj.mission_funding_source)
    results.append(getattr(obj, 'output_stream', ''))
    results.append(getattr(obj, 'obj.mission_scope', ''))
    results.append(getattr (obj, 'obj.mission_funding_source', ''))
    results.append(id_provinces.getTerm(obj.id_province).title)
    results.append(p01.vocabulary.country.ISO3166Alpha2CountryVocabulary(obj).getTerm(obj.country).title)
    results.append(obj.output_contribution.output)
    results.append(obj.title)
    results.append(obj.description)
      
    membership = obj.portal_membership
    for memberId in obj.mission_author:
        member = membership.getMemberById(memberId)
        results.append(member.getProperty('fullname'))

    for memberId in obj.mission_members:
        member = membership.getMemberById(memberId)
        results.append(member.getProperty('fullname'))

    for memberId in obj.mission_support_staff:
        member = membership.getMemberById(memberId)
        results.append(member.getProperty('fullname'))

    return " ".join(results)

grok.global_adapter(index_searchable, name='SearchableText')
grok.global_adapter(title, name='title')
grok.global_adapter(description, name='description')
