# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:46:07 2019

@author: dpcn
"""
def set_up_MIME_IMAGE(url, file_format):
    from io import BytesIO
    from requests import get as requestsget
    from PIL import Image
    from email.mime.image import MIMEImage
    
    stream_bytes = BytesIO()
    response = requestsget(url)
    img = Image.open(BytesIO(response.content))
    img.save(stream_bytes,file_format)
    stream_bytes.seek(0)
    img_obj = stream_bytes.read()
    
    return MIMEImage(img_obj)

def attach_image_inline(msg_root, msg_template, url, tag, file_format='jpeg'):
    '''Sets up image attachment in email'''
    mime_img = set_up_MIME_IMAGE(url, file_format)
    mime_img.add_header('Content-ID','<{}>'.format(tag))
    msg_root.attach(mime_img)
    
    html_tag = '''<br><b>{}</b><br><br><img src="cid:{}"><br>'''.format(tag,tag)
    return msg_template + html_tag


def add_table_to_template(template, df, table_title):
    formatted_df = df.to_html(border=1,index=False,classes='table width="800" cellpadding="5" cellspacing="0" style="border-collapse:collapse;text-align:center;"')
    
    html = """  <br>
                <h3><b>{}</b></h3>
                {}
                <br>
                """.format(table_title, formatted_df)
    return template+html

    
def survey123_to_email(layer, query_field, query_value, display_field, email_field):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from jinja2 import Environment
    
    mp_msg = MIMEMultipart()
    query = "{} = '{}'".format(query_field,query_value)
    feat_ob = Utils.from_layer(layer, query)

    TEMPLATE="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{}</title>
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
        <h1>{}</h1>
        <p>{}</p>
    
    """.format("Survey Report",layer.properties.name, feat_ob.attributes[display_field])
    
    TEMPLATE = add_table_to_template(TEMPLATE, feat_ob.build_field_order(), 'Main Feature')
    
    for att in feat_ob.att_res:
        TEMPLATE = attach_image_inline(mp_msg, TEMPLATE, att['DOWNLOAD_URL'], att['KEYWORDS'],'jpeg')
    
    for rel_data in feat_ob.related_data:
        TEMPLATE = add_table_to_template(TEMPLATE, rel_data.return_sdf(), rel_data.layer_name)
    
    TEMPLATE +="""</body>
                </html>
                """     
    
    mst_template = MIMEText(
    Environment().from_string(TEMPLATE).render(
        title='Feature Report',

        ), "html"
            )
    mp_msg.attach(mst_template)
    
    return mp_msg



#TEMPLATE = add_table_to_template(TEMPLATE, df_main, "MAIN FEATURE")
#TEMPLATE = add_table_to_template(TEMPLATE, df_relate.return_sdf(), "Related Table")



#
#import smtplib
#import pandas
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
#from jinja2 import Environment

# Create a text/html message from a rendered template
sender="dpcn@pge.com"
receiver=['dpcn@pge.com'
#          ,'j1vc@pge.com',
#          ,'nxlu@pge.com',
#          'b1hp@pge.com',
#          'c3wi@pge.com',
#          'a7so@pge.com',
#          'm8p6@pge.com'
          ]

#mp_msg = MIMEMultipart()
##mp_visible = MIMEMultipart()
#
#df_main = pandas.DataFrame(feat_ob.build_field_order())
#TEMPLATE = add_table_to_template(TEMPLATE, df_main, 'Main Feature')
#
#for att in feat_ob.att_res:
#    TEMPLATE = attach_image_inline(mp_msg, TEMPLATE, att['DOWNLOAD_URL'], att['KEYWORDS'],'jpeg')
#
#for rel_data in feat_ob.related_data:
#    TEMPLATE = add_table_to_template(TEMPLATE, rel_data.return_sdf(), rel_data.layer_name)
#
#
#TEMPLATE +="""</body>
#</html>
#"""  




#
#
#mst_template = MIMEText(
#    Environment().from_string(TEMPLATE).render(
#        title='Feature Report',
#
#        ), "html"
#            )
#
#
#
#mp_msg.attach(mst_template)

    
mp_msg['Subject'] = "Survey Report Test"
mp_msg['To'] = ', '.join(receiver)
mp_msg['From'] = 'dpcn@pge.com'

#mp_msg.attach(mp_visible)

#set SMTP
server=smtplib.SMTP('mailhost',25)
server.login

#set sender and reciever



#send email

server.sendmail(sender,receiver,mp_msg.as_string())


server.quit()






