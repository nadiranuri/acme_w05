
# http://127.0.0.1:8000/acme/report_seen_rx_mobile/index?cid=acme&rep_id=20496&password=1234&device_id=1234

def index():
    cid = request.vars.cid
    rep_id = request.vars.rep_id
    rep_pass = request.vars.rep_pass
    # return rep_pass
    sync_code=request.vars.device_id
    # ---------------------- rep check
    userRecords = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (
                db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.user_type, limitby=(0, 1))
    # return db._lastsql
    if not userRecords:
        response.flash = 'Invalid/Inactive Supervisor'
    else:
        name = userRecords[0].name
        user_type = userRecords[0].user_type

        session.cid = cid
        session.rep_id = rep_id
        session.user_id = rep_id
        session.user_type = user_type

        level_area_list = []

        if user_type=='rep':
            repAreaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,orderby=db.sm_rep_area.area_id)
            # return repAreaRows
            if not repAreaRows:
                response.flash = 'Rep Territory Not Available'
            else:
                for rRow in repAreaRows:
                    area_id=rRow.area_id
                    area_name = rRow.area_name

                    dictData = {'area_id': area_id, 'area_name': area_name}
                    level_area_list.append(dictData)

        else:
            supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)

            if not supLevelRows:
                response.flash = 'Supervisor Level Not Available'
            else:
                sup_level_id_list=[]
                level_depth_no=0
                for sRow in supLevelRows:
                    level_depth_no=sRow.level_depth_no
                    level_id=sRow.level_id
                    sup_level_id_list.append(level_id)

                if level_depth_no==0:
                    level3Rows = db((db.sm_level.cid == cid) & (db.sm_level.level0.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                if level_depth_no == 1:
                    level3Rows = db((db.sm_level.cid == cid) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                elif level_depth_no==2:
                    level3Rows = db((db.sm_level.cid == cid) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

        session.level_area_list=level_area_list
        # return session.level_area_list
        level_area_id_list = []
        for i in range(len(level_area_list)):
            level_area_str = level_area_list[i]
            level_area_id_list.append(level_area_str['area_id'])

        session.level_area_id_list = level_area_id_list
        
        redirect(URL(c='report_seen_rx_mobile_test', f='home',vars=dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,sync_code=sync_code)))

    return dict()


def home():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='report_seen_rx_mobile',f='index'))
    # return session.cid
    session.from_date =str(first_currentDate)[:10]
    session.to_date = current_date
    level_area_list = session.level_area_list

    cid = request.vars.cid
    rep_id= request.vars.rep_id
    rep_pass= request.vars.rep_pass
    sync_code= request.vars.sync_code
    
    btn_report=request.vars.btn_report

    if btn_report:
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        sch_area = request.vars.sch_area

        session.from_date=from_date
        session.to_date=to_date
        session.sch_area = sch_area

    qset=db()
    qset=qset(db.sm_prescription_seen_head.cid == session.cid)
    # return session.user_type
    if session.user_type=='rep':
        qset = qset(db.sm_prescription_seen_head.submit_by_id == rep_id)


    if session.user_type=='sup':
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)

        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)

                


        sup_rep_Rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(marketStrList) )).select(db.sm_rep_area.rep_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        # return repAreaRow
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        else:

            rp_areaList=[]
            rp_areaList.append(rep_id)


            for repAreaRow in repAreaRow:
                repArea_id=repAreaRow.rep_id
                rp_areaList.append(repArea_id)
                
        qset = qset(db.sm_prescription_seen_head.submit_by_id.belongs(rp_areaList))


    if session.from_date!='' and session.to_date!='':
        qset = qset((db.sm_prescription_seen_head.submit_date >= session.from_date)&(db.sm_prescription_seen_head.submit_date <= session.to_date))

    if session.sch_area!='' and session.sch_area!=None:
        qset = qset(db.sm_prescription_seen_head.area_id==session.sch_area)
    else:
        pass
        # qset = qset(db.sm_prescription_seen_head.area_id.belongs(session.level_area_id_list))


    records=qset.select(db.sm_prescription_seen_head.submit_date,db.sm_prescription_seen_head.submit_by_id,db.sm_prescription_seen_head.submit_by_name,db.sm_prescription_seen_head.area_id,db.sm_prescription_seen_head.id.count(),groupby=db.sm_prescription_seen_head.submit_date|db.sm_prescription_seen_head.submit_by_id|db.sm_prescription_seen_head.submit_by_name|db.sm_prescription_seen_head.area_id,orderby=db.sm_prescription_seen_head.area_id|db.sm_prescription_seen_head.submit_by_id)
    
    return db._lastsql
    # rx count
    qsetH = db()
    qsetH = qsetH(db.sm_prescription_seen_head.cid == session.cid)

    if session.user_type=='rep':
        qsetH = qsetH(db.sm_prescription_seen_head.submit_by_id == session.rep_id)

    if session.from_date!='' and session.to_date!='':
        qsetH = qsetH((db.sm_prescription_seen_head.submit_date >= session.from_date) & (
                    db.sm_prescription_seen_head.submit_date <= session.to_date))

    if session.sch_area!='' and session.sch_area!=None:
        qsetH = qsetH(db.sm_prescription_seen_head.area_id == session.sch_area)
    else:
        pass
        # qsetH = qsetH(db.sm_prescription_seen_head.area_id.belongs(session.level_area_id_list))

    recordsH=qsetH.count()

    
    return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,sync_code=sync_code,records=records,recordsH=recordsH,level_area_list=level_area_list)



def report_seen_rx_area_wise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    
    rep_pass = str(request.vars.rep_pass).strip()
    # return rep_pass
    sync_code = str(request.vars.sync_code).strip()
    area_id = str(request.vars.area_id).strip()
    to_date = str(request.vars.to_date).strip()
    from_dt = str(request.vars.from_date).strip()
    
    # return area_id
   
    session.cid=cid
    session.rep_id=rep_id     
    session.rep_pass=rep_pass
    session.sync_code=sync_code
    session.area_id=area_id

    
    session.to_date=to_date
    session.from_dt=from_dt


    redirect(URL(c='report_seen_rx_mobile',f='report_seen_rx_area_wise'))#,vars=dict(invoice_count=invoice_count)))



def report_seen_rx_area_wise():

    cid=session.cid
    rep_id=session.rep_id
    user_type=session.user_type
    rep_pass=session.rep_pass
    sync_code=session.sync_code
    area_id=session.area_id
    
    from_date=session.from_dt
    to_date=session.to_date

    # invoice_count=str(request.vars.invoice_count).strip()

    # return area_id
        
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_to=now + datetime.timedelta(days = 1)
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return rep_id
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

        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        # else:

            # rp_areaList=[]
            # repAreaStr=''
            # for repAreaRow in repAreaRow:
            #     repArea_id=repAreaRow.area_id
            #     rp_areaList.append(repArea_id)
            #     if repAreaStr=='':
            #         repAreaStr="'"+str(repArea_id)+"'"
            #     else:
            #         repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
        
    
        condition=""                
        condition="and  sm_prescription_seen_head.area_id  = '"+str(area_id) +"'"

        condition=condition+ "and sm_prescription_seen_head.submit_date  >= '"+str(session.from_date) +"' and sm_prescription_seen_head.submit_date  <= '"+str(session.to_date) +"'"
        # return condition
        records_ov=[]
            
        sql_str="SELECT COUNT(sm_prescription_seen_head.id) as id_count,(sm_prescription_seen_head.sl) as medicine_sl,(sm_prescription_seen_head.doctor_id) as doctor_id,(sm_prescription_seen_head.doctor_name) as doctor_name FROM sm_prescription_seen_head WHERE sm_prescription_seen_head.cid = '"+ str(cid)+"' and sm_prescription_seen_head.submit_by_id ='"+ rep_id +"'" +condition+"   GROUP BY doctor_id  ;"        
        
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):       
    

        condition=''
        condition=condition+" AND area_id IN ("+str(area_id)+")"  

        records_ov=[]
        # sql_str="SELECT (sm_order.client_id) as client_id,(sm_order.client_name) as client_name,SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.vsl as vsl FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' and sm_order.area_id='"+ area_id+"' and sm_order.order_date>='"+ from_date+"' and sm_order.order_date<='"+ to_date+"'  GROUP BY area_id,vsl ORDER BY vsl DESC  ;"
        sql_str="SELECT COUNT(sm_prescription_seen_head.id) as id_count,(sm_prescription_seen_head.sl) as medicine_sl,(sm_prescription_seen_head.doctor_id) as doctor_id,(sm_prescription_seen_head.doctor_name) as doctor_name FROM sm_prescription_seen_head WHERE sm_prescription_seen_head.cid = '"+ str(cid)+"' and sm_prescription_seen_head.submit_by_id ='"+ rep_id +"'" +condition+"   GROUP BY doctor_id  ;"        
        
        records_ov=db.executesql(sql_str,as_dict = True)               


    # order_date=''
    return dict(date_to=date_to,cid=cid,rep_id=rep_id,rep_pass=rep_pass,sync_code=sync_code,records_ov=records_ov,area_id=area_id)


def report_seen_rx_slWise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    rep_pass = str(request.vars.rep_pass).strip()
    sync_code = str(request.vars.sync_code).strip()
    area_id = str(request.vars.area_id).strip()
    medicine_sl = str(request.vars.medicine_sl).strip()
    doctor_id = str(request.vars.doctor_id).strip()
    # return doctor_id

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.rep_pass = rep_pass
    session.sync_code = sync_code
    session.area_id = area_id
    session.medicine_sl = medicine_sl
    session.doctor_id = doctor_id
    
    redirect(URL(c='report_seen_rx_mobile',f='report_seen_rx_slWise'))

def report_seen_rx_slWise():
   
    cid = session.cid       
    rep_id = session.rep_id    
    user_type = session.user_type    
    rep_pass = session.rep_pass    
    sync_code = session.sync_code    
    area_id = session.area_id    
    medicine_sl = session.medicine_sl    
    doctor_id = session.doctor_id
    # return rep_id
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
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
        repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        else:
            
           
            sql_str="SELECT medicine_name,medicine_id,sl FROM sm_prescription_seen_details WHERE sm_prescription_seen_details.cid = '"+ str(cid) +"' AND sm_prescription_seen_details.submit_by_id = '"+ str(rep_id) +"' AND sm_prescription_seen_details.sl= '"+ str(medicine_sl) +"' AND sm_prescription_seen_details.area_id='"+str(area_id)+"' AND sm_prescription_seen_details.doctor_id='"+str(doctor_id)+"'  GROUP BY sm_prescription_seen_details.area_id,medicine_id;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)
    
    
    if (user_type=='SUP'):
        repAreaRow = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id)).select(db.sm_supervisor_level.level_id,orderby=db.sm_supervisor_level.level_id,groupby=db.sm_supervisor_level.level_id)        
        if not repAreaRow:
           retStatus = 'FAILED<SYNCDATA>Invalid Area'
           return retStatus
        else:
            sql_str="SELECT medicine_name,medicine_id,sl FROM sm_prescription_seen_details WHERE sm_prescription_seen_details.cid = '"+ str(cid) +"' AND sm_prescription_seen_details.submit_by_id = '"+ str(rep_id) +"' AND sm_prescription_seen_details.sl= '"+ str(medicine_sl) +"' AND sm_prescription_seen_details.area_id='"+str(area_id)+"' AND sm_prescription_seen_details.doctor_id='"+str(doctor_id)+"'  GROUP BY sm_prescription_seen_details.area_id,medicine_id;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)

    return dict(records_ov=records_ov,medicine_sl=medicine_sl,area_id=area_id,doctor_id=doctor_id,rep_id=rep_id)

# def index_x():
#
#     c_id=request.vars.cid
#     rep_id=request.vars.rep_id
#     rep_pass=request.vars.rep_pass
#
#     #---------------------- rep check
#     userRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.password==rep_pass)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#
#     if not userRecords:
#         response.flash = 'Invalid/Inactive Supervisor'
#     else:
#         name=userRecords[0].name
#         user_type=userRecords[0].user_type
#
#         session.cid=c_id
#         session.rep_id=rep_id
#         session.user_id=rep_id
#
#
#         level_area_list = []
#
#         supLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
#
#         if not supLevelRows:
#             response.flash = 'Supervisor Level Not Available'
#         else:
#             sup_level_id_list=[]
#             level_depth_no=0
#             for sRow in supLevelRows:
#                 level_depth_no=sRow.level_depth_no
#                 level_id=sRow.level_id
#                 sup_level_id_list.append(level_id)
#
#             if level_depth_no==0:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             if level_depth_no == 1:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             elif level_depth_no==2:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             session.level_area_list=level_area_list
#
#             redirect(URL(c='ppm_mark_mobile',f='home'))
#
#     return dict()
#
#
#
#
#
#
# def rep_list():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#
#     repRows=db((db.sm_rep_area.cid == session.cid) & (db.sm_rep_area.area_id==session.area_id)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.rep_category,orderby=db.sm_rep_area.rep_name)
#     repListStr=''
#     for row in repRows:
#         rep_name=row.rep_name
#         rep_id = row.rep_id
#
#         if repListStr=='':
#             repListStr=rep_name+'|'+rep_id
#         else:
#             repListStr +='<rd>'+rep_name + '|' + rep_id
#
#     return repListStr
#
#
# def rep():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#
#
#     return dict()
#
#
# def ppm_list():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     ppmRows=db((db.sm_doctor_ppm.cid == session.cid)& (db.sm_doctor_ppm.status =='ACTIVE')).select(db.sm_doctor_ppm.gift_id,db.sm_doctor_ppm.gift_name,db.sm_doctor_ppm.item_brand,db.sm_doctor_ppm.item_price,orderby=db.sm_doctor_ppm.gift_name)
#
#     ppmListStr = ''
#     for row in ppmRows:
#         gift_id = str(row.gift_id)
#         gift_name = str(row.gift_name)
#         item_brand = str(row.item_brand)
#         item_price = str(row.item_price)
#
#         if ppmListStr == '':
#             ppmListStr = gift_name + '|' +gift_id+ '|' + item_brand+ '|' + item_price
#         else:
#             ppmListStr += '<rd>' + gift_name + '|' +gift_id+ '|' + item_brand+ '|' + item_price
#
#     return ppmListStr
#
#
# def ppm():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#     rep_name = request.vars.repName
#
#
#     return dict(rep_id=rep_id,rep_name=rep_name)
#
# def ppm_submit():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#
#     submitItem=request.vars.submitItem
#
#     emp_id=''
#     emp_name = ''
#     level_id = ''
#     level_name = ''
#
#     supLevelRows = db((db.sm_supervisor_level.cid == session.cid) & (db.sm_supervisor_level.sup_id == session.rep_id)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_name,limitby=(0,1))
#
#     if supLevelRows:
#         emp_id = supLevelRows[0].sup_id
#         emp_name = supLevelRows[0].sup_name
#         level_id = supLevelRows[0].level_id
#         level_name = supLevelRows[0].level_name
#
#         repAreaRows = db((db.sm_rep_area.cid == session.cid)&(db.sm_rep_area.area_id == session.area_id) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name,db.sm_rep_area.area_id, db.sm_rep_area.area_name,limitby=(0, 1))
#         sqlInsert=''
#         rep_name=''
#         if repAreaRows:
#             rep_id = repAreaRows[0].rep_id
#             rep_name = repAreaRows[0].rep_name
#             rep_area_id = repAreaRows[0].area_id
#
#             item_arr = submitItem.split('||')
#             sqlInsert=''
#             for i in range(len(item_arr)):
#                 itemStr=item_arr[i].split('|')
#                 item_id=itemStr[0]
#                 item_value = itemStr[1]
#
#                 try:
#                     item_value=int(item_value)
#                     if item_value<0 or item_value>10:
#                         item_value=0
#                 except:
#                     item_value=0
#
#                 if item_value==0:continue
#
#                 ppmRows = db((db.sm_doctor_ppm.cid == session.cid)&(db.sm_doctor_ppm.gift_id == item_id)).select(db.sm_doctor_ppm.gift_id,db.sm_doctor_ppm.gift_name,db.sm_doctor_ppm.item_brand,db.sm_doctor_ppm.item_price,limitby=(0,1))
#
#                 if ppmRows:
#                     gift_id=ppmRows[0].gift_id
#                     gift_name = ppmRows[0].gift_name
#                     item_brand = ppmRows[0].item_brand
#                     item_price = ppmRows[0].item_price
#
#                     sqlInsert = db.sm_ppm_mark_details.insert(emp_id=emp_id,emp_name=emp_name,level_id=level_id,level_name=level_name,rep_id=rep_id,rep_name=rep_name,rep_area=rep_area_id,ppm_id=gift_id,ppm_name=gift_name,item_brand=item_brand,item_price=item_price,item_value=item_value)
#
#         if sqlInsert:
#             session.flash='Submitted Successfullly ('+rep_name+'|'+rep_id+')'
#             redirect(URL(c='ppm_mark_mobile', f='rep'))
#
#
#     return dict(rep_id=rep_id,rep_name=rep_name)
#
#
# def ppm_history():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#     rep_name = request.vars.repName
#
#     records=db((db.sm_ppm_mark_details.cid == session.cid)&(db.sm_ppm_mark_details.emp_id == session.rep_id)&(db.sm_ppm_mark_details.rep_id == rep_id)).select(db.sm_ppm_mark_details.submit_date,db.sm_ppm_mark_details.ppm_id,db.sm_ppm_mark_details.ppm_name,db.sm_ppm_mark_details.item_brand,db.sm_ppm_mark_details.item_price,db.sm_ppm_mark_details.item_value,orderby=~db.sm_ppm_mark_details.id,limitby=(0,30))
#
#     return dict(records=records,rep_id=rep_id,rep_name=rep_name)





