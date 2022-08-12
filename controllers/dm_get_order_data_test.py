
# .../?pass=aaaadddddaaa123123
def get_order_data():
    idList=[]
    orderHStr=''
    orderHeadList=''
    # SELECT * FROM sm_order_head WHERE ho_status = 0 AND order_datetime < ADDTIME(NOW(), '05:59:00') ORDER BY id ASC LIMIT 20
    records="SELECT id FROM sm_order_head WHERE ho_status = 0 AND order_datetime < ADDTIME(NOW(), '05:59:00') ORDER BY id ASC LIMIT 20"
    orderHRecords=db.executesql(records,as_dict=True)
  
    for i in range(len(orderHRecords)):  
        recStr=orderHRecords[i]
        id=recStr['id'] 
   
        idList.append(id)
  
        if orderHStr=='':
            orderHStr=str(id)
        else:
            orderHStr +='_'+str(id)
        orderHeadList=orderHStr  
    
#     orderDRecords="SELECT id, vsl, depot_id, depot_name, sl, store_id, store_name,client_id,client_name,rep_id,rep_name,market_id,market_name,order_datetime,delivery_date, collection_date,payment_mode,area_id,area_name,item_id,item_name,quantity, price, item_vat FROM sm_order WHERE vsl benlogs (idList)"
    orderDStr=''
    orderDetailsList=''
    orderDRecords=db(db.sm_order.vsl.belongs(idList)).select(db.sm_order_head.ordeorder_datetime)#,db.sm_order.deldelivery_date,db.sm_order.collecollection_date)
    return orderDRecords
    # orderDRecords=db(db.sm_order.vsl.belongs(idList)).select(db.sm_order.ALL)
    for row in orderDRecords:       
        id=str(row.id)
        vsl=str(row.vsl)
        depot_id=str(row.depot_id)
        depot_name=str(row.depot_name)
        sl=str(row.sl)
        store_id=str(row.store_id)
        store_name=str(row.cid)
        client_id=str(row.client_id)
        client_name=str(row.client_name)
        rep_id=str(row.rep_id)
        rep_name=str(row.rep_name)
        market_id=str(row.market_id)
        market_name=str(row.market_name)
        order_datetime=str(row.order_datetime)
        delivery_date=str(row.delivery_date)
        collection_date=str(row.collection_date)
        payment_mode=str(row.payment_mode)
        area_id=str(row.area_id)
        area_name=str(row.area_name)
        item_id=str(row.item_id)
        item_name=str(row.item_name)
        quantity=str(row.quantity)
        price=str(row.price)
        item_vat=str(row.item_vat)
        
        if orderDStr=='':
            orderDStr=id+'__'+vsl+'__'+depot_id+'__'+depot_name+'__'+sl+'__'+store_id+'__'+store_name+'__'+client_id+'__'+client_name+'__'+rep_id+'__'+rep_name+'__'+market_id+'__'+market_name+'__'+order_datetime+'__'+delivery_date+'__'+collection_date+'__'+payment_mode+'__'+area_id+'__'+area_name+'__'+item_id+'__'+item_name+'__'+quantity+'__'+price+'__'+item_vat
        else:
            orderDStr +='_R_'+id+'__'+vsl+'__'+depot_id+'__'+depot_name+'__'+sl+'__'+store_id+'__'+store_name+'__'+client_id+'__'+client_name+'__'+rep_id+'__'+rep_name+'__'+market_id+'__'+market_name+'__'+order_datetime+'__'+delivery_date+'__'+collection_date+'__'+payment_mode+'__'+area_id+'__'+area_name+'__'+item_id+'__'+item_name+'__'+quantity+'__'+price+'__'+item_vat
        orderDetailsList=orderDStr  
        
    return orderHeadList+'rdrd'+orderDetailsList


	
#http://a007.yeapps.com/ipi/dm_get_order_data/update_order_status/?ordersl=1_2_3_4_5_6_7_8_9_10
def update_order_status():
	order_sl_list = str(request.vars.ordersl).strip().upper()
	order_sl_list= order_sl_list.replace('_',',')
	strSQL = 'update sm_order_head set ho_status = 1 where id in (' + order_sl_list +')'
	#return strSQL
	db.executesql(strSQL)
	return 'Success'
