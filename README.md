# IMAP
test IMAP"
!!! Uncomment function call from "if __name__ == '__main__':" IMAP/imap_response.py

$ cd IMAP/
$ python imap_response.py

Mailbox Status
++++++++++++++

MESSAGES :The number of messages in the mailbox.
RECENT :The number of messages with the Recent flag set.
UIDNEXT :The next unique identifier value of the mailbox.
UIDVALIDITY :The unique identifier validity value of the mailbox.
UNSEEN :The number of messages which do not have the Seen flag set.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Connect to the server
+++++++++++++++++++++

connection = imaplib.IMAP4_SSL('server name')

Login to our account
++++++++++++++++++++

connection.login('username', 'password')