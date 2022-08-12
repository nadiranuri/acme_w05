from random import randint
import urllib2
import calendar
import urllib

#============================= Image Upload
#http://52.230.87.124/image_hub/static/acmerx/image.png
# http://52.230.87.124/image_hub/acme_rx_image/acme_rx_image/
def acme_rx_image():
    import shutil
    filename = request.vars.upload.filename
    file = request.vars.upload.file
    shutil.copyfileobj(file, open('/home/www-data/web2py/applications/image_hub/static/acmerx/' + filename, 'wb'))
    return 'success'

def index():
    return 'access restricted'



