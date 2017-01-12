import imaplib
import re
import email
import time
import email.message

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

# check for search criteria
def search_criteria():
    typ, mailbox_data = c.list()
    for line in mailbox_data:
        flags, delimiter, mailbox_name = parse_list_response(line)
        c.select(mailbox_name, readonly=True)
        # Search for mail with subject m
        typ, msg_ids = c.search(None, '(SUBJECT "m")')
        # Search for mail with from contain "s" and subject contain "m"
        # typ, msg_ids = c.search(None, '(FROM "s" SUBJECT "m")')
        print mailbox_name, typ, msg_ids 

# feaching content from inbox and display it. 
def fetching_messages():
    
    c.select('INBOX', readonly=True)
    
    print 'HEADER:'
    typ, msg_data = c.fetch('1', '(BODY.PEEK[HEADER])')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            print response_part[1]
    
    print 'BODY TEXT:'
    typ, msg_data = c.fetch('1', '(BODY.PEEK[TEXT])')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            print response_part[1]

    print '\nFLAGS:'
    typ, msg_data = c.fetch('1', '(FLAGS)')
    for response_part in msg_data:
        print response_part
        print imaplib.ParseFlags(response_part)

# Retrieve the entire message as an RFC 2822 formatted mail message
def whole_messages():
    c.select('INBOX', readonly=True)
    
    typ, msg_data = c.fetch('1', '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            for header in [ 'subject', 'to', 'from' ]:
                print '%-8s: %s' % (header.upper(), msg[header])

# To add a new message to a mailbox
def uploading_messages():
    new_message = email.message.Message()
    new_message.set_unixfrom('pymotw')
    new_message['Subject'] = 'subject goes here'
    new_message['From'] = 'sanu@example.com'
    new_message['To'] = 'sanu@example.com'
    new_message.set_payload('This is the body of the message.\n')

    print new_message

    c.append('INBOX', '', imaplib.Time2Internaldate(time.time()), str(new_message))
    
    c.select('INBOX')
    typ, [msg_ids] = c.search(None, 'ALL')
    for num in msg_ids.split():
        typ, msg_data = c.fetch(num, '(BODY.PEEK[HEADER])')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                print '\n%s:' % num
                print response_part[1]

# moving_and_copying_messages
def moving_and_copying_messages():
    # Find the "SEEN" messages in INBOX
    c.select('INBOX')
    typ, [response] = c.search(None, 'UNSEEN')
    if typ != 'OK':
        raise RuntimeError(response)
    
    # Create a new mailbox, "Today"
    msg_ids = ','.join(response.split(' '))
    typ, create_response = c.create('Today')
    print 'CREATED Today:', create_response
    
    # Please uncomment "c.copy(msg_ids, 'Today')" for coping content from inbox to new mailbox "Today"
    # Copy the messages
    # print 'COPYING:', msg_ids
    # c.copy(msg_ids, 'Today')
    
    # Look at the results
    c.select('Today')
    typ, [response] = c.search(None, 'ALL')
    print 'COPIED:', response
    
# Delete message from mailbox
def deleting_messages():
    c.select('Today')

    # What ids are in the mailbox?
    typ, [msg_ids] = c.search(None, 'ALL')
    print 'Starting messages:', msg_ids
    
    # # Find the message(s)
    # typ, [msg_ids] = c.search(None, '(SUBJECT "subject")')
    # msg_ids = ','.join(msg_ids.split(' '))
    # print 'Matching messages:', msg_ids
    
    # # What are the current flags?
    # typ, response = c.fetch(msg_ids, '(FLAGS)')
    # print 'Flags before:', response
    
    # # Change the Deleted flag
    # typ, response = c.store(msg_ids, '+FLAGS', r'(\Deleted)')
    
    # # What are the flags now?
    # typ, response = c.fetch(msg_ids, '(FLAGS)')
    # print 'Flags after:', response
    
    # # Really delete the message.
    # typ, response = c.expunge()
    # print 'Expunged:', response
    
    # What ids are left in the mailbox?
    typ, [msg_ids] = c.search(None, 'ALL')
    print 'Remaining messages:', msg_ids


if __name__ == '__main__':
    # main config file calling
    c = open_connection()
    try:
        # Method Calling

        # listing_mailboxes()
        # mailbox_status()
        # selecting_mailbox()
        # searching_messages()
        # search_criteria()
        # fetching_messages()
        # whole_messages()
        # uploading_messages()
        # moving_and_copying_messages()
        deleting_messages()
    
    finally:
        c.logout()
        print('\nLogout success Goodbye!')
