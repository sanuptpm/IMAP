import imaplib
import re

from imap_conf import open_connection


list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

# print "list_response_pattern :", list_response_pattern


def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

# Listing mailboxes
def listing_mailboxes():
    resp, data = c.list()
    # IMAP instance
    print "\nIMAP4_SSL instance :", c
    # First parameter of the c.list()
    print '\nResponse code:', resp
    # Second parameter of the c.list()
    print "\nmailboxes available for an account :", data
    # Get the status
    for line in data:
        print '\nServer response:', line
        #  call for flags, delimiter, mailbox_name
        flags, delimiter, mailbox_name = parse_list_response(line)
        print 'Parsed response:', (flags, delimiter, mailbox_name)

# list status with mailboxname
def mailbox_status():
    resp, data = c.list()
    print "\n"
    for line in data:
        #  call for flags, delimiter, mailbox_name
        flags, delimiter, mailbox_name = parse_list_response(line)
        print c.status(mailbox_name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)')

# Selecting mailboxes
def selecting_mailbox():
    # Select Inbox 
    typ, data = c.select('INBOX')
    num_msgs = int(data[0])
    print 'There are %d messages in INBOX' % num_msgs
    # if mailbox is not specified
    typ, data = c.select('Does Not Exist')
    print typ, data

# Searching for Messages
def searching_messages():
    typ, mailbox_data = c.list()
    for line in mailbox_data:
        flags, delimiter, mailbox_name = parse_list_response(line)
        c.select(mailbox_name, readonly=True)
        typ, msg_ids = c.search(None, 'ALL')
        print mailbox_name, typ, msg_ids  



if __name__ == '__main__':
    # main config file calling
    c = open_connection()
    try:
        # Method Calling

        # listing_mailboxes()
        # mailbox_status()
        # selecting_mailbox()
        searching_messages()
    
    finally:
        c.logout()
