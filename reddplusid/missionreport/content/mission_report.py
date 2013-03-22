from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from reddplusid.missionreport import MessageFactory as _


# Interface class; used to define content-type schema.

class IMissionReport(form.Schema, IImageScaleTraversable):
    """
    REDD+ Indonesia Mission Report
    """

    mission_achievements = RichText(
            title=_(u'Summary of Main Achievements'),
            description=_(u'Please fill this section in short telex '
            'style.'),
            )

    mission_findings = RichText(
            title=_(u'Mission Findings'),
            description=_(u'Please keep to approx. 500 words.  '
            'Other relevant documents can be attached below.'),
            )

    mission_followup = RichText(
        title = _(u'Follow-up actions/next steps'),
        description = _(u'In point form, include who should be doing '
        'what.')
    )
    #FIXME distribution list

