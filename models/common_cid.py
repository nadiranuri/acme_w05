import datetime
import urllib
# db = DAL('mysql://w-mysql-002-se%skf_live:skfsamsung999live@w-mysql-002-se.mysql.database.azure.com/skf_live', decode_credentials=True)
db = DAL('mysql://acme:acme654321@psqlcba02-rep.mysql.database.azure.com/acme', decode_credentials=True)
mreporting_http_pass='abC321'
date_fixed=datetime.datetime.now()+datetime.timedelta(hours=6)
