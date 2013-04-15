from Acquisition import aq_inner, aq_parent
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema

import string
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import safe_unicode


class IMailAction(Interface):
    """Definition of the configuration available for a mail action
    """
    source = schema.TextLine(title=_(u"Email source"),
                             description=_("The email address that sends the \
email. If no email is provided here, it will use the address of the \
report owner."),
                             required=False)
    recipients = schema.TextLine(title=_(u"Email recipients"),
                                description=_("The email where you want to \
send this message. To send it to different email addresses, just separate them\
 with , By default email will be sent to addresses in the distribution\
 list of the mission report"),
                                required=False)

class MailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IMailAction, IRuleElementData)

    subject = u''
    source = u''
    recipients = u''
    message = u''

    element = 'plone.actions.Mail'

    @property
    def summary(self):
        return _(u"Email report to ${recipients}",
                 mapping=dict(recipients=self.recipients))


class MailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        recipients = [str(mail.strip()) for mail in \
                      self.element.recipients.split(',')]
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to \
execute this action'

        source = self.element.source
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        membertool = getToolByName(aq_inner(self.context),"portal_membership")
        #authortool = getToolByName(aq_inner(self.context),"getMemberInfo")
        portal = urltool.getPortalObject()
        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError, 'You must provide a source address for this \
action or enter an email in the portal properties'
            from_name = portal.getProperty('email_from_name')
            source = "%s <%s>" % (from_name, from_address)

        obj = self.event.object
        parent = aq_parent(self.event.object)

        event_title = safe_unicode(safe_unicode(obj.Title()))
        event_url = safe_unicode(obj.absolute_url())
        subject = event_title

        #Get email address of author

        creator = obj.Creator()
        member = membertool.getMemberById(creator)
        author = member.getProperty('email')
        authorinfo = membertool.getMemberInfo(creator)
        fullname = authorinfo['fullname']

        msg  = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = author

        #Variables for mission report

        #FIXME these loops can re refactored as single function

        mission_authors = []
        for author_id in obj.mission_author:
            mission_author = membertool.getMemberInfo(author_id)
            mission_authors.append(safe_unicode(mission_author['fullname']))

        mission_members = []
        for member_id in parent.mission_members:
            member = membertool.getMemberInfo(member_id)
            mission_members.append(safe_unicode(member['fullname']))

        mission_support_staff = []
        for staff_id in parent.mission_support_staff:
            staff = membertool.getMemberInfo(staff_id)
            mission_support_staff.append(safe_unicode(staff['fullname']))

        objective   = safe_unicode(parent.Description())

        output_stream = safe_unicode(parent.output_stream)
        output_contribution = safe_unicode(parent.output_contribution)

        funding_source = safe_unicode(parent.mission_funding_source)
        
        mission_achievements = safe_unicode(obj.mission_achievements)

        mission_findings = safe_unicode(obj.mission_findings)

        followup = safe_unicode(obj.mission_followup)

        period_start = safe_unicode(parent.start)
        period_end   = safe_unicode(parent.end)

        scope = safe_unicode(parent.mission_scope)

        mission_location = safe_unicode(parent.mission_location)

        distribution = safe_unicode(obj.mission_distribution)

        delimiter = u','.encode('utf-8')
        br = u'<br />'.encode('utf-8')


        #make values in tuples as unicode and utf-8 safe lists
        
        email_form = u'''
        <h3>Author(s)</h3>
        $authors

        <h3>Member(s)</h3>
        $mission_members

        <h3>Supporting Staff</h3>
        $mission_support_staff

        <h3>Mission Details</h3>
        <ul>
            <li>When: $period_start to $period_end </li>
            <li>Scope: </li>
            <li>Country: </li>
            <li>Province: </li>
            <li>City: </li>
            <li>Fundint source: </li>
        </ul>

        <h3>Output Stream</h3>
        $output_stream

        <h3>Contribution to Output</h3>
        $contribution

        <h3>Summary of Main Achievements</h3>
        $mission_achievements

        <h3>Findings</h3>
        $mission_findings

        <h3>Follow-up actions/next steps</h3>
        $mission_followup

        <h3>Distribution List</h3>
        $distribution
        <p>
        -- <br />
        This report is available online at: <br />
        <a href="$event_url">$event_url</a>
        '''

        email_template = string.Template(email_form)

        body = email_template.substitute({
            'authors' : br.join(mission_authors),
            'objective'     : parent.description, 
            'members'       : br.join(mission_members),
            'period_start'  : safe_unicode(period_start),
            'period_end'     : safe_unicode(period_end),
            'mission_location' :
            safe_unicode(delimiter.join(mission_location)),
            'distribution' : safe_unicode(delimiter.join(obj.mission_distribution)),
            'event_url' : event_url,
             })

        body_safe = body.encode('utf-8')
        htmlPart = MIMEText(body_safe, 'html', 'utf-8')
        msg.attach(htmlPart)

        #File attachments here should be rewritten into function

#        if str(obj.getAttachment1()):
#
#            file = str(obj.getAttachment1())
#            ctype = obj.attachment1.getContentType()
#            filename = obj.attachment1.filename
#
#            maintype, subtype = ctype.split(('/'), 1)
#
#            attachment = MIMEBase(maintype, subtype)
#            attachment.set_payload(file)
#            Encoders.encode_base64(attachment)
#
#            attachment.add_header('Content-Disposition', 'attachment',
#                    filename = filename)
#
#            msg.attach(attachment)

        #FIXME distribution needs error checking

        for recipient in distribution:
            #Delete previous To headers in loop as default behaviour is
            #append

            del msg['To']
            msg['To'] = recipient

            mailhost.send(msg.as_string())

        return True



class MailAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Add Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = MailAction()
        form.applyChanges(a, self.form_fields, data)
        return a

class MailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailAction)
    label = _(u"Edit Mail Action")
    description = _(u"A mail action can mail different recipient.")
    form_name = _(u"Configure element")
