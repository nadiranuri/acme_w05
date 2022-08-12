from random import randint
import urllib2
import calendar
import urllib
import time


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)




# http://127.0.0.1:8000/acme/sales_report_dcr/salesDcr_report_detail?cid=acme&rep_id=20952&rep_pass=1234&device_id=1234

def salesDcr_report_detail():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    rep_pass = str(request.vars.password).strip()
    if rep_pass=='None' or rep_pass==None:
        rep_pass = str(request.vars.rep_pass).strip()

    
    device_id = str(request.vars.device_id).strip()
    # return rep_pass
    rep_id_report = str(request.vars.rep_id_report).strip().upper()

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from

    btn_filter=request.vars.btn_filter
    # return btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    from_dt = str(request.vars.to_dt_2).strip().upper()
    to_date= str(request.vars.to_dt_3).strip().upper()

    if btn_filter:
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        # return from_dt
        session.btn_filter=btn_filter
        dateFlag=True
        
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
            session.from_dt=str(from_dt).split(' ')[0]
            session.to_date=str(to_date).split(' ')[0]
            
        except:
            session.from_dt=''
            session.to_date=''
            dateFlag=False
        
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        session.btn_all=btn_all
        session.from_dt=current_date
        session.to_date=current_date
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return db._lastsql
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    # dateFlag=''
    reqPage=len(request.args)
    
    
    if (user_type=='REP'):
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        # return repAreaRow
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        else:

            rp_areaList=[]
            repAreaStr=''
            for repAreaRow in repAreaRow:
                repArea_id=repAreaRow.area_id
                rp_areaList.append(repArea_id)
                if repAreaStr=='':
                    repAreaStr="'"+str(repArea_id)+"'"
                else:
                    repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        # qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        # qset = qset((db.sm_doctor_visit.visit_date >= session.from_dt) and (db.sm_doctor_visit.visit_date <= session.to_date))
        
        # return session.to_date
        if (session.from_dt and session.to_date)!='' and (session.from_dt and session.to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= session.from_dt) & (db.sm_doctor_visit.visit_date <= session.to_date))
        # return db._lastsql
        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.route_name|db.sm_doctor_visit.visit_date)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                # doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                # doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        # qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        # qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (session.from_dt and session.to_date)!='' and (session.from_dt and session.to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= session.from_dt) & (db.sm_doctor_visit.visit_date <= session.to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)

                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'"      


        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.route_id.belongs(marketStrList))
        # qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (session.from_dt and session.to_date)!='' and (session.from_dt and session.to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= session.from_dt) & (db.sm_doctor_visit.visit_date <= session.to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                # doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                # doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        # qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(marketStrList))
        # qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (session.from_dt and session.to_date)!='' and (session.from_dt and session.to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= session.from_dt) & (db.sm_doctor_visit.visit_date <= session.to_date))
            
        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.route_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)

    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,rep_pass=rep_pass,device_id=device_id,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)

def slsRptDcr_area_wise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.device_id).strip()
    visit_date = str(request.vars.visit_date).strip()
    route_id = str(request.vars.route_id).strip()
    
    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.visit_date = visit_date  
    session.route_id = route_id 
    

    redirect(URL(c='sales_report',f='slsRptDcr_area_wise'))

def slsRptDcr_area_wise():
    cid =session.cid
    rep_id =session.rep_id
    password =session.password
    synccode =session.synccode
    route_id =session.route_id
    visit_date=session.visit_date
    # return route_id
    
    
    date_to = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return cid
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    
    report_string=""    
    report_str=""
    
    if (user_type=='REP'):
        
        condition=""      
        condition="and s1.route_id='"+ str(route_id) +"' "        
        
        records_ov=[]
        sql_str="SELECT  COUNT(s1.doc_id)as doc_count,s1.doc_id as doc_id, s1.doc_name as doc_name,s1.id as id,s1.visit_dtime as visit_dtime,s1.giftnsample as giftnsample,s1.route_id as route_id,s1.route_name as route_name  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND s1.visit_date = '"+ str(visit_date) +"' "+ condition + " GROUP BY s1.route_id,s1.id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
        levelList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        
        # cTeam=0
        # for i in range(len(levelList)):
        #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
        #     for levelRow in levelRows:
        #         level_id = levelRow.level_id
        #         special_territory_code = levelRow.special_territory_code
        #         if level_id==special_territory_code:
        #             cTeam=1

        #         if marketStr=='':
        #             marketStr="'"+str(level_id)+"'"
        #         else:
        #             marketStr=marketStr+",'"+str(level_id)+"'" 
            
        #     if cTeam==1:    
        #         if special_territory_code not in spicial_codeList:
        #             if (special_territory_code !='' and level_id==special_territory_code):
        #                 spicial_codeList.append(special_territory_code)    
            
        #             levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

        #             for levelSpecialRow in levelSpecialRows:
        #                 level_id = levelSpecialRow.level_id
        #                 if marketStr=='':
        #                     marketStr="'"+str(Suplevel_id)+"'"
        #                 else:
        #                     marketStr=marketStr+",'"+str(level_id)+"'"          
        
        condition=''
        condition=condition+"AND route_id IN ("+str(route_id)+") "
        # return db._lastsql 
        records_ov=[]
        sql_str="SELECT  COUNT(s1.doc_id)as doc_count,s1.doc_id as doc_id, s1.doc_name as doc_name,s1.id as id,s1.visit_dtime as visit_dtime,s1.giftnsample as giftnsample,s1.route_id as route_id,s1.route_name as route_name  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND s1.visit_date = '"+ str(visit_date) +"' "+ condition + " GROUP BY s1.route_id,s1.id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)
    # return route_id
    return dict(date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,records_ov=records_ov,route_id=route_id,visit_date=visit_date)



def sales_rptDcr_slWise():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    route_id = str(request.vars.row_r_id).strip()

    visit_date=str(request.vars.visit_date).strip()
    doc_id = str(request.vars.doc_id).strip().upper()

    rowid = str(request.vars.rowid).strip()

    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):

        condition=""      
        condition="and s1.route_id='"+ str(route_id) +"' "

        records_ov=[]
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' "+ condition + " GROUP BY s1.route_id,s1.id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
        
        condition=''
        condition=condition+"AND route_id IN ("+str(route_id)+") "  

        records_ov=[]
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' GROUP BY s1.route_id,s1.id;"

        records_ov=db.executesql(sql_str,as_dict = True)

    return dict(records_ov=records_ov,rowid=rowid,visit_date=visit_date,route_id=route_id,doc_id=doc_id)


def sales_rptDcr_zm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 7)
    date_to=str(date_ton).split(' ')[0]
    # return date_to

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.from_dt).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()

        session.btn_filter=btn_filter
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        else:

            rp_areaList=[]
            repAreaStr=''
            for repAreaRow in repAreaRow:
                repArea_id=repAreaRow.area_id
                rp_areaList.append(repArea_id)
                if repAreaStr=='':
                    repAreaStr="'"+str(repArea_id)+"'"
                else:
                    repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        # qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)

                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'"      

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        # qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)



    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)







# =========== 20210606 End ==========
# =========== 20210606 End ==========




def get_territory():
    lvlStr = ''
    cid = session.cid

    rep_id = str(request.vars.rep_id).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()


   
    qset=db()
    qset=qset(db.sm_level.cid==session.cid)


    if user_type == 'SUP':  

        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return level


        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return SuplevelRows
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
            # return levelStr
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                # return levelRows
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3')& (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
            # return levelRows


            # levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id.belongs(session.level_idList))).select(db.sm_level.level0, db.sm_level.level0_name, orderby=db.sm_level.level0_name, groupby=db.sm_level.level0)
            for row in levelRows:
                level_id = str(row.level_id)
                name = str(row.level_name).replace('|', ' ').replace(',', ' ')
                
                if lvlStr == '':
                    lvlStr = name + '|' + level_id 
                else:
                    lvlStr += ',' + name + '|' +  level_id 
            
    else:
        rows = db((db.sm_rep_area.cid == cid)  & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id ,orderby=db.sm_rep_area.area_name)
        for row in rows:
            level_id = str(row.area_id)
            name = str(row.area_name).replace('|', ' ').replace(',', ' ')
            
            if lvlStr == '':
                lvlStr = name + '|' + level_id 
            else:
                lvlStr += ',' + name + '|' +  level_id 
            
    return lvlStr

