import imaplib
import re

from imap_conf import open_connection


list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

print "list_response_pattern :", list_response_pattern


def parse_list_response(line):
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)










# main config file calling

if __name__ == '__main__':
    c = open_connection(verbose=True)
    try:
        resp, data = c.list()
        # IMAP instance
        print "\nIMAP4_SSL instance :", c
        # first parameter of the c.list()
        print '\nResponse code:', resp
        # second parameter of the c.list()
        print "\nmailboxes available for an account :", data

        for line in data:
        	print 'Server response:', line
        	flags, delimiter, mailbox_name = parse_list_response(line)
        	print 'Parsed response:', (flags, delimiter, mailbox_name)
    finally:
        c.logout()
