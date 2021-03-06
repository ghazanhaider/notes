#!/usr/bin/python
#
##################################
#
# Simplest python http server serving inline strings and cookie auth v0.1
# -Ghazan Haider
#
##################################
#
# A default cookie of Cookie=test is created on first access
# 
# The user must manually change their cookie to the value in Magic_Cookie:
#
# Chrome: Developer tools -> Console -> document.cookie=<Magic_Cookie>
# Firefox: Developer toolbar -> "Cookie set <Cookie> <Value>"
# Safari: Safari Preferences -> Advanced -> Show develop menu.. -> On page press option+cmd+i ->
# ... In the console prompt at bottom type document.cookie="<cookie>=<value>"
# curl: curl -b "<cookie>=<value>" http://site
# wget: wget --header="Cookie: <cookie>=<value>" http://site
# IE: Fuck IE

import socket


# Strings
#########

HTTP_bad_response_header = '''HTTP/1.0 404 Not Found
Server: notes.py/0.0.1 Ghazan Haider
Content-Type: text/html
Set-Cookie: Cookie=test
Content-Length: '''

HTTP_bad_response_body='<h1> 404'

HTTP_good_response_header = '''HTTP/1.0 200 OK
Server: notes.py/0.0.1 Ghazan Haider
Content-Type: text/html
Content-Length: '''

HTTP_good_response_body = '<h1> Hello Monster!'

Magic_Cookie = "Cookie: Cookie=Monster"



# Main Program
##############


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))


# HTTP server loop

while 1:
  s.listen(5)
  conn,addr = s.accept()
  # print "Connected by ", addr

  databuf=""


  # Data receive loop.
  # Notes:
  # 1- conn.recv might require any number of attempts
  # 2- Even if data is less than buffer size (1024), there might be more waiting
  # 3- If we have all the data and run recv once again, it'll hang and wait forever!
  # 4- So we have to watch for HTTP header request ending as per standards
  # .. and not run recv once we have the ending of '\r\n\r\n'
  # 5- Single process nonthreaded server. If we get a second request during
  # .. processing of the first, it'l fail.

  while 1:
    data = conn.recv(1024)
    databuf += data
    if databuf[-4:] == '\r\n\r\n' : break

  print databuf  # Comment this out for a silent server

  if Magic_Cookie in databuf:
    conn.send(HTTP_good_response_header + str(len(HTTP_good_response_body)) + '\r\n\r\n' + HTTP_good_response_body )
  else:
    conn.send(HTTP_bad_response_header + str(len(HTTP_bad_response_body)) + '\r\n\r\n' + HTTP_bad_response_body )


  conn.close()

