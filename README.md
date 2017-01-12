# IMAP
test IMAP"
!!! Uncomment method call from "if __name__ == '__main__':" IMAP/imap_response.py

$ cd IMAP/
$ python imap_response.py

Mailbox Status
==============

MESSAGES :The number of messages in the mailbox.
RECENT :The number of messages with the Recent flag set.
UIDNEXT :The next unique identifier value of the mailbox.
UIDVALIDITY :The unique identifier validity value of the mailbox.
UNSEEN :The number of messages which do not have the Seen flag set.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Connect to the server
=====================

connection = imaplib.IMAP4_SSL('server name')

Login to our account
====================

connection.login('username', 'password')


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ERRORS
======

Traceback (most recent call last):
  File "imap_response.py", line 167, in <module>
    moving_and_copying_messages()
  File "imap_response.py", line 146, in moving_and_copying_messages
    c.copy(msg_ids, 'Archive.Today')
  File "/usr/lib/python2.7/imaplib.py", line 405, in copy
    return self._simple_command('COPY', message_set, new_mailbox)
  File "/usr/lib/python2.7/imaplib.py", line 1087, in _simple_command
    return self._command_complete(name, self._command(name, *args))
  File "/usr/lib/python2.7/imaplib.py", line 917, in _command_complete
    raise self.error('%s command error: %s %s' % (name, typ, data))
imaplib.error: COPY command error: BAD ['parse error: zero-length content']

if you get this type of error please choose any of the one line
===============================================================
def moving_and_copying_messages():

	typ, [response] = c.search(None, 'UNSEEN')

	OR

	typ, [response] = c.search(None, 'SEEN')