#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Matt Makai <matthew.makai@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
version_added: "2.0"
module: sendgrid
short_description: Sends an email with the SendGrid API
description:
   - "Sends an email with a SendGrid account through their API, not through
     the SMTP service."
notes:
   - "This module is non-idempotent because it sends an email through the
     external API. It is idempotent only in the case that the module fails."
   - "Like the other notification modules, this one requires an external
     dependency to work. In this case, you'll need an active SendGrid
     account."
   - "In order to use api_key, cc, bcc, attachments, from_name, html_body, headers
     you must pip install sendgrid"
   - "since 2.2 username and password are not required if you supply an api_key"
requirements:
  - sendgrid python library
options:
  username:
    description:
      - username for logging into the SendGrid account.
      - Since 2.2 it is only required if api_key is not supplied.
  password:
    description:
      - password that corresponds to the username
      - Since 2.2 it is only required if api_key is not supplied.
  from_address:
    description:
      - the address in the "from" field for the email
    required: true
  to_addresses:
    description:
      - a list with one or more recipient email addresses
    required: true
  subject:
    description:
      - the desired subject for the email
    required: true
  api_key:
    description:
      - sendgrid API key to use instead of username/password
    version_added: 2.2
  cc:
    description:
      - a list of email addresses to cc
    version_added: 2.2
  bcc:
    description:
      - a list of email addresses to bcc
    version_added: 2.2
  attachments:
    description:
      - a list of relative or explicit paths of files you want to attach (7MB limit as per SendGrid docs)
    version_added: 2.2
  from_name:
    description:
      - the name you want to appear in the from field, i.e 'John Doe'
    version_added: 2.2
  html_body:
    description:
      - whether the body is html content that should be rendered
    version_added: 2.2
    type: bool
    default: 'no'
  headers:
    description:
      - a dict to pass on as headers
    version_added: 2.2
author: "Matt Makai (@makaimc)"
'''

EXAMPLES = '''
# send an email to a single recipient that the deployment was successful
- sendgrid:
    username: "{{ sendgrid_username }}"
    password: "{{ sendgrid_password }}"
    from_address: "quantum@mycompany.com"
    to_addresses:
      - "ops@mycompany.com"
    subject: "Deployment success."
    body: "The most recent Quantum deployment was successful."
  delegate_to: localhost

# send an email to more than one recipient that the build failed
- sendgrid:
      username: "{{ sendgrid_username }}"
      password: "{{ sendgrid_password }}"
      from_address: "build@mycompany.com"
      to_addresses:
        - "ops@mycompany.com"
        - "devteam@mycompany.com"
      subject: "Build failure!."
      body: "Unable to pull source repository from Git server."
  delegate_to: localhost
'''

# =======================================
# sendgrid module support methods
#
import os
import traceback

SENDGRID_IMP_ERR = None
try:
    import sendgrid
    HAS_SENDGRID = True
except ImportError:
    SENDGRID_IMP_ERR = traceback.format_exc()
    HAS_SENDGRID = False

from quantum.module_utils.basic import QuantumModule, missing_required_lib
from quantum.module_utils.six.moves.urllib.parse import urlencode
from quantum.module_utils._text import to_bytes
from quantum.module_utils.urls import fetch_url


def post_sendgrid_api(module, username, password, from_address, to_addresses,
                      subject, body, api_key=None, cc=None, bcc=None, attachments=None,
                      html_body=False, from_name=None, headers=None):

    if not HAS_SENDGRID:
        SENDGRID_URI = "https://api.sendgrid.com/api/mail.send.json"
        AGENT = "Quantum"
        data = {'api_user': username, 'api_key': password,
                'from': from_address, 'subject': subject, 'text': body}
        encoded_data = urlencode(data)
        to_addresses_api = ''
        for recipient in to_addresses:
            recipient = to_bytes(recipient, errors='surrogate_or_strict')
            to_addresses_api += '&to[]=%s' % recipient
        encoded_data += to_addresses_api

        headers = {'User-Agent': AGENT,
                   'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json'}
        return fetch_url(module, SENDGRID_URI, data=encoded_data, headers=headers, method='POST')
    else:

        if api_key:
            sg = sendgrid.SendGridClient(api_key)
        else:
            sg = sendgrid.SendGridClient(username, password)

        message = sendgrid.Mail()
        message.set_subject(subject)

        for recip in to_addresses:
            message.add_to(recip)

        if cc:
            for recip in cc:
                message.add_cc(recip)
        if bcc:
            for recip in bcc:
                message.add_bcc(recip)

        if headers:
            message.set_headers(headers)

        if attachments:
            for f in attachments:
                name = os.path.basename(f)
                message.add_attachment(name, f)

        if from_name:
            message.set_from('%s <%s.' % (from_name, from_address))
        else:
            message.set_from(from_address)

        if html_body:
            message.set_html(body)
        else:
            message.set_text(body)

        return sg.send(message)
# =======================================
# Main
#


def main():
    module = QuantumModule(
        argument_spec=dict(
            username=dict(required=False),
            password=dict(required=False, no_log=True),
            api_key=dict(required=False, no_log=True),
            bcc=dict(required=False, type='list'),
            cc=dict(required=False, type='list'),
            headers=dict(required=False, type='dict'),
            from_address=dict(required=True),
            from_name=dict(required=False),
            to_addresses=dict(required=True, type='list'),
            subject=dict(required=True),
            body=dict(required=True),
            html_body=dict(required=False, default=False, type='bool'),
            attachments=dict(required=False, type='list')
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ['api_key', 'password'],
            ['api_key', 'username']
        ],
        required_together=[['username', 'password']],
    )

    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    bcc = module.params['bcc']
    cc = module.params['cc']
    headers = module.params['headers']
    from_name = module.params['from_name']
    from_address = module.params['from_address']
    to_addresses = module.params['to_addresses']
    subject = module.params['subject']
    body = module.params['body']
    html_body = module.params['html_body']
    attachments = module.params['attachments']

    sendgrid_lib_args = [api_key, bcc, cc, headers, from_name, html_body, attachments]

    if any(lib_arg is not None for lib_arg in sendgrid_lib_args) and not HAS_SENDGRID:
        reason = 'when using any of the following arguments: ' \
                 'api_key, bcc, cc, headers, from_name, html_body, attachments'
        module.fail_json(msg=missing_required_lib('sendgrid', reason=reason),
                         exception=SENDGRID_IMP_ERR)

    response, info = post_sendgrid_api(module, username, password,
                                       from_address, to_addresses, subject, body, attachments=attachments,
                                       bcc=bcc, cc=cc, headers=headers, html_body=html_body, api_key=api_key)

    if not HAS_SENDGRID:
        if info['status'] != 200:
            module.fail_json(msg="unable to send email through SendGrid API: %s" % info['msg'])
    else:
        if response != 200:
            module.fail_json(msg="unable to send email through SendGrid API: %s" % info['message'])

    module.exit_json(msg=subject, changed=False)


if __name__ == '__main__':
    main()
