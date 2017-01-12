import imaplib

def open_connection(verbose=False):
   
    # Connect to the server
    connection = imaplib.IMAP4_SSL('servername')

    # Login to our account
    connection.login('username', 'password')
    return connection

# if __name__ == '__main__':
#     c = open_connection(verbose=True)
#     try:
#         resp, data = c.list()
        
#         print "\nIMAP4_SSL instance :", c
#         print '\nResponse code:', resp
#         print "\nmailboxes available for an account :", data
#     finally:
#         c.logout()



