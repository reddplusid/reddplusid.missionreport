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
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
from collective.z3cform.widgets.enhancedtextlines import \
EnhancedTextLinesFieldWidget


from reddplusid.missionreport import MessageFactory as _


# Interface class; used to define content-type schema.

class IMissionReport(form.Schema, IImageScaleTraversable):
    """
    REDD+ Indonesia Mission Report
    """

    form.widget(mission_author=AutocompleteMultiFieldWidget)
    mission_author= schema.List(
            title=_(u'Author'),
            description=_(u'List of Authors. Enter '
                'name to search, select and press Enter to add. Repeat to '
                'to add additional members with principal author first.'),
            value_type=schema.Choice(vocabulary=u"plone.principalsource.Users"),
            default=[],
            missing_value=(),
            required=True,
            )

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

    form.widget(mission_distribution=EnhancedTextLinesFieldWidget)
    mission_distribution = schema.Tuple(
       title=_(u'Additional Email Distribution List'),
       description=_(u'Email addresses to which a copy of this '
           'report should be sent. One email per entry. Click Add  '
            'after each new entry. eg. '
           'username@unorcid.org. Authors, members and '
           'supporting staff are already included and need not '
           'be specified here.'),
       default=(),
       missing_value=(),
       value_type=schema.TextLine(
           ),
       required=False,
       )


