#doctor
# http://127.0.0.1:8000/acme_api/api_doctor/get_doctor?cid=ACME&user_id=02127&user_pass=1234

#doctor gift
# http://127.0.0.1:8000/acme_api/api_doctor/get_doctor_gift?cid=ACME&user_id=02127&user_pass=1234

#doctor sample
# http://127.0.0.1:8000/acme_api/api_doctor/get_doctor_sample?cid=ACME&user_id=02127&user_pass=1234

#doctor ppm
# http://127.0.0.1:8000/acme_api/api_doctor/get_doctor_ppm?cid=ACME&user_id=20604&user_pass=1234

def index():
    return 'Welcome to mReporting.'

def get_doctor():
    response.view = 'generic.json'

    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass

    res_data = ''
    if cid == None:
        cid = ''
    if user_id == None:
        user_id = ''
    if password == None:
        password = ''

    if cid == '' or user_id == '' or password == '':
        res_data = {'status': 'Failed', 'ret_str': 'Required All'}
    else:
        userRecords = 'select rep_id,name,user_type from sm_rep where cid="' + cid + '" and rep_id="' + user_id + '" and password="' + password + '" and status="ACTIVE" limit 0,1;'
        userRecords = db.executesql(userRecords, as_dict=True)

        if len(userRecords) == 0:
            res_data = {'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            for rRow in range(len(userRecords)):
                userRecordsStr = userRecords[rRow]
                user_type = str(userRecordsStr['user_type'])

                area_id_list = []
                if user_type=='rep':
                    area_id_list = []
                    rep_category=''
                    userAreaRecords = 'select area_id,rep_category from sm_rep_area where cid="' + cid + '" and rep_id="' + user_id + '";'
                    userAreaRecords = db.executesql(userAreaRecords, as_dict=True)
                    for i in range(len(userAreaRecords)):
                        userAreaRecordsStr = userAreaRecords[i]
                        rep_category = str(userAreaRecordsStr['rep_category'])
                        area_id = str(userAreaRecordsStr['area_id'])
                        area_id_list.append(area_id)

                    if rep_category=='C':
                        rep_area_id_str = str(area_id_list).replace('[', '').replace(']', '')
                        levelRecords = 'select level_id,level_name from sm_level where special_territory_code in (' + rep_area_id_str + ') ;'
                        levelRecords = db.executesql(levelRecords, as_dict=True)
                        area_id_list = []
                        for j in range(len(levelRecords)):
                            levelRecordsStr = levelRecords[j]
                            level_id = str(levelRecordsStr['level_id'])
                            area_id_list.append(level_id)

                else:
                    level_id_list=[]
                    userLevelRecords = 'select sup_id,sup_name,level_id,level_depth_no from sm_supervisor_level where cid="' + cid + '" and sup_id="' + user_id + '" ;'
                    userLevelRecords = db.executesql(userLevelRecords, as_dict=True)
                    for i in range(len(userLevelRecords)):
                        userLevelRecordsStr = userLevelRecords[i]
                        level_id = str(userLevelRecordsStr['level_id'])
                        level_depth_no = str(userLevelRecordsStr['level_depth_no'])

                        level_id_list.append(level_id)

                    level_id_str = str(level_id_list).replace('[', '').replace(']', '')

                    condition = 'cid="' + cid + '" and is_leaf=1'
                    if int(level_depth_no) == 0:
                        if len(level_id_list) > 0:
                            condition += ' and level0 in (' + level_id_str + ') '
                    elif int(level_depth_no) == 1:
                        if len(level_id_list) > 0:
                            condition += ' and level1 in (' + level_id_str + ') '
                    elif int(level_depth_no) == 2:
                        if len(level_id_list) > 0:
                            condition += ' and level2 in (' + level_id_str + ') '

                    levelRecords = 'select level_id,level_name from sm_level where ' + condition + ' ;'
                    levelRecords = db.executesql(levelRecords, as_dict=True)
                    for j in range(len(levelRecords)):
                        levelRecordsStr = levelRecords[j]
                        level_id = str(levelRecordsStr['level_id'])
                        area_id_list.append(level_id)

                if len(area_id_list)>0:
                    area_id_str=str(area_id_list).replace('[','').replace(']','')

                    records = 'select `doc_id`, `doc_name`, `area_id`, `area_name`, `address` FROM `sm_doctor_area` where cid="' + cid + '" and area_id in ('+area_id_str+') and status="ACTIVE" order by doc_name;'
                    records = db.executesql(records, as_dict=True)

                    res_data = {'status': 'Success', 'doctorList': records}

    return dict(res_data=res_data)


def get_doctor_gift():
    response.view = 'generic.json'

    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass

    res_data = ''
    if cid == None:
        cid = ''
    if user_id == None:
        user_id = ''
    if password == None:
        password = ''

    if cid == '' or user_id == '' or password == '':
        res_data = {'status': 'Failed', 'ret_str': 'Required All'}
    else:
        userRecords = 'select rep_id,name,user_type from sm_rep where cid="' + cid + '" and rep_id="' + user_id + '" and password="' + password + '" and status="ACTIVE" limit 0,1;'
        userRecords = db.executesql(userRecords, as_dict=True)

        if len(userRecords) == 0:
            res_data = {'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            records = 'select `gift_id`,`gift_name` FROM `sm_doctor_gift` where cid="' + cid + '" and status="ACTIVE" order by gift_name;'
            records = db.executesql(records, as_dict=True)

            res_data = {'status': 'Success', 'giftList': records}

    return dict(res_data=res_data)


def get_doctor_sample():
    response.view = 'generic.json'

    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass

    res_data = ''
    if cid == None:
        cid = ''
    if user_id == None:
        user_id = ''
    if password == None:
        password = ''

    if cid == '' or user_id == '' or password == '':
        res_data = {'status': 'Failed', 'ret_str': 'Required All'}
    else:
        userRecords = 'select rep_id,name,user_type from sm_rep where cid="' + cid + '" and rep_id="' + user_id + '" and password="' + password + '" and status="ACTIVE" limit 0,1;'
        userRecords = db.executesql(userRecords, as_dict=True)

        if len(userRecords) == 0:
            res_data = {'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            records = 'select `item_id` as sample_id,`name` as sample_name FROM `sm_doctor_sample` where cid="' + cid + '" and status="ACTIVE" order by name;'
            records = db.executesql(records, as_dict=True)

            res_data = {'status': 'Success', 'sampleList': records}

    return dict(res_data=res_data)


def get_doctor_ppm():
    response.view = 'generic.json'

    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass

    res_data = ''
    if cid == None:
        cid = ''
    if user_id == None:
        user_id = ''
    if password == None:
        password = ''

    if cid == '' or user_id == '' or password == '':
        res_data = {'status': 'Failed', 'ret_str': 'Required All'}
    else:
        userRecords = 'select rep_id,name,user_type from sm_rep where cid="' + cid + '" and rep_id="' + user_id + '" and password="' + password + '" and status="ACTIVE" limit 0,1;'
        userRecords = db.executesql(userRecords, as_dict=True)

        if len(userRecords) == 0:
            res_data = {'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            records = 'select `gift_id` as ppm_id,`gift_name` as ppm_name FROM `sm_doctor_ppm` where cid="' + cid + '" and status="ACTIVE" order by gift_name;'
            records = db.executesql(records, as_dict=True)
            res_data = {'status': 'Success', 'ppmList': records}

    return dict(res_data=res_data)

