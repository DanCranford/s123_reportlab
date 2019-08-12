# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:46:07 2019

@author: dpcn
"""



TEMPLATE="""
<!DOCTYPE html>
<html>
<head>
<title>{{ title }}</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

  <style>
table {
  border-collapse: collapse;
}
 table, th, td {
  border: 1px solid black;
  text-align: center;
}
  </style>


  
</head>
<body>
    <h1>{{layer_name}}</h1>
    <p>{{feature_id}}</p>

"""

def add_table_to_template(template, df, table_title):
    formatted_df = df.to_html(border=1,index=False,classes='table width="800" cellpadding="5" cellspacing="0" style="border-collapse:collapse;text-align:center;"')
    
    html = """  <br>
                <h3><b>{}</b></h3>
                {}
                <br>
                """.format(table_title, formatted_df)
    return template+html


TEMPLATE = add_table_to_template(TEMPLATE, df_main, "MAIN FEATURE")
TEMPLATE = add_table_to_template(TEMPLATE, df_relate, "Related Table")


TEMPLATE =TEMPLATE+"""</body>
</html>
"""  

import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment
# Create a text/html message from a rendered template
sender="dpcn@pge.com"
receiver=['dpcn@pge.com',
#          ,'j1vc@pge.com',
          'nxlu@pge.com',
#          'b1hp@pge.com',
#          'c3wi@pge.com',
#          'a7so@pge.com',
#          'm8p6@pge.com'
          ]


msg = MIMEText(
    Environment().from_string(TEMPLATE).render(
        title='CycloMedia PG&E Inventory',

    ), "html"
)
msg['Subject'] = "Survey Report Test"
msg['To'] = ', '.join(receiver)
msg['From'] = 'dpcn@pge.com'
#set SMTP
server=smtplib.SMTP('mailhost',25)
server.login

#set sender and reciever



#send email

server.sendmail(sender,receiver,msg.as_string())









