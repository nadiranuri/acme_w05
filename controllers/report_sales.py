# ===========================Data for access report
# http://127.0.0.1:8000/skf/report_sales/acreportData?c_id=SKF&dateFrom=2016-06-01&dateTo=2016-06-05&branch=
# http://c003.cloudapp.net/skf/report_sales/acreportData?c_id=SKF&dateFrom=2016-06-01&dateTo=2016-06-05&branch=170
# Region|Area|Territory|Market|Product ID | Product Name| TP| Stock| Catetory A/B/C| Qty
def acreportData():
    c_id=request.vars.c_id
    dateFrom=request.vars.dateFrom
    dateTo=request.vars.dateTo
    branch=request.vars.branch
    dateFlag=True
    try:
        dateFrom=datetime.datetime.strptime(str(dateFrom),'%Y-%m-%d')
        dateTo=datetime.datetime.strptime(str(dateTo),'%Y-%m-%d')
        date_to_m=dateTo + datetime.timedelta(days = 1)
        if dateFrom > dateTo :
            dateFlag=False
    except:
        dateFlag=False
     
    if dateFlag==False:
        return "Invalid Date"
    
    
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.cid==db.sm_invoice.cid)
    qset=qset(db.sm_depot_stock_balance.cid==db.sm_invoice.cid)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_invoice.item_id)
    qset=qset(db.sm_depot_stock_balance.batch_id==db.sm_invoice.batch_id)
    qset=qset(db.sm_invoice.status=='Invoiced')    
    qset=qset((sm_invoice.invoice_date >= dateFrom) & (sm_invoice.invoice_date < date_to_m))
    qset=qset(db.sm_invoice.depot_id==branch)
    
    records=qset.select(db.sm_invoice.level2_id,db.sm_invoice.level2_name,db.sm_invoice.level1_id,db.sm_invoice.level1_name,db.sm_invoice.level0_id,db.sm_invoice.level0_name,db.sm_invoice.market_id,db.sm_invoice.market_name, db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp, db.sm_invoice.category_id,db.sm_invoice.batch_id,db.sm_depot_stock_balance.quantity,db.sm_invoice.quantity.sum(), groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.market_id|db.sm_invoice.item_id|db.sm_invoice.batch_id, orderby= db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.market_id|db.sm_invoice.item_id|db.sm_invoice.batch_id)
#     return db._lastsql
    report_str=''
    for record in records:
        region=record[db.sm_invoice.level1_id]
        region_name=record[db.sm_invoice.level1_name]
        area=record[db.sm_invoice.level2_id]
        area_name=record[db.sm_invoice.level2_name]
        territory=record[db.sm_invoice.level3_id]
        territory_name=record[db.sm_invoice.level3_name]
        market=record[db.sm_invoice.market_id]
        market_name=record[db.sm_invoice.market_name]
        item=record[db.sm_invoice.item_id]
        item_name=record[db.sm_invoice.item_name]
        item_batch=record[db.sm_invoice.batch_id]
        tP=record[db.sm_invoice.actual_tp]
        catetory=record[db.sm_invoice.category_id]
        qty=record[db.sm_invoice.quantity.sum()]
        stock=record[db.sm_depot_stock_balance.quantity]
        if report_str=='':
            report_str=str(region)+'|'+str(region_name)+'|'+str(area)+str(area_name)+'|'+str(territory)+'|'+str(territory_name)+'|'+str(market)+'|'+str(market_name)+'|'+str(item)+'|'+str(item_name)+'|'+str(item_batch)+'|'+str(tP)+'|'+str(stock)+'|'+str(catetory)+'|'+str(qty)

        else:
            report_str=report_str+'<rdrd>'+str(region)+'|'+str(region_name)+'|'+str(area)+str(area_name)+'|'+str(territory)+'|'+str(territory_name)+'|'+str(market)+'|'+str(market_name)+'|'+str(item)+'|'+str(item_name)+'|'+str(item_batch)+'|'+str(tP)+'|'+str(stock)+'|'+str(catetory)+'|'+str(qty)

        
        
        
        


    return report_str




#======================= Report Home
def reports_home():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','home'))
    if int(session.setting_repot)!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Reports'
    #------------
#     session.s_textCteam=''
#     session.s_text=''
    btn_ledger_report=request.vars.btn_ledger_report
    btn_stock_report=request.vars.btn_stock_report
    btn_show_subdepot=request.vars.btn_show_subdepot
        
    #---------------------
    if btn_ledger_report:
        redirect(URL(c='utility',f='reports_home'))                
    elif btn_stock_report:
        redirect(URL(c='report_menu',f='report_home'))  
    elif btn_show_subdepot:
        redirect(URL(c='depot',f='sub_depot_list')) 
    else:
        return dict()
    #--------------
    

def home():
#    task_id='rm_analysis_view'
#    access_permission=check_role(task_id)
#    if (access_permission==False ):
#        session.flash='Access is Denied'
#        redirect (URL('default','home'))
    
    response.title='Report'
    
    c_id=session.cid
    
    search_form =SQLFORM(db.sm_search_date)
    
    
#    =============Sales btn Start Nadira===========
    btn_list_sales=request.vars.btn_list_sales
    btn_customer_wise_sales=request.vars.btn_customer_wise_sales
    btn_item_wise_batch_sales=request.vars.btn_item_wise_batch_sales
    btn_item_wise_sales=request.vars.btn_item_wise_sales
    btn_msowiseS=request.vars.btn_msowiseS
    btn_msowiseSDLoad=request.vars.btn_msowiseSDLoad

    
    btn_catMSOwiseS=request.vars.btn_catMSOwiseS
    btn_catDPwiseS=request.vars.btn_catDPwiseS
    btn_catDPwiseSD=request.vars.btn_catDPwiseSD
    btn_dpwiseSD=request.vars.btn_dpwiseSD
    btn_dpwiseSDD=request.vars.btn_dpwiseSDD
    btn_customerProductS=request.vars.btn_customerProductS
    btn_customerProductSD=request.vars.btn_customerProductSD
    btn_productS=request.vars.btn_productS
    btn_productSD=request.vars.btn_productSD
    btn_productSwithoutBonus=request.vars.btn_productSwithoutBonus
    btn_productSwithoutBonusD=request.vars.btn_productSwithoutBonusD
    
   
    btn_customerProductSIncludinBonus=request.vars.btn_customerProductSIncludinBonus
    btn_customerProductSIncludinBonusD=request.vars.btn_customerProductSIncludinBonusD
    
    btn_customerProductSExcludinBonus=request.vars.btn_customerProductSExcludinBonus
    btn_customerProductSExcludinBonusD=request.vars.btn_customerProductSExcludinBonusD
    
    btn_customerInvoiceProductS=request.vars.btn_customerInvoiceProductS
    btn_customerInvoiceProductSwithBonus=request.vars.btn_customerInvoiceProductSwithBonus
    btn_customerInvoiceProductSwithoutBonus=request.vars.btn_customerInvoiceProductSwithoutBonus
    btn_customerInvoiceProductSD=request.vars.btn_customerInvoiceProductSD
    btn_customerInvoiceProductSwithBonusD=request.vars.btn_customerInvoiceProductSwithBonusD
    btn_customerInvoiceProductSwithoutBonusD=request.vars.btn_customerInvoiceProductSwithoutBonusD
    
    
    
    btn_productInvoicewiseSD=request.vars.btn_productInvoicewiseSD 
    btn_productInvoicewiseSDwithBonus=request.vars.btn_productInvoicewiseSDwithBonus
    btn_productInvoicewiseSDwithoutBonus=request.vars.btn_productInvoicewiseSDwithoutBonus
    
    btn_productInvoicewiseSDD=request.vars.btn_productInvoicewiseSDD 
    btn_productInvoicewiseSDwithBonusD=request.vars.btn_productInvoicewiseSDwithBonusD
    btn_productInvoicewiseSDwithoutBonusD=request.vars.btn_productInvoicewiseSDwithoutBonusD
    
    
    btn_invoicewiseSD=request.vars.btn_invoicewiseSD
    btn_invoicewiseSDLoad=request.vars.btn_invoicewiseSDLoad
    
    btn_summary=request.vars.btn_summary
    btn_summaryD=request.vars.btn_summaryD
    
    btn_SalesClosingStockS=request.vars.btn_SalesClosingStockS
    btn_SalesClosingStockSD=request.vars.btn_SalesClosingStockSD
    btn_SalesClosingStockSB=request.vars.btn_SalesClosingStockSB
    btn_SalesClosingStockSBD=request.vars.btn_SalesClosingStockSBD
    
    btn_discPWise=request.vars.btn_discPWise
    btn_discPWiseD=request.vars.btn_discPWiseD
#    ============Order=========================
# Nadira
    btn_list_oderdetail=request.vars.btn_list_oderdetail
    btn_list_oderdSummary_spowise=request.vars.btn_list_oderdSummary_spowise
    btn_list_oderdSummary_spowiseDdate=request.vars.btn_list_oderdSummary_spowiseDdate
    btn_item_wise_sales_sheet=request.vars.btn_item_wise_sales_sheet
    
    btn_list_oderdSummary_Ddate=request.vars.btn_list_oderdSummary_Ddate
#   ===  
    
    btn_item_wise_sale_detail=request.vars.btn_item_wise_sale_detail
    btn_item_wise_sale_detail_land=request.vars.btn_item_wise_sale_detail_land
    btn_invoice_wise_sale_detail=request.vars.btn_invoice_wise_sale_detail
    btn_invoice_wise_sale_detailD=request.vars.btn_invoice_wise_sale_detailD
    
    
    
    
    btn_customer_wise_sale_detail=request.vars.btn_customer_wise_sale_detail
    btn_customer_wise_sale_detailP=request.vars.btn_customer_wise_sale_detailP
    btn_customer_wise_sale_detailPD=request.vars.btn_customer_wise_sale_detailPD
    
    btn_mso_wise_sale_detail=request.vars.btn_mso_wise_sale_detail
    btn_mso_wise_sale_detailD=request.vars.btn_mso_wise_sale_detailD
    
    btn_dp_wise_sale_detail=request.vars.btn_dp_wise_sale_detail
    btn_dp_wise_sale_detailD=request.vars.btn_dp_wise_sale_detailD
    
    
                                       
    btn_customer_nformation=request.vars.btn_customer_nformation
    btn_customer_nformationD=request.vars.btn_customer_nformationD
    
    
    btn_item_wise_sale_detailDLoad=request.vars.btn_item_wise_sale_detailDLoad
    
    btn_causeofrtn=request.vars.btn_causeofrtn
    btn_causeofrtnDLoad=request.vars.btn_causeofrtnDLoad
    
    btn_DP_wise_sale_ss=request.vars.btn_DP_wise_sale_ss
    btn_DP_wise_sale_ssD=request.vars.btn_DP_wise_sale_ssD
    
    
#     =====================Periodic
    btn_item_wise_sale_detailPeriodic=request.vars.btn_item_wise_sale_detailPeriodic
    btn_item_wise_sale_detailPeriodicDLoad=request.vars.btn_item_wise_sale_detailPeriodicDLoad
    
    btn_mso_wise_sale_detailPeriodic=request.vars.btn_mso_wise_sale_detailPeriodic
    btn_mso_wise_sale_detail_periodicDLoad=request.vars.btn_mso_wise_sale_detail_periodicDLoad
    
    btn_dp_wise_sale_detailPeriodic=request.vars.btn_dp_wise_sale_detailPeriodic
    btn_dp_wise_sale_detail_periodicDLoad=request.vars.btn_dp_wise_sale_detail_periodicDLoad
    
    btn_DP_wise_sale_ss_periodic=request.vars.btn_DP_wise_sale_ss_periodic
    btn_DP_wise_sale_ssD_periodic=request.vars.btn_DP_wise_sale_ssD_periodic
    
    btn_catDPwiseSPeriodic=request.vars.btn_catDPwiseSPeriodic
    btn_catDPwiseSDPeriodic=request.vars.btn_catDPwiseSDPeriodic
    
    btn_msowiseSP=request.vars.btn_msowiseSP
    btn_msowiseSDP=request.vars.btn_msowiseSDP
    
    btn_summaryP=request.vars.btn_summaryP
    btn_summaryPD=request.vars.btn_summaryPD
    
    btn_causeofrtnP=request.vars.btn_causeofrtnP
    btn_causeofrtnPDLoad=request.vars.btn_causeofrtnPDLoad
    
    btn_discPWiseP=request.vars.btn_discPWiseP
    btn_discPWisePD=request.vars.btn_discPWisePD 
    
    btn_SalesClosingStockSBP=request.vars.btn_SalesClosingStockSBP
    btn_SalesClosingStockSBPD=request.vars.btn_SalesClosingStockSBPD
    
    btn_customerInvoiceProductSP=request.vars.btn_customerInvoiceProductSP
    btn_customerInvoiceProductSPD=request.vars.btn_customerInvoiceProductSPD
    
    
    
    btn_sComparision=request.vars.btn_sComparision
    btn_sComparisionD=request.vars.btn_sComparisionD
    
    
    
#     Sales Comparision========================
    btn_salesComparisionNational=request.vars.btn_salesComparisionNational
    btn_salesComparisionNationalD=request.vars.btn_salesComparisionNationalD
    btn_salesComparisionRsm=request.vars.btn_salesComparisionRsm
    btn_salesComparisionRsmD=request.vars.btn_salesComparisionRsmD
    btn_salesComparisionFm=request.vars.btn_salesComparisionFm
    btn_salesComparisionFmD=request.vars.btn_salesComparisionFmD
    btn_salesComparisionTr=request.vars.btn_salesComparisionTr
    btn_salesComparisionTrD=request.vars.btn_salesComparisionTrD
    
    btn_salesComparisionTrDetail=request.vars.btn_salesComparisionTrDetail
    btn_salesComparisionTrDetailD=request.vars.btn_salesComparisionTrDetailD
    btn_salesComparisionFmDetail=request.vars.btn_salesComparisionFmDetail
    btn_salesComparisionFmDetailD=request.vars.btn_salesComparisionFmDetailD
    btn_salesComparisionRsmDetail=request.vars.btn_salesComparisionRsmDetail
    btn_salesComparisionRsmDetailD=request.vars.btn_salesComparisionRsmDetailD
    btn_salesComparisionMarketDetail=request.vars.btn_salesComparisionMarketDetail
    
    
    btn_salesComparisionTRDLoad=request.vars.btn_salesComparisionTRDLoad
    btn_salesComparisionTRDLoadAB=request.vars.btn_salesComparisionTRDLoadAB
    
    btn_salesComparisionTRDLoadInvoice=request.vars.btn_salesComparisionTRDLoadInvoice
    btn_salesComparisionTRDLoadInvoicePeriodicProcess=request.vars.btn_salesComparisionTRDLoadInvoicePeriodicProcess
    btn_salesComparisionTRDLoadInvoicePeriodic=request.vars.btn_salesComparisionTRDLoadInvoicePeriodic
    btn_salesComparisionTRDLExCInvoicePeriodic=request.vars.btn_salesComparisionTRDLExCInvoicePeriodic
    
    
    
    
    
    btn_salesComparisionFMDLoad=request.vars.btn_salesComparisionFMDLoad
    btn_salesComparisionFMDLoadAB=request.vars.btn_salesComparisionFMDLoadAB
    
    btn_salesComparisionTRDLoadCteam=request.vars.btn_salesComparisionTRDLoadCteam
    btn_salesComparisionTRDLoadCteamPeriodic=request.vars.btn_salesComparisionTRDLoadCteamPeriodic
    
    
    btn_salesComparisionFMDLoadCteam=request.vars.btn_salesComparisionFMDLoadCteam
    
    
    btn_salesComparisionTRDLoadABCteam=request.vars.btn_salesComparisionTRDLoadABCteam
#     btn_salesComparisionNationalCteam=request.vars.btn_salesComparisionNationalCteam
#     btn_salesComparisionNationalCteamD=request.vars.btn_salesComparisionNationalCteamD
    btn_salesComparisionRsmCteam=request.vars.btn_salesComparisionRsmCteam
    
    btn_salesComparisionRsmCteamD=request.vars.btn_salesComparisionRsmCteamD
    btn_salesComparisionRsmDetailCteam=request.vars.btn_salesComparisionRsmDetailCteam
    btn_salesComparisionRsmDetailCteamD=request.vars.btn_salesComparisionRsmDetailCteamD
    btn_salesComparisionFmCteam=request.vars.btn_salesComparisionFmCteam
    btn_salesComparisionFmCteamD=request.vars.btn_salesComparisionFmCteamD
    btn_salesComparisionFmDetailCteam=request.vars.btn_salesComparisionFmDetailCteam
    btn_salesComparisionFmDetailCteamD=request.vars.btn_salesComparisionFmDetailCteamD
    btn_salesComparisionTrCteam=request.vars.btn_salesComparisionTrCteam
    btn_salesComparisionTrCteamD=request.vars.btn_salesComparisionTrCteamD
    btn_salesComparisionTrDetailCteam=request.vars.btn_salesComparisionTrDetailCteam
    btn_salesComparisionTrDetailCteamD=request.vars.btn_salesComparisionTrDetailCteamD
    btn_salesComparisionMarketDetailCteam=request.vars.btn_salesComparisionMarketDetailCteam
    btn_salesComparisionMarketDetailCteam=request.vars.btn_salesComparisionMarketDetailCteam
    
    
    btn_salesComparisionTRDLoadInvoicePeriodicCteamProcess=request.vars.btn_salesComparisionTRDLoadInvoicePeriodicCteamProcess
#     =======================================
    
    btn_dp_wise_order_summary=request.vars.btn_dp_wise_order_summary
    
#     return btn_causeofrtn
    #     ================================================Sales Nadira==========================================================================================
#     Nadira 
    
    if (btn_list_sales or btn_customer_wise_sales or btn_item_wise_batch_sales or btn_item_wise_sales or btn_list_oderdetail or btn_list_oderdSummary_spowise or btn_list_oderdSummary_spowiseDdate or btn_list_oderdSummary_Ddate or btn_item_wise_sale_detail or btn_item_wise_sale_detailDLoad or btn_item_wise_sale_detail_land or btn_invoice_wise_sale_detail or btn_invoice_wise_sale_detailD or btn_customer_wise_sale_detail or btn_customer_wise_sale_detailP or btn_customer_wise_sale_detailPD or btn_mso_wise_sale_detail or btn_mso_wise_sale_detailD or btn_dp_wise_sale_detail or btn_dp_wise_sale_detailD or btn_customer_nformation or btn_customer_nformationD or btn_customerProductS or btn_customerProductSD or btn_msowiseS or btn_msowiseSDLoad or btn_catMSOwiseS or btn_catDPwiseS or btn_catDPwiseSD or btn_productS or btn_productSD or btn_productSwithoutBonus or btn_productSwithoutBonusD or btn_customerProductSIncludinBonus or btn_customerProductSIncludinBonusD or btn_customerProductSExcludinBonus or btn_customerProductSExcludinBonusD or btn_dpwiseSD or btn_dpwiseSDD or btn_customerInvoiceProductS or btn_customerInvoiceProductSD or btn_customerInvoiceProductSwithBonus or btn_customerInvoiceProductSwithBonusD or btn_customerInvoiceProductSwithoutBonus or btn_customerInvoiceProductSwithoutBonusD or btn_productInvoicewiseSD or btn_productInvoicewiseSDwithBonus or btn_productInvoicewiseSDwithoutBonus or btn_productInvoicewiseSDD or btn_productInvoicewiseSDwithBonusD or btn_productInvoicewiseSDwithoutBonusD or btn_invoicewiseSD or btn_invoicewiseSDLoad or btn_summary or btn_causeofrtn or btn_causeofrtnDLoad or btn_DP_wise_sale_ss or btn_DP_wise_sale_ssD or btn_summaryD or btn_SalesClosingStockS or btn_SalesClosingStockSD or btn_SalesClosingStockSB or btn_SalesClosingStockSBD or btn_sComparision or btn_sComparisionD or btn_discPWise or btn_discPWiseD or btn_item_wise_sale_detailPeriodic or btn_item_wise_sale_detailPeriodicDLoad or btn_mso_wise_sale_detailPeriodic or btn_mso_wise_sale_detail_periodicDLoad or btn_dp_wise_sale_detailPeriodic or btn_dp_wise_sale_detail_periodicDLoad or btn_DP_wise_sale_ss_periodic or btn_DP_wise_sale_ssD_periodic or btn_catDPwiseSPeriodic or btn_catDPwiseSDPeriodic or btn_msowiseSP or btn_msowiseSDP or btn_summaryP or btn_summaryPD or btn_causeofrtnP or btn_causeofrtnPDLoad or btn_discPWiseP or btn_discPWisePD or btn_SalesClosingStockSBP or btn_SalesClosingStockSBPD or btn_customerInvoiceProductSP or btn_customerInvoiceProductSPD):
          
          date_from=request.vars.from_dt_2
          date_to=request.vars.to_dt_2
          
          depot=str(request.vars.sales_depot_id_sales)
          store=str(request.vars.store_id_sales)
          
          customer=str(request.vars.customer_id_sales)
          customerCat=str(request.vars.customer_category)
          customerCatSub=str(request.vars.customer_categorySub)
          customer_market=str(request.vars.customer_market)
          dman=str(request.vars.dman_id_sales)
          teritory=str(request.vars.t_id_sales)
          mso=str(request.vars.mso_id_sales)
          status=str(request.vars.status_sales)
          selesTerm=str(request.vars.selesTerm)
          
          itemSales=str(request.vars.itemSales)
          rsm_Sales=str(request.vars.rsm_Sales)
          fm_Sales=str(request.vars.fm_Sales)
          
          depot_id=depot
          store_id=store
          customer_id=customer
          dman_id=dman
          teritory=teritory
          mso_id=mso
          
          customerCat_id=customerCat
          
          depot_name=''
          store_name=''
          customer_name=''
          dman_name=''
          mso_name=''
          teritory_name=''
          customerCat_name=''
          dateFlag=True
          try:
              from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
              to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 

              if from_dt2>to_dt2:
                  dateFlag=False
          except:
              dateFlag=False
        
          if dateFlag==False:
              response.flash="Invalid Date Range"
          else:            
            dateDiff=(to_dt2-from_dt2).days
            if dateDiff>90:
                response.flash="Maximum 90 days allowed between Date Range"
            else:                    
              if ((depot!='') & (depot.find('|') != -1)):             
                  depot_id=depot.split('|')[0].upper().strip()
                  depot_name=depot.split('|')[1].strip()
                  user_depot_address=''
                  if session.user_type!='Depot': 
                      depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                      if depotRows:
                          user_depot_address=depotRows[0].field1         
                          session.user_depot_address=user_depot_address
#               return btn_summary
              if ((depot=='') | (store_id=='')) & (btn_summary==None) & (btn_summaryD==None) & (btn_sComparision==None) & (btn_sComparisionD==None):
                  session.flash="Required Branch and Store"
                  redirect(URL(c='report_sales',f='home')) 
                  
              else:
                  if ((store!='') & (store.find('|') != -1)) : 
                      store_id=store.split('|')[0].upper().strip()
                      store_name=store.split('|')[1].strip()
                  else:
                      store_id=store_id
                      store_name=''
                  if ((customer!='') & (customer.find('|') != -1)) :       
                      customer_id=customer.split('|')[0].upper().strip()
                      customer_name=customer.split('|')[1].strip()
                  else:
                      customer_id=customer_id
                      customer_name=''
                  
                  if ((itemSales!='') & (itemSales.find('|') != -1)) :       
                      item_id=itemSales.split('|')[0].upper().strip()
                      item_name=itemSales.split('|')[1].strip()
                  else:
                      item_id=itemSales
                      item_name=''
                  if ((rsm_Sales!='') & (rsm_Sales.find('|') != -1)) :       
                      rsm_id=rsm_Sales.split('|')[0].upper().strip()
                      rsm_name=rsm_Sales.split('|')[1].strip()
                  else:
                      rsm_id=rsm_Sales
                      rsm_name=''
                  if ((fm_Sales!='') & (fm_Sales.find('|') != -1)) :       
                      fm_id=fm_Sales.split('|')[0].upper().strip()
                      fm_name=fm_Sales.split('|')[1].strip()
                  else:
                      fm_id=fm_Sales
                      fm_name=''
                  
                  
                  if ((customerCat!='') & (customerCat.find('|') != -1)) :       
                      customerCat_id=customerCat.split('|')[0].upper().strip()
                      customerCat_name=customerCat.split('|')[1].strip()
                  else:
                      customerCat_id=customer_id
                      customerCat_name=''
                  if ((customerCatSub!='') & (customerCatSub.find('|') != -1)) :       
                      customerCat_idSub=customerCatSub.split('|')[0].upper().strip()
                      customerCat_nameSub=customerCatSub.split('|')[1].strip()
                  else:
                      customerCat_idSub=customer_id
                      customerCat_nameSub=''    
                  
                  if ((dman!='') & (dman.find('|') != -1)) :     
                      dman_id=dman.split('|')[0].upper().strip()
                      dman_name=dman.split('|')[1].strip()
                  else:
                      dman_id=dman_id
                      dman_name=''
                  
                  if ((teritory!='') & (teritory.find('|') != -1)) :    
                      teritory_id=teritory.split('|')[0].upper().strip()
                      teritory_name=teritory.split('|')[1].strip()
                  else:
                      teritory_id=teritory
                      teritory_name=''
                      
                  if ((mso!='') & (mso.find('|') != -1)) :    
                      mso_id=mso.split('|')[0].upper().strip()
                      mso_name=mso.split('|')[1].strip()
                  else:
                      mso_id=mso
                      mso_name=''
                  if ((customer_market!='') & (customer_market.find('|') != -1)) :    
                      market_id=customer_market.split('|')[0].upper().strip()
                      market_name=customer_market.split('|')[1].strip()
                  else:
                      market_id=customer_market
                      market_name=''   
                      
                      
        #          return btn_list_sales
                  if btn_list_sales:
                        redirect (URL('list_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_customer_wise_sales:
                        redirect (URL('list_sales_customer_wise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_item_wise_batch_sales:
                        redirect (URL('list_item_wise_batch_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_item_wise_sales:
                        redirect (URL('list_item_wise_sales',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,dman_id=dman_id,dman_name=dman_name,mso_id=mso_id,mso_name=mso_name,status=status)))
                  if btn_list_oderdetail:
                        redirect (URL('list_oderdetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_list_oderdSummary_spowise:
                        redirect (URL('list_oderderSumRepWise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_list_oderdSummary_spowiseDdate:
                        redirect (URL('list_oderderSumRepWiseDdate',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_list_oderdSummary_Ddate:
                        redirect (URL('list_oderdSummary_Ddate',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))  
    #               if btn_item_wise_sales_sheet:
    #                     redirect (URL('oderSheet',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_item_wise_sale_detail:
                        redirect (URL('itemWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_item_wise_sale_detailDLoad:
                        redirect (URL('itemWiseSalesSDetailDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                      
                  if btn_item_wise_sale_detail_land:
                        redirect (URL('itemWiseSalesSDetailLand',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_invoice_wise_sale_detail:
                        redirect (URL('invoiceWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name,dman_id=dman_id)))
                  if btn_invoice_wise_sale_detailD:
                        redirect (URL('invoiceWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_customer_wise_sale_detail:
                        redirect (URL('customerWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name,selesTerm=selesTerm)))
                  if btn_customer_wise_sale_detailP:
                        redirect (URL('customerWiseSalesSDetailP',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name,selesTerm=selesTerm)))
                  if btn_customer_wise_sale_detailPD:
                        redirect (URL('customerWiseSalesSDetailPD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name,selesTerm=selesTerm)))
                  if btn_mso_wise_sale_detail:
                        redirect (URL('msoWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_mso_wise_sale_detailD:
                        redirect (URL('msoWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_dp_wise_sale_detail:
                        redirect (URL('dpWiseSalesSDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dp_wise_sale_detailD:
                        redirect (URL('dpWiseSalesSDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,mso_id=mso_id,teritory_id=teritory_id,teritory_name=teritory_name,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  
                  if btn_customer_nformation:
                        redirect (URL('customrInformation',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_customer_nformationD:
                        redirect (URL('customrInformationDownload',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  
                  if btn_msowiseS:  
                        redirect (URL('msowiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,customerCat_id=customerCat_id,customerCat_name=customerCat_name,customerCat_idSub=customerCat_idSub,customerCat_nameSub=customerCat_nameSub)))
                  if btn_msowiseSDLoad:  
                        redirect (URL('msowiseSDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,customerCat_id=customerCat_id,customerCat_name=customerCat_name,customerCat_idSub=customerCat_idSub,customerCat_nameSub=customerCat_nameSub)))
                  if btn_catMSOwiseS:
                        redirect (URL('catMSOwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_catDPwiseS:
                        redirect (URL('catDPwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name)))
                  if btn_catDPwiseSD:
                        redirect (URL('catDPwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dpwiseSD:
                       redirect (URL('dpwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_dpwiseSDD:
                       redirect (URL('dpwiseSDD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,customerCat_id=customerCat_id, customerCat_name=customerCat_name, dman_id=dman_id,dman_name=dman_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))        
                  if btn_customerProductS:
                        redirect (URL('customrProductwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerProductSD:
                        redirect (URL('customrProductwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))      
                  if btn_productS:
                      redirect (URL('productwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productSD:
                      redirect (URL('productwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productSwithoutBonus:
                      redirect (URL('productwiseSwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productSwithoutBonusD:
                      redirect (URL('productwiseSwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerProductSIncludinBonus:
                        redirect (URL('customrProductwiseSIncludingBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerProductSIncludinBonusD:
                        redirect (URL('customrProductwiseSIncludingBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerProductSExcludinBonus:
                       redirect (URL('customrProductwiseSExcludingBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerProductSExcludinBonusD:
                       redirect (URL('customrProductwiseSExcludingBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductS:
                       redirect (URL('customrInvoiceProductwiseS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSD:
                       redirect (URL('customrInvoiceProductwiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSwithBonus:
                        redirect (URL('customrInvoiceProductwiseSwithBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSwithBonusD:
                        redirect (URL('customrInvoiceProductwiseSwithBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSwithoutBonus:
                        redirect (URL('customrInvoiceProductwiseSwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSwithoutBonusD:
                        redirect (URL('customrInvoiceProductwiseSwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productInvoicewiseSD:
                        redirect (URL('productInvoicewiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productInvoicewiseSDD:
                        redirect (URL('productInvoicewiseSDD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))        
                  if btn_productInvoicewiseSDwithBonus:
                        redirect (URL('productInvoicewiseSDwithBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_productInvoicewiseSDwithBonusD:
                        redirect (URL('productInvoicewiseSDwithBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_productInvoicewiseSDwithoutBonus:
                        redirect (URL('productInvoicewiseSDwithoutBonus',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))

                  if btn_productInvoicewiseSDwithoutBonusD:
                        redirect (URL('productInvoicewiseSDwithoutBonusD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  
                  if btn_summary:
                        redirect (URL('summaryReport',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_summaryD:
                        redirect (URL('summaryReportD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                                  
                  if btn_invoicewiseSD:
                        redirect (URL('invoicewiseSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_invoicewiseSDLoad:
                        redirect (URL('invoicewiseSDLoad',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                                        
                  if btn_causeofrtn:
                        redirect (URL('causeofRet',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                  if btn_causeofrtnDLoad:
                        redirect (URL('causeofRetD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,market_id=market_id,market_name=market_name)))
                                            
                  if btn_DP_wise_sale_ss:
                        redirect (URL('dp_wise_sale_ss',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_DP_wise_sale_ssD:
                        redirect (URL('dp_wise_sale_ssD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockS:   
                        redirect (URL('salesClosingStockS',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockSD:   
                        redirect (URL('salesClosingStockSD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))  
                  if btn_SalesClosingStockSB:   
                        redirect (URL('salesClosingStockSB',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_SalesClosingStockSBD:   
                        redirect (URL('salesClosingStockSBD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_sComparision:
                        redirect (URL('msoSCTop',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_sComparisionD:
                        redirect (URL('msoSCTopD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name)))
                  if btn_discPWise:
                        redirect (URL('discPWise',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_discPWiseD:
                        redirect (URL('discPWiseD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                   
                  if btn_item_wise_sale_detailPeriodic:
                        redirect (URL('itemWiseSalesSDetailPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_item_wise_sale_detailPeriodicDLoad:
                        redirect (URL('itemWiseSalesSDetailDLoadPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_mso_wise_sale_detailPeriodic:
                        redirect (URL('msoWiseSalesSDetailPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_mso_wise_sale_detail_periodicDLoad:
                        redirect (URL('msoWiseSalesSDetailDLoadPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_dp_wise_sale_detailPeriodic:
                        redirect (URL('dpWiseSalesSDetailPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_dp_wise_sale_detail_periodicDLoad:
                        redirect (URL('dpWiseSalesSDetailDLoadPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_DP_wise_sale_ss_periodic:
                        redirect (URL('dp_wise_sale_ss_periodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_DP_wise_sale_ssD_periodic:
                        redirect (URL('dp_wise_sale_ss_d_periodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_catDPwiseSPeriodic:
                        redirect (URL('catDPwiseSPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_catDPwiseSDPeriodic:
                        redirect (URL('catDPwiseSDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_msowiseSP:
                        redirect (URL('msowiseSPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_msowiseSDP:
                        redirect (URL('msowiseSDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_summaryP:
                        redirect (URL('summaryReportPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_summaryPD:
                        redirect (URL('summaryReportDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_causeofrtnP:
                        redirect (URL('causeofRetPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_causeofrtnPDLoad:
                        redirect (URL('causeofRetDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_discPWiseP:
                        redirect (URL('discPWisePeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_discPWisePD:
                        redirect (URL('discPWiseDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_SalesClosingStockSBP:
                        redirect (URL('salesClosingStockSBPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_SalesClosingStockSBPD:
                        redirect (URL('salesClosingStockSBDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  
                  if btn_customerInvoiceProductSP:
                        redirect (URL('customrInvoiceProductwiseSPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                  if btn_customerInvoiceProductSPD:
                        redirect (URL('customrInvoiceProductwiseSDPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,dman_id=dman_id,dman_name=dman_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)))
                 
                
         #     ================================================Sales End Nadira==========================================================================================                     
#     if (btn_salesComparisionNational or btn_salesComparisionRsm or btn_salesComparisionFm or btn_salesComparisionTr or btn_salesComparisionTrDetail  or btn_salesComparisionNationalD or btn_salesComparisionRsmD or btn_salesComparisionFmD or btn_salesComparisionTrD or btn_salesComparisionTrDetail or btn_salesComparisionTrDetailD or btn_salesComparisionFmDetail or btn_salesComparisionFmDetailD or btn_salesComparisionRsmDetail or btn_salesComparisionRsmDetailD or btn_salesComparisionMarketDetail or btn_salesComparisionTRDLoad or btn_salesComparisionTRDLoadAB or btn_salesComparisionFMDLoad or btn_salesComparisionFMDLoadAB or btn_salesComparisionTRDLoadInvoice or btn_salesComparisionTRDLoadInvoicePeriodic or btn_salesComparisionTRDLExCInvoicePeriodic or btn_salesComparisionTRDLoadInvoicePeriodicProcess):
#           date_from=request.vars.from_dt_3
#           date_to=request.vars.to_dt_3
#
#           depot=str(request.vars.sales_depot_id_SC)
#           store=str(request.vars.store_id_SC)
#
#           rsm_SC=str(request.vars.rsm_SC)
#           fm_SC=str(request.vars.fm_SC)
#           tr_SC=str(request.vars.tr_SC)
#           product=str(request.vars.product)
#
#           depot_id=depot
#           store_id=store
#
#           depot_name=''
#           store_name=''
#
#           dateFlag=True
# #           return 'asfsaf'
#           try:
#               from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
#           except:
#               dateFlag=False
#
#
#           if ((depot!='') & (depot.find('|') != -1)):
#               depot_id=depot.split('|')[0].upper().strip()
#               depot_name=depot.split('|')[1].strip()
#
#           else:
#               depot_id=depot
#               depot_name=''
#
#           if ((store!='') & (store.find('|') != -1)) :
#               store_id=store.split('|')[0].upper().strip()
#               store_name=store.split('|')[1].strip()
#           else:
#               store_id=store_id
#               store_name=''
#
#           if ((rsm_SC!='') & (rsm_SC.find('|') != -1)) :
#               rsm_id=rsm_SC.split('|')[0].upper().strip()
#               rsm_name=rsm_SC.split('|')[1].strip()
#
#           else:
#               rsm_id=rsm_SC
#               rsm_name=''
#           if ((fm_SC!='') & (fm_SC.find('|') != -1)) :
#               fm_id=fm_SC.split('|')[0].upper().strip()
#               fm_name=fm_SC.split('|')[1].strip()
#           else:
#               fm_id=fm_SC
#               fm_name=''
#
#           if ((product!='') & (product.find('|') != -1)) :
#               product_id=product.split('|')[0].upper().strip()
#               product_name=product.split('|')[1].strip()
#           else:
#               product_id=product
#               product_name=''
#
#           if ((tr_SC!='') & (tr_SC.find('|') != -1)) :
#               tr_id=tr_SC.split('|')[0].upper().strip()
#               tr_name=tr_SC.split('|')[1].strip()
#           else:
#               tr_id=tr_SC
#               tr_name=''
#           if ((depot!='') & (depot.find('|') != -1)):
#                   depot_id=depot.split('|')[0].upper().strip()
#                   depot_name=depot.split('|')[1].strip()
#                   user_depot_address=''
#                   if session.user_type!='Depot':
#                       depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
#                       if depotRows:
#                           user_depot_address=depotRows[0].field1
#                           session.user_depot_address=user_depot_address
#
#           if dateFlag==False:
#               response.flash="Invalid Date "
#           if btn_salesComparisionNational:
#               redirect (URL('scNational',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionRsm:
#               redirect (URL('scRsm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFm:
#               redirect (URL('scFm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTr:
#               redirect (URL('scTr',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionNationalD:
#               redirect (URL('scNationalD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionRsmD:
#               redirect (URL('scRsmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFmD:
#               redirect (URL('scFmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTrD:
#               redirect (URL('scTrD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTrDetail:
#               redirect (URL('scTrDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFmDetail:
#               redirect (URL('scFmDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionRsmDetail:
#               redirect (URL('scRsmDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTrDetailD:
#               redirect (URL('scTrDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFmDetailD:
#               redirect (URL('scFmDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionRsmDetailD:
#               redirect (URL('scRsmDetailD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionMarketDetail:
#               redirect (URL('scMarketDetail',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoad:
#               redirect (URL('TRReport',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadAB:
#               redirect (URL('TRReportAB',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFMDLoad:
#               redirect (URL('FMReport',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFMDLoadAB:
#               redirect (URL('FMReportAB',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadInvoice:
#               redirect (URL('TRReportInvoice',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadInvoicePeriodicProcess:
#               redirect (URL('TRReportInvoicePeriodicalProcess',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadInvoicePeriodic:
#               redirect (URL('TRReportInvoicePeriodical',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLExCInvoicePeriodic:
#               redirect (URL('TRReportExCInvoicePeriodical',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#     ===================CTeam=============================
#     if (btn_salesComparisionRsmCteam or btn_salesComparisionRsmCteamD or btn_salesComparisionRsmDetailCteam or btn_salesComparisionRsmDetailCteamD or btn_salesComparisionFmCteam or btn_salesComparisionFmCteamD or btn_salesComparisionFmDetailCteam or btn_salesComparisionFmDetailCteamD or btn_salesComparisionTrCteam or btn_salesComparisionTrCteamD or btn_salesComparisionTrDetailCteam or btn_salesComparisionTrDetailCteamD or btn_salesComparisionMarketDetailCteam or btn_salesComparisionMarketDetailCteam or btn_salesComparisionTRDLoadCteam or btn_salesComparisionTRDLoadCteamPeriodic or btn_salesComparisionTRDLoadABCteam or btn_salesComparisionFMDLoadCteam or btn_salesComparisionTRDLoadInvoicePeriodicCteamProcess):
#           date_from=request.vars.from_dt_4
#           date_to=request.vars.to_dt_4
#
#           depot=str(request.vars.sales_depot_id_SC_C)
#           store=str(request.vars.store_id_SC_C)
#
# #           return depot
#           rsm_SC=str(request.vars.rsm_SC_C)
#           fm_SC=str(request.vars.fm_SC_C)
#           tr_SC=str(request.vars.tr_SC_C)
#           product=str(request.vars.product_c)
#
#           depot_id=depot
#           store_id=store
#
#           depot_name=''
#           store_name=''
#
#           dateFlag=True
# #           return 'asfsaf'
#           try:
#               from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
#           except:
#               dateFlag=False
#
#
#           if ((depot!='') & (depot.find('|') != -1)):
#               depot_id=depot.split('|')[0].upper().strip()
#               depot_name=depot.split('|')[1].strip()
#
#           else:
#               depot_id=depot
#               depot_name=''
#
#           if ((store!='') & (store.find('|') != -1)) :
#               store_id=store.split('|')[0].upper().strip()
#               store_name=store.split('|')[1].strip()
#           else:
#               store_id=store_id
#               store_name=''
#
#           if ((rsm_SC!='') & (store.find('|') != -1)) :
#               rsm_id=rsm_SC.split('|')[0].upper().strip()
#               rsm_name=store.split('|')[1].strip()
#           else:
#               rsm_id=rsm_SC
#               rsm_name=''
#           if ((fm_SC!='') & (fm_SC.find('|') != -1)) :
#               fm_id=fm_SC.split('|')[0].upper().strip()
#               fm_name=fm_SC.split('|')[1].strip()
#           else:
#               fm_id=fm_SC
#               fm_name=''
#
#           if ((product!='') & (product.find('|') != -1)) :
#               product_id=product.split('|')[0].upper().strip()
#               product_name=product.split('|')[1].strip()
#           else:
#               product_id=product
#               product_name=''
#
#           if ((tr_SC!='') & (tr_SC.find('|') != -1)) :
#               tr_id=tr_SC.split('|')[0].upper().strip()
#               tr_name=tr_SC.split('|')[1].strip()
#           else:
#               tr_id=tr_SC
#               tr_name=''
#           if ((depot!='') & (depot.find('|') != -1)):
#                   depot_id=depot.split('|')[0].upper().strip()
#                   depot_name=depot.split('|')[1].strip()
#                   user_depot_address=''
#                   if session.user_type!='Depot':
#                       depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
#                       if depotRows:
#                           user_depot_address=depotRows[0].field1
#                           session.user_depot_address=user_depot_address
#
#           if dateFlag==False:
#               response.flash="Invalid Date "
# #           C TEAM=================================
#           if btn_salesComparisionRsmCteam:
#               redirect (URL('scRsmCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#
# #           if btn_salesComparisionRsmCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionRsmDetailCteam:
#                redirect (URL('scRsmDetailCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionRsmDetailCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFmCteam:
#               redirect (URL('scFmCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionFmCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFmDetailCteam:
#               redirect (URL('scFmDetailCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionFmDetailCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTrCteam:
#               redirect (URL('scTrCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionTrCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTrDetailCteam:
#               redirect (URL('scTrDetailCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionTrDetailCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionMarketDetailCteam:
#               redirect (URL('scMarketDetailCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
# #           if btn_salesComparisionTrDetailCteamD:
# #               redirect (URL('scNationalCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name)))
#
#           if btn_salesComparisionTRDLoadCteam:
#               redirect (URL('TRReportCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadCteamPeriodic:
#               redirect (URL('TRReportCteamPeriodic',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionTRDLoadABCteam:
#               redirect (URL('TRReportABCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#           if btn_salesComparisionFMDLoadCteam:
#               redirect (URL('FMReportCteam',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
#
#           if btn_salesComparisionTRDLoadInvoicePeriodicCteamProcess:
#               redirect (URL('TRReportInvoicePeriodicalCteamProcess',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)))
                                                          
    if (btn_list_sales or btn_customer_wise_sales or btn_item_wise_batch_sales or btn_item_wise_sales or btn_list_oderdetail or btn_list_oderdSummary_spowise or btn_item_wise_sale_detail or btn_item_wise_sales_sheet or btn_dp_wise_order_summary):
          date_from=request.vars.to_dt
          date_to=request.vars.to_dt_2
          
          sl_from=request.vars.sales_sl_from
          sl_to=request.vars.sales_sl_to
          
          depot=str(request.vars.sales_depot_id_order)
          store=str(request.vars.store_id_order)
          
          customer=str(request.vars.customer_id_order)
          teritory=str(request.vars.t_id_order)
          mso=str(request.vars.mso_id_order)
          
          fm_order=str(request.vars.fm_order)
          
          RadioGroupCheck=str(request.vars.RadioGroupCheck)
#           return RadioGroupCheck
          
          depot_id=depot
          store_id=store
          customer_id=customer
          teritory_id=teritory
          mso_id=mso
          
          depot_name=''
          store_name=''
          customer_name=''
          teritory_name=''
          mso_name=''
          dateFlag=True
#           return 'asfsaf'
          try:
              from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
          except:
              dateFlag=False
          
#           return btn_item_wise_sales_sheet
          if ((depot!='') & (depot.find('|') != -1)):             
              depot_id=depot.split('|')[0].upper().strip()
              depot_name=depot.split('|')[1].strip()
              
          else:
              depot_id=depot
              depot_name=''
          
          if ((store!='') & (store.find('|') != -1)) : 
              store_id=store.split('|')[0].upper().strip()
              store_name=store.split('|')[1].strip()
          else:
              store_id=store_id
              store_name=''
          if ((customer!='') & (customer.find('|') != -1)) :       
              customer_id=customer.split('|')[0].upper().strip()
              customer_name=customer.split('|')[1].strip()
          else:
              customer_id=customer_id
              customer_name=''
          
          if ((teritory!='') & (teritory.find('|') != -1)) :     
              teritory_id=teritory.split('|')[0].upper().strip()
              teritory_name=teritory.split('|')[1].strip()
          else:
              teritory_id=teritory_id
              teritory_name=''
          if ((mso!='') & (mso.find('|') != -1)) :    
              mso_id=mso.split('|')[0].upper().strip()
              mso_name=mso.split('|')[1].strip()
          else:
              mso_id=mso_id
              mso_name=''
          
          if ((fm_order!='') & (fm_order.find('|') != -1)) :    
              fm_id=fm_order.split('|')[0].upper().strip()
              fm_name=fm_order.split('|')[1].strip()
          else:
              fm_id=fm_order
              fm_name=''
          
          if dateFlag==False:
              response.flash="Invalid Date "
          elif (teritory_id=='' and  mso_id=='' and customer_id=='' and fm_order=='' and btn_item_wise_sales_sheet!='Order Sheet' and btn_dp_wise_order_summary!='Order Summary' ):
              response.flash="Please select Teritory or Mso or Customer"
          else:               
              if btn_item_wise_sales_sheet:
                    redirect (URL('oderSheet',vars=dict(date_from=date_from,date_to=date_to,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,RadioGroupCheck=RadioGroupCheck,fm_id=fm_id,fm_name=fm_name)))  
              
              elif btn_dp_wise_order_summary:
                  redirect (URL('oderSummary',vars=dict(date_from=date_from,date_to=date_to,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id,customer_name=customer_name,teritory_id=teritory_id,teritory_name=teritory_name,mso_id=mso_id,mso_name=mso_name,RadioGroupCheck=RadioGroupCheck,fm_id=fm_id,fm_name=fm_name)))  
         
         
         #     ================================================Sales End Nadira==========================================================================================                     
    
                          
    
    return dict(search_form=search_form)







#===================================================Sales Start Nadira=====================
def order():
    c_id=session.cid
    
    response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
#    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    
    
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
   
    
    
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
    record_sum=qset.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0

    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    

def list_sales():
    c_id=session.cid
    
    response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
#    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
   
    
    
    records=qset.select(db.sm_invoice_head.ALL,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
    record_sum=qset.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0

    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    


def list_sales_customer_wise():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    #    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice_head.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice_head.status==status)
            qset_sum=qset_sum(db.sm_invoice_head.status==status)
        else:
            qset=qset((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice_head.status!='Invoiced') & (db.sm_invoice_head.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),  groupby=db.sm_invoice_head.client_id,orderby=db.sm_invoice_head.depot_id|db.sm_invoice_head.store_id|db.sm_invoice_head.sl,limitby=limitby)
#     return records
    record_sum=qset_sum.select(db.sm_invoice_head.total_amount.sum(),((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[db.sm_invoice_head.total_amount.sum()]
        net_return=rec[(((db.sm_invoice_head.return_tp + db.sm_invoice_head.return_vat) - db.sm_invoice_head.return_discount)).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    


def list_item_wise_batch_sales():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
     
    
    #    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice.status==status)
            qset_sum=qset_sum(db.sm_invoice.status==status)
        else:
            qset=qset((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.price,db.sm_invoice.discount,db.sm_invoice.item_vat,db.sm_invoice.item_vat.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.return_rate,  groupby=db.sm_invoice.item_id | db.sm_invoice.batch_id,orderby=db.sm_invoice.item_name|db.sm_invoice.batch_id,limitby=limitby)
#     return records
    record_sum=qset_sum.select(((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum(),(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()  )
#     return db._lastsql
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum()]
        net_return=rec[(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()]
        if net_amount==None:
            net_amount=0.0
        if net_return==None:
            net_return=0.0
    
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    

    
def list_item_wise_sales():
    c_id=session.cid
    
    response.title='Sales-Customer Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    status=str(request.vars.status).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    #    return status
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_invoice_head.invoice_media!='OPENING')
    qset=qset(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
#     qset_sum=qset_sum(db.sm_invoice_head.invoice_media!='OPENING')
    qset_sum=qset_sum(db.sm_invoice_head.sl==db.sm_invoice.sl)
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice.client_id==customer_id)
    if (dman_id!=''):
        qset=qset(db.sm_invoice.d_man_id==dman_id)
        qset_sum=qset_sum(db.sm_invoice.d_man_id==dman_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
        
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice.rep_id==mso_id)
    if (status!=''):
        if (status=='Invoiced'):
            qset=qset(db.sm_invoice.status==status)
            qset_sum=qset_sum(db.sm_invoice.status==status)
        else:
            qset=qset((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
            qset_sum=qset_sum((db.sm_invoice.status!='Invoiced') & (db.sm_invoice.status!='Cancelled'))
    
    
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.batch_id,db.sm_invoice.quantity.sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.price,db.sm_invoice.item_vat.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.return_rate,  groupby=db.sm_invoice.item_id,orderby=db.sm_invoice.item_name,limitby=limitby)
#     return records
    record_sum=qset_sum.select(((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum(),(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()  )
#     return record_sum
    net_amount=0.0
    net_return=0.0
    
    net_return=0.0
    for rec in record_sum:
        net_amount=rec[((db.sm_invoice.price+db.sm_invoice.item_vat) * db.sm_invoice.quantity+db.sm_invoice.discount).sum()]
        net_return=rec[(db.sm_invoice.return_qty * db.sm_invoice.return_rate).sum()]
    
    #     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,status=status,net_amount=net_amount,net_return=net_return,page=page,items_per_page=items_per_page)    





# Nadira
#=====================================Order detail==============================================

def list_oderdetail():
    c_id=session.cid
    
    response.title='Order Detail'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)

    qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
        qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order.ALL,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

    total=0.0
    
    for rec in record_sum:
        total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    
 #=====================================Order detail Download==============================================

def downloadorderDetail():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
   
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)

    qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order.cid==c_id)

    qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
        qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order.ALL,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl)
#     return db._lastsql
    record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

    total=0.0
    
    for rec in record_sum:
        total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
 
    
    
    #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='SL,Region,Region Name,Area,Area Name,Territory,Territory Name,MSO,MSOName,Customer ID,Customer Name,Item ID,Item Name,Qty,Rate,Total\n'
    
    
    for rec in records:
        sl=rec.sl
        region=rec.level2_id
        rigion_name=rec.level2_name
        area=rec.level1_id
        area_name=rec.level1_name
        teritory=rec.area_id
        teritory_name=rec.area_name
        rep_id=rec.rep_id
        rep_name=rec.rep_name
        client_id=rec.client_id
        client_name=rec.client_name
        item=rec.item_id
        item_name=rec.item_name
        qty=rec.quantity
        price=rec.price
        total_amn=float(price)*float(qty)
        
        

         
               
        myString+=str(sl)+','+str(region)+','+str(rigion_name)+','+str(area)+','+str(area_name)+','+str(teritory)+','+str(teritory_name)+','+str(rep_id)+','+str(rep_name)+','+str(client_id)+','+str(client_name)+','+str(item)+','+str(item_name)+','+str(qty)+','+str(price)+','+str(total_amn)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_detail.csv'   
    return str(myString) 

#=====================================list_oderderSumRepWise==============================================

def list_oderderSumRepWise():
    c_id=session.cid
    
    response.title='Order Count MSO Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)

    qset_sum=qset_sum((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id | db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id ,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    

def list_oderderSumRepWiseDdate():
    c_id=session.cid
    
    response.title='Order Count MSO Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)

    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id ,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)    
def list_oderderSumRepWiseDownloadDdate():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id )
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
        
   #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='MSO,Name,Territory,Territory Name,Total\n'
    
    
    for rec in records:
        rep_id=rec[db.sm_order_head.rep_id]
        rep_name=rec[db.sm_order_head.rep_name]
        teritory=rec[db.sm_order_head.area_id]
        teritory_name=rec[db.sm_order_head.area_name]
        
        total_o=rec[db.sm_order_head.sl.count()]
        
        

         
               
        myString+=str(rep_id)+','+str(rep_name)+','+str(teritory)+','+str(teritory_name)+','+str(total_o)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_orderCountRepWiswDelDate.csv'   
    return str(myString) 


# ===========================
def list_oderdSummary_Ddate():
    c_id=session.cid
    
    response.title='Order Count '
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)

    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.delivery_date,groupby=db.sm_order_head.delivery_date ,limitby=limitby)
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,total=total,page=page,items_per_page=items_per_page)

def list_oderdSummary_DdateDownload():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order_head.delivery_date >= date_from) & (db.sm_order_head.delivery_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.delivery_date,groupby=db.sm_order_head.delivery_date )
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
        
   #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='OrderDate,DeliveryDate,Total\n'
    
    
    for rec in records:
        order_date=rec[db.sm_order_head.order_date]
        delivery_date=rec[db.sm_order_head.delivery_date]
        
        
        total_o=rec[db.sm_order_head.sl.count()]
        
        

         
               
        myString+=str(order_date)+','+str(delivery_date)+','+str(total_o)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_orderCountDelDate.csv'   
    return str(myString) 


# ======================
def list_oderderSumRepWiseDownload():
    c_id=session.cid
    
#     response.title='Sales-Invoice Wise'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)

    qset=qset((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_order_head.cid==c_id)
    
    qset_sum=qset_sum((db.sm_order_head.order_date >= date_from) & (db.sm_order_head.order_date < date_to_m))
    if (depot_id!=''):
        qset=qset(db.sm_order_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_order_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_order_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_order_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_order_head.rep_id==mso_id)
        
  
    records=qset.select(db.sm_order_head.ALL,db.sm_order_head.sl.count(),orderby=db.sm_order_head.depot_id|db.sm_order_head.store_id|db.sm_order_head.rep_id|db.sm_order_head.area_id,groupby=db.sm_order_head.rep_id|db.sm_order_head.area_id )
#     return db._lastsql
    record_sum=qset.select(db.sm_order_head.sl.count())
#     return records
    total=0.0
    
    for rec in record_sum:
        total=rec[db.sm_order_head.sl.count()]
        
   #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    myString=myString+'Total,'+str(total)+'\n\n\n'
        
    myString+='MSO,Name,Territory,Territory Name,Total\n'
    
    
    for rec in records:
        rep_id=rec[db.sm_order_head.rep_id]
        rep_name=rec[db.sm_order_head.rep_name]
        teritory=rec[db.sm_order_head.area_id]
        teritory_name=rec[db.sm_order_head.area_name]
        
        total_o=rec[db.sm_order_head.sl.count()]
        
        

         
               
        myString+=str(rep_id)+','+str(rep_name)+','+str(teritory)+','+str(teritory_name)+','+str(total_o)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_orderCountRepWisw.csv'   
    return str(myString) 


def oderSheet():
    c_id=session.cid
    
    response.title='Order Sheet'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    sl_from=request.vars.sl_from
    sl_to=request.vars.sl_to
#     return  sl_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    RadioGroupCheck=str(request.vars.RadioGroupCheck).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    date_from_check=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
    date_to_check=datetime.datetime.strptime(str(date_to_m).split(' ')[0],'%Y-%m-%d') 
    
    
    dateDiff=(date_to_check-date_from_check).days
#     return dateDiff
    if int(dateDiff) > 7:
        session.flash="Maximum 7 days allowed between Date Range"
        redirect(URL(c='report_sales',f='home')) 
#     return dateDiff
    
#     return 'asdas'
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.client_id==db.sm_order.client_id)
    
    if RadioGroupCheck=='Order':
        qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    if RadioGroupCheck=='Delivery':
        qset=qset((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date < date_to_m))
    
    
    
    
    
#     qset_sum=db()
#     qset_sum=qset_sum(db.sm_order.cid==c_id)
#     if RadioGroupCheck=='Order':
#         qset_sum=qset_sum((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
#     if RadioGroupCheck=='Delivery':
#         qset_sum=qset_sum((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date < date_to_m))
    
    if (sl_from!=''):
        qset=qset(db.sm_order.sl>=sl_from)
#         qset_sum=qset_sum(db.sm_order.sl>=sl_from)
        
    if (sl_to!=''):    
        qset=qset(db.sm_order.sl<=sl_to)        
#         qset_sum=qset_sum(db.sm_order.sl<=sl_to)
    
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
#         qset_sum=qset_sum(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
#         qset_sum=qset_sum(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
#         qset_sum=qset_sum(db.sm_order.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_order.area_id==teritory_id)
#         qset_sum=qset_sum(db.sm_order.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
#         qset_sum=qset_sum(db.sm_order.rep_id==mso_id)
    if (fm_id!=''):
        qset=qset(db.sm_order.level2_id==fm_id)    
  
    records=qset.select(db.sm_order.ALL,db.sm_client.address,db.sm_client.market_id,db.sm_client.market_name,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl)



#     return db._lastsql
    if not records:
        session.flash="Order Not Available"
        redirect(URL(c='report_sales',f='home')) 
        
    
#     record_sum=qset.select((db.sm_order.price* db.sm_order.quantity).sum())

#     total=0.0
#     
#     for rec in record_sum:
#         total=rec[(db.sm_order.price* db.sm_order.quantity).sum()]
    
#     net_return=((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-db.sm_invoice_head.return_discount)
    
    return dict(records=records,date_from=date_from,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)    
 

def oderSummary():
    c_id=session.cid
    
    response.title='Order Summary'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    sl_from=request.vars.sl_from
    sl_to=request.vars.sl_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    RadioGroupCheck=str(request.vars.RadioGroupCheck).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    
    date_from_check=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
    date_to_check=datetime.datetime.strptime(str(date_to_m).split(' ')[0],'%Y-%m-%d') 
    
    
    dateDiff=(date_to_check-date_from_check).days
    if int(dateDiff) > 7:
        session.flash="Maximum 7 days allowed between Date Range"
        redirect(URL(c='report_sales',f='home')) 
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_order.cid==c_id)
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.client_id==db.sm_order.client_id)
    
    if RadioGroupCheck=='Order':
        qset=qset((db.sm_order.order_date >= date_from) & (db.sm_order.order_date < date_to_m))
    if RadioGroupCheck=='Delivery':
        qset=qset((db.sm_order.delivery_date >= date_from) & (db.sm_order.delivery_date < date_to_m))
    

    if (sl_from!=''):
        qset=qset(db.sm_order.sl>=sl_from)
        
    if (sl_to!=''):    
        qset=qset(db.sm_order.sl<=sl_to)   
    
    if (depot_id!=''):
        qset=qset(db.sm_order.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_order.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_order.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_order.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_order.rep_id==mso_id)
    if (fm_id!=''):
        qset=qset(db.sm_order.level2_id==fm_id)    
  
    records=qset.select(db.sm_order.ALL,db.sm_client.address,db.sm_client.market_id,db.sm_client.market_name,groupby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl,orderby=db.sm_order.depot_id|db.sm_order.store_id|db.sm_order.sl)

    if not records:
        session.flash="Order Not Available"
        redirect(URL(c='report_sales',f='home')) 
    
    
    return dict(records=records,date_from=date_from,sl_from=sl_from,sl_to=sl_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)    

    
 
def itemWiseSalesSDetail():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.quantity*db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.item_discount.sum(),orderby=db.sm_invoice.item_name ,groupby=db.sm_invoice.item_id|db.sm_invoice.item_name)
#     return records
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt,sum(item_vat * quantity) as inv_vat_amnt,sum(item_vat * return_qty) as ret_vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
#     records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
#     return records_retS
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            ret_vat_amnt=records_ret['ret_vat_amnt']
            inv_vat_amnt=records_ret['inv_vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:  
            invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
            returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
            vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]        
#             disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
#             spdisc=spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
#             retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
        
        return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
           
def itemWiseSalesSDetailDLoad():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.item_discount.sum(),orderby=db.sm_invoice.item_name ,groupby=db.sm_invoice.item_id|db.sm_invoice.item_name)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
       
       
        myString='12.2\n\n'
        myString=myString+'Item Wise Sales Statement Detail\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        

        
        myString+='Item,ItemName,InvCount,RetCount, InvS.Qty,InvB.Qty,InvTP,RetS.Qty,RetB.Qty,RetTP,RTN%,NetS.Qty,NetB.Qty,NetTP,Disc,Vat,Net (TP+Vat),NS%\n'
          
        for record in records:
            itmInv=0
            itmRet=0
            item_id =record[db.sm_invoice.item_id]
            if [s for s in invList if item_id in s]:
                index_element = invList.index(item_id)           
                itmInv=invList_str[index_element]
            if [s for s in retList if item_id in s]:
                ret_index_element = retList.index(item_id)           
                itmRet=retList_str[ret_index_element]
            invSale= float(record[(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum()])
            netRet= record[(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum()]
            rtnP=0
               
            if (invSale > 0):
                rtnP=(netRet*100)/invSale
            netQty=int(record[db.sm_invoice.quantity.sum()])-int(record[db.sm_invoice.return_qty.sum()])
            netSale  =  invSale-netRet 
            vat=record[(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum()]-record[(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum()]
            nsP=0
            if (invSale > 0):
                nsP =(netSale *100)/invSale
                                                                                                                                        
       
            disc=record[db.sm_invoice.item_discount.sum()]                                                                                                                                                    
            myString+=str(record[db.sm_invoice.item_id])+','+str(record[db.sm_invoice.item_name])+','+str(itmInv)+','+str(itmRet)+','+str(record[db.sm_invoice.quantity.sum()])+','+str(record[db.sm_invoice.bonus_qty.sum()])+','+str(record[(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum()])+','+str(record[db.sm_invoice.return_qty.sum()])+','+str(record[db.sm_invoice.return_bonus_qty.sum()])+','+str(netRet)+','+str(round(rtnP,2))+','+str(netQty)+','+str(int(record[db.sm_invoice.bonus_qty.sum()])-int(record[db.sm_invoice.return_bonus_qty.sum()]))+','+str(invSale - netRet)+','+str(disc)+','+str(vat)+','+str(netSale+vat)+','+str(round(nsP,2))+'\n'
#         return myString
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ItemWiseSalesStatementDetail.csv'   
        return str(myString)  
        
#         return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
def itemWiseSalesSDetailLand():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp.max(),db.sm_invoice.return_rate.max(),db.sm_invoice.item_vat.max(),(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum(),(db.sm_invoice.return_rate *db.sm_invoice.quantity).sum(),(db.sm_invoice.quantity*db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name ,groupby=db.sm_invoice.item_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
#     records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt,sum(item_vat * quantity) as inv_vat_amnt,sum(item_vat * return_qty) as ret_vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            ret_vat_amnt=records_ret['ret_vat_amnt']
            inv_vat_amnt=records_ret['inv_vat_amnt']
#             vat_amnt=records_ret['vat_amnt']
#             inv_qty=records_ret['inv_qty']
#             inv_bonus_qty=records_ret['inv_bonus_qty']
#             inv_tp=records_ret['inv_tp']
#             inv_amnt=records_ret['inv_amnt']
#             ret_qty=records_ret['ret_qty']
#             ret_bonus_qty=records_ret['ret_bonus_qty']
#             ret_amnt=records_ret['ret_amnt']
#             vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         record_sum=qset_sum.select(db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:      
            invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
            returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
            vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]    
#             disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
#             spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
#             retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
        
        return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
           
def invoiceWiseSalesSDetail():
    c_id=session.cid
    response.title='Invoice Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.sl,db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.cl_category_name,db.sm_invoice_head.payment_mode,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.sl,groupby=db.sm_invoice_head.sl)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt,sum(item_vat * quantity) as inv_vat_amnt,sum(item_vat * return_qty) as ret_vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            ret_vat_amnt=records_ret['ret_vat_amnt']
            inv_vat_amnt=records_ret['inv_vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:      
            invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
            returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
            vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]
    
        
        
        
            
        
        return dict(records=records,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


def invoiceWiseSalesSDetailD():
    c_id=session.cid
    response.title='Invoice Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.invoice_date,db.sm_invoice_head.sl,db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.cl_category_name,db.sm_invoice_head.payment_mode,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.sl,groupby=db.sm_invoice_head.sl)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
    if records:
        myString='12.3,12.11\n\n Inv Wise Sales\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='Date  ,  Inv Number ,Depot  ,MarketName,Market,SalesTerm,CustType,  CustomerID, CustomerName  ,  MSOID, MSO Name  ,  InvTP   , InvDisc  ,  InvVat  ,  InvNet ,   RetTP  ,  RetDisc  ,  RetVat   , RetNet  ,  NetTP  ,  NetDisc  ,  NetVat  ,  Net\n'
          
        for record in records: 
#             retTP=record[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum()]
# #             retTP=record[(db.sm_invoice_head.return_tp).sum()]
#             retNet=retTP+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]) 
#             retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            inv= 'INV'+str(record[db.sm_invoice_head.depot_id])+'-'+str(record[db.sm_invoice_head.sl])
            retTP=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_sp_discount.sum()]
            retNet=retTP+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            netSold=record[db.sm_invoice_head.actual_total_tp.sum()]-retTP
            
            myString=myString+str(record[db.sm_invoice_head.invoice_date])+','+str(inv)+','+str(record[db.sm_invoice_head.depot_id])+','+str(record[db.sm_invoice_head.market_name])+','+str(record[db.sm_invoice_head.market_id])+','+str(record[db.sm_invoice_head.payment_mode])+','+str(record[db.sm_invoice_head.cl_category_name])+','+str(record[db.sm_invoice_head.client_id])+','+str(record[db.sm_invoice_head.client_name])+','+str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name])+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])+','+str(record[db.sm_invoice_head.vat_total_amount.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()])+','+str(retTP)+','+str(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])+','+str(record[db.sm_invoice_head.return_vat.sum()])+','+str(retNet)+','+str(netSold)+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=InvWiseSalesStatementDetail.csv'   
        return str(myString)
       
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


# --------------------------------------------------
def customerWiseSalesSDetail():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    selesTerm=str(request.vars.selesTerm).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (selesTerm!=''):
       qset=qset(db.sm_invoice_head.payment_mode==selesTerm)
       qset_sum=qset_sum(db.sm_invoice_head.payment_mode==selesTerm)
        
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.depot_id,db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name,db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.depot_id|db.sm_invoice_head.client_id|db.sm_invoice_head.client_name|db.sm_invoice_head.rep_id|db.sm_invoice_head.rep_name|db.sm_invoice_head.market_id|db.sm_invoice_head.market_name)
#     return db._lastsql
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    if (selesTerm!=''):
        condition_ret=condition_ret+"AND payment_mode= '"+str(selesTerm)+"'"
    
#     records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt,sum(item_vat * quantity) as inv_vat_amnt,sum(item_vat * return_qty) as ret_vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            ret_vat_amnt=records_ret['ret_vat_amnt']
            inv_vat_amnt=records_ret['inv_vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
            returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
            vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
        if (selesTerm!=''):
            qsetRet=qsetRet(db.sm_invoice.payment_mode==selesTerm)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)

        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,selesTerm=selesTerm)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def customerWiseSalesSDetailP():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    selesTerm=str(request.vars.selesTerm).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (selesTerm!=''):
       qset=qset(db.sm_invoice_head.payment_mode==selesTerm)
       qset_sum=qset_sum(db.sm_invoice_head.payment_mode==selesTerm)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.client_id|db.sm_invoice_head.rep_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    if (selesTerm!=''):
        condition_ret=condition_ret+"AND payment_mode= '"+str(selesTerm)+"'"

    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
        if (selesTerm!=''):
            qsetRet=qsetRet(db.sm_invoice.payment_mode==selesTerm)

            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total,page=page,items_per_page=items_per_page,selesTerm=selesTerm)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customerWiseSalesSDetailPD():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    selesTerm=str(request.vars.selesTerm).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (selesTerm!=''):
       qset=qset(db.sm_invoice_head.payment_mode==selesTerm)
       qset_sum=qset_sum(db.sm_invoice_head.payment_mode==selesTerm)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.client_id,db.sm_invoice_head.client_name,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.market_id,db.sm_invoice_head.market_name,db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.client_name,groupby=db.sm_invoice_head.client_id|db.sm_invoice_head.rep_id)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    if (selesTerm!=''):
        condition_ret=condition_ret+"AND payment_mode= '"+str(selesTerm)+"'"

    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
        if (selesTerm!=''):
            qsetRet=qsetRet(db.sm_invoice.payment_mode==selesTerm)

            
            

        retCountRows=qsetRet.select(db.sm_invoice.client_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.client_name,groupby=db.sm_invoice.client_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retCust_id = retCountRows[db.sm_invoice.client_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retCust_id)
            retList_str.append(retCount)
        
            
    if records:
        myString='12.6\n\nCustomer Wise Sales Statement Detail\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n'
        myString=myString+'Sales Term,'+selesTerm+'\n\n'
         
       
         
        myString+='CustomerID,CustomerName  ,  MSOID,MSOName  ,   InvCount  ,  RetCount  ,  InvTP  ,  RetTP  ,  NetTP  ,  NetDisc  ,  NetVat ,   Net\n'
          
        for record in records: 
            custRet=0
            client_id=record[db.sm_invoice_head.client_id]
            if [s for s in retList if client_id in s]:
                ret_index_element = retList.index(client_id)           
                custRet=retList_str[ret_index_element]
#             retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            retTP=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_sp_discount.sum()]
            retNet=retTP+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]) 
            myString=myString+str(record[db.sm_invoice_head.client_id])+','+str(record[db.sm_invoice_head.client_name])+','+str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name.max()])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(custRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(retTP)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-retTP)+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustWiseSalesStatementDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# ---------------------------------------------------------------
def msoWiseSalesSDetail():
    c_id=session.cid
    response.title='MSO Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.level2_id,db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.rep_name,groupby=db.sm_invoice_head.depot_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id|db.sm_invoice_head.rep_name)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retRep_id = retCountRows[db.sm_invoice.rep_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retRep_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,spdisc=spdisc,retdisc=retdisc,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  
        
def msoWiseSalesSDetailD():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.level2_id,db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.rep_name,groupby=db.sm_invoice_head.depot_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id|db.sm_invoice_head.rep_name)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            retRep_id = retCountRows[db.sm_invoice.rep_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retRep_id)
            retList_str.append(retCount)
        
            
    if records:
        
     
        myString='12.8\n\nMSO WiseSales StatementDetail\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='MSOID,MsoName  ,  InvCount  ,  RetCount  ,  InvTP  ,  RetTP  ,  NetTP  ,  Disc  ,  Vat   , Net\n'
          
        for record in records: 
            repRet=0
            rep_id=record[db.sm_invoice_head.rep_id]
            if [s for s in retList if rep_id in s]:
                ret_index_element = retList.index(rep_id)           
                repRet=retList_str[ret_index_element]
                
                
#             retNet=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            retTP=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_sp_discount.sum()]
            retNet=retTP+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            netSold=record[db.sm_invoice_head.actual_total_tp.sum()]-retTP    
            myString=myString+str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name.max()])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(repRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(retTP)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()]-retNet)+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(netSold)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=MSOWiseSalesStatementDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))          
        
        
        
# ----------------------------------------------------------------        
              
def dpWiseSalesSDetail():
    c_id=session.cid
    response.title='DP Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
#     records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt,sum(item_vat * quantity) as inv_vat_amnt,sum(item_vat * return_qty) as ret_vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            ret_vat_amnt=records_ret['ret_vat_amnt']
            inv_vat_amnt=records_ret['inv_vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
#         record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
            returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
            vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.d_man_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.d_man_id,groupby=db.sm_invoice.d_man_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            dman_id = retCountRows[db.sm_invoice.d_man_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(dman_id)
            retList_str.append(retCount)
        
            
        
        return dict(records=records,retList=retList,retList_str=retList_str,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))   
        


def dpWiseSalesSDetailD():
    c_id=session.cid
    response.title='Customer Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
   
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice_head.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice_head.sl.count(),db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_sp_discount.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''): 
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            

        retCountRows=qsetRet.select(db.sm_invoice.d_man_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.d_man_id,groupby=db.sm_invoice.d_man_id)
    #     return invCountRows
        
        retList=[]
        retList_str=[]
        for retCountRows in retCountRows:
            dman_id = retCountRows[db.sm_invoice.d_man_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(dman_id)
            retList_str.append(retCount)
        
             
             
         
    if records:
        
     
        myString='12.9\n\nDelivery Person Wise Sales Statement Detail\n'
        myString=myString+'DateRange,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
         
       
         
        myString+='DeliveryManID, DeliveryManName   , InvCount  ,  RetCount  ,  InvTP  ,  InvDisc  ,  InvVat  ,  InvNet  ,  RetTP  ,  RetDisc  ,  RetVat  ,  RetNet  ,  NetTP  ,  NetDisc  ,  NetVat  ,  Net\n'
          
        for record in records: 
            repRet=0
            d_man_id=record[db.sm_invoice_head.d_man_id]
            if [s for s in retList if d_man_id in s]:
                ret_index_element = retList.index(d_man_id)           
                repRet=retList_str[ret_index_element]
            
            retTP=record[db.sm_invoice_head.return_tp.sum()]+record[db.sm_invoice_head.return_sp_discount.sum()]
            retNet=retTP+record[db.sm_invoice_head.return_vat.sum()]-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])
            netSold=record[db.sm_invoice_head.actual_total_tp.sum()]-retTP
            
            myString=myString+str(record[db.sm_invoice_head.d_man_id])+','+str(record[db.sm_invoice_head.d_man_name.max()])+','+str(record[db.sm_invoice_head.sl.count()])+','+str(repRet)+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])+','+str(record[db.sm_invoice_head.vat_total_amount.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()])+','+str(retTP)+','+str(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()])+','+str(record[db.sm_invoice_head.return_vat.sum()])+','+str(retNet)+','+str(netSold)+','+str((record[db.sm_invoice_head.discount.sum()]+record[db.sm_invoice_head.sp_discount.sum()])-(record[db.sm_invoice_head.return_sp_discount.sum()]+record[db.sm_invoice_head.return_discount.sum()]))+','+str(record[db.sm_invoice_head.vat_total_amount.sum()]-record[db.sm_invoice_head.return_vat.sum()])+','+str(record[db.sm_invoice_head.total_amount.sum()]-retNet)+'\n'
         
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=DPWiseSalesStatementDetail.csv'   
        return str(myString) 
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
                 
# ---------------------------------
def customrInformation():
    
    c_id=session.cid
    
    response.title='Customer Information'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a teritory"
#         redirect(URL(c='report_sales',f='home'))
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_rep_area.cid==c_id)
    qset=qset(db.sm_rep_area.area_id==db.sm_client.area_id)

    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_client.cid==c_id)
    qset_sum=qset(db.sm_rep_area.area_id==db.sm_client.area_id)
    
    if (depot_id!=''):
        qset=qset(db.sm_client.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_client.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_client.store_id==store_id)
        qset_sum=qset_sum(db.sm_client.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_client.client_id==customer_id)
        qset_sum=qset_sum(db.sm_client.client_id==customer_id)
     
    if (teritory_id!=''):
        qset=qset(db.sm_client.area_id==teritory_id)
        qset_sum=qset_sum(db.sm_client.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_rep_area.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_rep_area.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_client.market_id==market_id)
        qset_sum=qset_sum(db.sm_client.market_id==market_id)
        
  
    records=qset.select(db.sm_client.ALL,db.sm_rep_area.ALL,orderby=db.sm_client.client_id)
    if records:
        record_sum=qset_sum.select(db.sm_client.id.count())
    #     return record_sum
        total=0.0
        
        for rec in record_sum:
            customer_count=rec[db.sm_client.id.count()]
    
    
    
        
        
        return dict(records=records,customer_count=customer_count,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customrInformationDownload():
    
    c_id=session.cid
    
    response.title='Customer Information'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_rep_area.cid==c_id)
    qset=qset(db.sm_rep_area.area_id==db.sm_client.area_id)

    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_client.cid==c_id)
    qset_sum=qset(db.sm_rep_area.area_id==db.sm_client.area_id)
    
    if (depot_id!=''):
        qset=qset(db.sm_client.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_client.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_client.store_id==store_id)
        qset_sum=qset_sum(db.sm_client.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_client.client_id==customer_id)
        qset_sum=qset_sum(db.sm_client.client_id==customer_id)
     
    if (teritory_id!=''):
        qset=qset(db.sm_client.area_id==teritory_id)
        qset_sum=qset_sum(db.sm_client.area_id==teritory_id) 
    if (mso_id!=''):
        qset=qset(db.sm_rep_area.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_rep_area.rep_id==mso_id)
        
  
    records=qset.select(db.sm_client.ALL,db.sm_rep_area.ALL,orderby=db.sm_client.client_id)
    if records:
        record_sum=qset_sum.select(db.sm_client.id.count())
    #     return record_sum
        total=0.0
        
        for rec in record_sum:
            customer_count=rec[db.sm_client.id.count()]
    
        myString='Customer Information\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString=myString+'Total,'+str(customer_count)+'\n\n\n'
        
        myString+='CustID,CustName,CustAddress,Teritory, TeritoryName,MarketID,MarketName,MSO TR,MSO Name\n'
         
        for records in records:
            CustID=str(records[db.sm_client.client_id]).replace(',','')
            CustName=str(records[db.sm_client.name]).replace(',','')
            CustAddress=str(records[db.sm_client.address]).replace(',','')
            Teritory=str(records[db.sm_client.area_id]).replace(',','')
            TeritoryName=str(records[db.sm_rep_area.area_name]).replace(',','')
            MarketID=str(records[db.sm_client.market_id]).replace(',','')
            MarketName=str(records[db.sm_client.market_name]).replace(',','')
            MSOTR=str(records[db.sm_rep_area.rep_id]).replace(',','')
            MSOName=str(records[db.sm_rep_area.rep_name]).replace(',','')
            
            myString+=str(CustID)+','+str(CustName)+','+str(CustAddress)+','+str(Teritory)+','+str(TeritoryName)+','+str(MarketID)+','+str(MarketName)+','+str(MSOTR)+','+str(MSOName)+'\n'
        
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=customerInformation.csv'   
        return str(myString) 
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
#      btn_MSOwiseS   

def msowiseS():
    c_id=session.cid
    
    response.title='MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    customerCat_idSub=str(request.vars.customerCat_idSub).strip()
    customerCat_nameSub=str(request.vars.customerCat_nameSub).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

    
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)

    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    
    
    
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice_head.cid==c_id)

    qset_total=qset_total(db.sm_invoice_head.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
       
        qset_total=qset_total(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        
        qset_total=qset_total(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
       
        qset_total=qset_total(db.sm_invoice_head.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        
        
        qset_total=qset_total(db.sm_invoice_head.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        
        qset_total=qset_total(db.sm_invoice_head.rep_id==mso_id)
        
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.msarket_id==msarket_id)
        
        qset_total=qset_total(db.sm_invoice_head.msarket_id==msarket_id)
        
    if (customerCat_id!=''):
        qset=qset(db.sm_invoice_head.cl_category_id==customerCat_id)
       
        qset_total=qset_total(db.sm_invoice_head.cl_category_id==customerCat_id)
    if (customerCat_idSub!=''):
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customerCat_idSub)
        
        qset_total=qset_total(db.sm_invoice_head.cl_sub_category_id==customerCat_idSub)

    records=qset.select(db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.area_name.max(),db.sm_invoice_head.market_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id,groupby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id)
    records_total=qset_total.select(db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.area_name.max(),db.sm_invoice_head.market_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id,groupby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id )
    
    qsetRet=db()
    qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
    qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
    qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
    qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
    qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
    qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
    qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    if (depot_id!=''): 
        qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
    if (store_id!=''):
        qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
        
    if (customer_id!=''):
        qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
     
    if (mso_id!=''):
        qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
    if (market_id!=''):
        qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
    if (customerCat_id!=''):
        qsetRet=qsetRet(db.sm_invoice.cl_category_id==customerCat_id)
    if (customerCat_idSub!=''):
        qsetRet=qsetRet(db.sm_invoice.cl_sub_category_id==customerCat_idSub)
        

    retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    retList=[]
    retList_str=[]
    for retCountRows in retCountRows:
        retRep_id = retCountRows[db.sm_invoice.rep_id]
        retCount = retCountRows[db.sm_invoice_head.sl.count()]
        retList.append(retRep_id)
        retList_str.append(retCount)

    if records:  
        return dict(records=records,retList=retList,retList_str=retList_str,records_total=records_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,customerCat_id=customerCat_id,customerCat_name=customerCat_name,customerCat_idSub=customerCat_idSub, customerCat_nameSub=customerCat_nameSub)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


# ===========D===========
def msowiseSDLoad():
    c_id=session.cid
    
    response.title='MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    customerCat_idSub=str(request.vars.customerCat_idSub).strip()
    customerCat_nameSub=str(request.vars.customerCat_nameSub).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

    
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)

    qset=qset(db.sm_invoice_head.status=='Invoiced')    
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    
    
    
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice_head.cid==c_id)

    qset_total=qset_total(db.sm_invoice_head.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
       
        qset_total=qset_total(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)
        
        qset_total=qset_total(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==customer_id)
       
        qset_total=qset_total(db.sm_invoice_head.client_id==customer_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        
        
        qset_total=qset_total(db.sm_invoice_head.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id)
        
        qset_total=qset_total(db.sm_invoice_head.rep_id==mso_id)
        
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.msarket_id==msarket_id)
        
        qset_total=qset_total(db.sm_invoice_head.msarket_id==msarket_id)
        
    if (customerCat_id!=''):
        qset=qset(db.sm_invoice_head.cl_category_id==customerCat_id)
       
        qset_total=qset_total(db.sm_invoice_head.cl_category_id==customerCat_id)
    if (customerCat_idSub!=''):
        qset=qset(db.sm_invoice_head.cl_sub_category_id==customerCat_idSub)
        
        qset_total=qset_total(db.sm_invoice_head.cl_sub_category_id==customerCat_idSub)

    records=qset.select(db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.area_name.max(),db.sm_invoice_head.market_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id,groupby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id)
#     return db._lastsql
    records_total=qset_total.select(db.sm_invoice_head.area_id,db.sm_invoice_head.rep_id,db.sm_invoice_head.rep_name.max(),db.sm_invoice_head.area_name.max(),db.sm_invoice_head.market_id.max(),db.sm_invoice_head.market_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),db.sm_invoice_head.return_discount.sum(),orderby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id,groupby=db.sm_invoice_head.area_id|db.sm_invoice_head.rep_id )
     
    qsetRet=db()
    qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
    qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
    qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
    qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
    qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
    qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
    qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    if (depot_id!=''): 
        qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
    if (store_id!=''):
        qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
        
    if (customer_id!=''):
        qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
     
    if (mso_id!=''):
        qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
    if (market_id!=''):
        qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
    if (customerCat_id!=''):
        qsetRet=qsetRet(db.sm_invoice.cl_category_id==customerCat_id)
    if (customerCat_idSub!=''):
        qsetRet=qsetRet(db.sm_invoice.cl_sub_category_id==customerCat_idSub)
        

    retCountRows=qsetRet.select(db.sm_invoice.rep_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.rep_name,groupby=db.sm_invoice.rep_id)
    retList=[]
    retList_str=[]
    for retCountRows in retCountRows:
        retRep_id = retCountRows[db.sm_invoice.rep_id]
        retCount = retCountRows[db.sm_invoice_head.sl.count()]
        retList.append(retRep_id)
        retList_str.append(retCount)
    

    if records:  
       
        myString='17.1\n\nMSO wise Sales\n'
        myString=myString+'Date Range,'+date_from+','+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
#         myString=myString+'Total,'+str(customer_count)+'\n\n\n'
        
        myString+='MSO TR ,   MSO Name  ,  Market  ,  Invoice Total  ,  No of Invoice ,   Return Total ,No of Return  ,  Exec %  ,  Return %  ,  Net Sold \n'
         
        for record in records:
#             area_id=record[db.sm_invoice_head.area_idma]
#             area_name=record[db.sm_invoice_head.area_name]
            market_id=record[db.sm_invoice_head.market_id.max()]
            total_amount=record[db.sm_invoice_head.total_amount.sum()]
            invCount=record[db.sm_invoice_head.id.count()]
            return_amount=record[db.sm_invoice_head.return_tp.sum()] + record[db.sm_invoice_head.return_vat.sum()]-record[db.sm_invoice_head.return_discount.sum()]
            netSold=record[db.sm_invoice_head.total_amount.sum()]-return_amount
            sale=record[db.sm_invoice_head.total_amount.sum()]
            rSale=return_amount
            eP=(netSold/sale)*100
            rP=(return_amount/sale)*100
            repRet=0
            rep_id=record[db.sm_invoice_head.rep_id]
            if [s for s in retList if rep_id in s]:
                ret_index_element = retList.index(rep_id)           
                repRet=retList_str[ret_index_element]
            
            myString+=str(record[db.sm_invoice_head.rep_id])+','+str(record[db.sm_invoice_head.rep_name.max()])+','+str(market_id)+','+str(total_amount)+','+str(invCount)+','+str(return_amount)+','+str(repRet)+','+str(round(eP,2))+','+str(round(rP))+','+str(netSold)+'\n'
        
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=MSOwiseSales.csv'   
        return str(myString) 
    
    
    
    
    
    
    
    
    
    
    
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

        


#      btn_MSOwiseS   

def catMSOwiseS():
    c_id=session.cid
    
    response.title='Catagory and MSO wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    if customerCat_id=='':        
        session.flash="Please select Teritory and Customer Category"
        redirect(URL(c='report_sales',f='home'))
    
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
#     return levelRows
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.client_id==db.sm_invoice.client_id)
    qset=qset(db.sm_invoice.status=='Invoiced')    
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    qset_rsm=db()
    qset_rsm=qset_rsm(db.sm_invoice.cid==c_id)
    qset_rsm=qset_rsm(db.sm_client.cid==c_id)
    qset_rsm=qset_rsm(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_rsm=qset_rsm(db.sm_invoice.status=='Invoiced')  
    qset_rsm=qset_rsm((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    qset_fm=db()
    qset_fm=qset_fm(db.sm_invoice.cid==c_id)
    qset_fm=qset_fm(db.sm_client.cid==c_id)
    qset_fm=qset_fm(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_fm=qset_fm(db.sm_invoice.status=='Invoiced')  
    qset_fm=qset_fm((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    
    qset_total=db()
    qset_total=qset_total(db.sm_invoice.cid==c_id)
    qset_total=qset_total(db.sm_client.cid==c_id)
    qset_total=qset_total(db.sm_client.client_id==db.sm_invoice.client_id)
    qset_total=qset_total(db.sm_invoice.status=='Invoiced')  
    qset_total=qset_total((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_fm=qset_fm(db.sm_invoice.depot_id==depot_id)
        qset_rsm=qset_rsm(db.sm_invoice.depot_id==depot_id)
        qset_total=qset_total(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_fm=qset_fm(db.sm_invoice.store_id==store_id)
        qset_rsm=qset_rsm(db.sm_invoice.store_id==store_id)
        qset_total=qset_total(db.sm_invoice.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_fm=qset_fm(db.sm_invoice.client_id==customer_id)
        qset_rsm=qset_rsm(db.sm_invoice.client_id==customer_id)
        qset_total=qset_total(db.sm_invoice.client_id==customer_id)
    
    if (customerCat_id!=''):
        qset=qset(db.sm_client.category_id==customerCat_id)
        qset_fm=qset_fm(db.sm_client.category_id==customerCat_id)
        qset_rsm=qset_rsm(db.sm_client.category_id==customerCat_id)
        qset_total=qset_total(db.sm_client.category_id==customerCat_id)
    
    if (teritory_id!=''):
        qset=qset(db.sm_invoice.area_id==teritory_id)
        qset_rsm=qset_rsm(db.sm_invoice.level1_id==rsm)
        qset_fm=qset_fm(db.sm_invoice.level2_id==fm)
        qset_total=qset_total(db.sm_invoice.area_id==teritory_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_fm=qset_fm(db.sm_invoice.rep_id==mso_id)
        qset_rsm=qset_rsm(db.sm_invoice.rep_id==mso_id)
        qset_total=qset_total(db.sm_invoice.rep_id==mso_id)
        
  
    records=qset.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.area_id | db.sm_client.category_id,groupby=db.sm_invoice.area_id | db.sm_client.category_id,limitby=limitby)
    records_fm=qset_fm.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.level2_id | db.sm_client.category_id,limitby=limitby)
    records_rsm=qset_rsm.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id, (db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.level1_id | db.sm_client.category_id,limitby=limitby)
#     return records_rsm
    records_total=qset_total.select(db.sm_invoice.ALL,db.sm_client.category_id,db.sm_client.category_name,db.sm_client.market_id,(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),orderby=db.sm_invoice.item_name,limitby=limitby)
    
    reportfmDict={}
    reportfmList=[]
    reportfmmsoList=[]
    
    for records_fm in records_fm:
       mso_tr=records_fm[db.sm_invoice.area_id]
       fm=records_fm[db.sm_invoice.level2_id]
       fm_invTotal=records_fm[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]
       fm_retTotal=records_fm[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()]
       fm_noRet=records_fm[db.sm_invoice.return_qty.sum()]   
       reportfmDict={'mso_tr':mso_tr,'fm':fm,'fm_invTotal':fm_invTotal,'fm_retTotal':fm_retTotal,'fm_noRet':fm_noRet}  
       reportfmList.append(reportfmDict)
       reportfmmsoList.append(mso_tr)
       
    reportrsmDict={}
    reportrsmList=[]
    reportrsmmsoList=[]
#     return records_rsm
    for records_rsm in records_rsm:
       mso_tr_rsm=records_rsm[db.sm_invoice.area_id]
       rsm=records_rsm[db.sm_invoice.level1_id]
       rsm_invTotal=records_rsm[(db.sm_invoice.quantity * db.sm_invoice.price).sum()]
       rsm_retTotal=records_rsm[(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum()]
       rsm_noRet=records_rsm[db.sm_invoice.return_qty.sum()]   
       reportrsmDict={'mso_tr_rsm':mso_tr_rsm,'rsm':rsm,'rsm_invTotal':rsm_invTotal,'rsm_retTotal':rsm_retTotal,'rsm_noRet':rsm_noRet}  
       reportrsmList.append(reportrsmDict)
       reportrsmmsoList.append(mso_tr_rsm)
    
    if records:  
        return dict(records=records,records_fm=records_fm,records_rsm=records_rsm,records_total=records_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
        
def catDPwiseS():
    c_id=session.cid
    
    response.title='Catagory and DP wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging

    condition=''
    conditionInv=''
    conditionRet=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        conditionInv=conditionInv+"AND depot_id = '"+str(depot_id)+"'"
        conditionRet=conditionRet+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        conditionInv=conditionInv+"AND store_id = '"+str(store_id)+"'"
        conditionRet=conditionRet+"AND store_id = '"+str(store_id)+"'"
    if (dman_id!=''):
        condition=condition+"AND d_man_id = '"+str(dman_id)+"'"   
        conditionInv=conditionInv+"AND d_man_id = '"+str(dman_id)+"'"   
        conditionRet=conditionRet+"AND d_man_id = '"+str(dman_id)+"'"        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"      
        conditionInv=conditionInv+"AND client_id = '"+str(customer_id)+"'"      
        conditionRet=conditionRet+"AND client_id = '"+str(customer_id)+"'"      
    if (customerCat_id!=''):
        condition=condition+"AND cl_category_id = '"+str(customerCat_id)+"'" 
        conditionInv=conditionInv+"AND category_id = '"+str(customerCat_id)+"'" 
        conditionRet=conditionRet+"AND category_id = '"+str(customerCat_id)+"'"    
    if (teritory_id!=''):
        condition=condition+"AND area_id = '"+str(teritory_id)+"'"
        conditionInv=conditionInv+"AND area_id = '"+str(teritory_id)+"'"
        conditionRet=conditionRet+"AND area_id = '"+str(teritory_id)+"'"     
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        conditionInv=conditionInv+"AND rep_id = '"+str(mso_id)+"'"
        conditionRet=conditionRet+"AND rep_id = '"+str(mso_id)+"'"

    dateRecords="SELECT d_man_id, max(d_man_name),market_id,max(market_name),category_id, SUM(quantity * actual_tp) as invTP,SUM(actual_tp *return_qty) as retTP FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"

    records=db.executesql(dateRecords,as_dict = True) 
    
    

    
    
    
    
    
    
    
    dateRecordsInv="SELECT distinct(sl) as sl,d_man_id, max(d_man_name),market_id,max(market_name),category_id, count(id) as invCount  FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionInv+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"
#     return dateRecordsInv
    recordsInv=db.executesql(dateRecordsInv,as_dict = True) 
    dateRecordsRet="SELECT distinct(sl) as sl,d_man_id, max(d_man_name),market_id,max(market_name),category_id, count(id) as retCount  FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND return_qty > 0 AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionRet+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"
    recordsRet=db.executesql(dateRecordsRet,as_dict = True)
#     return dateRecordsRet
    invList=[]
    invCheckList=[]
    invTest=''
    for i in range(len(recordsInv)):
        recordInv=recordsInv[i]
        invTest=str(recordInv['d_man_id'])+'|'+str(recordInv['market_id'])+'|'+str(recordInv['category_id'])
        invCheckList.append(invTest)
        invList.append(recordInv['invCount'])
        
    retList=[]
    retCheckList=[]
    retTest=''
    for x in range(len(recordsRet)):
        recordRet=recordsRet[x]
        retTest=str(recordRet['d_man_id'])+'|'+str(recordRet['market_id'])+'|'+str(recordRet['category_id'])
        retCheckList.append(retTest)
        retList.append(recordRet['retCount'])
                   
                   
    if records:  
        return dict(records=records,invList=invList,invCheckList=invCheckList,retList=retList,retCheckList=retCheckList,customerCat_id=customerCat_id,customerCat_name=customerCat_name,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name, teritory_id=teritory_id, teritory_name=teritory_name, mso_id=mso_id, mso_name=mso_name,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def catDPwiseSD():
    c_id=session.cid
    
    response.title='Catagory and DP wise Sales'
    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    customerCat_id=str(request.vars.customerCat_id).strip()
    customerCat_name=str(request.vars.customerCat_name).strip()
    
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging

    condition=''
    conditionInv=''
    conditionRet=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        conditionInv=conditionInv+"AND depot_id = '"+str(depot_id)+"'"
        conditionRet=conditionRet+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        conditionInv=conditionInv+"AND store_id = '"+str(store_id)+"'"
        conditionRet=conditionRet+"AND store_id = '"+str(store_id)+"'"
    if (dman_id!=''):
        condition=condition+"AND d_man_id = '"+str(dman_id)+"'"   
        conditionInv=conditionInv+"AND d_man_id = '"+str(dman_id)+"'"   
        conditionRet=conditionRet+"AND d_man_id = '"+str(dman_id)+"'"        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"      
        conditionInv=conditionInv+"AND client_id = '"+str(customer_id)+"'"      
        conditionRet=conditionRet+"AND client_id = '"+str(customer_id)+"'"      
    if (customerCat_id!=''):
        condition=condition+"AND cl_category_id = '"+str(customerCat_id)+"'" 
        conditionInv=conditionInv+"AND category_id = '"+str(customerCat_id)+"'" 
        conditionRet=conditionRet+"AND category_id = '"+str(customerCat_id)+"'"    
    if (teritory_id!=''):
        condition=condition+"AND area_id = '"+str(teritory_id)+"'"
        conditionInv=conditionInv+"AND area_id = '"+str(teritory_id)+"'"
        conditionRet=conditionRet+"AND area_id = '"+str(teritory_id)+"'"     
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        conditionInv=conditionInv+"AND rep_id = '"+str(mso_id)+"'"
        conditionRet=conditionRet+"AND rep_id = '"+str(mso_id)+"'"

    dateRecords="SELECT d_man_id, max(d_man_name),market_id,max(market_name),category_id, SUM(quantity * actual_tp) as invTP,SUM(actual_tp *return_qty) as retTP FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"

    records=db.executesql(dateRecords,as_dict = True) 
    
    

    
    
    
    
    
    
    
    dateRecordsInv="SELECT distinct(sl) as sl,d_man_id, max(d_man_name),market_id,max(market_name),category_id, count(id) as invCount  FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionInv+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"
#     return dateRecordsInv
    recordsInv=db.executesql(dateRecordsInv,as_dict = True) 
    dateRecordsRet="SELECT distinct(sl) as sl,d_man_id, max(d_man_name),market_id,max(market_name),category_id, count(id) as retCount  FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND return_qty > 0 AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionRet+" GROUP BY d_man_id,category_id ORDER BY d_man_id,category_id;"
    recordsRet=db.executesql(dateRecordsRet,as_dict = True)
#     return dateRecordsRet
    invList=[]
    invCheckList=[]
    invTest=''
    for i in range(len(recordsInv)):
        recordInv=recordsInv[i]
        invTest=str(recordInv['d_man_id'])+'|'+str(recordInv['market_id'])+'|'+str(recordInv['category_id'])
        invCheckList.append(invTest)
        invList.append(recordInv['invCount'])
        
    retList=[]
    retCheckList=[]
    retTest=''
    for x in range(len(recordsRet)):
        recordRet=recordsRet[x]
        retTest=str(recordRet['d_man_id'])+'|'+str(recordRet['market_id'])+'|'+str(recordRet['category_id'])
        retCheckList.append(retTest)
        retList.append(recordRet['retCount'])
                   
                    
    if records:  
        myString='17.2\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
#         myString+='Category,'+customerCat_id+'|'+customerCat_name+'\n\n'
                                        
        myString =myString+ 'DP ID  ,  DP Name  ,Category,Market,MarketName,   Invoice Total  ,  Return Total ,No of Inv ,  No of Reurn ,   Exec %  ,  Returm %  ,  Net Sold \n' 
                         
        for i in range(len(records)):
            record=records[i]
            invCount=0
            retCount=0
            head_check=str(record['d_man_id'])+'|'+str(record['market_id'])+'|'+str(record['category_id'])
            if [s for s in invCheckList if head_check in s]:
                index_element = invCheckList.index(head_check)    
                invCount=invList[index_element]  
            if [z for z in retCheckList if head_check in z]:
                index_element = retCheckList.index(head_check)  
                retCount=retList[index_element] 
                  
                  
            netSold=record['invTP']-record['retTP']
            sale=record['invTP']
            rSale=record['retTP']
#             netSoldTotal=netSoldTotal+netSold
#             saleTotal=saleTotal+sale
#             rSaleTotal=rSaleTotal+rSale
            eP=0
            rP=0
            if sale > 0: 
                eP=(netSold*100)/sale 
            if sale > 0: 
                rP=(rSale*100)/sale
            
            
            myString=myString+str(record['d_man_id'])+','+str(record['max(d_man_name)'])+','+str(record['category_id'])+','+str(record['market_id'])+','+str(record['max(market_name)'])+','+str(record['invTP'])+','+str(record['retTP'])+','+str(invCount)+','+str(retCount)+','+str(round(eP,2))+','+str(round(rP,2))+','+str(netSold)+'\n'
            
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CatagoryMSOwiseSales.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =======================


        
def dpwiseSD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount)>0)

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return db._lastsql
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    if records:
        return dict(records=records,dmanList=dmanList,invCList=invCList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def dpwiseSDD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount)>0)

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return db._lastsql
    
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    
    if records:  
        myString='12.10 \n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
#         myString+='Category,'+customerCat_id+'|'+customerCat_name+'\n\n'
                                        
        myString =myString+ 'DP ID  ,  Delivery Person Name  ,  No. of Inv.  ,  No. of Return  ,  Inv Amnt.  ,  Ret Amnt  ,  Exec%  ,  Ret%  ,  Net Sold TP \n' 
                         
        for records in records:
            retCount=0
            d_man_id=records[db.sm_invoice_head.d_man_id]
#             return d_man_id
            if [s for s in dmanList if d_man_id in s]:
                
               index_element = dmanList.index(d_man_id)           
               retCount=invCList[index_element]
                
            retAmn=records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
            invAmn=(records[db.sm_invoice_head.actual_total_tp.sum()])     
            netSold=0
            sale=records[db.sm_invoice_head.actual_total_tp.sum()]
            netSold=records[db.sm_invoice_head.actual_total_tp.sum()]-retAmn
            
            
            
            
            
            eP=(netSold*100)/sale
            rP=(retAmn*100)/sale
            
            myString=myString+str(records[db.sm_invoice_head.d_man_id])+','+str(records[db.sm_invoice_head.d_man_name.max()])+','+str(records[db.sm_invoice_head.id.count()])+','+str(retCount)+','+str(records[db.sm_invoice_head.actual_total_tp.sum()])+','+str(retAmn)+','+str(round(eP))+','+str(round(rP))+','+str(invAmn-retAmn)+'\n'
 
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=DeliveryPersonWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =================================================        
#         customrProductwiseS
def customrProductwiseS():
    
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()

    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    condition=''

    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    
    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name, item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrProductwiseSD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,groupby=db.sm_level.level1|db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
 
    
    
    condition=''


    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"


    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"


    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"


    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"


    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"


    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"


    
    
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 

    if records:
        myString='10.2 11.2\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
       
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['unitTP'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
# =============================================       
def customrProductwiseSIncludingBonus():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        

    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,groupby=db.sm_level.level1|db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    condition=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    
    
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY  client_id,item_id  ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    
    
    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrProductwiseSIncludingBonusD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    if (teritory_id==''):
        session.flash="Please select a Teritory"
        redirect(URL(c='report_sales',f='home'))
        
    levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == teritory_id)).select(db.sm_level.level1,db.sm_level.level2,groupby=db.sm_level.level1|db.sm_level.level2,limitby=(0,1))
    if levelRows:
        rsm=levelRows[0].level1
        fm=levelRows[0].level2
        
    condition=''
   
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    
    
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY  client_id,item_id  ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    

    if records:
        myString='10.4\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
       
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['unitTP'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatementWithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# =======================================================

        
def customrProductwiseSExcludingBonus():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    

    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))

    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
        
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 

    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  

def customrProductwiseSExcludingBonusD():
    c_id=session.cid   
    response.title='Customer-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        

    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
        
    records_S="SELECT  client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,item_id ORDER BY client_id,item_id;"
    records=db.executesql(records_S,as_dict = True) 
    if records:
        myString='10.5 \n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n\n'
                                        
        
        myString =myString+ '\n\nClientID,ClientName,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        for i in range(len(records)):
            record=records[i]
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
                    
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id']+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold))+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerProductWiseSalesStatementWithoutBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))  

# ============================================     
#         productwiseS
def productwiseS():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    

    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        


#     ===================
    condition=''

    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        
    
    records_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_name;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    

    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def productwiseSD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    

    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    

#     ===================
    condition=''
   
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    records_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_name;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    

    
    if records:
        myString='11.1\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
        
        myString =myString+ 'ItemID ,   ItemName  ,  UOM   , UnitPrice ,   Ret% ,  InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice   ,  ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  ,  NetQnty  ,  NetBonus  ,  NetTradePrice \n' 
                            
        for i in range(len(records)):
            record=records[i]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['max(item_unit)'])+','+str(record['unitTP'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
# ========================================
def productwiseSwithoutBonus():   
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    

    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        


#     ===================
    condition=''

    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        
    
    records_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_name;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    

    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def productwiseSwithoutBonusD():   
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    

    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    

#     ===================
    condition=''
   
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    records_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id ORDER BY item_name;"
    records=db.executesql(records_S,as_dict = True) 
    
#     records=qset.select(db.sm_invoice.ALL,(db.sm_invoice.quantity * db.sm_invoice.actual_tp).sum(),(db.sm_invoice.quantity * db.sm_invoice.price).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(), groupby=db.sm_invoice.item_id, orderby=db.sm_invoice.item_name)
    

    
    if records:
        myString='10.3\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
        
        myString =myString+ 'ItemID ,   ItemName  ,  UOM   , UnitPrice ,   Ret% ,  InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice   ,  ReturnQnty  ,  ReturnBonus  ,  ReturnTradePrice  ,  NetQnty  ,  NetBonus  ,  NetTradePrice \n' 
                            
        for i in range(len(records)):
            record=records[i]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['max(item_unit)'])+','+str(record['unitTP'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            
    
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementWithoutBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ==================================       
def customrInvoiceProductwiseS():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    
        
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
   
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"    
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"

    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id  ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    
    recordshead_S="SELECT  sl,client_id,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition_head+"  GROUP BY client_id ORDER BY client_id;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)
        
        
        
        
        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
def customrInvoiceProductwiseSD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    
        
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
        
   
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"    
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"

    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id  ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    
    recordshead_S="SELECT  sl,client_id,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition_head+"  GROUP BY client_id ORDER BY client_id;"
    records_head=db.executesql(recordshead_S,as_dict = True) 
   
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        
        
        
        myString='10.6 11.3 \n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
            myString =myString+'INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['max(invoice_date)']) +','+str(record['max(area_name)'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['unitTP'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSalesStatement.csv'   
        return str(myString)
        
        
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))   
#  =========================================================   
def customrInvoiceProductwiseSwithBonus():
    
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
        
    
    
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id ORDER BY client_id;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    

    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)

        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrInvoiceProductwiseSwithBonusD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
        
    
    
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,actual_tp as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id ORDER BY client_id;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True)  
    
 
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        

        myString='10.7 \n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
            myString =myString+'INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['max(invoice_date)']) +','+str(record['max(area_name)'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSStatWithBonust.csv'   
        return str(myString)        
           
        
        
        
       
    else:
        
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))       
# =========================================================
        
def customrInvoiceProductwiseSwithoutBonus():
    
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)
        
        
        
        
        return dict(records=records,reportHeadList=reportHeadList,InvSlList=InvSlList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
def customrInvoiceProductwiseSwithoutBonusD():
    c_id=session.cid   
    response.title='Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
        
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,max(item_name),max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl,item_id ORDER BY client_id,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  sl,client_id,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY client_id,sl ORDER BY client_id,sl;"
#     return recordshead_S
    records_head=db.executesql(recordshead_S,as_dict = True) 
    
        
    if records:
        reportHeadDict={}
        reportHeadList=[]
        InvSlList=[] 
#         return len(records_head)
        for i in range(len(records_head)):
            
            head_sl=records_head[i]['sl']
            head_client=records_head[i]['client_id']
            head_qty=records_head[i]['inv_qty']
            head_Bonusqty=records_head[i]['inv_bonus_qty']
            head_ret_qty=records_head[i]['ret_qty']
            head_ret_bonus_qty=records_head[i]['ret_bonus_qty']
            head_check=str(head_sl)+'-'+str(head_client)
            
            head_invTotal=records_head[i]['actual_tp']
            head_retTotal=records_head[i]['retTP']
            reportHeadDict={'head_sl':head_sl,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}
            
            
            reportHeadList.append(reportHeadDict)
            InvSlList.append(head_check)        

        
        myString='10.8\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
        
        myString = '\nClientID,ClientName,Inv,InvDate,AreaName,HeadInvTotal,HeadRetTotal,HeadTotal,ItemID ,   ItemName  ,  UOM  ,  UnitPrice ,   Ret% , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        clientID=''
        invsl=''
        
        for i in range(len(records)):
            record=records[i]
            head_check=str(record['sl'])+'-'+str(record['client_id']) 
            if [s for s in InvSlList if head_check in s]:
              index_element = InvSlList.index(head_check)           
              head_data=reportHeadList[index_element] 

                
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            myString =myString+str(record['client_id'])+',' +str(record['max(client_name)'])+','
            myString =myString+'INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['max(invoice_date)']) +','+str(record['max(area_name)'])   +','+str(head_data['head_invTotal'])+','+ str(head_data['head_retTotal']) +',' +str(float(head_data['head_invTotal'])-float(head_data['head_retTotal'])) +','
            myString=myString+str(record['item_id'])+','+str(record['max(item_name)'])+','+str(record['max(item_unit)'])+','+str(record['actual_tp'])+','+str(rP)+','+str(record['inv_qty'])+','+str(record['inv_bonus_qty'])+','+str(record['actual_tp'])+','+str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold)+'\n'
            clientID=record['client_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CustomerInvoiceProductWiseSStatWithoutBonust.csv'   
        return str(myString) 
        
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
# ================================
        
def productInvoicewiseSD():
    
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    
    
#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
        return dict(records=records,reportHeadList=reportHeadList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        
# =====================================================
def productInvoicewiseSDD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    
#     return records
    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='10.9 11.4\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(head_data['head_price'])+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(head_data['head_invTotal'])+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(head_data['head_retTotal'])+','+str(float(head_data['head_invTotal'])-float(head_data['head_retTotal']))+','
            
            myString =myString+str(record['max(invoice_date)'])+',INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['max(client_name)']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(record['actual_tp']) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatement.csv'   
        return str(myString)



    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))       
        
        
        
# ========================================        
        
def productInvoicewiseSDwithBonus():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND  invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND      invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
        
    
        return dict(records=records,reportHeadList=reportHeadList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def productInvoicewiseSDwithBonusD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND  invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty > 0 AND      invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='10.10\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(head_data['head_price'])+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(head_data['head_invTotal'])+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(head_data['head_retTotal'])+','+str(float(head_data['head_invTotal'])-float(head_data['head_retTotal']))+','
            
            myString =myString+str(record['max(invoice_date)'])+',INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['max(client_name)']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(record['actual_tp']) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementwithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ================================        
def productInvoicewiseSDwithoutBonus():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND  invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND      invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
        
   
        return dict(records=records,reportHeadList=reportHeadList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
    
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))


def productInvoicewiseSDwithoutBonusD():
    c_id=session.cid   
    response.title='Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
    
    condition=''
    condition_head=''
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
        condition_head=condition_head+"AND depot_id = '"+str(depot_id)+"'"
        
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        condition_head=condition_head+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
        condition_head=condition_head+"AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        condition_head=condition_head+"AND rep_id = '"+str(rep_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        condition_head=condition_head+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        condition_head=condition_head+"AND area_id = '"+str(teritory_id)+"'"
    
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
        condition_head=condition_head+"AND item_id = '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
        condition_head=condition_head+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
        condition_head=condition_head+"AND level2_id = '"+str(fm_id)+"'"
        
        
    records_S="SELECT  max(depot_id),max(invoice_date),max(area_name),sl,client_id,max(client_name),item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND  invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY   sl,client_id,item_id,item_name ORDER BY item_name,sl;"
    records=db.executesql(records_S,as_dict = True) 
    recordshead_S="SELECT  item_id,item_name,max(item_unit),max(actual_tp) as unitTP,sum(quantity * actual_tp) as actual_tp, sum((return_rate+return_sp_discount_item) *return_qty) as retTP ,sum(bonus_qty) as inv_bonus_qty,sum(quantity) as inv_qty,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND bonus_qty = 0 AND      invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY item_id,item_name ORDER BY item_name;"
    records_head=db.executesql(recordshead_S,as_dict = True) 

    if records:
        reportHeadDict={}
        reportHeadList=[]
        itemList=[] 
        for i in range(len(records_head)):
           head_item=records_head[i]['item_id']
           head_unit=records_head[i]['max(item_unit)']
           head_price=records_head[i]['unitTP']
           head_qty=records_head[i]['inv_qty']
           head_Bonusqty=records_head[i]['inv_bonus_qty']
           head_ret_qty=records_head[i]['ret_qty']
           head_ret_bonus_qty=records_head[i]['ret_bonus_qty']

           head_invTotal=records_head[i]['actual_tp']
           head_retTotal=records_head[i]['retTP']
           reportHeadDict={'head_item':head_item,'head_unit':head_unit,'head_price':head_price,'head_qty':head_qty,'head_Bonusqty':head_Bonusqty,'head_ret_qty':head_ret_qty,'head_ret_bonus_qty':head_ret_bonus_qty,'head_invTotal':head_invTotal,'head_retTotal':head_retTotal}  
           reportHeadList.append(reportHeadDict)
           itemList.append(head_item)
           
           
        
        myString='10.11\n\nDateRange,'+date_from+','+date_to+'\n'
        myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n'
        myString+='Market,'+market_id+'|'+market_name+'\n'
        myString+='item,'+item_id+'|'+item_name+'\n'
        myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
        myString+='FM,'+fm_id+'|'+fm_name+'\n\n'
                                        
       
        
        myString =myString+ '\n\nItemID , ItemName , Unit , TP ,HeadQty,HeadBonusqty,HeadinvTotal,HeadRetQty,HeadRetBonusQty,HeadRetTotal,headNetTotal,Date  ,  Inv Number   , CustomerID  ,  CustomerNmae , InvioceQnty  ,  InvioceBonus  ,  InvioceTradePrice ,ReturnQnty   , ReturnBonus  ,  ReturnTradePrice ,NetQnty  ,  NetBonus ,   NetTradePrice \n'
        p=0
        itemID=''
        invsl=''
        for i in range(len(records)):
            record=records[i]
            item_check= record['item_id']
            if itemID != record['item_id']:
                if [s for s in itemList if item_check in s]:
                    index_element = itemList.index(item_check)           
                    head_data=reportHeadList[index_element]
            netSold=record['actual_tp']-record['retTP']
            sale=record['actual_tp']
            rSale=record['retTP']
            rP=0
            if (rSale > 0):
                rP=(rSale*100)/sale
            
                  
            myString =myString+str(record['item_id'])+',' +str(record['item_name'])+','+str(head_data['head_unit'])+','+str(head_data['head_price'])+','+str(head_data['head_qty'])+','+str(head_data['head_Bonusqty'])+','+str(head_data['head_invTotal'])+','+str(head_data['head_ret_qty'])+','+str(head_data['head_ret_bonus_qty'])+','+str(head_data['head_retTotal'])+','+str(float(head_data['head_invTotal'])-float(head_data['head_retTotal']))+','
            
            myString =myString+str(record['max(invoice_date)'])+',INV'+str(record['max(depot_id)'])+'-'+str(record['sl'])+','+str(record['client_id'])+',' +str(record['max(client_name)']) +','+str(record['inv_qty'])   +','+str(record['inv_bonus_qty'])+','+ str(record['actual_tp']) +',' +str(record['ret_qty'])+','+str(record['ret_bonus_qty'])+','+str(record['retTP'])+','+str(record['inv_qty']-record['ret_qty'])+','+str(record['inv_bonus_qty']-record['ret_bonus_qty'])+','+str(netSold) +'\n'
            
            itemID=record['item_id']
        
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ProductWiseSalesStatementwithBonus.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        
        

        









# =====================================================


        
def invoicewiseSD():
    
    c_id=session.cid   
    response.title='Invoice Wise Sales Detail'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
   
    condition=''
   
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
       
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
       
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,sl,max(invoice_date),max(cl_category_name),max(payment_mode),max(client_id),max(client_name),max(rep_id),max(rep_name),max(market_name),max(market_id),sum(actual_total_tp) as actual_tp, sum(return_tp+return_sp_discount) as retTP ,sum(vat_total_amount-return_vat) as vat ,sum(discount-return_discount) as discount ,sum(sp_discount-return_sp_discount) as spDiscount FROM sm_invoice_head WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY depot_id,sl ORDER BY sl;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    
    
    

    if records:
        return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

# ===============Download===================
def invoicewiseSDLoad():
    c_id=session.cid   
    response.title='Invoice Wise Sales Detail'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     if (teritory_id==''):
#         session.flash="Please select a Teritory"
#         redirect(URL(c='report_sales',f='home'))
        
   
    condition=''
   
    
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
       
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
        
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
       
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
        
    records_S="SELECT  depot_id,sl,max(invoice_date),max(cl_category_name),max(payment_mode),max(client_id),max(client_name),max(rep_id),max(rep_name),max(market_name),max(market_id),sum(actual_total_tp) as actual_tp, sum(return_tp+return_sp_discount) as retTP ,sum(vat_total_amount-return_vat) as vat ,sum(discount-return_discount) as discount ,sum(sp_discount-return_sp_discount) as spDiscount FROM sm_invoice_head WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND  invoice_date < '"+str(date_to_m)+"'"+condition+"  GROUP BY depot_id,sl ORDER BY sl;"
#     return records_S
    records=db.executesql(records_S,as_dict = True) 
    
    if records:
        myString='12.4\n\nDepot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString+='Store,'+store_id+'|'+store_name+'\n'
        myString+='Customer,'+customer_id+'|'+customer_name+'\n'
        myString+='Area,'+teritory_id+'|'+teritory_name+'\n'
        myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
        myString=myString+'Date  ,  Inv Number ,DepotID,MaketID,MarketName  ,CustType,SalesTerm,   CustomerID,CustomerName ,   MSOID,MsoName  ,    InvioceTradePrice,    ReturnTradePrice,    NetTP,NetDisc ,NetSpDisc  ,  NetVat ,   NetTradePrice\n'
    
        for i in range(len(records)):
            record=records[i]
            delivery_date =record['max(invoice_date)'].strftime('%d-%b-%Y')
            InvNumber='INV'+str(record['depot_id'])+'-'+str(record['sl'])
            CustomerID =record['max(client_id)']
            CustomerName=record['max(client_name)']
            MSOID=record['max(rep_id)']
            MsoName=record['max(rep_name)']
            MaketID=record['max(market_id)']
            MarketName=record['max(market_name)']
            sale=(record['actual_tp']+record['vat'])-record['discount']-record['spDiscount']
            rSale=record['retTP']
            netSold=(record['actual_tp']-rSale)+record['vat']-record['discount']-record['spDiscount']

            InvioceTradePrice=record['actual_tp']
            ReturnTradePrice=record['retTP']
            NetTP=record['actual_tp']-record['retTP']
            NetDisc =record['discount']
            NetspDiscount=record['spDiscount']
            NetVat    =record['vat']
            NetTradePrice=netSold
    
                                                                                                                                                        
            
            myString=myString+str(delivery_date)+','+str(InvNumber)+','+str(record['depot_id'])+','+str(MaketID)+','+str(MarketName)+','+str(record['max(cl_category_name)'])+','+str(record['max(payment_mode)'])+','+str(CustomerID)+','+str(CustomerName)+','+str(MSOID)+','+str(MsoName)+','+str(InvioceTradePrice)+','+str(ReturnTradePrice)+','+str(NetTP)+','+str(NetDisc)+','+str(NetspDiscount)+','+str(NetVat)+','+str(NetTradePrice)+'\n'
            
    
    
        #Save as csv
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=InvoiceWiseSalesDetail.csv'   
        return str(myString)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))



def causeofRet():  
    c_id=session.cid   
    response.title='Cause of Return Analysis'       
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset((db.sm_return_head.invoice_date >= date_from) & (db.sm_return_head.invoice_date < date_to_m))

#     qset=qset(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_invoice_head.return_tp > 0)  
#     qset=qset(db.sm_invoice_head.status=='Invoiced')    
#     qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
#     qset=qset(db.sm_invoice_head.sl == db.sm_return_head.invoice_sl  )  


    
    qset_inv=db()

    qset_inv=qset_inv(db.sm_invoice_head.cid==c_id)
#     qset_inv=qset_inv(db.sm_invoice_head.return_tp > 0)  
    
#     qset_inv=qset_inv(db.sm_invoice_head.status=='Invoiced')    
    qset_inv=qset_inv((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_return_head.depot_id==depot_id)
        qset_inv=qset_inv(db.sm_invoice_head.depot_id==depot_id)
        
    if (store_id!=''):
        qset=qset(db.sm_return_head.store_id==store_id)   
        qset_inv=qset_inv(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_return_head.client_id==customer_id)
        qset_inv=qset_inv(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_return_head.area_id==teritory_id)
        qset_inv=qset_inv(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_return_head.rep_id==mso_id) 
        qset_inv=qset_inv(db.sm_invoice_head.rep_id==rep_id)
        
    records=qset.select(db.sm_return_head.d_man_id,db.sm_return_head.invoice_date,db.sm_return_head.ret_actual_total_tp.sum(),db.sm_return_head.ret_reason,db.sm_return_head.total_amount.sum(),db.sm_return_head.id.count(), orderby=db.sm_return_head.d_man_id|db.sm_return_head.invoice_date|db.sm_return_head.ret_reason,groupby=db.sm_return_head.d_man_id|db.sm_return_head.invoice_date|db.sm_return_head.ret_reason)
#     return records
#     return db._lastsql
    ret_str=''
    retDeate_past=''
    dman_past=''
    sepPast=''
    for records in records:      
        retDman = records[db.sm_return_head.d_man_id]
        retDeate = records[db.sm_return_head.invoice_date]
        ret_reason= str(records[db.sm_return_head.ret_reason]).upper()
        ret_count= records[db.sm_return_head.id.count()]
        ret_amn= records[db.sm_return_head.ret_actual_total_tp.sum()]
#         ret_amn= records[db.sm_return_head.total_amount.sum()]
#         return ret_amn
#         causeofRet
        
        if ((ret_reason=='CANCELED / CASH SHORT') or (ret_reason=='SHOP CLOSED') or (ret_reason=='NEX DAY DELIVERY') or (ret_reason=='PRODUCT SHORT') or (ret_reason=='NOT DELIVERED') or (ret_reason=='NOT ORDERED') or (ret_reason=='COMPUTER MISTAKE') or (ret_reason=='PART SALE')):
            pass
        else:
            ret_reason='NOT MENTIONED'
        
        sep=str(retDman)+'|'+str(retDeate)
        if sepPast=='':
            ret_str ='<'+str(retDman)+'|'+str(retDeate)+'>'+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        else:
            if sepPast != str(sep):
                ret_str =ret_str+'<'+str(retDman)+'|'+str(retDeate)+'>'+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
            else:
                ret_str=ret_str+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        
        
        retDeate_past=str(retDeate)
        sepPast=sep=str(retDman)+'|'+str(retDeate)
        
#     return ret_str    
    records_inv=qset_inv.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.invoice_date,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.ret_actual_total_tp.sum(), orderby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date,groupby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date)
#     return db._lastsql

    return dict(records_inv=records_inv,ret_str=ret_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)
    
           
def causeofRetD():  
    c_id=session.cid   
    response.title='Cause of Return Analysis'       
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    
    qset=db()
    qset=qset(db.sm_return_head.cid==c_id)
    qset=qset(db.sm_return_head.status=='Returned')
    qset=qset((db.sm_return_head.invoice_date >= date_from) & (db.sm_return_head.invoice_date < date_to_m))

#     qset=qset(db.sm_invoice_head.cid==c_id)
#     qset=qset(db.sm_invoice_head.return_tp > 0)  
#     qset=qset(db.sm_invoice_head.status=='Invoiced')    
#     qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
#     qset=qset(db.sm_invoice_head.sl == db.sm_return_head.invoice_sl  )  


    
    qset_inv=db()

    qset_inv=qset_inv(db.sm_invoice_head.cid==c_id)
#     qset_inv=qset_inv(db.sm_invoice_head.return_tp > 0)  
    
#     qset_inv=qset_inv(db.sm_invoice_head.status=='Invoiced')    
    qset_inv=qset_inv((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_return_head.depot_id==depot_id)
        qset_inv=qset_inv(db.sm_invoice_head.depot_id==depot_id)
        
    if (store_id!=''):
        qset=qset(db.sm_return_head.store_id==store_id)   
        qset_inv=qset_inv(db.sm_invoice_head.store_id==store_id)
        
    if (customer_id!=''):
        qset=qset(db.sm_return_head.client_id==customer_id)
        qset_inv=qset_inv(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_return_head.area_id==teritory_id)
        qset_inv=qset_inv(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_return_head.rep_id==mso_id) 
        qset_inv=qset_inv(db.sm_invoice_head.rep_id==rep_id)
        
    records=qset.select(db.sm_return_head.d_man_id,db.sm_return_head.invoice_date,db.sm_return_head.ret_actual_total_tp.sum(),db.sm_return_head.ret_reason,db.sm_return_head.total_amount.sum(),db.sm_return_head.id.count(), orderby=db.sm_return_head.d_man_id|db.sm_return_head.invoice_date|db.sm_return_head.ret_reason,groupby=db.sm_return_head.d_man_id|db.sm_return_head.invoice_date|db.sm_return_head.ret_reason)
#     return records
#     return db._lastsql
    ret_str=''
    retDeate_past=''
    dman_past=''
    sepPast=''
    for records in records:      
        retDman = records[db.sm_return_head.d_man_id]
        retDeate = records[db.sm_return_head.invoice_date]
        ret_reason= str(records[db.sm_return_head.ret_reason]).upper()
        ret_count= records[db.sm_return_head.id.count()]
        ret_amn= records[db.sm_return_head.ret_actual_total_tp.sum()]
#         ret_amn= records[db.sm_return_head.total_amount.sum()]
#         return ret_amn
#         causeofRet
        
        if ((ret_reason=='CANCELED / CASH SHORT') or (ret_reason=='SHOP CLOSED') or (ret_reason=='NEX DAY DELIVERY') or (ret_reason=='PRODUCT SHORT') or (ret_reason=='NOT DELIVERED') or (ret_reason=='NOT ORDERED') or (ret_reason=='COMPUTER MISTAKE') or (ret_reason=='PART SALE')):
            pass
        else:
            ret_reason='NOT MENTIONED'
        
        sep=str(retDman)+'|'+str(retDeate)
        if sepPast=='':
            ret_str ='<'+str(retDman)+'|'+str(retDeate)+'>'+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        else:
            if sepPast != str(sep):
                ret_str =ret_str+'<'+str(retDman)+'|'+str(retDeate)+'>'+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
            else:
                ret_str=ret_str+'fdfd'+str(ret_reason)+'fdfd'+str(ret_count)+'fdfd'+str(ret_amn)
        
        
        retDeate_past=str(retDeate)
        sepPast=sep=str(retDman)+'|'+str(retDeate)
        
#     return ret_str    
    records_inv=qset_inv.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.invoice_date,db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.ret_actual_total_tp.sum(), orderby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date,groupby=db.sm_invoice_head.d_man_id | db.sm_invoice_head.invoice_date)
#     return db._lastsql

    
    
    myString='18\n\nDateRange,'+date_from+','+date_to+'\n'
    myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n\n'
    
    
        
    myString+='InvoiceDate , Doc/Tp, Invoice, Rerurn ,NextDay Delivery ,Cancelled CashShort , Shop Closed  ,  Product Short  ,  Not Delivered  ,  Not Ordered   , Computer Mistake  ,  Part Sale  ,  Not Mentioned\n'
    
    dp_past=''
    for record in records_inv:
        srt_get=''
        ret_reason= ''
        ret_count_sclosed= 0
        ret_amn_sclosed=0.0
        ret_count_cacShop= 0
        ret_amn_cacShop=0.0
        ret_count_ndd= 0
        ret_amn_ndd=0.0
        ret_count_pShort= 0
        ret_amn_pShort=0.0
        ret_count_nd= 0
        ret_amn_nd=0.0
        ret_count_no= 0
        ret_amn_no=0.0
        ret_count_cm= 0
        ret_amn_cm=0.0
        ret_count_psale= 0
        ret_amn_psale=0.0
        ret_count_nm= 0
        ret_amn_nm=0.0
        
        invoice_date =str(record[db.sm_invoice_head.invoice_date])
        splitstr='<'+str(record[db.sm_invoice_head.d_man_id])+'|'+invoice_date+'>'
        if ret_str.find(splitstr)!=-1:
            srt_get1= ret_str.split(splitstr)[1]
            srt_get= str(record[db.sm_invoice_head.d_man_id])+'|'+invoice_date+srt_get1.split('<')[0]

        reason='CANCELED / CASH SHORT'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_cacShop= int(reasonStr.split('fdfd')[1])
            ret_amn_cacShop= float(reasonStr.split('fdfd')[2])
            
        reason='SHOP CLOSED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_sclosed= int(reasonStr.split('fdfd')[1])
            ret_amn_sclosed= float(reasonStr.split('fdfd')[2])

        reason='NEX DAY DELIVERY'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_ndd= int(reasonStr.split('fdfd')[1])
            ret_amn_ndd= float(reasonStr.split('fdfd')[2])

        reason='PRODUCT SHORT'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_pShort= int(reasonStr.split('fdfd')[1])
            ret_amn_pShort= float(reasonStr.split('fdfd')[2])

        reason='NOT DELIVERED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_nd= int(reasonStr.split('fdfd')[1])
            ret_amn_nd= float(reasonStr.split('fdfd')[2])

        reason='NOT ORDERED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_no= int(reasonStr.split('fdfd')[1])
            ret_amn_no= float(reasonStr.split('fdfd')[2])
              
        reason='COMPUTER MISTAKE'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_cm= int(reasonStr.split('fdfd')[1])
            ret_amn_cm= float(reasonStr.split('fdfd')[2])
                
        reason='PART SALE'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_psale= int(reasonStr.split('fdfd')[1])
            ret_amn_psale= float(reasonStr.split('fdfd')[2])

        reason='NOT MENTIONED'
        if (srt_get.find(reason)!=-1):
            reasonStr=srt_get.split(reason)[1]
            ret_count_nm= int(reasonStr.split('fdfd')[1])
            ret_amn_nm= float(reasonStr.split('fdfd')[2])
        
        total_ret_count=ret_count_cacShop+ret_count_sclosed+ret_count_ndd+ret_count_pShort+ret_count_nd+ret_count_no+ret_count_cm+ret_count_psale+ret_count_nm
#         total_retamn=ret_amn_cacShop+ret_amn_sclosed+ret_amn_ndd+ret_amn_pShort+ret_amn_nd+ret_amn_no+ret_amn_cm+ret_amn_psale+ret_amn_nm
        total_retamn=record[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
#         return total_retamn
        
        if ( dp_past!=record[db.sm_invoice_head.d_man_id]):
              myString=myString+'Delivery Person: '+str(record[db.sm_invoice_head.d_man_id])+'-'+str(record[db.sm_invoice_head.d_man_name])+'\n'
                                                                                                                                                                       
        myString=myString+str(record[db.sm_invoice_head.invoice_date])+','+'Document'+','+str(record[db.sm_invoice_head.id.count()])+','+str(total_ret_count)+','+str(ret_count_ndd)+','+str(ret_count_cacShop)+','+str(ret_count_sclosed)+','+str(ret_count_pShort)+','+str(ret_count_nd)+','+str(ret_count_no)+','+str(ret_count_cm)+','+str(ret_count_psale)+','+str(ret_count_nm)+'\n'
        myString=myString+','+'TP'+','+str(record[db.sm_invoice_head.actual_total_tp.sum()])+','+str(total_retamn)+','+str(ret_amn_ndd)+','+str(ret_amn_cacShop)+','+str(ret_amn_sclosed)+','+str(ret_amn_pShort)+','+str(ret_amn_nd)+','+str(ret_amn_no)+','+str(ret_amn_cm)+','+str(ret_amn_psale)+','+str(ret_amn_nm)+'\n'
        dp_past=record[db.sm_invoice_head.d_man_id]


    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=CauseofReturn.csv'   
    return str(myString) 
    
    

            
def summaryReport():  
    c_id=session.cid   
    response.title='Summary Report'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))

    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)   
    if (customer_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (teritory_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id) 
        
    records=qset_sum.select(db.sm_invoice_head.level1_id,db.sm_invoice_head.level2_id,db.sm_invoice_head.level3_id,  db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_tp-db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount).sum(),(db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id)
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)   

def summaryReportD():  
    c_id=session.cid   
    response.title='Summary Report'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))

    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)   
    if (customer_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
    if (teritory_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id) 
        
    records=qset_sum.select(db.sm_invoice_head.level1_id,db.sm_invoice_head.level2_id,db.sm_invoice_head.level3_id,db.sm_invoice_head.actual_total_tp.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_tp-db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount).sum(),(db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id,groupby=db.sm_invoice_head.level1_id|db.sm_invoice_head.level2_id|db.sm_invoice_head.level3_id)
    
    #REmove , from record.Cause , means new column in excel    
    myString='11\n\n Daterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    
    
   
    
   
        
    myString+='RSM ,  FM ,  TR, InvCount ,InvTotalTP, InvVat ,  InvDisc ,InvSPDisc,InvAmount,RetTotalTP ,RetVat,  RetDisc ,RetSPDisc,RetAmount, Net\n'
    
    rsm_past=''
    fm_past=''
    tr_past=''
    for records in records:
        rsm=records[db.sm_invoice_head.level1_id]
#         rsm_name=records[db.sm_invoice_head.level1_name]
        fm=records[db.sm_invoice_head.level2_id]
#         fm_name=records[db.sm_invoice_head.level2_name]
        tr=records[db.sm_invoice_head.level3_id]
#         tr_name=records[db.sm_invoice_head.level3_name]
        invCount=records[db.sm_invoice_head.id.count()]
        invtTP=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        invVat=records[db.sm_invoice_head.vat_total_amount.sum()]
        invSpDisc=records[db.sm_invoice_head.sp_discount.sum()]
        invRDisc=records[db.sm_invoice_head.discount.sum()]
        invDisc=records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]
        invAmn=records[db.sm_invoice_head.total_amount.sum()]
#         rettTP=records[db.sm_invoice_head.return_tp.sum()]
        rettTP=records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
        retVat=records[db.sm_invoice_head.return_vat.sum()]
        retDisc=records[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
        retSPDisc=records[db.sm_invoice_head.return_sp_discount.sum()]
        retRDisc=records[db.sm_invoice_head.return_discount.sum()]
        retAmn=float(records[db.sm_invoice_head.return_tp.sum()])+float(records[db.sm_invoice_head.return_vat.sum()])-(float(records[db.sm_invoice_head.return_discount.sum()])+float(records[db.sm_invoice_head.return_sp_discount.sum()]))+float(records[db.sm_invoice_head.return_sp_discount.sum()])
        
        net=records[db.sm_invoice_head.total_amount.sum()]-retAmn
    
    

         
              
        myString+=str(rsm)+','+str(fm)+','+str(tr)+','+str(invCount)+','+str(invtTP)+','+str(invVat)+','+str(invRDisc)+','+str(invSpDisc)+','+str(invAmn)+','+str(rettTP)+','+str(retVat)+','+str(retRDisc)+','+str(retSPDisc)+','+str(retAmn)+','+str(net)+'\n'
        
        
        
#         rsm_past=records[db.sm_invoice_head.level1_id]
#         fm_past=records[db.sm_invoice_head.level2_id]
#         tr_past=records[db.sm_invoice_head.level3_id]
        
       
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=SummaryReport.csv'   
    return str(myString) 
    
#     return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name,  mso_id=mso_id, mso_name=mso_name)   

def dp_wise_sale_ss():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.actual_total_tp == (db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)

     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
    if records:
        return dict(records=records,dmanList=dmanList,invCList=invCList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))

def dp_wise_sale_ssD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.actual_total_tp == (db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name.max(),db.sm_invoice_head.id.count(),db.sm_invoice_head.actual_total_tp.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)

     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
            
    
    #REmove , from record.Cause , means new column in excel    
    myString='15\n\nDaterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Teritory,'+teritory_id+'|'+teritory_name+'\n'
    myString+='DeliveryMan,'+dman_id+'|'+dman_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Market,'+market_id+'|'+market_name+'\n\n'
    
   
        
    myString+='DP ID ,   Delivery Person Name ,   No of Inv.  ,  Full Return No  ,  Inv Amnt ,   Ret Amnt ,   Exec%  ,  Ret%  ,  Net Sold TP\n'
    
    invTotal=0
    retTotal=0
    invTamn=0
    retTamn=0
    ntTotal=0
    saleTotal=0
    netSoldTotal=0
    for records in records:

        retCount=0
        d_man_id=records[db.sm_invoice_head.d_man_id]
        if [s for s in dmanList if d_man_id in s]:
            index_element = dmanList.index(d_man_id)           
            retCount=invCList[index_element]
        d_man_id=records[db.sm_invoice_head.d_man_id]
        d_man_name=records[db.sm_invoice_head.d_man_name.max()]
        noInvCount=records[db.sm_invoice_head.id.count()]
        invTotal=invTotal+records[db.sm_invoice_head.id.count()]
        
        retTotal=retTotal+retCount
        invAmn=(records[db.sm_invoice_head.actual_total_tp.sum()])
        
        invTamn=invTamn+invAmn
        
        retAmn=records[(db.sm_invoice_head.return_tp+db.sm_invoice_head.return_sp_discount).sum()]
        
        retTamn=retTamn+retAmn
        sale=records[db.sm_invoice_head.actual_total_tp.sum()]
        netSold=records[db.sm_invoice_head.actual_total_tp.sum()]-retAmn
    
    
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        eP=(netSold*100)/sale
        rP=(retAmn*100)/sale

        ntTotal=ntTotal+(invAmn-retAmn)
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        ePTotal=(netSoldTotal*100)/saleTotal
        rPTotal=(retTamn*100)/saleTotal
         
               
        myString+=str(d_man_id)+','+str(d_man_name)+','+str(noInvCount)+','+str(retCount)+','+str(invAmn)+','+str(retAmn)+','+str(round(eP,2))+','+str(round(rP,2))+','+str(netSold)+'\n'
      
#     myString+='\n\n,,'+str(invTotal)+','+str(retTotal)+','+str(invTamn)+','+str(retTamn)+','+str(ePTotal)+','+str(rPTotal)+','+str(ntTotal)+'\n'     
#     return myString
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DeliveryPersonWiseSalesStatement.csv'   
    return str(myString) 

    
def dp_wise_sale_ssTPD():
    c_id=session.cid   
#     return c_id
    response.title='Delivery Person Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return dman_id
        
#     if (dman_id==""):
#         session.flash="Please select deliery person."
#         redirect(URL(c='report_sales',f='home'))
        
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=db()
    qset_fr=qset_fr(db.sm_invoice_head.cid==c_id)
    qset_fr=qset_fr(db.sm_invoice_head.status=='Invoiced')
    qset_fr=qset_fr((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    qset_fr=qset_fr(db.sm_invoice_head.total_amount == ((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_vat)-(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount)))

    if (depot_id!=''):
        qset=qset(db.sm_invoice_head.depot_id==depot_id)
        qset_fr=qset_fr(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice_head.store_id==store_id)   
        qset_fr=qset_fr(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice_head.client_id==client_id)
        qset_fr=qset_fr(db.sm_invoice_head.client_id==client_id)
    if (teritory_id!=''):
        qset=qset(db.sm_invoice_head.area_id==teritory_id)
        qset_fr=qset_fr(db.sm_invoice_head.area_id==teritory_id)
    if (mso_id!=''):
        qset=qset(db.sm_invoice_head.rep_id==mso_id) 
        qset_fr=qset_fr(db.sm_invoice_head.rep_id==mso_id) 
    if (dman_id!=''):
        qset=qset(db.sm_invoice_head.d_man_id==dman_id)
        qset_fr=qset_fr(db.sm_invoice_head.d_man_id==dman_id) 
    if (market_id!=''):
        qset=qset(db.sm_invoice_head.market_id==market_id)
        qset_fr=qset_fr(db.sm_invoice_head.market_id==market_id)

        
    records=qset.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.d_man_name,db.sm_invoice_head.id.count(),db.sm_invoice_head.total_amount.sum(),db.sm_invoice_head.vat_total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
    records_fr=qset_fr.select(db.sm_invoice_head.d_man_id,db.sm_invoice_head.id.count(), orderby=db.sm_invoice_head.d_man_id,groupby=db.sm_invoice_head.d_man_id)
#     return records_fr
#     return db._lastsql
     
    dmanList=[]
    invCList=[]
    for records_fr in records_fr:
        dman_id = records_fr[db.sm_invoice_head.d_man_id]
        invCount = records_fr[db.sm_invoice_head.id.count()]
        dmanList.append(dman_id)
        invCList.append(invCount)
            
    
    #REmove , from record.Cause , means new column in excel    
    myString='Daterange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='Teritory,'+teritory_id+'|'+teritory_name+'\n'
    myString+='DeliveryMan,'+dman_id+'|'+dman_name+'\n'
    myString+='Customer,'+customer_id+'|'+customer_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Market,'+market_id+'|'+market_name+'\n\n'
    
   
        
    myString+='DP ID ,   Delivery Person Name ,   No of Inv.  ,  Full Return No  ,  Inv Amnt ,   Ret Amnt ,   Exec%  ,  Ret%  ,  Net Sold TP\n'
    
    invTotal=0
    retTotal=0
    invTamn=0
    retTamn=0
    ntTotal=0
    saleTotal=0
    netSoldTotal=0
    for records in records:
        retCount=0
        d_man_id=records[db.sm_invoice_head.d_man_id]
        if [s for s in dmanList if d_man_id in s]:
            index_element = dmanList.index(d_man_id)           
            retCount=invCList[index_element]
        d_man_id=records[db.sm_invoice_head.d_man_id]
        d_man_name=records[db.sm_invoice_head.d_man_name]
        noInvCount=records[db.sm_invoice_head.id.count()]
        invTotal=invTotal+records[db.sm_invoice_head.id.count()]
        retTotal=retTotal+retCount
        invAmn=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]

        invTamn=invTamn+invAmn
        retAmn=records[db.sm_invoice_head.return_tp.sum()]
        retTamn=retTamn+retAmn
        sale=records[db.sm_invoice_head.total_amount.sum()]
        netSold=records[db.sm_invoice_head.total_amount.sum()]-retAmn
    
    
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        eP=(netSold*100)/sale
        rP=(retAmn*100)/sale
#         ntSTP=(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        
        ntTotal=ntTotal+(records[db.sm_invoice_head.total_amount.sum()]+records[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()])-records[db.sm_invoice_head.vat_total_amount.sum()]
        saleTotal=saleTotal+sale
        netSoldTotal=netSoldTotal+netSold
        ePTotal=(netSoldTotal*100)/saleTotal
        rPTotal=(retTamn*100)/saleTotal
         
               
        myString+=str(d_man_id)+','+str(d_man_name)+','+str(noInvCount)+','+str(retCount)+','+str(invAmn)+','+str(retAmn)+','+str(eP)+','+str(rP)+','+str(netSold)+'\n'
      
    myString+='\n\n,,'+str(invTotal)+','+str(retTotal)+','+str(invTamn)+','+str(retTamn)+','+str(ePTotal)+','+str(rPTotal)+','+str(ntTotal)+'\n'     
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DeliveryPersonWiseSalesStatementTP.csv'   
    return str(myString) 
    
      
      
def salesClosingStockS():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum(),((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id)
#     return db._lastsql
    itemList=[]
    itemQtyList=[]
    sateQtyList=[]
    retQtyList=[]
    itemSList=[]
    totalSaleTP=0
    for records_inv in records_inv:
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()]
        
#         saleQty=records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
#         retQty=records_inv[(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum()]
        
        itemS=records_inv[(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum()]
#         itemTP=records_inv[db.sm_invoice.actual_tp]
        totalSaleTP=totalSaleTP+itemS
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemSList.append(itemS)
#         sateQtyList.append(saleQty)
#         retQtyList.append(retQty)
#         itemTPList.append(itemTP)
#     return totalTp
    qset_inv_note=db()
    qset_inv_note=qset_inv_note(db.sm_invoice.cid==c_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.depot_id==depot_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.store_id==store_id)
    
    qset_inv_note=qset_inv_note(db.sm_invoice.status=='Invoiced')
    qset_inv_note=qset_inv_note((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv_note=qset_inv_note.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id| db.sm_invoice.actual_tp)
#     return records_inv_note

    
    item_str=""
    item_past=''
    for records_inv_note in records_inv_note:
        item_id = records_inv_note[db.sm_invoice.item_id]
        itemQty = records_inv_note[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemTP = records_inv_note[db.sm_invoice.actual_tp]
        
        if item_past!=item_id:           
           item_str=item_str+"Item"+str(item_id)
           note=""
           tp=""
        if tp=='':
            tp=str(itemTP)  
        else:
            tp=tp+','+str(itemTP) 
        if note=='':
            note="("+str(itemTP)+"*"+str(itemQty)+")" 
        else:
            note=note+'+'+"("+str(itemTP)+"*"+str(itemQty)+")"
        
        item_str=item_str+"TP"+tp+"Note"+note
        
        item_past=item_id
             
    return dict(records=records,itemList=itemList,itemQtyList=itemQtyList,itemSList=itemSList,item_str=item_str,totalSaleTP=totalSaleTP,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

def salesClosingStockSD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum(),((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id)
#     return db._lastsql
    itemList=[]
    itemQtyList=[]
    sateQtyList=[]
    retQtyList=[]
    itemSList=[]
    totalSaleTP=0
    for records_inv in records_inv:
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()]
        
#         saleQty=records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
#         retQty=records_inv[(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty).sum()]
        
        itemS=records_inv[(db.sm_invoice.actual_tp*((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty))).sum()]
#         itemTP=records_inv[db.sm_invoice.actual_tp]
        totalSaleTP=totalSaleTP+itemS
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemSList.append(itemS)
#         sateQtyList.append(saleQty)
#         retQtyList.append(retQty)
#         itemTPList.append(itemTP)
#     return totalTp
    qset_inv_note=db()
    qset_inv_note=qset_inv_note(db.sm_invoice.cid==c_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.depot_id==depot_id)
    qset_inv_note=qset_inv_note(db.sm_invoice.store_id==store_id)
    
    qset_inv_note=qset_inv_note(db.sm_invoice.status=='Invoiced')
    qset_inv_note=qset_inv_note((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv_note=qset_inv_note.select(db.sm_invoice.item_id,db.sm_invoice.actual_tp,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.item_id,groupby=db.sm_invoice.item_id| db.sm_invoice.actual_tp)
#     return records_inv_note

    
    item_str=""
    item_past=''
    for records_inv_note in records_inv_note:
        item_id = records_inv_note[db.sm_invoice.item_id]
        itemQty = records_inv_note[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemTP = records_inv_note[db.sm_invoice.actual_tp]
        
        if item_past!=item_id:           
           item_str=item_str+"Item"+str(item_id)
           note=""
           tp=""
        if tp=='':
            tp=str(itemTP)  
        else:
            tp=tp+','+str(itemTP) 
        if note=='':
            note="("+str(itemTP)+"*"+str(itemQty)+")" 
        else:
            note=note+'+'+"("+str(itemTP)+"*"+str(itemQty)+")"
        
        item_str=item_str+"TP"+tp+"Note"+note
        
        item_past=item_id
         
        
            
#CSV  
    myString='DateRange,'+date_from+'-'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    

        
    myString+='Item  ,  ItemName  ,  SalesTP   , SalesS.Qty  ,  SalesTP*S.Qty   , Notes  ,  SalesSClosing stock Qty   , StockTP  ,  StockTP*Closing stock Qty\n'
    
    totalStockTP=0
    for record in records:
        item_id =record[db.sm_item.item_id]
        itemQty=0
        itemS=0
    
        if [s for s in itemList if item_id in s]:
            index_element = itemList.index(item_id)
            itemQty=itemQtyList[index_element]
            itemS=itemSList[index_element]
        
        item_idF="Item"+str(record[db.sm_item.item_id]+"TP")
        tp=''
        Note=''
        item_str_get=''
        if (item_str.find(item_idF)!=-1):
            item_str_get=item_str.split(item_idF)[1].split("Item")[0] 
            item_strList= item_str_get.split("TP")
            for i in range(len(item_strList)):
                tp=item_strList[i].split("Note")[0].replace(',','/')
                Note=item_strList[i].split("Note")[1].replace(',','')

        
      
        totalStockTP=totalStockTP + record[(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum()]
        myString+=str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(tp)+','+str(itemQty)+','+str(itemS)+','+str(Note)+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','+str(record[db.sm_item.price])+','+str(record[(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum()])+'\n'
    myString+=',,,,'+str(totalSaleTP)+',,,,'+str(totalStockTP)+'\n'
              
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=salesClosingStockS.csv'   
    return str(myString)    
    

def salesClosingStockSB():
    c_id=session.cid   
#     return c_id
    response.title='B Sales Closing StockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum(),orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    itemList=[]
    itemQtyList=[]
    itemTPList=[]
    stTPList=[]
    totalSTP=0
    for records in records:
        item_id = records[db.sm_item.item_id]
        itemQty = records[db.sm_depot_stock_balance.quantity.sum()]
        itemP=records[db.sm_item.price]
#         stTP=float(records[(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum()])
        stTP=itemP*itemQty
        totalSTP=totalSTP+stTP
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemTPList.append(itemP)
        stTPList.append(stTP)
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),orderby=db.sm_invoice.item_name | db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id | db.sm_invoice.actual_tp)
   
   
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.quantity>0)
    
    qsetStock=qsetStock(db.sm_item.cid==c_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    recordsStock=qsetStock.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
#     return recordsStock
    return dict(records_inv=records_inv,recordsStock=recordsStock,itemList=itemList,itemQtyList=itemQtyList,itemTPList=itemTPList,stTPList=stTPList,totalSTP=totalSTP,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name)

def salesClosingStockSBD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum(),orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    itemList=[]
    itemQtyList=[]
    itemTPList=[]
    stTPList=[]
    totalSTP=0
    for records in records:
        item_id = records[db.sm_item.item_id]
        itemQty = records[db.sm_depot_stock_balance.quantity.sum()]
        itemP=records[db.sm_item.price]
#         stTP=float(records[(db.sm_depot_stock_balance.quantity*db.sm_item.price).sum()])
        stTP=itemP*itemQty
        totalSTP=totalSTP+stTP
        itemList.append(item_id)
        itemQtyList.append(itemQty)
        itemTPList.append(itemP)
        stTPList.append(stTP)
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),orderby=db.sm_invoice.item_name | db.sm_invoice.actual_tp,groupby=db.sm_invoice.item_id | db.sm_invoice.actual_tp)
   
   
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.quantity>0)
    
    qsetStock=qsetStock(db.sm_item.cid==c_id)
    qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)
    
       
    recordsStock=qsetStock.select(db.sm_item.item_id,db.sm_item.name,db.sm_depot_stock_balance.quantity.sum(),(db.sm_depot_stock_balance.quantity * db.sm_item.price).sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    #CSV  
    myString='DateRange,'+date_from+'-'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='Item  ,  ItemName  ,  SalesTP   , SalesS.Qty  ,  SalesTP*S.Qty  ,  SalesSClosing stock Qty   , StockTP  ,  StockTP*Closing stock Qty\n'
    
    totalSaleTP=0
    STP_total=0.0
    pastItem=''
    itemStr=''
    for records_inv in records_inv:
        item_id =records_inv[db.sm_invoice.item_id]
        itemStr=itemStr+str(item_id)+'rdrd'
        itemQty=0
        itemS=0
        itemTP=0
        stTP=0
        if [s for s in itemList if item_id in s]:
              index_element = itemList.index(item_id)
              itemQty=itemQtyList[index_element]
              itemTP=itemTPList[index_element]
              stTP=stTPList[index_element]
        
        
#         totalSaleTP=totalSaleTP+records_inv[(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum()]
        totalSaleTP=totalSaleTP+records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()] * records_inv[db.sm_invoice.actual_tp]
        
        if pastItem!=records_inv[db.sm_invoice.item_id]:
            STP_total=STP_total+stTP
            myString+=str(records_inv[db.sm_invoice.item_id])+','+str(records_inv[db.sm_invoice.item_name])+','+str(records_inv[db.sm_invoice.actual_tp])+','+str(records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()])+','+str(records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()] * records_inv[db.sm_invoice.actual_tp])+','+str(itemQty)+','+str(itemTP)+','+str(stTP)+'\n'
        else:
            myString+=str(records_inv[db.sm_invoice.item_id])+','+str(records_inv[db.sm_invoice.item_name])+','+str(records_inv[db.sm_invoice.actual_tp])+','+str(records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()])+','+str(records_inv[((db.sm_invoice.quantity+db.sm_invoice.bonus_qty)-(db.sm_invoice.return_qty+db.sm_invoice.return_bonus_qty)).sum()] * records_inv[db.sm_invoice.actual_tp])+','+','+','+'\n'
        pastItem=records_inv[db.sm_invoice.item_id]
        
    myString=myString+'*Stock available but not sold within the period'+'\n'
    for recordsStock in recordsStock:
        item_idCheck =recordsStock[db.sm_item.item_id]
        if itemStr.find(item_idCheck)==-1:    
            STP_total=STP_total+float(recordsStock[(db.sm_depot_stock_balance.quantity).sum()]*recordsStock[db.sm_item.price])
            myString+=str(recordsStock[db.sm_item.item_id])+','+str(recordsStock[db.sm_item.name])+','+','+','+','+str(recordsStock[db.sm_depot_stock_balance.quantity.sum()])+','+str(recordsStock[db.sm_item.price])+','+str(recordsStock[(db.sm_depot_stock_balance.quantity).sum()]*recordsStock[db.sm_item.price])+'\n'
    myString+=',,,,'+str(totalSaleTP)+',,,'+str(STP_total)+'\n'
              
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=salesClosingStockSB.csv'   
    return str(myString)    
        
        
        
#  =====================       
def discPWise():
    c_id=session.cid   
#     return c_id
    response.title='discPWise'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return item_id
        
    qset=db()
    qset=qset(db.sm_item.cid==c_id)
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    

    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
    
    
    records_invStr="SELECT  item_id, discount_type ,actual_tp,item_discount,sum(quantity-return_qty) as soldQty,sum(bonus_qty-return_bonus_qty) as bonusQty,sum(item_discount) as discount_amn,sum(quantity*actual_tp) as  acTP,sum(return_qty*actual_tp) as  retTP FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,discount_type ORDER BY item_id;"
#     return records_invStr
    records_inv=db.executesql(records_invStr,as_dict = True) 
    itemPast=''
    invString=''
    for record_inv in records_inv:
        item_id_check = record_inv['item_id']
        discount_type=record_inv['discount_type']
        discount_amn=record_inv['discount_amn']
        soldQty=record_inv['soldQty']
        bonusQty=record_inv['bonusQty']
        acTP=record_inv['acTP']#-record_inv['retTP']
        
#         return 'aa'
        if itemPast!=item_id_check:
            invString=invString+'<'+str(item_id_check)+'>'  
        invString=invString+str(discount_type)+','+str(discount_amn)+','+str(soldQty)+','+str(bonusQty)+','+str(acTP)+'rdrd'
        itemPast=record_inv['item_id']
    invString=invString+'<'   

#     return db._lastsql
    #return item_id
    
    dateRecordsH="SELECT  DISTINCT item_id, count(sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id ORDER BY item_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    itemList=[]
    invCountList=[]
    for records_head in records_head:
#         return records_head['invcount']
        itemList.append(records_head['item_id'])
        invCountList.append(records_head['invcount'])
        
    
    return dict(records=records,invString=invString,itemList=itemList,invCountList=invCountList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)
def discPWiseD():
    c_id=session.cid   
#     return c_id
    response.title='discPWise'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
#     return item_id
        
    qset=db()
    qset=qset(db.sm_item.cid==c_id)
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+"AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+"AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id= '"+str(fm_id)+"'"
    
    
    records_invStr="SELECT  item_id, discount_type ,actual_tp,item_discount,sum(quantity-return_qty) as soldQty,sum(bonus_qty-return_bonus_qty) as bonusQty,sum(item_discount) as discount_amn,sum(quantity*actual_tp) as  acTP,sum(return_qty*actual_tp) as  retTP FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,discount_type ORDER BY item_id;"
#     return records_invStr
    records_inv=db.executesql(records_invStr,as_dict = True) 
    itemPast=''
    invString=''
    for record_inv in records_inv:
        item_id_check = record_inv['item_id']
        discount_type=record_inv['discount_type']
        discount_amn=record_inv['discount_amn']
        soldQty=record_inv['soldQty']
        bonusQty=record_inv['bonusQty']
        acTP=record_inv['acTP']#-record_inv['retTP']
        
#         return 'aa'
        if itemPast!=item_id_check:
            invString=invString+'<'+str(item_id_check)+'>'  
        invString=invString+str(discount_type)+','+str(discount_amn)+','+str(soldQty)+','+str(bonusQty)+','+str(acTP)+'rdrd'
        itemPast=record_inv['item_id']
    invString=invString+'<'   

#     return db._lastsql
    #return item_id
    
    dateRecordsH="SELECT  DISTINCT item_id, count(sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id ORDER BY item_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    itemList=[]
    invCountList=[]
    for records_head in records_head:
#         return records_head['invcount']
        itemList.append(records_head['item_id'])
        invCountList.append(records_head['invcount'])
    
    
        
    myString='22\n\nDiscount and Bonus Statement- Product wisel\n'
    myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
    myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString=myString+'Store,'+store_id+'|'+store_name+'\n'
    myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
    myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
    myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n'
    myString=myString+'Item,'+item_id+'|'+item_name+'\n'
    myString=myString+'RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString=myString+'FM,'+fm_id+'|'+fm_name+'\n\n'
    myString=myString+'Item  ,  ItemName  ,  RcentPrice   , SoldQty ,   BonusQty ,   TradePrice ,   TotalDisc  ,  RegularDisc ,   SpecialDisc ,   Discount%  ,  InvCount\n'
    TotalTP=0.00
    Tdisc=0.00
    Rdisc=0.00
    Sdisc=0.00
    Tinv=0
    for record in records:
        soldQtyT=0
        bonusQtyT=0
        discount_amn_rdT=0
        discount_amn_spT=0
        acTPT=0
        itm_id=record[db.sm_item.item_id]
        if invString.find('<'+itm_id+'>')!=-1:
            itemStr1=invString.split('<'+itm_id+'>')[1]
            itemSingle=itemStr1.split('<')[0]
            itemStrSingle=itemSingle.split('rdrd')
            soldQtyT=0
            bonusQtyT=0
            discount_amn_rdT=0
            discount_amn_spT=0
            acTPT=0
            i=0
            while i < len(itemStrSingle)-1:
                discount_type=itemStrSingle[i].split(',')[0]
                discount_amn_rd=0
                discount_amn_sp=0
                if discount_type=='RD':
                    discount_amn_rd=itemStrSingle[i].split(',')[1]
                else:
                    discount_amn_sp=itemStrSingle[i].split(',')[1]

                discount_amn=itemStrSingle[i].split(',')[1]
                soldQty=itemStrSingle[i].split(',')[2]
                bonusQty=itemStrSingle[i].split(',')[3]
                acTP=itemStrSingle[i].split(',')[4]
                soldQtyT=soldQtyT+int(soldQty)
                bonusQtyT=bonusQtyT+int(bonusQty)
                discount_amn_rdT=discount_amn_rdT+float(discount_amn_rd)
                discount_amn_spT=discount_amn_spT+float(discount_amn_sp)
                #acTPT=float(acTP)*float(soldQty)
                acTPT=acTPT+float(acTP)
                i=i+1
                        
        dicP=0
        if float(acTPT) > 0:
            dicP=((discount_amn_rdT+discount_amn_spT)/float(acTPT))*100        
        invCount=0
        if [s for s in itemList if itm_id in s]:
            index_element = itemList.index(itm_id)           
            invCount=invCountList[index_element]                 
                        
        myString+=str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(soldQtyT)+','+str(bonusQtyT)+','+str(acTPT)+','+str(discount_amn_rdT+discount_amn_spT)+','+str(discount_amn_rdT)+','+str(discount_amn_spT)+','+str(round(dicP,2))+','+str(invCount)+'\n'
#         return myString
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=discPWiseD.csv'   
    return str(myString)  
# ==========================Sales Comparision===========================    
def msoSCTop():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.item_id,db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.item_id | db.sm_invoice.category_id |db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id |db.sm_invoice.item_id | db.sm_invoice.category_id)
    
    invDict={}
    invList=[]
    itemList=[]
    for records_sum in records_sum:
        item_id= records_sum[db.sm_invoice.item_id]
        category_id = records_sum[db.sm_invoice.category_id]
        itemQty = records_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= records_sum[db.sm_invoice.level1_id]
        fm= records_sum[db.sm_invoice.level2_id]
        tr= records_sum[db.sm_invoice.level3_id]
        itemList.append(item_id)
        invDict={'item_id':item_id,'category_id':category_id,'itemQty':itemQty,'rsm':rsm,'fm':fm,'tr':tr}
        invList.append(invDict)
    return dict(records=records,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)


def msoSCTopD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.item_id,db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.item_id | db.sm_invoice.category_id |db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id |db.sm_invoice.item_id | db.sm_invoice.category_id)
    
    invDict={}
    invList=[]
    itemList=[]
    for records_sum in records_sum:
        item_id= records_sum[db.sm_invoice.item_id]
        category_id = records_sum[db.sm_invoice.category_id]
        itemQty = records_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= records_sum[db.sm_invoice.level1_id]
        fm= records_sum[db.sm_invoice.level2_id]
        tr= records_sum[db.sm_invoice.level3_id]
        itemList.append(item_id)
        invDict={'item_id':item_id,'category_id':category_id,'itemQty':itemQty,'rsm':rsm,'fm':fm,'tr':tr}
        invList.append(invDict)
    
#     CSV
    #REmove , from record.Cause , means new column in excel    
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n'
    
    
    
        
    myString+='Item   , ItemName ,   TP ,   Stock ,   RSM  ,  FM  ,  TR ,   A  ,  B  ,  C  ,  Bonus\n'
    
    
    pastItem=''
    pastRsm=''
    pastFm=''
    pastTr=''
    for records in records:
        item_id=records[db.sm_item.item_id]
        if [s for s in itemList if item_id in s]:
            index_element = itemList.index(item_id)           
            itemCount= itemList.count(item_id)    
            c=index_element
            while c < index_element+itemCount: 
                qtyA=0
                qtyB=0
                qtyC=0  
                qtyBonus=0
                if invList[c]['category_id']=='A':
                    qtyA=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='B':
                    qtyB=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='C':
                    qtyC=str(invList[c]['itemQty'])
                elif invList[c]['category_id']=='BONUS':
                    qtyBonus=str(invList[c]['itemQty']) 
#                 if pastItem!=records[db.sm_item.item_id]:
#                     myString=myString+'\n'
                myString=myString+str(records[db.sm_item.item_id])+','+str(records[db.sm_item.name])+','+str(records[db.sm_item.price])+','+str(records[db.sm_depot_stock_balance.quantity.sum()])+','+str(invList[c]['rsm']) +','+str(invList[c]['fm'])+','+str(invList[c]['tr'])+','+str(qtyA)+','+str(qtyB) +','+str(qtyC)+','+str(qtyBonus)                   
                pastItem=records[db.sm_item.item_id]
                pastRsm=invList[c]['rsm']
                pastFm=invList[c]['fm']
                pastTr=invList[c]['tr']
                c=c+1
                myString=myString+'\n'

         
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=msoSCTop.csv'   
    return str(myString) 
    
    
    
    return dict(records=records,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

def msoSCTopSum():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.category_id,groupby=db.sm_item.category_id)
#     prodDict={}
#     prodList=[]
#     prodcatList=[]
#     for record in records:
#         item_id= record[db.sm_item.item_id]
#         item_name= record[db.sm_item.name]
#         category_id = record[db.sm_item.category_id]
#         stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
#         TP= record[db.sm_item.price]
#          
#         prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
#         prodList.append(prodDict)
#         prodcatList.append(category_id)
    
    
#     Summary
    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    if (depot_id!=''):
        qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        qset_sum=qset_sum(db.sm_invoice.store_id==store_id)                  
    records_sum=qset_sum.select(db.sm_invoice.category_id,db.sm_invoice.level1_id,db.sm_invoice.level2_id,db.sm_invoice.level3_id,db.sm_invoice.level1_name,db.sm_invoice.level2_name,db.sm_invoice.level3_name  ,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(), orderby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id|db.sm_invoice.category_id ,groupby=db.sm_invoice.level1_id|db.sm_invoice.level2_id|db.sm_invoice.level3_id | db.sm_invoice.category_id)
#     return records_sum
    invDict={}
    invList=[]
    itemList=[]
    qtyA=0
    qtyB=0
    qtyC=0
    qtyBonus=0
    tr_past=''
    qty_str1=''
    qty_str=''
    for record_sum in records_sum:
        category_id = record_sum[db.sm_invoice.category_id]
        itemQty = record_sum[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        rsm= record_sum[db.sm_invoice.level1_id]
        fm= record_sum[db.sm_invoice.level2_id]
        tr= record_sum[db.sm_invoice.level3_id]
        if category_id=='A':
            qtyA=itemQty
        if category_id=='B':
            qtyA=itemQty
        if category_id=='C':
            qtyA=itemQty
        if category_id=='BONUS':
            qtyA=itemQty
            
        itemList.append(category_id)
        
        if tr_past!=tr :
                qty_str=qty_str+'<fdrd>'+str(tr)
        qty_str=qty_str+str(qtyA)+','+str(qtyB)+','+str(qtyC)+','+str(qtyBonus)+'<rd>'        
        
        tr_past=tr
        
        
        
        
        
        
#     return qty_str
        
#         if tr_past!=tr:
#             if tr_past!='':
#                 qty_str1=
#                 invDict={'category_id':category_id,'qtyA':qtyA,'qtyB':qtyB,'qtyC':qtyC,'qtyA':qtyA,'rsm':rsm,'fm':fm,'tr':tr}
#                 invList.append(invDict)
    
        
    return dict(records_sum=records_sum,qty_str=qty_str,invList=invList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)
 
def msoSC():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

        
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    qset=qset(db.sm_depot_stock_balance.store_id==store_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    
    
    qset_tr=db()
    qset_tr=qset_tr(db.sm_invoice.cid==c_id)
    qset_tr=qset_tr(db.sm_invoice.depot_id==depot_id)
    qset_tr=qset_tr(db.sm_invoice.store_id==store_id)
    qset_tr=qset_tr(db.sm_invoice.status=='Invoiced')
    qset_tr=qset_tr((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_tr=qset_tr.select(db.sm_invoice.area_id ,db.sm_invoice.item_id,db.sm_invoice.category_id,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.area_id ,groupby=db.sm_invoice.area_id )
#     return records_tr
    
    
    qset_inv=db()
    qset_inv=qset_inv(db.sm_invoice.cid==c_id)
    qset_inv=qset_inv(db.sm_invoice.depot_id==depot_id)
    qset_inv=qset_inv(db.sm_invoice.store_id==store_id)
    qset_inv=qset_inv(db.sm_invoice.status=='Invoiced')
    qset_inv=qset_inv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
    records_inv=qset_inv.select(db.sm_invoice.area_id ,db.sm_invoice.item_id,db.sm_invoice.category_id,(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum(),orderby=db.sm_invoice.area_id | db.sm_invoice.item_id | db.sm_invoice.category_id,groupby=db.sm_invoice.area_id | db.sm_invoice.item_id | db.sm_invoice.category_id)

    itemList=[]
    itemQtyDict={}
    itemQtyList=[]
   

    for records_inv in records_inv:
        tr= records_inv[db.sm_invoice.area_id]
        item_id = records_inv[db.sm_invoice.item_id]
        itemQty = records_inv[(db.sm_invoice.quantity+db.sm_invoice.bonus_qty).sum()]
        itemCategory = records_inv[db.sm_invoice.category_id]

        itemList.append(str(item_id)+"-"+str(itemCategory))
        
        itemQtyDict={'tr':tr , 'item':item_id , 'category':  itemCategory,'qty':itemQty}  
        itemQtyList.append(itemQtyDict)



    return dict(records=records,itemList=itemList,records_inv=records_inv,records_tr=records_tr,itemQtyList=itemQtyList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

# ============================================
def scNational():
    c_id=session.cid   
#     return c_id
    response.title='NationalSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  


    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
        
        
        
        
        
    dateRecordsH="SELECT  level0_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level0_id ORDER BY level0_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level0_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT category_id, level0_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level0_id, category_id ORDER BY level0_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level0_id']:
            cat_str=cat_str+'<fdrd'+str(record['level0_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level0_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

def scNationalD():
    c_id=session.cid   
#     return c_id
    response.title='NationalSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
        
    dateRecordsH="SELECT  level0_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level0_id ORDER BY level0_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level0_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
#         qset_sum=qset_sum(db.sm_invoice.depot_id==depot_id)
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT category_id, level0_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level0_id, category_id ORDER BY level0_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n\n\n'
    
    myString+='Zone ,   InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level0_id']:
            cat_str=cat_str+'<fdrd'+str(record['level0_id'])+'>'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level0_id']
#     return cat_str
#     strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    for i in range(len(records)):  
        record=records[i]  
        spStr='<fdrd'+str(record['level0_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            amnA='0'
            amnB='0'
            amnC='0'
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)
    
    
# ===========     
        
        rsm=record['level0_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm!=record['level0_id']:
            myString+=str(record['level0_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
#         strShow= strShow+' past:'+str(pastRsm)+' rec:'+str(record['level0_id']) 
        pastRsm= record['level0_id']
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=NationalSummary.csv'   
    return str(myString)
    
    
    
# =============================================================
def scRsm():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"    
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"    
        
    dateRecordsH="SELECT  level1_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level1_id ORDER BY level1_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level1_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
  
    dateRecords="SELECT category_id, level1_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id ORDER BY level1_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level1_id']:
            cat_str=cat_str+'<fdrd'+str(record['level1_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level1_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)
# ========================
def scRsmD():
    c_id=session.cid   
    response.title='RSMSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    
    dateRecordsH="SELECT  level1_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level1_id ORDER BY level1_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level1_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT category_id, level0_id, level1_id , SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level0_id,level1_id, category_id ORDER BY level0_id,level1_id, category_id;"

    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n\n\n'
    myString+='Zone , RSM ,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level1_id']:
            cat_str=cat_str+'<fdrd'+str(record['level1_id'])+'>'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level1_id']
#     return cat_str
#     strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level1_id'])+'>'
        #=cat_str
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            amnA='0'
            amnB='0'
            amnC='0'
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)
    
    
# ===========     
        
        rsm=record['level1_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm!=record['level1_id']:
            myString+=str(record['level0_id'])+','+str(record['level1_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
#         strShow= strShow+' past:'+str(pastRsm)+' rec:'+str(record['level0_id']) 
        pastRsm= record['level1_id']
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=RSMSummary.csv'   
    return str(myString)


# ===================================================
def scFm():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level2_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level2_id ORDER BY level2_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level2_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
   
    dateRecords="SELECT category_id,level1_id ,level2_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id, category_id ORDER BY level1_id,level2_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level2_id']:
            cat_str=cat_str+'<fdrd'+str(record['level2_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level2_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

# ========================
def scFmD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level2_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level2_id ORDER BY level2_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level2_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
   
    dateRecords="SELECT category_id,level1_id ,level2_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id, category_id ORDER BY level1_id,level2_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level2_id']:
            cat_str=cat_str+'<fdrd'+str(record['level2_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level2_id']
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level2_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level2_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level2_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level2_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=FMSummary.csv'   
    return str(myString)

# ==========================================================
def scTr():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level3_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level3_id ORDER BY level3_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level3_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    
    dateRecords="SELECT category_id, level1_id,level2_id, level3_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id,level3_id, category_id ORDER BY level1_id,level2_id,level3_id, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level3_id']:
            cat_str=cat_str+'<fdrd'+str(record['level3_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level3_id']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)


def scTrD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level3_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level3_id ORDER BY level3_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level3_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    
    dateRecords="SELECT category_id, level1_id,level2_id, level3_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id,level3_id, category_id ORDER BY level1_id,level2_id,level3_id, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level3_id']:
            cat_str=cat_str+'<fdrd'+str(record['level3_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level3_id']

    
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,TR,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level3_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level3_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level3_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(record['level3_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level3_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TRSummary.csv'   
    return str(myString)


# ==============================================
def scTrDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id ,level3_id,level3_id, category_id,item_id,item_name,actual_tp ORDER BY   item_name,category_id,level3_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)
def scTrDetailD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id ,level3_id,level3_id, category_id,item_id,item_name,actual_tp ORDER BY   item_name,category_id,level3_id;"
    records=db.executesql(dateRecords,as_dict = True)  
    
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    itemPast=''
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='FM,'+tr_id+'|'+tr_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n\n'
        
    myString+='Item,    ItemName,    TP,    Stock,    RSM,    FM,    TR,    A,    B,    C,    TotalSalesTP\n'
    for i in range(len(records)):
        record=records[i]
        item=record['item_id']
        if [s for s in itemList if item in s]:
            index_element = itemList.index(item)           
            stockList= prodList[index_element]
            stock=stockList['stockBalance']
        qtyA=0
        qtyB=0
        qtyC=0
        if record['category_id']=='A':
            qtyA=record['qty']
        
        if record['category_id']=='B':
            qtyB=record['qty']
        
        if record['category_id']=='C':
            qtyC=record['qty']
        BTotal=BTotal+(float(qtyB)*float(record['actual_tp']))
        ATotal=ATotal+(float(qtyA)*float(record['actual_tp']))
        CTotal=CTotal+(float(qtyC)*float(record['actual_tp']))
        SaleT=int(qtyA)+int(qtyB)+int(qtyC)
        if itemPast!=item:
            myString+=str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+str(stock)+','+str(record['level1_id'])+','+str(record['level2_id'])+','+str(record['level3_id'])+','+str(qtyA)+','+str(qtyB)+','+str(qtyC)+','+str(record['actual_tp']*SaleT)+'\n'
        else:
            myString+=str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+','+str(record['level1_id'])+','+str(record['level2_id'])+','+str(record['level3_id'])+','+str(qtyA)+','+str(qtyB)+','+str(qtyC)+','+str(record['actual_tp']*SaleT)+'\n'
        itemPast=record['item_id']
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=scTrDetail.csv'   
    return str(myString) 
    

# ==============================================
def scFmDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"    

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id,level2_id ,level2_id, category_id,item_id,item_name,actual_tp ORDER BY   item_name,category_id,level2_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

def scRsmDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id,)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id,item_id,item_name,actual_tp ORDER BY   item_name,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)


def scRsmDetailD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id,item_id ORDER BY   level1_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)


def scMarketDetail():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id,market_id,market_name, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY market_id, category_id,item_id,item_name ORDER BY   item_name,category_id,market_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)



# Sales Comparism C Team-----------------------------

    
# =============================================================
def scRsmCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND special_territory_code = '"+str(tr_id)+"'"    
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
        
        
    dateRecordsH="SELECT  special_rsm_code, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY special_rsm_code ORDER BY special_rsm_code;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['special_rsm_code'])
        invCountList.append(records_head['invcount'])

    
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
        
    dateRecords="SELECT category_id, special_rsm_code, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND special_rsm_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY special_rsm_code, category_id ORDER BY special_rsm_code, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']

        if rsm_past!=record['special_rsm_code'] :
            cat_str=cat_str+'<fdrd'+str(record['special_rsm_code'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'

        
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['special_rsm_code']

    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

# ========================
def scRsmCteamD():
    c_id=session.cid   
    response.title='RSMSummary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level1_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level1_id ORDER BY level1_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level1_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT category_id, level0_id, level1_id , SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id ORDER BY level1_id, category_id;"

    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n\n\n'
    myString+='Zone , RSM ,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level1_id']:
            cat_str=cat_str+'<fdrd'+str(record['level1_id'])+'>'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level1_id']
#     return cat_str
#     strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level1_id'])+'>'
        #=cat_str
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            amnA='0'
            amnB='0'
            amnC='0'
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)
    
    
# ===========     
        
        rsm=record['level1_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm!=record['level1_id']:
            myString+=str(record['level0_id'])+','+str(record['level1_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
#         strShow= strShow+' past:'+str(pastRsm)+' rec:'+str(record['level0_id']) 
        pastRsm= record['level1_id']
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=RSMSummary.csv'   
    return str(myString)


# ===================================================
def scFmCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND special_territory_code = '"+str(tr_id)+"'"    
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
        
        
    dateRecordsH="SELECT  special_fm_code, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_fm_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY special_fm_code ORDER BY special_fm_code;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['special_fm_code'])
        invCountList.append(records_head['invcount'])

    
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT category_id, special_rsm_code,special_fm_code, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND special_fm_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY special_rsm_code,special_fm_code, category_id ORDER BY special_rsm_code,special_fm_code, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    cat_str=''
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['special_fm_code']:
            cat_str=cat_str+'<fdrd'+str(record['special_fm_code'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['special_fm_code']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

# ========================
def scFmCteamD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level2_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level2_id ORDER BY level2_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level2_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"

    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
   
    dateRecords="SELECT category_id,level1_id ,level2_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level2_id, category_id ORDER BY level2_id, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level2_id']:
            cat_str=cat_str+'<fdrd'+str(record['level2_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level2_id']
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level2_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level2_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level2_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level2_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=FMSummary.csv'   
    return str(myString)

# ==========================================================
def scTrCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND special_territory_code = '"+str(tr_id)+"'"    
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"    
        
    dateRecordsH="SELECT  special_territory_code, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY special_territory_code ORDER BY special_territory_code;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['special_territory_code'])
        invCountList.append(records_head['invcount'])

    
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT category_id, special_rsm_code,special_fm_code,special_territory_code, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced'  AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY special_rsm_code,special_fm_code,special_territory_code, category_id ORDER BY special_rsm_code,special_fm_code,special_territory_code, category_id;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 
#     return records
    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    cat_str=''
    for i in range(len(records)):
        record=records[i]
        
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['special_territory_code']:
            cat_str=cat_str+'<fdrd'+str(record['special_territory_code'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['special_territory_code']
#     return cat_str
    return dict(records=records,rsmList=rsmList,invCountList=invCountList,cat_str=cat_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)


def scTrCteamD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    conditionH=''
    if (depot_id!=''):
        conditionH=conditionH+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        conditionH=conditionH+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        conditionH=conditionH+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        conditionH=conditionH+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        conditionH=conditionH+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        conditionH=conditionH+"AND item_id = '"+str(product_id)+"'"
    dateRecordsH="SELECT  level3_id, count(DISTINCT  sl) as invcount FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+conditionH+" GROUP BY level3_id ORDER BY level3_id;"
#     return dateRecordsH
    records_head=db.executesql(dateRecordsH,as_dict = True) 
    rsmList=[]
    invCountList=[]
    for records_head in records_head:
        rsmList.append(records_head['level3_id'])
        invCountList.append(records_head['invcount'])


    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    
    dateRecords="SELECT category_id, level1_id,level2_id, level3_id, SUM((quantity - return_qty) * actual_tp) as amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id ORDER BY level3_id, category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    cat_str=''
    rsm_past=''
    
    totalAmount=0
    amnt=0
    for i in range(len(records)):
        record=records[i]
        category_id=record['category_id']
        amnt=record['amnt']
        if rsm_past!=record['level3_id']:
            cat_str=cat_str+'<fdrd'+str(record['level3_id'])+'>'
            amnA='0'
            amnB='0'
            amnC='0'
        if category_id=='A':
            amnA=str(amnt)
        if category_id=='B':
            amnB=str(amnt)
        if category_id=='C':
            amnC=str(amnt)
        cat_str=cat_str+amnA+','+amnB+','+amnC+'<rd>'
        rsm_past=record['level3_id']

    
    
    
    strShow=''
    pastRsm=''
    ATotal=0
    BTotal=0
    CTotal=0
    Total=0
    rsm_past=''
    amnA='0'
    amnB='0'
    amnC='0'
    totalAmount=0
    amnt=0
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n\n\n'
    myString+='RSM , FM,TR,  InvCount  ,  Total TP  ,TP A  ,  TP B  ,  TPC\n'
    for i in range(len(records)):    
        record=records[i]
        spStr='<fdrd'+str(record['level3_id'])+'>'
        rsmStr=cat_str.split(spStr)[1].split('<fdrd')[0]
        rsmStrList=rsmStr.split('<rd>')
        i=0
        while i < len(rsmStrList)-1:
            catA=rsmStrList[i].split(',')[0]
            catB=rsmStrList[i].split(',')[1]
            catC=rsmStrList[i].split(',')[2]
            i=i+1
        
        ATotal=ATotal+float(catA)
        BTotal=BTotal+float(catB)
        CTotal=CTotal+float(catC)
        Total=float(catA)+float(catB)+float(catC)

# ===========     
        rsm=record['level3_id']
        invCount=0
        if [s for s in rsmList if rsm in s]:
            index_element = rsmList.index(rsm)           
            invCount= invCountList[index_element]
        
        if pastRsm != record['level3_id']:
            myString+=str(record['level1_id'])+','+str(record['level2_id'])+','+str(record['level3_id'])+','+str(invCount)+','+str(Total)+','+str(ATotal)+','+str(BTotal)+','+str(CTotal)+'\n'
        strShow = strShow+' past:'+str(pastRsm)+' rec:'+str(record['level2_id'])
        pastRsm = record['level3_id']
         
#         return strShow
        
#     return strShow
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TRSummary.csv'   
    return str(myString)


# ==============================================
def scTrDetailCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"    

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code  ORDER BY   item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

def scTrDetailCteamD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level3_id, category_id,item_id ORDER BY   level3_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)

# ==============================================
def scFmDetailCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code , SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code   ORDER BY   item_name,item_id,actual_tp,category_id,special_rsm_code,special_fm_code ;"
    records=db.executesql(dateRecords,as_dict = True) 
    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

def scRsmDetailCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT item_id,item_name,actual_tp,category_id,special_rsm_code , SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,item_name,actual_tp,category_id,special_rsm_code   ORDER BY  item_name,actual_tp,category_id,special_rsm_code ;"
    records=db.executesql(dateRecords,as_dict = True) 
    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)


def scRsmDetailCteamD():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"

    dateRecords="SELECT item_id,item_name,actual_tp,category_id,level1_id,level2_id ,level3_id, SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY level1_id, category_id,item_id ORDER BY   level1_id,item_id,category_id;"
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name)


def scMarketDetailCteam():
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)

  
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    records=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    prodDict={}
    prodList=[]
    itemList=[]
    for record in records:
        item_id= record[db.sm_item.item_id]
        item_name= record[db.sm_item.name]
        category_id = record[db.sm_item.category_id]
        stockBalance = record[db.sm_depot_stock_balance.quantity.sum()]
        TP= record[db.sm_item.price]
        
        prodDict={'item_id':item_id,'item_name':item_name,'category_id':category_id,'stockBalance':stockBalance,'TP':TP}
        prodList.append(prodDict)
        itemList.append(item_id)
        
    condition=''
    if (depot_id!=''):
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+"AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition=condition+"AND special_rsm_code = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+"AND special_fm_code = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition=condition+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition=condition+"AND item_id = '"+str(product_id)+"'"
    dateRecords="SELECT item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code,market_id,market_name ,SUM(quantity - return_qty)  as qty FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND special_rsm_code != '' AND special_fm_code != '' AND special_territory_code != '' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition+" GROUP BY item_id,item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code,market_id,market_name  ORDER BY   item_name,actual_tp,category_id,special_rsm_code,special_fm_code ,special_territory_code,market_id,market_name;"
#     return dateRecords
    records=db.executesql(dateRecords,as_dict = True) 

    return dict(records=records,prodList=prodList,itemList=itemList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name)

# =========================TR================================


def TRReport():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1 = '"+str(rsm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
        
    if (fm_id!=''):
        condition_fm=condition_fm+" AND level2 = '"+str(fm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
    if (tr_id!=''):
        condition_fm=condition_fm+" AND level3 = '"+str(tr_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
   
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition_inv=condition_inv+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_inv=condition_inv+" AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level3_id,item_id,category_id,sum(quantity-return_qty) as quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' And category_id!='BONUS' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY level3_id,item_id,category_id  ORDER BY  level3_id,item_id,category_id;"
#     return invRecordsStr
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['level3_id'])    
#     return invStr    
    
    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,,'+str(recordFm['level_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0
    
    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['level_id'])+str(d)
            tr=str(recordfmStr['level_id'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
#                return trAllStr
               if trAllStr.find(item)==-1:
                   myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
                   
               else:

                   trItemSingle1=trAllStr.split(item)[1]
                   trItemSingle=trItemSingle1.split('rdrd')[0]
                   
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
                   
                   if category=='A':
                       myString=myString+str(qty)+',0,0,'
                   if category=='B':
                      
                       myString=myString+'0,'+str(qty)+',0,'
                   if category=='C':
                       myString=myString+'0,0,' +str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)
    
def TRReportAB():    
    c_id=session.cid   
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
#     return itemRecords
    
    
    
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1 = '"+str(rsm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
        
    if (fm_id!=''):
        condition_fm=condition_fm+" AND level2 = '"+str(fm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
    if (tr_id!=''):
        condition_fm=condition_fm+" AND level3 = '"+str(tr_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
    
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"' "+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition_inv=condition_inv+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_inv=condition_inv+" AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level3_id,item_id,category_id,sum(quantity-return_qty) as quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' And category_id!='BONUS' And category_id!='C' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY level3_id,item_id,category_id  ORDER BY  level3_id,item_id,category_id;"
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['level3_id'])    
        

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,'+str(recordFm['level_id']) 
        x=x+1

    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B'#,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['level_id'])+str(d)
            tr=str(recordfmStr['level_id'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
                   myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
                   if category=='A':
                       myString=myString+str(qty)+',0,'
                   if category=='B':
                       myString=myString+'0,'+str(qty)+','

                       
               
        myString=myString+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)   
    
# =================FM Start=============    
def FMReport():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' :
       session.flash='Please select RSM '
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1 = '"+str(rsm_id)+"'"
        condition_fm=condition_fm+" AND depth = 2"

   
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"

    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level2_id,item_id,category_id,sum(quantity-return_qty) as quantity FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' And category_id!='BONUS' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY level2_id,item_id,category_id  ORDER BY  level2_id,item_id,category_id;"
#     return invRecordsStr
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level2_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['level2_id'])    
#     return invStr  

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
#     myString+='FM,'+fm_id+'|'+fm_name+'\n'
#     myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,,'+str(recordFm['level_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['level_id'])+str(d)
            tr=str(recordfmStr['level_id'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
#                    return str(tr)+','+str(item)
                   myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
                   if category=='A':
                       myString=myString+str(qty)+',0,0,'
                   if category=='B':
                       myString=myString+'0,'+str(qty)+',0,'
                   if category=='C':
                       myString=myString+'0,0,' +str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=FMReport.csv'   
    return str(myString)

def FMReportAB():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM '
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1 = '"+str(rsm_id)+"'"
        condition_fm=condition_fm+" AND depth = 2"

   
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"

    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level2_id,item_id,category_id,sum(quantity-return_qty) as quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' And category_id!='BONUS' And category_id!='C' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY level2_id,item_id,category_id  ORDER BY  level2_id,item_id,category_id;"
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level2_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['level2_id'])    
        

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,'+str(recordFm['level_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B'#,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['level_id'])+str(d)
            tr=str(recordfmStr['level_id'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
                   myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
                   if category=='A':
                       myString=myString+str(qty)+',0,'
                   if category=='B':
                       myString=myString+'0,'+str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=FMReport.csv'   
    return str(myString)
# ==================FM End===============
# ============================C Team================================
def TRReportCteam():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' :
       session.flash='Please select RSM '
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_item.category_id=='C')
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
#     return itemRecords
    
    
#     ==================sptr list
    qsetSP=db()
    qsetSP=qsetSP(db.sm_level.cid==c_id)  
    qsetSP=qsetSP(db.sm_level.is_leaf==1)   
    if (rsm_id!=''):
        qsetSP=qsetSP(db.sm_level.level1==rsm_id)
    if (fm_id!=''):
        qsetSP=qsetSP(db.sm_level.level2==fm_id) 
    if (tr_id!=''):
        qsetSP=qsetSP(db.sm_level.level3==qsetSP) 
        
        
        
    spRecords=qsetSP.select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
    sptrList=''
    for spRecord in spRecords:
        sptr=spRecord[db.sm_level.level_id]
        if sptrList=='':
            sptrList="'"+str(sptr)+"'"
        else:
            sptrList=sptrList+","+"'"+str(sptr)+"'"

#     ====================sptr list end
    
    if sptrList!='':
        fmRecordsStr="SELECT special_territory_code  FROM sm_level WHERE  cid='"+c_id +"' AND special_territory_code in ("+sptrList+") GROUP BY special_territory_code  ORDER BY  special_territory_code;"
#         return fmRecordsStr
        fmrecords=db.executesql(fmRecordsStr,as_dict = True) 
    else: 
        fmrecords=''
    
   
   
   
#     fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
#     fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
#     if (rsm_id!=''):
#         condition_inv=condition_inv+"AND special_rsm_code = '"+str(rsm_id)+"'"
#     if (fm_id!=''):
#         condition_inv=condition_inv+"AND special_fm_code = '"+str(fm_id)+"'"
#     if (tr_id!=''):
#         condition_inv=condition_inv+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
    if sptrList!='':    
        invRecordsStr="SELECT special_territory_code,item_id,category_id,sum(quantity-return_qty) as quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' AND special_territory_code in ("+sptrList+") And category_id='C' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY special_territory_code,item_id,category_id  ORDER BY  special_territory_code,item_id,category_id;"
        invRecords=db.executesql(invRecordsStr,as_dict = True) 
    else: 
        invRecords=''
#     return invRecordsStr
   
    
    
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['special_territory_code'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['special_territory_code'])    
        

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['special_territory_code'])
            fmFlag=1
        else:
            myString=myString+','+str(recordFm['special_territory_code']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['special_territory_code'])+str(d)
            tr=str(recordfmStr['special_territory_code'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
#                    return str(tr)+','+str(item)
                   myString=myString+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
#                    if category=='A':
#                        myString=myString+str(qty)+',0,0,'
#                    if category=='B':
#                        myString=myString+'0,'+str(qty)+',0,'
                   if category=='C':
                       myString=myString +str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)


# ===================Process

def TRReportInvoicePeriodicalCteamProcess():    
    c_id=session.cid   
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    date_to_m= str(date_to_m)[0:10]
    
    fromMonth=str(date_from).split('-')[1]
    toMonth=str(date_to).split('-')[1]
#     return toMonth
    if fromMonth!=toMonth:
       session.flash='Please select Date of same month'
       redirect (URL('report_sales','home'))
    
    if depot_id=='' or store_id=='':
       session.flash='Please select Depot or Store'
       redirect (URL('report_sales','home'))
       
#     if rsm_id=='' and fm_id=='' and tr_id=='':
#        session.flash='Please select RSM or FM or TR'
#        redirect (URL('report_sales','home'))
    condition_item=''
    if (product_id!=''):
        condition_item=condition_item+" AND item_id = '"+str(product_id)+"'"

        
    #     ==================sptr list
#     qsetSP=db()
#     qsetSP=qsetSP(db.z_mso_area.cid==c_id)  
# #     qsetSP=qsetSP(db.sm_level.is_leaf==1)   
#     if (rsm_id!=''):
#         qsetSP=qsetSP(db.z_mso_area.level1_id==rsm_id)
#     if (fm_id!=''):
#         qsetSP=qsetSP(db.z_mso_area.level2_id==fm_id) 
#     if (tr_id!=''):
#         qsetSP=qsetSP(db.z_mso_area.area_id==tr_id) 
#         
#         
#         
#     spRecords=qsetSP.select(db.z_mso_area.area_id,orderby=db.z_mso_area.area_id,groupby=db.z_mso_area.area_id)
#     return db._lastsql
#     sptrList=''
#     for spRecord in spRecords:
#         sptr=spRecord[db.z_mso_area.area_id]
#         if sptrList=='':
#             sptrList="'"+str(sptr)+"'"
#         else:
#             sptrList=sptrList+","+"'"+str(sptr)+"'"    
        
        
#     return sptrList    
    
    
    deleteTableStr="""delete from z_tr_report_cteam where user_id='"""+str(session.user_id)+"""'"""
#     return deleteTableStr
    deleteTable=db.executesql(deleteTableStr)
   
#     s_text="'date_from="+str(date_from)+",date_to="+str(date_to)+",depot_id="+str(depot_id)+",depot_name="+str(depot_name)+",store_id="+str(store_id)+",store_name="+str(store_name)+",rsm_id="+str(rsm_id)+",rsm_name="+str(rsm_name)+",fm_id="+str(fm_id)+",fm_name="+str(fm_name)+",tr_id="+str(tr_id)+",tr_name="+str(tr_name)+",product_id="+str(product_id)+",product_name="+str(product_name)+"'"
    s_text="'"+str(date_from)+","+str(date_to)+","+str(depot_id)+","+str(depot_name)+","+str(store_id)+","+str(store_name)+","+str(rsm_id)+","+str(rsm_name)+","+str(fm_id)+","+str(fm_name)+","+str(tr_id)+","+str(tr_name)+","+str(product_id)+","+str(product_name)+"'"
     
    
#     invoiceStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum(quantity) as qty, actual_tp, category_id, level3_id,special_territory_code,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_invoice 
#                 where status ='Invoiced' And category_id!='BONUS' and quantity > 0 and invoice_date >='"""+str(date_from)+"""'  and invoice_date < '"""+str(date_to_m)+"""' 
#                 AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And special_territory_code in ("""+str(sptrList)+""")"""+ condition_item+"""
#                 group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
#     retStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum((quantity) * -1) as qty, actual_tp, category_id, level3_id,special_territory_code,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_return  
#                 where status ='Returned' And category_id!='BONUS' and quantity > 0  and invoice_date >='"""+str(date_from)+"""'  and invoice_date < '"""+str(date_to_m)+"""' 
#                 AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And special_territory_code in ("""+str(sptrList)+""")"""+ condition_item+"""
#                 group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
    
    invoiceStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum(quantity) as qty, actual_tp, category_id, level3_id,special_territory_code,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_invoice 
                where status ='Invoiced' And category_id!='BONUS' and quantity > 0 and invoice_date >='"""+str(date_from)+"""'  and invoice_date < '"""+str(date_to_m)+"""' 
                AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And special_territory_code !=''"""+ condition_item+"""
                group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
    retStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum((quantity) * -1) as qty, actual_tp, category_id, level3_id,special_territory_code,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_return  
                where status ='Returned' And category_id!='BONUS' and quantity > 0  and return_date >='"""+str(date_from)+"""'  and return_date < '"""+str(date_to_m)+"""' 
                AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And special_territory_code !=''"""+ condition_item+"""
                group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """ 
#     return invoiceStr
#     return retStr
    
    strInvoice="""INSERT INTO z_tr_report_cteam (cid,rpt_date,item_id,item_name,quantity,actual_tp,category_id,level3_id,special_territory_code,msoCategory,itembaseGroup,user_id,s_text) """+invoiceStr
    invInsert=db.executesql(strInvoice)
    strRet="""INSERT INTO z_tr_report_cteam (cid,rpt_date,item_id,item_name,quantity,actual_tp,category_id,level3_id,special_territory_code,msoCategory,itembaseGroup,user_id,s_text) """+retStr
    retInsert=db.executesql(strRet) 

#     return invInsert
#     if invInsert > 0 or retInsert > 0:
    session.s_textCteam=s_text
    
    session.flash='Processed Successfully '
    redirect (URL('report_sales','home'))

# =======================
def TRReportCteamPeriodic():    
    response.title='salesClosingStockS'    
#     return len(session.s_textCteam)
#     session.s_textCteam='2016-11-01,2016-11-30,170,Savar,170140,Commercial,CCS,Commercial,,,,,,'
    if session.s_textCteam==None:
        session.flash='Please Process First'
        redirect (URL('report_sales','home'))
    
    if len(session.s_textCteam) < 10 :
        session.flash='Please Processe First'
        redirect (URL('report_sales','home'))
    
    search_criteria= (session.s_textCteam).replace("'","")
    search_criteriaList=search_criteria.split(',')
    c_id=session.cid   
#     return search_criteriaList[0]
    
    date_from=search_criteriaList[0]
    date_to=search_criteriaList[1]
    depot_id=search_criteriaList[2]
    depot_name=search_criteriaList[3]  
    store_id=search_criteriaList[4]
    store_name=search_criteriaList[5]
    rsm_id=search_criteriaList[6]
    rsm_name=search_criteriaList[7]
    fm_id=search_criteriaList[8]
    fm_name=search_criteriaList[9]
    tr_id=search_criteriaList[10]
    tr_name=search_criteriaList[11]
    product_id=search_criteriaList[12]
    product_name=search_criteriaList[13]
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    dateMSO=str(date_from)[0:7] + '-01'
#     if rsm_id=='' :
#        session.flash='Please select RSM '
#        redirect (URL('report_sales','home'))
       
  
    
    qset=db()
#     qset=qset(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.z_tr_report_cteam.cid==c_id)
    qset=qset(db.z_tr_report_cteam.category_id=='C')
#     qset=qset(db.sm_depot_stock_balance.item_id==db.z_tr_report_cteam.item_id)      
#     if (depot_id!=''):
#         qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
#     if (store_id!=''):
#         qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.z_tr_report_cteam.item_id==product_id) 
    itemRecords=qset.select(db.z_tr_report_cteam.item_id,db.z_tr_report_cteam.item_name,db.z_tr_report_cteam.category_id,db.z_tr_report_cteam.actual_tp,orderby=db.z_tr_report_cteam.item_name|db.z_tr_report_cteam.item_id|db.z_tr_report_cteam.actual_tp,groupby=db.z_tr_report_cteam.item_id|db.z_tr_report_cteam.item_name|db.z_tr_report_cteam.category_id|db.z_tr_report_cteam.actual_tp)
#     return db._lastsql
#     ===============StockBalance===================
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
#     qset=qset(db.sm_depot_stock_balance.quantity>0)
#     qset=qset(db.z_tr_report_cteam.cid==c_id)
#     qset=qset(db.z_tr_report_cteam.category_id=='C')
#     qset=qset(db.sm_depot_stock_balance.item_id==db.z_tr_report_cteam.item_id)      
    if (depot_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==product_id) 
    itemStoctRecords=qsetStock.select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
#     return db._lastsql
#     return itemStoctRecords
    strStock=''
    for itemStoctRecords in itemStoctRecords:
        if strStock=='':
            strStock=str(itemStoctRecords[db.sm_depot_stock_balance.item_id])+'|'+str(itemStoctRecords[db.sm_depot_stock_balance.quantity.sum()])
        else:
            strStock=strStock+'<fd>'+str(itemStoctRecords[db.sm_depot_stock_balance.item_id])+'|'+str(itemStoctRecords[db.sm_depot_stock_balance.quantity.sum()])
            
    strStock=strStock+'<fd>'
    
#     return strStock
    
    

# #     ====================sptr list end
    
#     condition_fm=''
#     if (rsm_id!=''):
#         condition_fm=condition_fm+" AND level1_id = '"+str(rsm_id)+"'"
# 
#     if (fm_id!=''):
#         condition_fm=condition_fm+" AND level2_id = '"+str(fm_id)+"'"
#         
#     if (tr_id!=''):
#         condition_fm=condition_fm+" AND area_id = '"+str(tr_id)+"'"
#         
#         
#     fmRecordsStr="SELECT sp_area_code  FROM z_mso_area WHERE  cid='"+c_id +"' "+condition_fm+" GROUP BY sp_area_code  ORDER BY  sp_area_code;"
# #     return fmRecordsStr
    fmRecordsStr="SELECT a.sp_area_code  FROM z_mso_area a,z_tr_report_cteam t WHERE  a.cid=t.cid and a.first_date='"+dateMSO+"' and  t.user_id='"+str(session.user_id)+"' and a.sp_area_code=t.special_territory_code  GROUP BY a.sp_area_code ORDER BY  a.sp_area_code;"
#     return fmRecordsStr
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 
    

    fDate=str(first_currentDate)[0:10]
#     fmInvStr="""select sp_area_code,rep_id,rep_category from  z_mso_area where first_date ='"""+str(fDate)+"""' and cid <='"""+str(c_id)+"""' """+"""and sp_area_code!='' GROUP BY sp_area_code,rep_id,rep_category  ORDER BY  sp_area_code,rep_id,rep_category;"""
    fmInvStr=fmRecordsStr="SELECT a.sp_area_code,a.rep_id,a.rep_category  FROM z_mso_area a,z_tr_report_cteam t WHERE  a.cid=t.cid and a.first_date='"+dateMSO+"' and  t.user_id='"+str(session.user_id)+"' and a.sp_area_code=t.special_territory_code  GROUP BY a.sp_area_code,a.rep_id,a.rep_category  ORDER BY  a.sp_area_code,a.rep_id,a.rep_category;"
#     return fmInvStr
    fmInvRecords=db.executesql(fmInvStr,as_dict = True) 
    
    fmStr=''
    trFMPast=''
    for fm in range(len(fmInvRecords)):
        fmInvRecord=fmInvRecords[fm]
        trfm=str(fmInvRecord['sp_area_code'])
        if (trfm!=trFMPast):
            fmStr=fmStr+'<'+str(trfm)+'>'
        fmStr=fmStr+str(fmInvRecord['rep_category'])+','
        trFMPast=str(fmInvRecord['sp_area_code']) 
    fmStr=fmStr+'<'
#     return fmStr  
    
#     ===============FM List End
    
    invRecordsStr="""select 
        item_id, item_name, actual_tp, category_id,level3_id ,sum(quantity) as qty,special_territory_code,msoCategory,itembaseGroup 
        from 
        z_tr_report_cteam where 
        user_id='"""+str(session.user_id)+"""' and category_id='C' GROUP BY special_territory_code,item_id,category_id,actual_tp  ORDER BY  special_territory_code,item_id,category_id,actual_tp;"""
#     return invRecordsStr
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
#     return len(invRecords)
    for inv in range(len(invRecords)):
        categoryID=''
        recordInv=invRecords[inv]
        tr=str(recordInv['special_territory_code'])
#         return recordInv
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
         
            trFMInfo1=fmStr.split('<'+str(tr)+'>')
            trFMInfo=trFMInfo1[1].split('<')
            

        if (trFMInfo[0].find(recordInv['category_id']) !=-1):
            categoryID=str(recordInv['category_id'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='C')):
            categoryID=str(recordInv['itembaseGroup'])
            if (str(recordInv['itembaseGroup'])==''):
                if (trFMInfo[0].find('A') !=-1):
                    categoryID='A'
                if (trFMInfo[0].find('B') !=-1):
                    categoryID='B'
                if (trFMInfo[0].find('Z') !=-1):
                    categoryID='Z'
            else:
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) !=-1)):
                    categoryID=recordInv['itembaseGroup']
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='A')):
                    if (trFMInfo[0].find('B') !=-1):
                        categoryID='B'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z'     
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='B')):
                    if (trFMInfo[0].find('A') !=-1):
                        categoryID='A'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z' 
            
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='A')):
            if (trFMInfo[0].find('B') !=-1):
                categoryID='B'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z' 
#             return categoryID
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='B')):
            if (trFMInfo[0].find('A') !=-1):
                categoryID='A'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z'
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='X')):
            categoryID=str(recordInv['msoCategory'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (str(recordInv['msoCategory'])=='') and (str(recordInv['itembaseGroup'])=='')):   
            categoryID='Z'

        invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp'])+'fdfd'+categoryID+'fdfd'+str(recordInv['qty'])+'fdfd'+str(recordInv['actual_tp'])+'rdrd'
        trPast=str(recordInv['special_territory_code'])    

    
# ===============================
#     return invStr
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['special_territory_code'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp'])+'fdfd'+categoryID+'fdfd'+str(recordInv['qty'])+'fdfd'+str(recordInv['actual_tp'])+'rdrd'
#         invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp']+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['qty'])+'rdrd'
        trPast=str(recordInv['special_territory_code'])    
    invStr=invStr+'<'    
#     return invStr
    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['sp_area_code'])
            fmFlag=1
        else:
            myString=myString+','+str(recordFm['sp_area_code']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',C'
            n=n+1
    myString=myString+'\n'

    flagFm=0
#     return invStr
    itemPast=''
    for record in itemRecords:
        item=str(record.item_id)
        actual_tp=str(record.actual_tp)
        item_name=str(record.item_name)
        itemStock='0'
#         return item
#         return strStock.find(item)
        if strStock.find(item)!=-1:
            itemStock=strStock.split(item)[1].split('<fd>')[0].replace('|','')
        if itemStock=='':
            itemStock='0'     
        if itemPast!=item:
            myString=myString+str(item)+','+str(item_name)+','+str(actual_tp)+','+str(itemStock)+','#+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        else:
            myString=myString+str(item)+','+str(item_name)+','+str(actual_tp)+','+','
        itemPast=str(record.item_id)
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['sp_area_code'])+str(d)
            tr=str(recordfmStr['sp_area_code'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catC)+','
            else:
#                return invStr
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               itemCheck=str(item)+'|'+str(actual_tp)
#                trAllStr='1101fdfdBfdfd1164rdrd'
               if trAllStr.find(itemCheck)==-1:
#                    return str(tr)+','+str(item)
                   myString=myString+str(catC)+','
                   
               else:
#                    category='C'
#                    qty='0'
                   
                   trItemSingle=trAllStr.split(itemCheck)[1].split('rdrd')[0]
#                        return trItemSingle
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
#                    if category=='A':
#                        myString=myString+str(qty)+',0,0,'
#                    if category=='B':
#                        myString=myString+'0,'+str(qty)+',0,'
                   if category=='C':
                       myString=myString +str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)
# =============FM Start====================     
def FMReportCteam():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
#     fm_id=str(request.vars.fm_id).strip()
#     fm_name=str(request.vars.fm_name).strip()
#     tr_id=str(request.vars.tr_id).strip()
#     tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' :
       session.flash='Please select RSM '
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_item.category_id=='C')
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
    
    
    
#     ==================sptr list
    qsetSP=db()
    qsetSP=qsetSP(db.sm_level.cid==c_id)  
    qsetSP=qsetSP(db.sm_level.is_leaf==1)   
    if (rsm_id!=''):
        qsetSP=qsetSP(db.sm_level.level1==rsm_id)
#     if (fm_id!=''):
#         qsetSP=qsetSP(db.sm_level.level2==fm_id) 
#     if (tr_id!=''):
#         qsetSP=qsetSP(db.sm_level.level3==qsetSP) 
        
        
        
    spRecords=qsetSP.select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
    sptrList=''
    for spRecord in spRecords:
        sptr=spRecord[db.sm_level.level_id]
        if sptrList=='':
            sptrList="'"+str(sptr)+"'"
        else:
            sptrList=sptrList+","+"'"+str(sptr)+"'"

#     ====================sptr list end
    
   
    fmRecordsStr="SELECT special_territory_code  FROM sm_level WHERE  cid='"+c_id +"' AND special_territory_code in ("+sptrList+") GROUP BY special_territory_code  ORDER BY  special_territory_code;"
#     return fmRecordsStr
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 
    
    
   
   
   
#     fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
#     fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+"AND store_id = '"+str(store_id)+"'"

    if (product_id!=''):
        condition_inv=condition_inv+"AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT special_territory_code,item_id,category_id,quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND special_territory_code in ("+sptrList+") And category_id='C' "+condition_inv+"  GROUP BY special_territory_code,item_id,category_id  ORDER BY  category_id,special_territory_code,item_id;"
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
#     return invRecordsStr
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['special_territory_code'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['special_territory_code'])    
        

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['special_territory_code'])
            fmFlag=1
        else:
            myString=myString+','+str(recordFm['special_territory_code']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['special_territory_code'])+str(d)
            tr=str(recordfmStr['special_territory_code'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
#                    return str(tr)+','+str(item)
                   myString=myString+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
#                    if category=='A':
#                        myString=myString+str(qty)+',0,0,'
#                    if category=='B':
#                        myString=myString+'0,'+str(qty)+',0,'
                   if category=='C':
                       myString=myString +str(qty)+','
                       
               
        myString=myString+'\n'
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)
# ===============FM End======================
def TRReportABCteam():    
    c_id=session.cid   
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
       
  
    
    qset=db()
    qset=qset(db.sm_depot_stock_balance.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.quantity>0)
    qset=qset(db.sm_item.cid==c_id)
    qset=qset(db.sm_depot_stock_balance.item_id==db.sm_item.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_depot_stock_balance.item_id==product_id) 
    itemRecords=qset.select(db.sm_item.item_id,db.sm_item.name,db.sm_item.category_id,db.sm_depot_stock_balance.quantity.sum(),db.sm_item.price,orderby=db.sm_item.name,groupby=db.sm_item.item_id|db.sm_item.name|db.sm_item.category_id)
#     return itemRecords
    
    
    
    #     ==================sptr list
    qsetSP=db()
    qsetSP=qsetSP(db.sm_level.cid==c_id)  
    qsetSP=qsetSP(db.sm_level.is_leaf==1)   
    if (rsm_id!=''):
        qsetSP=qsetSP(db.sm_level.level1==rsm_id)
    if (fm_id!=''):
        qsetSP=qsetSP(db.sm_level.level2==fm_id) 
    if (tr_id!=''):
        qsetSP=qsetSP(db.sm_level.level3==qsetSP) 
        
        
        
    spRecords=qsetSP.select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
    sptrList=''
    for spRecord in spRecords:
        sptr=spRecord[db.sm_level.level_id]
        if sptrList=='':
            sptrList="'"+str(sptr)+"'"
        else:
            sptrList=sptrList+","+"'"+str(sptr)+"'"

#     ====================sptr list end
    
   
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"' AND special_territory_code in ("+sptrList+") GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
#     return fmRecordsStr
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+"AND store_id = '"+str(store_id)+"'"
#     if (rsm_id!=''):
#         condition_inv=condition_inv+"AND special_rsm_code = '"+str(rsm_id)+"'"
#     if (fm_id!=''):
#         condition_inv=condition_inv+"AND special_fm_code = '"+str(fm_id)+"'"
#     if (tr_id!=''):
#         condition_inv=condition_inv+"AND special_territory_code = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+"AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level3_id,item_id,category_id,quantity  FROM sm_invoice WHERE  cid='"+c_id+"' And category_id!='BONUS' And category_id!='C' "+condition_inv+"  GROUP BY level3_id,item_id,category_id  ORDER BY  category_id,level3_id,item_id;"
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'rdrd'
        trPast=str(recordInv['level3_id'])    
        

    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,'+str(recordFm['level_id']) 
        x=x+1

    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B'#,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0

    for record in itemRecords:
        item=str(record.sm_item.item_id)
        myString=myString+str(record[db.sm_item.item_id])+','+str(record[db.sm_item.name])+','+str(record[db.sm_item.price])+','+str(record[db.sm_depot_stock_balance.quantity.sum()])+','
        d_value=''
        for d in range(len(fmrecords)):
            recordfmStr=fmrecords[d]
            d_value=d_value+str(recordfmStr['level_id'])+str(d)
            tr=str(recordfmStr['level_id'])
            catA=0
            catB=0
            catC=0
            
            if invStr.find(tr)==-1:
                myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
            else:
               
               trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
               
               if trAllStr.find(item)==-1:
                   myString=myString+str(catA)+','+str(catB)+','#+str(catC)+','
                   
               else:
                   trItemSingle=trAllStr.split(item)[1].split('rdrd')[0]
                   category=trItemSingle.split('fdfd')[1]
                   qty=trItemSingle.split('fdfd')[2]
                   if category=='A':
                       myString=myString+str(qty)+',0,'
                   if category=='B':
                       myString=myString+'0,'+str(qty)+','

                       
               
        myString=myString+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)   
    
    
    
# =========================Comperisio report with invoiceTP================================


def TRReportInvoice():    
    c_id=session.cid   
#     return c_id
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    
    if depot_id=='' and store_id=='':
       session.flash='Please select Depot or Store'
       redirect (URL('report_sales','home'))
       
    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
       
  
 
    qset=db()
    qset=qset((db.sm_invoice.quantity-db.sm_invoice.return_qty)>0)
    qset=qset(db.sm_invoice.cid==c_id)
    
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
#     qsetStock=qsetStock(db.sm_depot_stock_balance.quantity>0)

#     qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==db.sm_invoice.item_id)      
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qset=qset(db.sm_invoice.item_id==product_id)
        qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==product_id) 
        
    itemRecords=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.category_id,db.sm_invoice.actual_tp,orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id|db.sm_invoice.category_id|db.sm_invoice.actual_tp)
#     return db._lastsql
    stockitemRecords=qsetStock.select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
#     return stockitemRecords
   
    itemStockStr=''
    for recordStock in stockitemRecords:
     itemStock=str(recordStock[db.sm_depot_stock_balance.item_id])
     balanceStock=str(recordStock[db.sm_depot_stock_balance.quantity.sum()])

     itemStockStr=itemStockStr+itemStock+'|'+balanceStock+'<rdrd>'
     
#     return itemStockStr
   
#     ========================
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1 = '"+str(rsm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
        
    if (fm_id!=''):
        condition_fm=condition_fm+" AND level2 = '"+str(fm_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
    if (tr_id!=''):
        condition_fm=condition_fm+" AND level3 = '"+str(tr_id)+"'"
        condition_fm=condition_fm+" AND is_leaf = 1"
   
    fmRecordsStr="SELECT level_id,level_name  FROM sm_level WHERE  cid='"+c_id +"'"+condition_fm+" GROUP BY level_id,level_name  ORDER BY  level_id,level_name;"
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 

    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition_inv=condition_inv+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_inv=condition_inv+" AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
    invRecordsStr="SELECT level3_id,item_id,actual_tp,category_id,sum(quantity-return_qty) as quantity  FROM sm_invoice WHERE  cid='"+c_id+"' AND status = 'Invoiced' And category_id!='BONUS' AND invoice_date >= '"+str(date_from)+"' AND invoice_date < '"+str(date_to_m)+"'"+condition_inv+"  GROUP BY level3_id,item_id,category_id,actual_tp  ORDER BY  level3_id,item_id,category_id,actual_tp;"
#     return invRecordsStr
    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
    
    invStr=''
    trPast=''
    for inv in range(len(invRecords)):
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
        invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp'])+'fdfd'+str(recordInv['category_id'])+'fdfd'+str(recordInv['quantity'])+'fdfd'+str(recordInv['actual_tp'])+'rdrd'
        trPast=str(recordInv['level3_id'])    
#     return invStr    
    
    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['level_id'])
            fmFlag=1
        else:
            myString=myString+',,,'+str(recordFm['level_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B,C'
            n=n+1
    myString=myString+'\n'

    flagFm=0
    itemCheck_past=''
    item_past=''
    for record in itemRecords:
        item=str(record[db.sm_invoice.item_id])
        acTP=str(record[db.sm_invoice.actual_tp])
        itemCheck=str(item)+'|'+str(acTP)
        if itemCheck!=itemCheck_past:
            
            stockStock=0
    #         return itemStockStr
            if itemStockStr.find(str(item)+'|')!=-1:
    #             return itemStockStr.find(str(item)+'|')
                sp=str(item)+'|'
                stockStock=itemStockStr.split(sp)[1].split('<rdrd>')[0]
    #             stockStock=stockStock1.split(sp)[1]#.split['<rdrd>'][0]
    #             return stockStock
            if item_past!=item:
                myString=myString+str(record[db.sm_invoice.item_id])+','+str(record[db.sm_invoice.item_name])+','+str(record[db.sm_invoice.actual_tp])+','+str(stockStock)+','
            else:
                myString=myString+str(record[db.sm_invoice.item_id])+','+str(record[db.sm_invoice.item_name])+','+str(record[db.sm_invoice.actual_tp])+','+','
            d_value=''
            for d in range(len(fmrecords)):
                recordfmStr=fmrecords[d]
                d_value=d_value+str(recordfmStr['level_id'])+str(d)
                tr=str(recordfmStr['level_id'])
                catA=0
                catB=0
                catC=0
    
                if invStr.find(tr)==-1:
                    myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
                else:
                   
                   trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
    
                   if trAllStr.find(itemCheck)==-1:
                       myString=myString+str(catA)+','+str(catB)+','+str(catC)+','
                   else:
    #                    return itemCheck
    #                    return trAllStr
                       trItemSingle1=trAllStr.split(itemCheck)[1]
                       
                       trItemSingle=trItemSingle1.split('rdrd')[0]
                       category=trItemSingle.split('fdfd')[1]
                       qty=trItemSingle.split('fdfd')[2]
    
                       if category=='A':
                           myString=myString+str(qty)+',0,0,'
                       if category=='B':
                          
                           myString=myString+'0,'+str(qty)+',0,'
                       if category=='C':
                           myString=myString+'0,0,' +str(qty)+','
                           
                  
            myString=myString+'\n'
        itemCheck_past=itemCheck 
        item_past=item
        
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)


# =====================Periodical===================
def TRReportInvoicePeriodicalProcess():    
    c_id=session.cid   
    response.title='salesClosingStockS'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    date_to_m= str(date_to_m)[0:10]
    
#     return 'date_to_m'
    fromMonth=str(date_from).split('-')[1]
    toMonth=str(date_to).split('-')[1]
#     return toMonth
    if fromMonth!=toMonth:
       session.flash='Please select Date of same month'
       redirect (URL('report_sales','home'))
#     if depot_id=='' and store_id=='':
    if depot_id=='' :
       session.flash='Please select Depot'
       redirect (URL('report_sales','home'))
       
    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
    condition_item=''
    if (product_id!=''):
        condition_item=condition_item+" AND item_id = '"+str(product_id)+"'"
    if (fm_id!=''):
        condition_item=condition_item+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_item=condition_item+" AND level3_id = '"+str(tr_id)+"'"
    
    
    deleteTableStr="""delete from z_tr_report where user_id='"""+str(session.user_id)+"""'"""
    deleteTable=db.executesql(deleteTableStr)
        
#     s_text="'date_from="+str(date_from)+",date_to="+str(date_to)+",depot_id="+str(depot_id)+",depot_name="+str(depot_name)+",store_id="+str(store_id)+",store_name="+str(store_name)+",rsm_id="+str(rsm_id)+",rsm_name="+str(rsm_name)+",fm_id="+str(fm_id)+",fm_name="+str(fm_name)+",tr_id="+str(tr_id)+",tr_name="+str(tr_name)+",product_id="+str(product_id)+",product_name="+str(product_name)+"'"
    s_text="'"+str(date_from)+","+str(date_to)+","+str(depot_id)+","+str(depot_name)+","+str(store_id)+","+str(store_name)+","+str(rsm_id)+","+str(rsm_name)+","+str(fm_id)+","+str(fm_name)+","+str(tr_id)+","+str(tr_name)+","+str(product_id)+","+str(product_name)+"'"
     
#     invoiceStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum(quantity) as qty, actual_tp, category_id, level3_id,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_invoice 
#                 where status ='Invoiced' And category_id!='BONUS' and quantity > 0 and invoice_date >='"""+str(date_from)+"""'  and invoice_date < '"""+str(date_to_m)+"""' 
#                 AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And level1_id = '"""+str(rsm_id)+"""'"""+ condition_item+"""
#                 group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
#     retStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum((quantity) * -1) as qty, actual_tp, category_id, level3_id,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_return  
#                 where status ='Returned' And category_id!='BONUS' and quantity > 0  and return_date >='"""+str(date_from)+"""'  and return_date < '"""+str(date_to_m)+"""' 
#                 AND depot_id = '"""+str(depot_id)+"""' AND store_id = '"""+str(store_id)+"""' And level1_id = '"""+str(rsm_id)+"""'"""+ condition_item+"""
#                 group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """

    invoiceStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum(quantity) as qty, actual_tp, category_id, level3_id,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_invoice 
                where status ='Invoiced' And category_id!='BONUS' and quantity > 0 and invoice_date >='"""+str(date_from)+"""'  and invoice_date < '"""+str(date_to_m)+"""' 
                AND depot_id = '"""+str(depot_id)+"""' And level1_id = '"""+str(rsm_id)+"""'"""+ condition_item+"""
                group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
    retStr="""SELECT cid,'"""+str(current_date)+"""' as rpt_date,item_id,item_name, sum((quantity) * -1) as qty, actual_tp, category_id, level3_id,msoCategory,itembaseGroup,'"""+str(session.user_id)+"""' as user_id, """+str(s_text)+""" as s_text FROM sm_return  
                where status ='Returned' And category_id!='BONUS' and quantity > 0  and return_date >='"""+str(date_from)+"""'  and return_date < '"""+str(date_to_m)+"""' 
                AND depot_id = '"""+str(depot_id)+"""' And level1_id = '"""+str(rsm_id)+"""'"""+ condition_item+"""
                group by item_id, actual_tp, category_id, level3_id,msoCategory,itembaseGroup """
     
#     return invoiceStr
#     return retStr
    
    strInvoice="""INSERT INTO z_tr_report (cid,rpt_date,item_id,item_name,quantity,actual_tp,category_id,level3_id,msoCategory,itembaseGroup,user_id,s_text) """+invoiceStr
    invInsert=db.executesql(strInvoice)
    strRet="""INSERT INTO z_tr_report (cid,rpt_date,item_id,item_name,quantity,actual_tp,category_id,level3_id,msoCategory,itembaseGroup,user_id,s_text) """+retStr
    retInsert=db.executesql(strRet) 

#     return invInsert
#     if invInsert > 0 or retInsert > 0:
    session.s_text=s_text
    session.flash='Processed Successfully '
    redirect (URL('report_sales','home'))
    
    
# ==============
def TRReportInvoicePeriodical():  
    response.title='salesClosingStockS'    
#     return len(session.s_text)
    
    if session.s_text==None:
        session.flash='Please Process First'
        redirect (URL('report_sales','home'))
        
    if len(session.s_text) < 10:
        session.flash='Please Process First'
        redirect (URL('report_sales','home'))
    
    search_criteria= (session.s_text).replace("'","")
    search_criteriaList=search_criteria.split(',')
    c_id=session.cid   
#     return search_criteriaList[0]
    
    date_from=search_criteriaList[0]
    date_to=search_criteriaList[1]
    depot_id=search_criteriaList[2]
    depot_name=search_criteriaList[3]  
    store_id=search_criteriaList[4]
    store_name=search_criteriaList[5]
    rsm_id=search_criteriaList[6]
    rsm_name=search_criteriaList[7]
    fm_id=search_criteriaList[8]
    fm_name=search_criteriaList[9]
    tr_id=search_criteriaList[10]
    tr_name=search_criteriaList[11]
    product_id=search_criteriaList[12]
    product_name=search_criteriaList[13]

    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    date_to_m= str(date_to_m)[0:10]
    
    dateMSO=str(date_from)[0:7] + '-01'
#     return dateMSO
#     if depot_id=='' and store_id=='':
    if depot_id=='' :
       session.flash='Please select Depot'
       redirect (URL('report_sales','home'))
       
    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
    

    
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
    
    if (depot_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
    if (store_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==product_id) 
        
    stockitemRecords=qsetStock.select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
#     return stockitemRecords
   
    itemStockStr=''
    for recordStock in stockitemRecords:
     itemStock=str(recordStock[db.sm_depot_stock_balance.item_id])
     balanceStock=str(recordStock[db.sm_depot_stock_balance.quantity.sum()])

     itemStockStr=itemStockStr+itemStock+'|'+balanceStock+'<rdrd>'
     
#     return itemStockStr
    
#     ========================
    condition_item=''
    if (product_id!=''):
        condition_item=condition_item+" AND item_id = '"+str(product_id)+"'"
    itemRecordsStr="""select 
        item_id, item_name, actual_tp, category_id
        from 
        z_tr_report where 
        user_id='"""+str(session.user_id)+"""' GROUP BY item_id, actual_tp, category_id  ORDER BY  item_id, actual_tp, category_id ;"""
    
#     return itemRecordsStr
    itemRecords=db.executesql(itemRecordsStr,as_dict = True) 
    
#     ========================
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1_id = '"+str(rsm_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
        
    if (fm_id!=''):
        condition_fm=condition_fm+" AND level2_id = '"+str(fm_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
    if (tr_id!=''):
        condition_fm=condition_fm+" AND area_id = '"+str(tr_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
#     return c_id
    fmRecordsStr="SELECT area_id  FROM z_mso_area WHERE  first_date='"+dateMSO+"' and cid='"+c_id +"'"+condition_fm+" GROUP BY area_id  ORDER BY  area_id;"
#     return fmRecordsStr
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 
    
#     return fmRecordsStr
    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
#     if (store_id!=''):
#         condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition_inv=condition_inv+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_inv=condition_inv+" AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
#     ================FmList
    
    fDate=str(date_from).split('-')[0]+'-'+str(date_from).split('-')[1]+'-'+'1'
#     return fDate
#     fDate=str(first_currentDate)[0:10]
    fmInvStr="""select area_id,rep_id,rep_category from  z_mso_area where first_date ='"""+str(dateMSO)+"""' and cid <='"""+str(c_id)+"""' """+""" GROUP BY area_id,rep_id,rep_category  ORDER BY  area_id,rep_id,rep_category;"""
#     return fmInvStr
    fmInvRecords=db.executesql(fmInvStr,as_dict = True) 
    
    fmStr=''
    trFMPast=''
    for fm in range(len(fmInvRecords)):
        fmInvRecord=fmInvRecords[fm]
        trfm=str(fmInvRecord['area_id'])
        if (trfm!=trFMPast):
            fmStr=fmStr+'<'+str(trfm)+'>'
        fmStr=fmStr+str(fmInvRecord['rep_category'])+','
        trFMPast=str(fmInvRecord['area_id']) 
    fmStr=fmStr+'<'
#     return fmStr  
    
#     ===============FM List End
    
    
    

    
    invRecordsStr="""select 
        item_id, item_name, actual_tp, category_id,level3_id ,sum(quantity) as qty,msoCategory,itembaseGroup 
        from 
        z_tr_report where 
        user_id='"""+str(session.user_id)+"""' GROUP BY level3_id,item_id,category_id,actual_tp  ORDER BY  level3_id,item_id,category_id,actual_tp;"""

    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
#     return fmStr
    invStr=''
    trPast=''
#     return len(invRecords)
    for inv in range(len(invRecords)):
        categoryID=''
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
         
            trFMInfo1=fmStr.split('<'+str(tr)+'>')
            trFMInfo=trFMInfo1[1].split('<')
            
    

        if (trFMInfo[0].find(recordInv['category_id']) !=-1):
#             if tr=='CT43':
#                 return recordInv['category_id']
            categoryID=str(recordInv['category_id'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='C')):
            categoryID=str(recordInv['itembaseGroup'])
            if (str(recordInv['itembaseGroup'])==''):
                if (trFMInfo[0].find('A') !=-1):
                    categoryID='A'
                if (trFMInfo[0].find('B') !=-1):
                    categoryID='B'
                if (trFMInfo[0].find('Z') !=-1):
                    categoryID='Z'
            else:
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) !=-1) ):
                    categoryID=recordInv['itembaseGroup']
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='A')):
                    if (trFMInfo[0].find('B') !=-1):
                        categoryID='B'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z'     
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='B')):
                    if (trFMInfo[0].find('A') !=-1):
                        categoryID='A'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z' 
            
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='A')):
            if (trFMInfo[0].find('B') !=-1):
                categoryID='B'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z' 
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='B')):
            if (trFMInfo[0].find('A') !=-1):
                categoryID='A'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z'
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='X')):
            categoryID=str(recordInv['msoCategory'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (str(recordInv['msoCategory'])=='') and (str(recordInv['itembaseGroup'])=='')):
            categoryID='Z'

        invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp'])+'fdfd'+categoryID+'fdfd'+str(recordInv['qty'])+'fdfd'+str(recordInv['actual_tp'])+'rdrd'
        trPast=str(recordInv['level3_id'])  
    invStr=invStr+'<'  
#     return invStr    
    
    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
#     myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
#     return len(fmrecords)
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['area_id'])
            fmFlag=1
        else:
            myString=myString+',,,,'+str(recordFm['area_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B,C,Z'
            n=n+1
    myString=myString+'\n'

    flagFm=0
    itemCheck_past=''
    item_past=''
#     for record in itemRecords:
#     return len(itemRecords)
    for r in range(len(itemRecords)):
        record=itemRecords[r]
        item=str(record['item_id'])
        acTP=str(record['actual_tp'])
        itemCheck=str(item)+'|'+str(acTP)
        if itemCheck!=itemCheck_past:
            
            stockStock=0
    #         return itemStockStr
            if itemStockStr.find(str(item)+'|')!=-1:
    #             return itemStockStr.find(str(item)+'|')
                sp=str(item)+'|'
                stockStock=itemStockStr.split(sp)[1].split('<rdrd>')[0]
    #             stockStock=stockStock1.split(sp)[1]#.split['<rdrd>'][0]
    #             return stockStock
            if item_past!=item:
                myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+str(stockStock)+','
            else:
                myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+','
            
            d_value=''
            for d in range(len(fmrecords)):
                recordfmStr=fmrecords[d]
                d_value=d_value+str(recordfmStr['area_id'])+str(d)
                tr=str(recordfmStr['area_id'])
                catA=0
                catB=0
                catC=0
                catZ=0
#                 return invStr
                if invStr.find(tr)==-1:
                    myString=myString+str(catA)+','+str(catB)+','+str(catC)+','+str(catZ)+','
                else:
#                    return tr
                   trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0] 
                   
#                    return trAllStr
#                    return itemCheck
                   if trAllStr.find(itemCheck)==-1:
                       myString=myString+str(catA)+','+str(catB)+','+str(catC)+','+str(catZ)+','
                   else:
                       trItemSingle1=trAllStr.split(itemCheck)[1]
                       
                       trItemSingle=trItemSingle1.split('rdrd')[0]
                       category=trItemSingle.split('fdfd')[1]
                       qty=trItemSingle.split('fdfd')[2]
    
                       if category=='A':
                           myString=myString+str(qty)+',0,0,0,'
                       if category=='B':
                           myString=myString+'0,'+str(qty)+',0,0,'
                       if category=='C':
                           myString=myString+'0,0,' +str(qty)+',0,'
                       if category=='Z':
                           myString=myString+'0,0,0,' +str(qty)+','
                           
                  
            myString=myString+'\n'
        itemCheck_past=itemCheck 
        item_past=item
        
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)




# ====================================================================================
def TRReportExCInvoicePeriodical():    
    response.title='salesClosingStockS'    
#     return len(session.s_text)
    if session.s_text==None:
        session.flash='Please Process First'
        redirect (URL('report_sales','home'))
    if len(session.s_text) < 10:
        session.flash='Please Process First'
        redirect (URL('report_sales','home'))
    
    search_criteria= (session.s_text).replace("'","")
    search_criteriaList=search_criteria.split(',')
    c_id=session.cid   
#     return search_criteriaList[0]
    
    date_from=search_criteriaList[0]
    date_to=search_criteriaList[1]
    depot_id=search_criteriaList[2]
    depot_name=search_criteriaList[3]  
    store_id=search_criteriaList[4]
    store_name=search_criteriaList[5]
    rsm_id=search_criteriaList[6]
    rsm_name=search_criteriaList[7]
    fm_id=search_criteriaList[8]
    fm_name=search_criteriaList[9]
    tr_id=search_criteriaList[10]
    tr_name=search_criteriaList[11]
    product_id=search_criteriaList[12]
    product_name=search_criteriaList[13]

    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  
    date_to_m= str(date_to_m)[0:10]
    dateMSO=str(date_from)[0:7] + '-01'
#     if depot_id=='' and store_id=='':
    if depot_id=='' :
       session.flash='Please select Depot '
       redirect (URL('report_sales','home'))
       
    if rsm_id=='' and fm_id=='' and tr_id=='':
       session.flash='Please select RSM or FM or TR'
       redirect (URL('report_sales','home'))
    

    
    qsetStock=db()
    qsetStock=qsetStock(db.sm_depot_stock_balance.cid==c_id)
    
    if (depot_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.depot_id==depot_id)
#     if (store_id!=''):
#         qsetStock=qsetStock(db.sm_depot_stock_balance.store_id==store_id) 
    if (product_id!=''):
        qsetStock=qsetStock(db.sm_depot_stock_balance.item_id==product_id) 
        
    stockitemRecords=qsetStock.select(db.sm_depot_stock_balance.item_id,db.sm_depot_stock_balance.quantity.sum(),orderby=db.sm_depot_stock_balance.item_id,groupby=db.sm_depot_stock_balance.item_id)
#     return stockitemRecords
   
    itemStockStr=''
    for recordStock in stockitemRecords:
     itemStock=str(recordStock[db.sm_depot_stock_balance.item_id])
     balanceStock=str(recordStock[db.sm_depot_stock_balance.quantity.sum()])

     itemStockStr=itemStockStr+itemStock+'|'+balanceStock+'<rdrd>'
     
#     return itemStockStr
    
#     ========================
    condition_item=''
    if (product_id!=''):
        condition_item=condition_item+" AND item_id = '"+str(product_id)+"'"
    itemRecordsStr="""select 
        item_id, item_name, actual_tp, category_id
        from 
        z_tr_report where 
        user_id='"""+str(session.user_id)+"""' GROUP BY item_id, actual_tp, category_id  ORDER BY  item_id, actual_tp, category_id ;"""
    
#     return itemRecordsStr
    itemRecords=db.executesql(itemRecordsStr,as_dict = True) 
    
#     ========================
    condition_fm=''
    if (rsm_id!=''):
        condition_fm=condition_fm+" AND level1_id = '"+str(rsm_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
        
    if (fm_id!=''):
        condition_fm=condition_fm+" AND level2_id = '"+str(fm_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
    if (tr_id!=''):
        condition_fm=condition_fm+" AND area_id = '"+str(tr_id)+"'"
#         condition_fm=condition_fm+" AND is_leaf = 1"
    
    fmRecordsStr="SELECT area_id  FROM z_mso_area WHERE  first_date='"+dateMSO+"' and cid='"+c_id +"'"+condition_fm+" GROUP BY area_id  ORDER BY  area_id;"
#     return fmRecordsStr
    fmrecords=db.executesql(fmRecordsStr,as_dict = True) 
    
#     return fmRecordsStr
    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+" AND depot_id = '"+str(depot_id)+"'"
#     if (store_id!=''):
#         condition_inv=condition_inv+" AND store_id = '"+str(store_id)+"'"
    if (rsm_id!=''):
        condition_inv=condition_inv+" AND level1_id = '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition_inv=condition_inv+" AND level2_id = '"+str(fm_id)+"'"
    if (tr_id!=''):
        condition_inv=condition_inv+" AND level3_id = '"+str(tr_id)+"'"
    if (product_id!=''):
        condition_inv=condition_inv+" AND item_id= '"+str(product_id)+"'"
        
#     ================FmList
    
    fDate=str(date_from).split('-')[0]+'-'+str(date_from).split('-')[1]+'-'+'1'
#     return fDate
#     fDate=str(first_currentDate)[0:10]
    fmInvStr="""select area_id,rep_id,rep_category from  z_mso_area where first_date ='"""+str(dateMSO)+"""' and cid <='"""+str(c_id)+"""' """+""" GROUP BY area_id,rep_id,rep_category  ORDER BY  area_id,rep_id,rep_category;"""
#     return fmInvStr
    fmInvRecords=db.executesql(fmInvStr,as_dict = True) 
    
    fmStr=''
    trFMPast=''
    for fm in range(len(fmInvRecords)):
        fmInvRecord=fmInvRecords[fm]
        trfm=str(fmInvRecord['area_id'])
        if (trfm!=trFMPast):
            fmStr=fmStr+'<'+str(trfm)+'>'
        fmStr=fmStr+str(fmInvRecord['rep_category'])+','
        trFMPast=str(fmInvRecord['area_id']) 
    fmStr=fmStr+'<'
#     return fmStr  
    
#     ===============FM List End
    
    
    

    
    invRecordsStr="""select 
        item_id, item_name, actual_tp, category_id,level3_id ,sum(quantity) as qty,msoCategory,itembaseGroup 
        from 
        z_tr_report where 
        user_id='"""+str(session.user_id)+"""' GROUP BY level3_id,item_id,category_id,actual_tp  ORDER BY  level3_id,item_id,category_id,actual_tp;"""

    invRecords=db.executesql(invRecordsStr,as_dict = True) 
    
#     return fmStr
    invStr=''
    trPast=''
#     return len(invRecords)
    for inv in range(len(invRecords)):
        categoryID=''
        recordInv=invRecords[inv]
        tr=str(recordInv['level3_id'])
        if (tr!=trPast):
            invStr=invStr+'<'+str(tr)+'>'
         
            trFMInfo1=fmStr.split('<'+str(tr)+'>')
            trFMInfo=trFMInfo1[1].split('<')
            
    

        if (trFMInfo[0].find(recordInv['category_id']) !=-1):
#             if tr=='CT43':
#                 return recordInv['category_id']
            categoryID=str(recordInv['category_id'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='C')):
            categoryID=str(recordInv['itembaseGroup'])
            if (str(recordInv['itembaseGroup'])==''):
                if (trFMInfo[0].find('A') !=-1):
                    categoryID='A'
                if (trFMInfo[0].find('B') !=-1):
                    categoryID='B'
                if (trFMInfo[0].find('Z') !=-1):
                    categoryID='Z'
            else:
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) !=-1) ):
                    categoryID=recordInv['itembaseGroup']
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='A')):
                    if (trFMInfo[0].find('B') !=-1):
                        categoryID='B'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z'     
                if ((trFMInfo[0].find(recordInv['itembaseGroup']) ==-1) and (recordInv['itembaseGroup']=='B')):
                    if (trFMInfo[0].find('A') !=-1):
                        categoryID='A'
                    if (trFMInfo[0].find('Z') !=-1):
                        categoryID='Z' 
            
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='A')):
            if (trFMInfo[0].find('B') !=-1):
                categoryID='B'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z' 
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='B')):
            if (trFMInfo[0].find('A') !=-1):
                categoryID='A'
            if (trFMInfo[0].find('Z') !=-1):
                categoryID='Z'
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (recordInv['category_id']=='X')):
            categoryID=str(recordInv['msoCategory'])
        if ((trFMInfo[0].find(recordInv['category_id']) ==-1) and (str(recordInv['msoCategory'])=='') and (str(recordInv['itembaseGroup'])=='')):
            categoryID='Z'

        invStr=invStr+str(recordInv['item_id'])+'|'+str(recordInv['actual_tp'])+'fdfd'+categoryID+'fdfd'+str(recordInv['qty'])+'fdfd'+str(recordInv['actual_tp'])+'rdrd'
        trPast=str(recordInv['level3_id'])  
    invStr=invStr+'<'  
#     return invStr    
    
    myString=''
    myString='Date Range,'+date_from+'to'+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
#     myString+='Store,'+store_id+'|'+store_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='TR,'+tr_id+'|'+tr_name+'\n'
    myString+='Item,'+product_id+'|'+product_name+'\n'
    flagItem=0
    x=0
    fmFlag=0
#     return len(fmrecords)
    for f in range(len(fmrecords)):
        recordFm=fmrecords[f]
        if fmFlag==0:
            myString=myString+',,,,'+str(recordFm['area_id'])
            fmFlag=1
        else:
            myString=myString+',,,'+str(recordFm['area_id']) 
        x=x+1
#     return x
    myString=myString+'\nItem,ItemName,TP,Stock'
    n=0
    while n < x:
            myString=myString+',A,B,Z'
            n=n+1
    myString=myString+'\n'

    flagFm=0
    itemCheck_past=''
    item_past=''
#     for record in itemRecords:
#     return len(itemRecords)
    for r in range(len(itemRecords)):
        record=itemRecords[r]
        item=str(record['item_id'])
        acTP=str(record['actual_tp'])
        itemCheck=str(item)+'|'+str(acTP)
        if itemCheck!=itemCheck_past:
            
            stockStock=0
    #         return itemStockStr
            if itemStockStr.find(str(item)+'|')!=-1:
    #             return itemStockStr.find(str(item)+'|')
                sp=str(item)+'|'
                stockStock=itemStockStr.split(sp)[1].split('<rdrd>')[0]
    #             stockStock=stockStock1.split(sp)[1]#.split['<rdrd>'][0]
    #             return stockStock
            if item_past!=item:
                myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+str(stockStock)+','
            else:
                myString=myString+str(record['item_id'])+','+str(record['item_name'])+','+str(record['actual_tp'])+','+','
            
            d_value=''
            for d in range(len(fmrecords)):
                recordfmStr=fmrecords[d]
                d_value=d_value+str(recordfmStr['area_id'])+str(d)
                tr=str(recordfmStr['area_id'])
                catA=0
                catB=0
                catC=0
                catZ=0
#                 return invStr
                if invStr.find(tr)==-1:
                    myString=myString+str(catA)+','+str(catB)+','+str(catZ)+','
                else:
                   
                   trAllStr=invStr.split('<'+tr+'>')[1].split('<')[0]
                   
#                    return trAllStr
#                    return itemCheck
                   if trAllStr.find(itemCheck)==-1:
                       myString=myString+str(catA)+','+str(catB)+','+str(catZ)+','
                   else:
                       trItemSingle1=trAllStr.split(itemCheck)[1]
                       
                       trItemSingle=trItemSingle1.split('rdrd')[0]
                       category=trItemSingle.split('fdfd')[1]
                       qty=trItemSingle.split('fdfd')[2]
    
                       if category=='A':
                           myString=myString+str(qty)+',0,0,'
                       if category=='B':
                           myString=myString+'0,'+str(qty)+',0,'
                       if category=='C':
                            myString=myString+'0,0,0,'
                       if category=='Z':
                           myString=myString+'0,0,' +str(qty)+','
                        
                  
            myString=myString+'\n'
        itemCheck_past=itemCheck 
        item_past=item
        
            
#     return myString 
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR.csv'   
    return str(myString)

# ==========================12.2==============================

def itemWiseSalesSDetailPeriodic_x():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition_inv=''
    if (depot_id!=''):
        condition_inv=condition_inv+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_inv=condition_inv+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_inv=condition_inv+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_inv=condition_inv+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_inv=condition_inv+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_inv=condition_inv+"AND area_id= '"+str(teritory_id)+"'"
    
    records_S="""select 
    item_id,item_name,item_vat,sum(inv_vat_amnt) as inv_vat_amnt,sum(ret_vat_amnt) as ret_vat_amnt,sum(Invqty) as Invqty,sum(Retqty) as Retqty,(Invqty-Retqty) as qty,
    sum(inv_bonus_qty) as inv_bonus_qty,sum(ret_bonus_qty) as ret_bonus_qty,sum(inv_tp) as inv_tp, sum(ret_tp) as ret_tp,sum(item_discount) as item_discount
    from
    (SELECT 
    item_id,item_name,(item_vat*quantity) as item_vat,(item_vat * quantity) as inv_vat_amnt,0 as ret_vat_amnt,quantity as Invqty,0 as Retqty,
    bonus_qty as inv_bonus_qty,0 as ret_bonus_qty,(quantity * actual_tp) as inv_tp,0 as ret_tp,item_discount
    FROM sm_invoice 
    where status ='Invoiced' And 
    category_id!='BONUS' and 
    invoice_date >="""+str(date_from)+""" and invoice_date < '"""+str(date_to_m)+"""' """+ condition_inv+"""
    union
    select 
    item_id,item_name,(item_vat*(quantity * -1)) as item_vat,0 as inv_vat_amnt,(item_vat*(quantity * -1)) as ret_vat_amnt,0 as Invqty,(quantity * -1) as Retqty,0 as inv_bonus_qty,
    bonus_qty as ret_bonus_qty,0 as inv_tp,(quantity * actual_tp) as ret_tp,item_discount
    FROM sm_return
    where status ='Returned' And 
    category_id!='BONUS' and 
    return_date >="""+str(date_from)+""" and return_date <='"""+str(date_to_m)+"""' """+ condition_inv+""") p GROUP BY item_id  ORDER BY  item_id,item_name;"""
    records=db.executesql(records_S,as_dict = True)
    
    recordsTotal_S="""select 
    item_vat,sum(inv_vat_amnt) as inv_vat_amnt,sum(ret_vat_amnt) as ret_vat_amnt,sum(Invqty) as Invqty,sum(Retqty) as Retqty,(Invqty-Retqty) as qty,
    sum(inv_bonus_qty) as inv_bonus_qty,sum(ret_bonus_qty) as ret_bonus_qty,sum(inv_tp) as inv_tp, sum(ret_tp) as ret_tp,sum(item_discount) as item_discount
    from
    (SELECT 
    (item_vat*quantity) as item_vat,(item_vat * quantity) as inv_vat_amnt,0 as ret_vat_amnt,quantity as Invqty,0 as Retqty,
    bonus_qty as inv_bonus_qty,0 as ret_bonus_qty,(quantity * actual_tp) as inv_tp,0 as ret_tp,item_discount
    FROM sm_invoice 
    where status ='Invoiced' And 
    category_id!='BONUS' and 
    invoice_date >="""+str(date_from)+""" and invoice_date < '"""+str(date_to_m)+"""' """+ condition_inv+"""
    union
    select 
    item_id,item_name,(item_vat*(quantity * -1)) as item_vat,0 as inv_vat_amnt,(item_vat*(quantity * -1)) as ret_vat_amnt,0 as Invqty,(quantity * -1) as Retqty,0 as inv_bonus_qty,
    bonus_qty as ret_bonus_qty,0 as inv_tp,(quantity * actual_tp) as ret_tp,item_discount
    FROM sm_return
    where status ='Returned' And 
    category_id!='BONUS' and 
    return_date >="""+str(date_from)+""" and return_date <='"""+str(date_to_m)+"""' """+ condition_inv+""") p;"""
    recordsTotal=db.executesql(recordsTotal_S,as_dict = True)
    
    
    
    invList = []
    invList_str = []
      
    retList = []
    retList_str = []
    
    qsetInv=db()
    qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
    qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
    qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
    qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
    qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
    qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
      
      
    qsetRet=db()
    qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
    qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
    qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
    qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
    qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
    qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
    qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
      
    if (depot_id!=''):
        qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
        qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
    if (store_id!=''):
        qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
        qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
          
    if (customer_id!=''):
        qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
        qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
       
    if (mso_id!=''):
        qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
        qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
    if (market_id!=''):
        qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
        qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
         
         
    
    invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
     
    retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
    for invCountRows in invCountRows:
        item_id = invCountRows[db.sm_invoice.item_id]
        invCount = invCountRows[db.sm_invoice_head.sl.count()]
        invList.append(item_id)
        invList_str.append(invCount)
     
    for retCountRows in retCountRows:
        retitem_id = retCountRows[db.sm_invoice.item_id]
        retCount = retCountRows[db.sm_invoice_head.sl.count()]
        retList.append(retitem_id)
        retList_str.append(retCount)
    
    return dict(records=records,recordsTotal=recordsTotal,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)
    
#     records_retS="""select 
#     item_id,item_name,sum(item_vat) as vat_amnt,sum(inv_vat_amnt) as inv_vat_amnt,sum(ret_vat_amnt) as ret_vat_amnt,Invqty,Retqty,(Invqty-Retqty) as qty,
#     sum(inv_bonus_qty) as inv_bonus_qty,sum(ret_bonus_qty) as ret_bonus_qty,sum(inv_tp) as inv_tp
#     from
#     (SELECT 
#     item_id,item_name,(item_vat*quantity) as item_vat,(item_vat * quantity) as inv_vat_amnt,0 as ret_vat_amnt,quantity as Invqty,0 as Retqty,
#     bonus_qty as inv_bonus_qty,0 as ret_bonus_qty,(quantity * actual_tp) as inv_tp
#     FROM sm_invoice 
#     where status ='Invoiced' And 
#     category_id!='BONUS' and 
#     invoice_date >="""+str(date_from)+""" and invoice_date < '"""+str(date_to_m)+"""' """+ condition_inv+"""
#     union
#     select 
#     item_id,item_name,(item_vat*(quantity * -1)) as item_vat,0 as inv_vat_amnt,(item_vat*(quantity * -1)) as ret_vat_amnt,0 as Invqty,(quantity * -1) as Retqty,0 as inv_bonus_qty,
#     bonus_qty as ret_bonus_qty,(quantity * actual_tp) as inv_tp
#     FROM sm_return
#     where status ='Returned' And 
#     category_id!='BONUS' and 
#     return_date >="""+str(date_from)+""" and return_date <='"""+str(date_to_m)+"""' """+ condition_inv+""") p ;"""
#     records_ret=db.executesql(records_retS,as_dict = True)
     
     
 
#     if len(records):
#         for records_ret in records_ret:
#             vat_amnt=records_ret['vat_amnt']
#             inv_qty=records_ret['inv_qty']
#             inv_bonus_qty=records_ret['inv_bonus_qty']
#             inv_tp=records_ret['inv_tp']
#             inv_amnt=records_ret['inv_amnt']
#             ret_qty=records_ret['ret_qty']
#             ret_bonus_qty=records_ret['ret_bonus_qty']
#             ret_amnt=records_ret['ret_amnt']
#             ret_vat_amnt=records_ret['ret_vat_amnt']
#             inv_vat_amnt=records_ret['inv_vat_amnt']
#              
#  
#             rtnP_total=(ret_amnt*100)/inv_amnt
#             nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
#  
#             rtnP_total=(ret_amnt*100)/inv_amnt
             
#         record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
 
#         total=0.0
#         
#          
#         for rec in record_sum:  
#             invDisc=rec[(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum()]    
#             returnDisc=rec[(db.sm_invoice_head.return_discount+db.sm_invoice_head.return_sp_discount).sum()]
#             disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
#             spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
#             retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
#             vatAmn=rec[db.sm_invoice_head.vat_total_amount.sum()]        
# #             disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
# #             spdisc=spdisc=rec[db.sm_invoice_head.sp_discount.sum()]-rec[(db.sm_invoice_head.return_sp_discount).sum()]
# #             retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]
#  
#      

            
#         return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total)
#         return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,disc=disc,inv_vat_amnt=inv_vat_amnt,invDisc=invDisc,returnDisc=returnDisc,spdisc=spdisc,retdisc=retdisc,ret_vat_amnt=ret_vat_amnt,vatAmn=vatAmn,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_tp=inv_tp,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,total=total)
#     else:
#         session.flash="Data Not Available"
#         redirect(URL(c='report_sales',f='home'))
           
def itemWiseSalesSDetailDLoad():
    c_id=session.cid
    response.title='Item Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    qset=db()
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset(db.sm_invoice.status=='Invoiced')
    qset=qset((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))


    qset_sum=db()
    qset_sum=qset_sum(db.sm_invoice_head.cid==c_id)
    qset_sum=qset_sum(db.sm_invoice_head.status=='Invoiced')
    qset_sum=qset_sum((db.sm_invoice_head.invoice_date >= date_from) & (db.sm_invoice_head.invoice_date < date_to_m))
    
    if (depot_id!=''):
        qset=qset(db.sm_invoice.depot_id==depot_id)
        qset_sum=qset_sum(db.sm_invoice_head.depot_id==depot_id)
    if (store_id!=''):
        qset=qset(db.sm_invoice.store_id==store_id)
        qset_sum=qset_sum(db.sm_invoice_head.store_id==store_id)
    if (customer_id!=''):
        qset=qset(db.sm_invoice.client_id==customer_id)
        qset_sum=qset_sum(db.sm_invoice_head.client_id==customer_id)
     
    if (mso_id!=''):
        qset=qset(db.sm_invoice.rep_id==mso_id)
        qset_sum=qset_sum(db.sm_invoice_head.rep_id==mso_id)
    if (market_id!=''):
        qset=qset(db.sm_invoice.market_id==market_id)
        qset_sum=qset_sum(db.sm_invoice_head.market_id==market_id)
        
    if (teritory_id!=''):
       qset=qset(db.sm_invoice.area_id==teritory_id)
       qset_sum=qset_sum(db.sm_invoice_head.area_id==teritory_id)
    
    records=qset.select(db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.actual_tp,db.sm_invoice.return_rate,db.sm_invoice.item_vat,(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum(),(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum(),db.sm_invoice.quantity.sum(),db.sm_invoice.price,db.sm_invoice.item_vat,(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum(),(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum(),(db.sm_invoice.return_rate *db.sm_invoice.return_qty).sum(),(db.sm_invoice.actual_tp*db.sm_invoice.quantity).sum(),(db.sm_invoice.quantity*db.sm_invoice.price).sum(),(db.sm_invoice.return_qty*db.sm_invoice.price).sum(),db.sm_invoice.bonus_qty.sum(),db.sm_invoice.return_qty.sum(),db.sm_invoice.return_bonus_qty.sum(),db.sm_invoice.item_discount.sum(),orderby=db.sm_invoice.item_name ,groupby=db.sm_invoice.item_id|db.sm_invoice.item_name)
   
    
    condition_ret=''
    if (depot_id!=''):
        condition_ret=condition_ret+"AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition_ret=condition_ret+"AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition_ret=condition_ret+"AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition_ret=condition_ret+"AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition_ret=condition_ret+"AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition_ret=condition_ret+"AND area_id= '"+str(teritory_id)+"'"
    
    records_retS="SELECT  sum(item_vat * (quantity-return_qty)) as vat_amnt, sum(quantity) as inv_qty ,sum(bonus_qty) as inv_bonus_qty,sum(quantity * actual_tp) as inv_tp,sum(quantity * actual_tp) as inv_amnt,sum(return_qty) as ret_qty,sum(return_bonus_qty) as ret_bonus_qty,sum(return_qty * actual_tp) as ret_amnt FROM sm_invoice WHERE cid = '"+ c_id +"' AND status = 'Invoiced' AND     invoice_date >= '"+str(date_from)+"' AND     invoice_date < '"+str(date_to_m)+"'"+condition_ret+"  limit  1;"
    records_ret=db.executesql(records_retS,as_dict = True) 

    if records:
        for records_ret in records_ret:
            vat_amnt=records_ret['vat_amnt']
            inv_qty=records_ret['inv_qty']
            inv_bonus_qty=records_ret['inv_bonus_qty']
            inv_tp=records_ret['inv_tp']
            inv_amnt=records_ret['inv_amnt']
            ret_qty=records_ret['ret_qty']
            ret_bonus_qty=records_ret['ret_bonus_qty']
            ret_amnt=records_ret['ret_amnt']
            vat_amnt=records_ret['vat_amnt']
            

            rtnP_total=(ret_amnt*100)/inv_amnt
            nsP_total =((inv_amnt-ret_amnt) *100)/inv_amnt
            
            
            
            
            rtnP_total=(ret_amnt*100)/inv_amnt
            
#         return ret_amnt
        record_sum=qset_sum.select((db.sm_invoice_head.return_tp+db.sm_invoice_head.return_discount).sum(),db.sm_invoice_head.total_amount.sum(),(db.sm_invoice_head.discount+db.sm_invoice_head.sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.discount.sum(),db.sm_invoice_head.sp_discount.sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_tp.sum(),db.sm_invoice_head.return_vat.sum(),(db.sm_invoice_head.return_discount).sum(),(db.sm_invoice_head.return_sp_discount).sum(),db.sm_invoice_head.vat_total_amount.sum(),db.sm_invoice_head.return_vat.sum(), limitby=(0,1))
#         return db._lastsql
        total=0.0
       
        
        for rec in record_sum:          
            disc=rec[db.sm_invoice_head.discount.sum()]-rec[db.sm_invoice_head.return_discount.sum()]
            spdisc=rec[db.sm_invoice_head.sp_discount.sum()]
            retdisc=rec[db.sm_invoice_head.return_sp_discount.sum()]

    
        invList = []
        invList_str = []
        
        retList = []
        retList_str = []
    
        qsetInv=db()
        qsetInv=qsetInv(db.sm_invoice_head.cid==c_id)
        qsetInv=qsetInv(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetInv=qsetInv(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetInv=qsetInv(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetInv=qsetInv(db.sm_invoice.status=='Invoiced')
        qsetInv=qsetInv((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        
        qsetRet=db()
        qsetRet=qsetRet(db.sm_invoice_head.cid==c_id)
        qsetRet=qsetRet(db.sm_invoice.cid==db.sm_invoice_head.cid)
        qsetRet=qsetRet(db.sm_invoice.sl==db.sm_invoice_head.sl)
        qsetRet=qsetRet(db.sm_invoice.depot_id==db.sm_invoice_head.depot_id)
        qsetRet=qsetRet(db.sm_invoice.status=='Invoiced')
        qsetRet=qsetRet(db.sm_invoice.return_qty!=0)
        qsetRet=qsetRet((db.sm_invoice.invoice_date >= date_from) & (db.sm_invoice.invoice_date < date_to_m))
        
        if (depot_id!=''):
            qsetInv=qsetInv(db.sm_invoice.depot_id==depot_id)  
            qsetRet=qsetRet(db.sm_invoice.depot_id==depot_id)   
        if (store_id!=''):
            qsetInv=qsetInv(db.sm_invoice.store_id==store_id)
            qsetRet=qsetRet(db.sm_invoice.store_id==store_id)
            
        if (customer_id!=''):
            qsetInv=qsetInv(db.sm_invoice.client_id==customer_id)
            qsetRet=qsetRet(db.sm_invoice.client_id==customer_id)
         
        if (mso_id!=''):
            qsetInv=qsetInv(db.sm_invoice.rep_id==mso_id)
            qsetRet=qsetRet(db.sm_invoice.rep_id==mso_id)
        if (market_id!=''):
            qsetInv=qsetInv(db.sm_invoice.market_id==market_id)
            qsetRet=qsetRet(db.sm_invoice.market_id==market_id)
            
            
      
        invCountRows=qsetInv.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
        
        retCountRows=qsetRet.select(db.sm_invoice.item_id,db.sm_invoice_head.sl.count(),orderby=db.sm_invoice.item_name,groupby=db.sm_invoice.item_id)
    #     return invCountRows
        for invCountRows in invCountRows:
            item_id = invCountRows[db.sm_invoice.item_id]
            invCount = invCountRows[db.sm_invoice_head.sl.count()]
            invList.append(item_id)
            invList_str.append(invCount)
        
        for retCountRows in retCountRows:
            retitem_id = retCountRows[db.sm_invoice.item_id]
            retCount = retCountRows[db.sm_invoice_head.sl.count()]
            retList.append(retitem_id)
            retList_str.append(retCount)
            
       
       
        myString='12.2\n\n'
        myString=myString+'Item Wise Sales Statement Detail\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        

        
        myString+='Item,ItemName,InvCount,RetCount, InvS.Qty,InvB.Qty,InvTP,RetS.Qty,RetB.Qty,RetTP,RTN%,NetS.Qty,NetB.Qty,NetTP,Disc,Vat,Net (TP+Vat),NS%\n'
          
        for record in records:
            itmInv=0
            itmRet=0
            item_id =record[db.sm_invoice.item_id]
            if [s for s in invList if item_id in s]:
                index_element = invList.index(item_id)           
                itmInv=invList_str[index_element]
            if [s for s in retList if item_id in s]:
                ret_index_element = retList.index(item_id)           
                itmRet=retList_str[ret_index_element]
            invSale= float(record[(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum()])
            netRet= record[(db.sm_invoice.actual_tp *db.sm_invoice.return_qty).sum()]
            rtnP=0
               
            if (invSale > 0):
                rtnP=(netRet*100)/invSale
            netQty=int(record[db.sm_invoice.quantity.sum()])-int(record[db.sm_invoice.return_qty.sum()])
            netSale  =  invSale-netRet 
            vat=record[(db.sm_invoice.item_vat*db.sm_invoice.quantity).sum()]-record[(db.sm_invoice.item_vat*db.sm_invoice.return_qty).sum()]
            nsP=0
            if (invSale > 0):
                nsP =(netSale *100)/invSale
                                                                                                                                        
       
            disc=record[db.sm_invoice.item_discount.sum()]                                                                                                                                                    
            myString+=str(record[db.sm_invoice.item_id])+','+str(record[db.sm_invoice.item_name])+','+str(itmInv)+','+str(itmRet)+','+str(record[db.sm_invoice.quantity.sum()])+','+str(record[db.sm_invoice.bonus_qty.sum()])+','+str(record[(db.sm_invoice.actual_tp *db.sm_invoice.quantity).sum()])+','+str(record[db.sm_invoice.return_qty.sum()])+','+str(record[db.sm_invoice.return_bonus_qty.sum()])+','+str(netRet)+','+str(round(rtnP,2))+','+str(netQty)+','+str(int(record[db.sm_invoice.bonus_qty.sum()])-int(record[db.sm_invoice.return_bonus_qty.sum()]))+','+str(invSale - netRet)+','+str(disc)+','+str(vat)+','+str(netSale+vat)+','+str(round(nsP,2))+'\n'
#         return myString
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=ItemWiseSalesStatementDetail.csv'   
        return str(myString)  
        
#         return dict(records=records,invList=invList,invList_str=invList_str,retList=retList,retList_str=retList_str,vat_amnt=vat_amnt,inv_qty=inv_qty,inv_bonus_qty=inv_bonus_qty,inv_amnt=inv_amnt,ret_qty=ret_qty,ret_bonus_qty=ret_bonus_qty,ret_amnt=ret_amnt,rtnP_total=rtnP_total,nsP_total=nsP_total,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,total=total,page=page,items_per_page=items_per_page)
    else:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))
        

#=========================== a ============



def msoWiseSalesSDetailPeriodic():
    c_id=session.cid
    response.title='12.8 MSO Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT cid,level2_id,area_id,`rep_id`,rep_name,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT cid,level2_id,area_id,`rep_id`,rep_name,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select level2_id,area_id,`rep_id`,rep_name,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by rep_id;"
    records=db.executesql(records,as_dict = True)
        
    records_sum="select level2_id,area_id,`rep_id`,rep_name,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
     
    return dict(records=records,records_sum=records_sum,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)

def msoWiseSalesSDetailDLoadPeriodic():
    c_id=session.cid
    response.title='12.8 MSO Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT cid,level2_id,area_id,`rep_id`,rep_name,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT cid,level2_id,area_id,`rep_id`,rep_name,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select level2_id,area_id,`rep_id`,rep_name,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by rep_id;"
    records=db.executesql(records,as_dict = True)
        
    records_sum="select level2_id,area_id,`rep_id`,rep_name,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
 
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='12.8\n\n'
        myString=myString+'MSO Wise Sales Statement Detail Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString+='Summary\n'
        myString+='Inv TP,Ret TP,Net TP,Sp Disc,Reg Disc,Vat,Net (TP+Vat)\n'
        
                    
       
        for j in range(len(records_sum)):
            record_sum=records_sum[j]
                       
            invTp=float(record_sum['invTp'])
            
            invDisc=float(record_sum['invDisc'])
            invSpDisc=float(record_sum['invSpDisc'])           
            
            retTp=record_sum['retTp']            
            
            netTp=record_sum['invTp']-record_sum['retTp']
            
            disc=float(record_sum['invDisc']-record_sum['retDisc'])
            spDisc=float(record_sum['invSpDisc']-record_sum['retSpDisc'])
            
            netVat=record_sum['invVat']-record_sum['retVat']
            
            netTpVat=float(netTp+netVat-(disc+spDisc))
            
                   
            myString+=str(round(invTp,2))+','+str(round(retTp,2))+','+str(round(netTp,2))+','+str(round(spDisc,2))+','+str(round(disc,2))+','+str(round(netVat,2))+','+str(round(netTpVat,2))+'\n\n'
       
       
       
        myString+='MSO ID,MSO Name,TR,FM,Inv. Count,Ret. Count,Inv TP,Ret TP,Net TP,Disc,Vat,Net\n'
       
        for k in range(len(records)):
            record=records[k]  
            
            msoIDD=record['rep_id']
            msoNameD=record['rep_name']
            trD=record['level2_id']
            fmD=record['area_id']
            invCountD=record['invCount']
            retInvCountD=record['retInvCount']
            invTpD=float(record['invTp'])
            invDiscD=record['invDisc']
            invSpDiscD=record['invSpDisc']
            invVatD=record['invVat']
             
            retTpD=record['retTp']
            retDiscD=record['retDisc']
            retSpDiscD=record['retSpDisc']
            retVatD=record['retVat']       
            
            netTpD=record['invTp']-record['retTp']
            netDiscD=record['invDisc']-record['retDisc']
            netSpDiscD=record['invSpDisc']-record['retSpDisc']
            netVatD=float(record['invVat']-record['retVat'])
            
            netTpVatD=float(netTpD+netVatD-(netDiscD+netSpDiscD))
                        
            
            myString+=str(msoIDD)+','+str(msoNameD)+','+str(trD)+','+str(fmD)+','+str(invCountD)+','+str(retInvCountD)+','+str(round(invTpD,2))+','+str(round(retTpD,2))+','+str(round(netTpD,2))+','+str(netDiscD)+','+str(round(netVatD,2))+','+str(round(netTpVatD,2))+'\n'
       
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=msoWiseSalesStatementDetailPeriodic.csv'   
        return str(myString)   


def dpWiseSalesSDetailPeriodic():
    c_id=session.cid
    response.title='12.9 DP Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
        
    tranInvSql="(SELECT cid,`d_man_id`,`d_man_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT cid,`d_man_id`,`d_man_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    records=db.executesql(records,as_dict = True)
        
    records_sum="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
     
    
    return dict(records=records,records_sum=records_sum,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)

def dpWiseSalesSDetailDLoadPeriodic():
    c_id=session.cid
    response.title='12.9 DP Wise Sales Statement Detail'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT cid,`d_man_id`,`d_man_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT cid,`d_man_id`,`d_man_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    records=db.executesql(records,as_dict = True)
        
    records_sum="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
        
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='12.9\n\n'
        myString=myString+'DP Wise Sales Statement Detail\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString+='Summary\n'
        myString+='Inv TP, Inv Disc, Inv Vat, Inv Net, Ret TP,Ret Disc, Ret Vat, Ret Net, Net TP, Sp Disc, Reg Disc, Net Vat, Net\n'
        
                    
        
        
        for j in range(len(records_sum)):
            record_sum=records_sum[j]
                       
            invTp=float(record_sum['invTp'])
            invDisc=float(record_sum['invDisc'])
            invSpDisc=float(record_sum['invSpDisc']) 
            invVat=float(record_sum['invVat']) 
            netInv=record_sum['invTp']+record_sum['invVat']-(record_sum['invDisc']+record_sum['invSpDisc'])                                
            retTp=record_sum['retTp']
            retDisc=float(record_sum['retDisc'])
            retSpDisc=float(record_sum['retSpDisc'])            
            retVat=record_sum['retVat']
            netRet=record_sum['retTp']+record_sum['retVat']-(record_sum['retDisc']+record_sum['retSpDisc'])
            
                               
            myString+=str(round(invTp,2))+','+str(round(invDisc+invSpDisc,2))+','+str(round(invVat,2))+','+str(round(netInv,2))+','+str(round(retTp,2))+','+str(round(retDisc+retSpDisc,2))+','+str(round(retVat,2))+','+str(round(netRet,2))+','+str(round((invTp-retTp),2))+','+str(round((invSpDisc-retSpDisc),2))+','+str(round((invDisc-retDisc),2))+','+str(round((invVat-retVat),2))+','+str(round((netInv-netRet),2))+'\n\n'
       
       
       
        myString+='DM ID,DM Name,Inv. Count,Ret. Count,Inv TP, Inv Disc, Inv Vat, Inv Net,Ret TP, Ret Disc, Ret Vat, Ret Net,Net Tp, Net Disc, Net Vat, Net Tp\n'
       
        for k in range(len(records)):
            record=records[k]  
            
                        
            dmID=record['d_man_id']
            dmNameD=record['d_man_name']
            invCountD=record['invCount']
            retInvCountD=record['retInvCount']
            invTpD=float(record['invTp'])
            invDiscD=float(record['invDisc']+record['invSpDisc'])
            invVatD=float(record['invVat'])
            invNetTpD=float(record['invTp']+record['invVat']-invDiscD) 
            
            retTpD=record['retTp'] 
            retDiscD=record['retDisc']+record['retSpDisc']
            retVatD=record['retVat']           
            retNetTpD=record['retTp']+record['retVat']-retDiscD
            
            netTpD=record['invTp']-record['retTp']
            netDiscD=invDiscD-retDiscD
            netVatD=float(record['invVat']-record['retVat'])
            netTpVatD=float(invNetTpD-retNetTpD)
                        
            
            myString+=str(dmID)+','+str(dmNameD)+','+str(invCountD)+','+str(retInvCountD)+','+str(invTpD)+','+str(invDiscD)+','+\
            str(round(invVatD,2))+','+str(round(invNetTpD,2))+','+str(round(retTpD,2))+','+str(retDiscD)+','+str(round(retVatD,2))+','+\
            str(round(retNetTpD,2))+','+str(round(netTpD,2))+','+str(round(netDiscD,2))+','+str(round(netVatD,2))+','+str(round(netTpVatD,2))+'\n'
       
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=dpWiseSalesStatementDetailPeriodic.csv'   
        return str(myString)   

def dp_wise_sale_ss_periodic():
    c_id=session.cid
    response.title='15 DP Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `d_man_id`,`d_man_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `d_man_id`,`d_man_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    
    records=db.executesql(records,as_dict = True)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)


def dp_wise_sale_ss_d_periodic():
    c_id=session.cid
    response.title='15 DP Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `d_man_id`,`d_man_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `d_man_id`,`d_man_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    
    records=db.executesql(records,as_dict = True)
      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='15\n\n'
        myString=myString+'DP Wise Sales Statement Detail Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        
        
        myString+='DP ID,Delivery Person Name,No. of Inv,Full Return No,Inv Amnt,Ret Amnt,Exec%,Ret%,Net Sold TP\n'
        
        execPer=0
        retPer=0
         
        totalInv=0
        totalRet=0
        totalInvTp=0
        totalRetTp=0
        totalExecPer=0
        totalRetPer=0
        totalNetTp=0        
          
        for k in range(len(records)):
            record=records[k]  
            
            d_man_id=record['d_man_id']
            d_man_name=record['d_man_name']
            invCount=record['invCount']
            retInvCount=record['retInvCount']
            invTp=record['invTp']
            retTp=record['retTp']           
            execPer=100-(round((record['retTp']*100/record['invTp']),2))
            retPer=round((record['retTp']*100/record['invTp']),2)
            netTp=record['invTp']-record['retTp']
            
            totalInv+=invCount
            totalRet+=retInvCount
            totalInvTp+=invTp
            totalRetTp+=retTp
           
                                    
            
            myString+=str(d_man_id)+','+str(d_man_name)+','+str(invCount)+','+str(retInvCount)+','+str(invTp)+','+str(retTp)+','+str(execPer)+','+str(retPer)+','+str(round(netTp,2))+'\n'
       
        
                
        myString+=',,'+str(totalInv)+','+str(totalRet)+','+str(totalInvTp)+','+str(totalRetTp)+','+str(100-(round((totalRetTp*100/totalInvTp),2)))+','+str(round((totalRetTp*100/totalInvTp),2))+','+str(round((totalInvTp-totalRetTp),2))+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=dpWiseSalesDetailsPeriodic.csv'   
        return str(myString)


def catDPwiseSPeriodic():
    c_id=session.cid
    response.title='17.2 Category and DP wise Sales. Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `d_man_id`,`d_man_name`,`market_id`,`market_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `d_man_id`,`d_man_name`,`market_id`,`market_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,`market_id`,`market_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    
    records=db.executesql(records,as_dict = True)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)

def catDPwiseSDPeriodic():
    c_id=session.cid
    response.title='17.2 Category and DP wise Sales. Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `d_man_id`,`d_man_name`,`market_id`,`market_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `d_man_id`,`d_man_name`,`market_id`,`market_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `d_man_id`,`d_man_name`,`market_id`,`market_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by d_man_id;"
    
    records=db.executesql(records,as_dict = True)
      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='17.2\n\n'
        myString=myString+'Category and DP wise Sales. Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
                
        myString+='DP ID,DP Name,Market ID, Market Name,Inv Amnt,Ret Amnt,No. of Inv,Full Return No,Exec%,Ret%,Net Sold TP\n'
        
        execPer=0
        retPer=0
         
        totalInv=0
        totalRet=0
        totalInvTp=0
        totalRetTp=0
        totalExecPer=0
        totalRetPer=0
        totalNetTp=0        
          
        for k in range(len(records)):
            record=records[k]  
            
            d_man_id=record['d_man_id']
            d_man_name=record['d_man_name']
            market_id=record['market_id']
            market_name=record['market_name']            
            
            invTp=record['invTp']
            retTp=record['retTp'] 
            invCount=record['invCount']
            retInvCount=record['retInvCount']
                      
            execPer=100-(round((record['retTp']*100/record['invTp']),2))
            retPer=round((record['retTp']*100/record['invTp']),2)
            netTp=record['invTp']-record['retTp']
            
            totalInv+=invCount
            totalRet+=retInvCount
            totalInvTp+=invTp
            totalRetTp+=retTp                                            
            
            myString+=str(d_man_id)+','+str(d_man_name)+','+str(market_id)+','+str(market_name)+','+str(invCount)+','+str(retInvCount)+','+str(invTp)+','+str(retTp)+','+str(execPer)+','+str(retPer)+','+str(round(netTp,2))+'\n'
                               
        myString+=',,,,'+str(totalInvTp)+','+str(totalRetTp)+','+str(totalInv)+','+str(totalRet)+','+str(100-(round((totalRetTp*100/totalInvTp),2)))+','+str(round((totalRetTp*100/totalInvTp),2))+','+str(round((totalInvTp-totalRetTp),2))+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=catDpWiseSalesPeriodic.csv'   
        return str(myString)

def msowiseSPeriodic():
    c_id=session.cid
    response.title='MSO Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `rep_id`,`rep_name`,`market_id`,`market_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `rep_id`,`rep_name`,`market_id`,`market_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `rep_id`,`rep_name`,`market_id`,`market_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by rep_id;"
    
    records=db.executesql(records,as_dict = True)
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)

def msowiseSDPeriodic():    
    c_id=session.cid
    response.title='17.1 MSO Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    tranInvSql="(SELECT `rep_id`,`rep_name`,`market_id`,`market_name`,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,0 as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT `rep_id`,`rep_name`,`market_id`,`market_name`,`inv_sl` as invSl,`inv_sl` as retInvSl,0 as invTp,`tp_amt` as retTp FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select `rep_id`,`rep_name`,`market_id`,`market_name`,count(distinct(invSl)) as invCount,count(distinct(retInvSl))-1 as retInvCount,sum(invTp) as invTp,sum(retTp*-1) as retTp from ("+tranInvSql+" union all "+tranRetSql+") p group by rep_id;"
    
    
    records=db.executesql(records,as_dict = True)
      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='17.1\n\n'
        myString=myString+'MSO Wise Sales Statement Detail Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        
        myString+='MSO TR,MSO Name,Market ID,Market Name,Inv Amnt,Ret Amnt,No. of Inv.,Full Return No,Exec%,Ret%,Net Sold TP\n'
        
               
        for k in range(len(records)):
            record=records[k]  
            
            rep_id=record['rep_id']
            rep_name=record['rep_name']
            market_id=record['market_id']
            market_name=record['market_name']
            invTp=float(record['invTp'])
            retTp=float(record['retTp'])
            invCount=float(record['invCount'])
            retInvCount=float(record['retInvCount'])
            execPer=100-(round((record['retTp']*100/record['invTp']),2)) 
            retPer=round((record['retTp']*100/record['invTp']),2)            
            netTp=record['invTp']-record['retTp']
                        
            
            myString+=str(rep_id)+','+str(rep_name)+','+str(market_id)+','+str(market_name)+','+str(invTp)+','+str(retTp)+','+\
            str(invCount)+','+str(retInvCount)+','+str(round(execPer,2))+','+str(round(retPer,2))+','+str(round(netTp,2))+'\n'
       
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=msoWiseSalesStatementPeriodic.csv'   
        return str(myString)
    

def summaryReportPeriodic():
    c_id=session.cid
    response.title='11 Summary Report Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    tranInvSql="(SELECT level1_id,level2_id,area_id as level3_id,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT level1_id,level2_id,area_id as level3_id,`inv_sl` as invSl,1 as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select level1_id,level2_id,level3_id,count(distinct(invSl)) as invCount,sum(retInvSl) as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by level1_id,level2_id,level3_id;"
    records=db.executesql(records,as_dict = True)
            
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)


def summaryReportDPeriodic():
    c_id=session.cid
    response.title='11 Summary Report Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    tranInvSql="(SELECT level1_id,level2_id,area_id as level3_id,`inv_sl` as invSl,0 as retInvSl,`tp_amt` as invTp,`vat_amt` as invVat,`disc_amt` as invDisc,`spdisc_amt` as invSpDisc,0 as retTp,0 as retVat,0 as retDisc,0 as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and `transaction_type`='INV' "+condition+") "
    tranRetSql="(SELECT level1_id,level2_id,area_id as level3_id,`inv_sl` as invSl,1 as retInvSl,0 as invTp,0 as invVat,0 as invDisc,0 as invSpDisc,`tp_amt` as retTp,`vat_amt` as retVat,`disc_amt` as retDisc,`spdisc_amt` as retSpDisc FROM `sm_rpt_transaction` WHERE cid='"+c_id+"' and transaction_date>='"+date_from+"' and transaction_date<='"+date_to+"' and `transaction_type`='RET' "+condition+") "
    records="select level1_id,level2_id,level3_id,count(distinct(invSl)) as invCount,sum(retInvSl) as retInvCount,sum(invTp) as invTp,sum(invVat) as invVat,sum(invDisc) as invDisc,sum(invSpDisc) as invSpDisc,sum(retTp*-1) as retTp,sum(retVat*-1) as retVat,sum(retDisc*-1) as retDisc,sum(retSpDisc*-1) as retSpDisc from ("+tranInvSql+" union all "+tranRetSql+") p group by level1_id,level2_id,level3_id;"
    records=db.executesql(records,as_dict = True)      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='11\n\n'
        myString=myString+'Summary Report Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
                                
        myString+='RSM,FM,TR,InvCount,Inv Amount,Inv TP,Inv Vat,Inv Disc,Inv SP.Disc,Ret Amount,Ret TP,Ret Vat,Ret Disc,Ret SP.Disc,Net\n'
        
        
        totalInvAmt=0
        totalInvTp=0
        totalRetAmt=0
        totalRetTp=0
        
        totalNetTp=0        
          
        for k in range(len(records)):
            record=records[k]  
            
            level1_id=record['level1_id']
            level2_id=record['level2_id']
            level3_id=record['level3_id']
            invCount=record['invCount']            
                        
            invTp=record['invTp'] 
            invVat=record['invVat']
            invDisc=record['invDisc']            
            invSpDisc=record['invSpDisc']
            imvAmt=record['invTp']+record['invVat']-(record['invDisc']+record['invSpDisc'])
                        
            retTp=record['retTp'] 
            retVat=record['retVat']
            retDisc=record['retDisc']            
            retSpDisc=record['retSpDisc']
            retAmt=record['retTp']+record['retVat']-(record['retDisc']+record['retSpDisc'])
            
            netTp=imvAmt-retAmt
            
            totalInvAmt+=imvAmt
            totalInvTp+=invTp
            totalRetAmt+=retAmt
            totalRetTp+=retTp  
            totalNetTp+=netTp                                        
            
            myString+=str(level1_id)+','+str(level2_id)+','+str(level3_id)+','+str(invCount)+','+str(round(imvAmt,2))+','+str(round(invTp,2))+','+str(round(invVat,2))+','+str(round(invDisc,2))+','+str(round(invSpDisc,2))+','+str(round(retAmt,2))+','+str(round(retTp,2))+','+str(round(retVat,2))+','+str(round(retDisc,2))+','+str(round(retSpDisc,2))+','+str(round(netTp,2))+'\n'
                               
        myString+=',,,,'+str(totalInvAmt)+','+str(totalInvTp)+',,,,'+str(totalRetAmt)+','+str(totalRetTp)+',,,,'+str(round(totalNetTp,2))+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=catDpWiseSalesPeriodic.csv'   
        return str(myString)


def causeofRetPeriodic():
    c_id=session.cid
    response.title='18 Cause of Return Analysis Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
        
    
    
    invHSql=" (select cid,d_man_id,d_man_name,invoice_date as invDate, '' as retDate,sl as invSL,actual_total_tp as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" )"
    retHSql1=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,ret_actual_total_tp as nd_delivery_tp,1 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NEX DAY DELIVERY' "+condition+" )"
    retHSql2=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,ret_actual_total_tp as cancel_cash_shot_tp,1 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='CANCELED / CASH SHORT' "+condition+" )"
    retHSql3=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,ret_actual_total_tp as shop_close_tp,1 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='SHOP CLOSED' "+condition+" )"
    retHSql4=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,ret_actual_total_tp as product_short_tp,1 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='PRODUCT SHORT' "+condition+" )"
    retHSql5=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,ret_actual_total_tp as not_delivered_tp,1 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT DELIVERED' "+condition+" )"
    retHSql6=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,ret_actual_total_tp as not_ordered_tp,1 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT ORDERED' "+condition+" )"
    retHSql7=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,ret_actual_total_tp as computer_mistake_tp,1 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='COMPUTER MISTAKE' "+condition+" )"
    retHSql8=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,ret_actual_total_tp as part_sale_tp,1 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='PART SALE' "+condition+" )"
    retHSql9=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,ret_actual_total_tp as not_mention_tp,1 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT MENTIONED' "+condition+" )"
    retHSql10=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,ret_actual_total_tp as mso_mistake_tp,1 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and (ret_reason='APPROVED RETURN' or ret_reason='MSO MISTAKE') "+condition+" )" #MSO Mistake
    records="select cid,d_man_id,d_man_name,invDate,retDate,count(distinct(invSL)) as invSL,sum(invTp) as invTp,sum(nd_delivery_tp) as nd_delivery_tp,sum(nd_delivery) as nd_delivery,sum(cancel_cash_shot_tp) as cancel_cash_shot_tp,sum(cancel_cash_shot) as cancel_cash_shot,sum(shop_close_tp) as shop_close_tp,sum(shop_close) as shop_close,sum(product_short_tp) as product_short_tp,sum(product_short) as product_short,sum(not_delivered_tp) as not_delivered_tp,sum(not_delivered) as not_delivered,sum(not_ordered_tp) as not_ordered_tp,sum(not_ordered) as not_ordered,sum(computer_mistake_tp) as computer_mistake_tp,sum(computer_mistake) as computer_mistake,sum(part_sale_tp) as part_sale_tp,sum(part_sale) as part_sale,sum(not_mention_tp) as not_mention_tp,sum(not_mention) as not_mention,sum(mso_mistake_tp) as mso_mistake_tp,sum(mso_mistake) as mso_mistake from ("+invHSql+"union all"+retHSql1+"union all"+retHSql2+"union all"+retHSql3+"union all"+retHSql4+"union all"+retHSql5+"union all"+retHSql6+"union all"+retHSql7+"union all"+retHSql8+"union all"+retHSql9+"union all"+retHSql10+") p group by d_man_id,invDate;"
    records=db.executesql(records,as_dict = True) 
    

    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)


def causeofRetDPeriodic():
    c_id=session.cid
    response.title='18 Cause of Return Analysis Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
        
    
    
    invHSql=" (select cid,d_man_id,d_man_name,invoice_date as invDate, '' as retDate,sl as invSL,actual_total_tp as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" )"
    retHSql1=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,ret_actual_total_tp as nd_delivery_tp,1 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NEX DAY DELIVERY' "+condition+" )"
    retHSql2=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,ret_actual_total_tp as cancel_cash_shot_tp,1 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='CANCELED / CASH SHORT' "+condition+" )"
    retHSql3=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,ret_actual_total_tp as shop_close_tp,1 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='SHOP CLOSED' "+condition+" )"
    retHSql4=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,ret_actual_total_tp as product_short_tp,1 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='PRODUCT SHORT' "+condition+" )"
    retHSql5=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,ret_actual_total_tp as not_delivered_tp,1 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT DELIVERED' "+condition+" )"
    retHSql6=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,ret_actual_total_tp as not_ordered_tp,1 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT ORDERED' "+condition+" )"
    retHSql7=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,ret_actual_total_tp as computer_mistake_tp,1 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='COMPUTER MISTAKE' "+condition+" )"
    retHSql8=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,ret_actual_total_tp as part_sale_tp,1 as part_sale,0 as not_mention_tp,0 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='PART SALE' "+condition+" )"
    retHSql9=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,ret_actual_total_tp as not_mention_tp,1 as not_mention,0 as mso_mistake_tp,0 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and ret_reason='NOT MENTIONED' "+condition+" )"
    retHSql10=" (select cid,d_man_id,d_man_name,invoice_date as invDate,return_date as retDate,invoice_sl as invSL,0 as invTp,0 as nd_delivery_tp,0 as nd_delivery,0 as cancel_cash_shot_tp,0 as cancel_cash_shot,0 as shop_close_tp,0 as shop_close,0 as product_short_tp,0 as product_short,0 as not_delivered_tp,0 as not_delivered,0 as not_ordered_tp,0 as not_ordered,0 as computer_mistake_tp,0 as computer_mistake,0 as part_sale_tp,0 as part_sale,0 as not_mention_tp,0 as not_mention,ret_actual_total_tp as mso_mistake_tp,1 as mso_mistake from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' and (ret_reason='APPROVED RETURN' or ret_reason='MSO MISTAKE') "+condition+" )" #MSO Mistake
    records="select cid,d_man_id,d_man_name,invDate,retDate,count(distinct(invSL)) as invSL,sum(invTp) as invTp,sum(nd_delivery_tp) as nd_delivery_tp,sum(nd_delivery) as nd_delivery,sum(cancel_cash_shot_tp) as cancel_cash_shot_tp,sum(cancel_cash_shot) as cancel_cash_shot,sum(shop_close_tp) as shop_close_tp,sum(shop_close) as shop_close,sum(product_short_tp) as product_short_tp,sum(product_short) as product_short,sum(not_delivered_tp) as not_delivered_tp,sum(not_delivered) as not_delivered,sum(not_ordered_tp) as not_ordered_tp,sum(not_ordered) as not_ordered,sum(computer_mistake_tp) as computer_mistake_tp,sum(computer_mistake) as computer_mistake,sum(part_sale_tp) as part_sale_tp,sum(part_sale) as part_sale,sum(not_mention_tp) as not_mention_tp,sum(not_mention) as not_mention,sum(mso_mistake_tp) as mso_mistake_tp,sum(mso_mistake) as mso_mistake from ("+invHSql+"union all"+retHSql1+"union all"+retHSql2+"union all"+retHSql3+"union all"+retHSql4+"union all"+retHSql5+"union all"+retHSql6+"union all"+retHSql7+"union all"+retHSql8+"union all"+retHSql9+"union all"+retHSql10+") p group by d_man_id,invDate;"
    records=db.executesql(records,as_dict = True)      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='18 \n\n'
        myString=myString+'Cause of Return Analysis Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        
        
                                
        myString+='InvoiceDate,Doc/Tp,Invoice,Return net,Return gross,NextDay Delivery,Cancelled and CashShort,Shop Closed,Product Short,Not Delivered,Not Ordered,Computer Mistake,Part Sale,Not Mentioned,MSO Mistake\n'
        
        
        dp_past=''    
        retInv=0
        retGrossInv=0
        retTp=0
        retGrossTp=0
        
        invT=0
        retT=0
        retGrossT=0
        invTpT=0
        retTpT=0
        retGrossTpT=0
        retGrossTp=0
        
        nd_delivery_t=0
        cancel_cash_shot_t=0
        shop_close_t=0
        product_short_t=0
        not_delivered_t=0
        not_ordered_t=0
        computer_mistake_t=0
        part_sale_t=0
        not_mention_t=0
        mso_mistake_t=0
        
        nd_delivery_tp_t=0
        cancel_cash_shot_tp_t=0
        shop_close_tp_t=0
        product_short_tp_t=0
        not_delivered_tp_t=0
        not_ordered_tp_t=0
        computer_mistake_tp_t=0
        part_sale_tp_t=0
        not_mention_tp_t=0
        mso_mistake_tp_t=0   
        
        for i in range(len(records)):
            record=records[i]
            
            retGrossInv=record['nd_delivery']+record['cancel_cash_shot']+record['shop_close']+record['product_short']+record['not_delivered']+record['not_ordered']+record['computer_mistake']+record['part_sale']+record['not_mention']+record['mso_mistake']
            retInv=record['nd_delivery']+record['cancel_cash_shot']+record['shop_close']+record['product_short']+record['not_delivered']+record['not_ordered']+record['computer_mistake']+record['part_sale']+record['not_mention']
            
            retGrossTp=record['nd_delivery_tp']+record['cancel_cash_shot_tp']+record['shop_close_tp']+record['product_short_tp']+record['not_delivered_tp']+record['not_ordered_tp']+record['computer_mistake_tp']+record['part_sale_tp']+record['not_mention_tp']+record['mso_mistake_tp']
            retTp=record['nd_delivery_tp']+record['cancel_cash_shot_tp']+record['shop_close_tp']+record['product_short_tp']+record['not_delivered_tp']+record['not_ordered_tp']+record['computer_mistake_tp']+record['part_sale_tp']+record['not_mention_tp']
            
            invT+=record['invSL']
            retGrossT+=retGrossInv
            retT+=retInv
            invTpT+=record['invTp']
            retTpT+=retTp
            retGrossTpT+=retGrossTp
            
            nd_delivery_t+=record['nd_delivery']
            cancel_cash_shot_t+=record['cancel_cash_shot']
            shop_close_t+=record['shop_close']
            product_short_t+=record['product_short']
            not_delivered_t+=record['not_delivered']
            not_ordered_t+=record['not_ordered']
            computer_mistake_t+=record['computer_mistake']
            part_sale_t+=record['part_sale']
            not_mention_t+=record['not_mention']
            mso_mistake_t+=record['mso_mistake']
            
            nd_delivery_tp_t+=record['nd_delivery_tp']
            cancel_cash_shot_tp_t+=record['cancel_cash_shot_tp']
            shop_close_tp_t+=record['shop_close_tp']
            product_short_tp_t+=record['product_short_tp']
            not_delivered_tp_t+=record['not_delivered_tp']
            not_ordered_tp_t+=record['not_ordered_tp']
            computer_mistake_tp_t+=record['computer_mistake_tp']
            part_sale_tp_t+=record['part_sale_tp']
            not_mention_tp_t+=record['not_mention_tp']
            mso_mistake_tp_t+=record['mso_mistake_tp']
            
            if (dp_past != record['d_man_id'] ):
                myString+='Delivery Person:'+str(record['d_man_id'])+' '+str(record['d_man_name'])+'\n'
            
            myString+=str(record['invDate'])+','+'Document,'+str(record['invSL'])+','+str(retInv)+','+str(retGrossInv)+','+str(record['nd_delivery'])+','+str(record['cancel_cash_shot'])+','+str(record['shop_close'])+','+str(record['product_short'])+','+str(record['not_delivered'])+','+str(record['not_ordered'])+','+str(record['computer_mistake'])+','+str(record['part_sale'])+','+str(record['not_mention'])+','+str(record['mso_mistake'])+'\n'
            myString+=','+'Tp,'+str(record['invTp'])+','+str(retTp)+','+str(retGrossTp)+','+str(record['nd_delivery_tp'])+','+str(record['cancel_cash_shot_tp'])+','+str(record['shop_close_tp'])+','+str(record['product_short_tp'])+','+str(record['not_delivered_tp'])+','+str(record['not_ordered_tp'])+','+str(record['computer_mistake_tp'])+','+str(record['part_sale_tp'])+','+str(record['not_mention_tp'])+','+str(record['mso_mistake_tp'])+'\n'
            
            
            dp_past=record['d_man_id']
            
        #summary
        myString+='\n\n'
        myString+='Summary'+','+'Document,'+str(invT)+','+str(retT)+','+str(retGrossT)+','+str(nd_delivery_t)+','+str(cancel_cash_shot_t)+','+str(shop_close_t)+','+str(product_short_t)+','+str(not_delivered_t)+','+str(not_ordered_t)+','+str(computer_mistake_t)+','+str(part_sale_t)+','+str(not_mention_t)+','+str(mso_mistake_t)+'\n'
        myString+=','+'Tp,'+str(invTpT)+','+str(retTpT)+','+str(retGrossTpT)+','+str(nd_delivery_tp_t)+','+str(cancel_cash_shot_tp_t)+','+str(shop_close_tp_t)+','+str(product_short_tp_t)+','+str(not_delivered_tp_t)+','+str(not_ordered_tp_t)+','+str(computer_mistake_tp_t)+','+str(part_sale_tp_t)+','+str(not_mention_tp_t)+','+str(mso_mistake_tp_t)+'\n'
        
        
        #net 
        
        retTpP=0
        retGrossTpP=0
        Tret_amn_nddP=0
        Tret_amn_cacShopP=0
        Tret_amn_sclosedP=0
        Tret_amn_pShortP=0
        Tret_amn_ndP=0
        Tret_amn_noP=0
        Tret_amn_cmP=0
        Tret_amn_psaleP=0
        Tret_amn_nmP=0
        Tret_amn_nmP=0
        Tret_amn_msomP=0
       
        if invTpT > 0:
            retTpP=round((retTpT/invTpT)*100,2)
            retGrossTpP=round((retGrossTpT/invTpT)*100,2)
            Tret_amn_nddP=round((nd_delivery_tp_t/invTpT)*100,2)
            Tret_amn_cacShopP=round((cancel_cash_shot_tp_t/invTpT)*100,2)
            Tret_amn_sclosedP=round((shop_close_tp_t/invTpT)*100,2)
            Tret_amn_pShortP=round((product_short_tp_t/invTpT)*100,2)
            Tret_amn_ndP=round((not_delivered_tp_t/invTpT)*100,2)
            Tret_amn_noP=round((not_ordered_tp_t/invTpT)*100,2)
            Tret_amn_cmP=round((computer_mistake_tp_t/invTpT)*100,2)
            Tret_amn_psaleP=round((part_sale_tp_t/invTpT)*100,2)
            Tret_amn_nmP=round((not_mention_tp_t/invTpT)*100,2)
            Tret_amn_msomP=round((mso_mistake_tp_t/invTpT)*100,2)
        
        
        myString+=','+'Return%,,'+str(retTpP)+','+str(retGrossTpP)+','+str(Tret_amn_nddP)+','+str(Tret_amn_cacShopP)+','+str(Tret_amn_sclosedP)+','+str(Tret_amn_pShortP)+','+str(Tret_amn_ndP)+','+str(Tret_amn_noP)+','+str(Tret_amn_cmP)+','+str(Tret_amn_psaleP)+','+str(Tret_amn_nmP)+','+str(Tret_amn_msomP)+'\n'
            
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=CauseOfReturnAnalysisPeriodic.csv'   
        return str(myString) 


def discPWisePeriodic():
    c_id=session.cid 
    response.title='22 Discount and Bonus Statement- Product wise Periodic'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    
    
    itemSql="Select cid,item_id,name as item_name,price as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_item where cid='"+c_id+"'"
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+" AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+" AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+" AND level2_id= '"+str(fm_id)+"'"
    
    
    invSql=" (select cid, `item_id`,`item_name`,0 as recentPrice,sl as invSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,actual_vat as invVat,discount as invItemDisc,sp_discount_item as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced'  "+condition+") "
    retSql=" (select cid, `item_id`,`item_name`,0 as recentPrice,invoice_sl as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,actual_vat as retVat,discount as retItemDisc,(actual_tp-price)*quantity as retItemSpDisc from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned'  "+condition+") "
    records="select cid,item_id,item_name,sum(recentPrice) as recentPrice,count(distinct(invSL)) as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invVat) as invVat,sum(invItemDisc) as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retVat) as retVat,sum(retItemDisc) as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+itemSql+" union all "+invSql+" union all "+retSql+") p group by item_id;"
    records=db.executesql(records,as_dict = True)
    
    records_sum="select cid,sum(invSL) as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invQty*invVat) as invVat,sum(invItemDisc) as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retQty*retVat) as retVat,sum(retItemDisc) as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+itemSql+" union all "+invSql+" union all "+retSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
    
    # summary regular discount
    invRdSql=" (select cid,sl as invSL,discount as invDisc,0 as retDisc,status from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retRdSql=" (select cid,invoice_sl as invSL,0 as invDisc,discount as retDisc,status from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records_sum_rd="select  invSL,sum(invDisc) as invDisc,sum(retDisc) as retDisc,status from ("+invRdSql+" union all "+retRdSql+") p group by cid;"
    records_sum_rd=db.executesql(records_sum_rd,as_dict = True)
    

    return dict(records=records,records_sum=records_sum,records_sum_rd=records_sum_rd,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  teritory_id=teritory_id, teritory_name=teritory_name, dman_id=dman_id,dman_name=dman_name, mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)


def discPWiseDPeriodic():
    c_id=session.cid 
    response.title='22 Discount and Bonus Statement- Product wise Periodic'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    item_id=str(request.vars.item_id).strip()
    item_name=str(request.vars.item_name).strip()
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    
    
    itemSql="Select cid,item_id,name as item_name,price as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_item where cid='"+c_id+"'"
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"
    if (item_id!=''):
        condition=condition+" AND item_id= '"+str(item_id)+"'"
    if (rsm_id!=''):
        condition=condition+" AND level1_id= '"+str(rsm_id)+"'"
    if (fm_id!=''):
        condition=condition+" AND level2_id= '"+str(fm_id)+"'"
    
    
    invSql=" (select cid, `item_id`,`item_name`,0 as recentPrice,sl as invSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,actual_vat as invVat,discount as invItemDisc,sp_discount_item as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced'  "+condition+") "
    retSql=" (select cid, `item_id`,`item_name`,0 as recentPrice,invoice_sl as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,actual_vat as retVat,discount as retItemDisc,(actual_tp-price)*quantity as retItemSpDisc from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned'  "+condition+") "
    records="select cid,item_id,item_name,sum(recentPrice) as recentPrice,count(distinct(invSL)) as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invVat) as invVat,sum(invItemDisc) as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retVat) as retVat,sum(retItemDisc) as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+itemSql+" union all "+invSql+" union all "+retSql+") p group by item_id;"
    records=db.executesql(records,as_dict = True)
    
    records_sum="select cid,sum(invSL) as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invQty*invVat) as invVat,sum(invItemDisc) as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retQty*retVat) as retVat,sum(retItemDisc) as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+itemSql+" union all "+invSql+" union all "+retSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
    
    # summary regular discount
    invRdSql=" (select cid,sl as invSL,discount as invDisc,0 as retDisc,status from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retRdSql=" (select cid,invoice_sl as invSL,0 as invDisc,discount as retDisc,status from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records_sum_rd="select  invSL,sum(invDisc) as invDisc,sum(retDisc) as retDisc,status from ("+invRdSql+" union all "+retRdSql+") p group by cid;"
    records_sum_rd=db.executesql(records_sum_rd,as_dict = True)
      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='22\n\n'
        myString=myString+'Discount and Bonus Statement- Product wise Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        
        
        myString+='Item,ItemName,RcentPrice,SoldQty,BonusQty,TradePrice,TotalDisc,RegularDisc,SpecialDisc,Discount%,InvCount\n'
        
        
        discPer=0       
        for k in range(len(records)):
            record=records[k]  
            
            item_id=record['item_id']
            item_name=record['item_name']
            recentPrice=record['recentPrice']
            soldQty=record['invQty']-record['retQty']
            bonusQty=record['invBQty']-record['retBQty']
            price=record['invTp']-record['retTp']
            disc=0
            itemDisc=0
            itemSpDisc=record['invItemSpDisc']-record['retItemSpDisc']
            
            if price>0:
                discPer=round((disc*100/price),2)
            
            invCount=record['invSL']
            
                        
            
            myString+=str(item_id)+','+str(item_name)+','+str(recentPrice)+','+str(soldQty)+','+str(bonusQty)+','+str(price)+','+\
            str(disc)+','+str(itemDisc)+','+str(round(itemSpDisc,2))+','+str(round(discPer,2))+','+str(invCount)+'\n'
       
        
        #summary
        
        rDisc=0
        for j in range(len(records_sum_rd)):
            record_sum_rd=records_sum_rd[j]
            rDisc=record_sum_rd['invDisc']-record_sum_rd['retDisc']
        
        discPer=0
        for i in range(len(records_sum)):
            record_sum=records_sum[i]
            tpSum=record_sum['invTp']-record_sum['retTp']
            discSum=rDisc+(record_sum['invItemSpDisc']-record_sum['retItemSpDisc'])
            spDiscSum=record_sum['invItemSpDisc']-record_sum['retItemSpDisc']
            
            if tpSum>0:
                discPer=round((rDisc*100/tpSum),2)
        
        
            myString+=',,,,,'+str(tpSum)+','+str(discSum)+','+str(rDisc)+','+str(spDiscSum)+','+str(discPer)+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=discAndBonusStatementPeriodic.csv'   
        return str(myString)



def itemWiseSalesSDetailPeriodic():
    c_id=session.cid
    response.title='12.2 Item Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
 
    
    invSql=" (select cid, `item_id`,`item_name`,sl as invSL,0 as retInvSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,item_vat as invVat,0 as invItemDisc,sp_discount_item as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retSql=" (select cid, `item_id`,`item_name`,invoice_sl as invSL,1 as retInvSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,item_vat as retVat,0 as retItemDisc,(actual_tp-price)*quantity as retItemSpDisc from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records="select cid,item_id,item_name,count(distinct(invSL)) as invSL,sum(retInvSL) as retInvSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invVat) as invVat,0 as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retVat) as retVat,0 as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+invSql+" union all "+retSql+") p group by item_id;"
    records=db.executesql(records,as_dict = True)
            
    records_sum="select count(distinct(invSL)) as invSL,sum(retInvSL) as retInvSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invQty*invVat) as invVat,0 as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retQty*retVat) as retVat,0 as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+invSql+" union all "+retSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
    # summary regular discount
    invRdSql=" (select cid,sl as invSL,discount as invDisc,0 as retDisc,status from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retRdSql=" (select cid,invoice_sl as invSL,0 as invDisc,discount as retDisc,status from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records_sum_rd="select  invSL,sum(invDisc) as invDisc,sum(retDisc) as retDisc,status from ("+invRdSql+" union all "+retRdSql+") p group by cid;"
    records_sum_rd=db.executesql(records_sum_rd,as_dict = True)
    
     
    return dict(records=records,records_sum=records_sum,records_sum_rd=records_sum_rd,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)
    

def itemWiseSalesSDetailDLoadPeriodic():
    c_id=session.cid
    response.title='12.2 Item Wise Sales Statement Detail Periodic'
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    
    condition=''
    if (depot_id!=''):
        condition=condition+" and depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" and store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" and client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" and rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" and market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" and area_id= '"+str(teritory_id)+"'"
    
    
    invSql=" (select cid, `item_id`,`item_name`,sl as invSL,0 as retInvSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,item_vat as invVat,0 as invItemDisc,sp_discount_item as invItemSpDisc,0 as retQty,0 as retBQty,0 as retTp,0 as retVat,0 as retItemDisc,0 as retItemSpDisc from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retSql=" (select cid, `item_id`,`item_name`,invoice_sl as invSL,1 as retInvSL,0 as invQty,0 as invBQty,0 as invTp,0 as invVat,0 as invItemDisc,0 as invItemSpDisc,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,item_vat as retVat,0 as retItemDisc,(actual_tp-price)*quantity as retItemSpDisc from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records="select cid,item_id,item_name,count(distinct(invSL)) as invSL,sum(retInvSL) as retInvSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invVat) as invVat,0 as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retVat) as retVat,0 as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+invSql+" union all "+retSql+") p group by item_id;"
    records=db.executesql(records,as_dict = True)
            
    records_sum="select count(distinct(invSL)) as invSL,sum(retInvSL) as retInvSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(invQty*invVat) as invVat,0 as invItemDisc,sum(invItemSpDisc) as invItemSpDisc,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(retQty*retVat) as retVat,0 as retItemDisc,sum(retItemSpDisc) as retItemSpDisc from ("+invSql+" union all "+retSql+") p group by cid;"
    records_sum=db.executesql(records_sum,as_dict = True)
    
    # summary regular discount
    invRdSql=" (select cid,sl as invSL,discount as invDisc,0 as retDisc,status from sm_invoice_head where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+") "
    retRdSql=" (select cid,invoice_sl as invSL,0 as invDisc,discount as retDisc,status from sm_return_head where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+") "
    records_sum_rd="select  invSL,sum(invDisc) as invDisc,sum(retDisc) as retDisc,status from ("+invRdSql+" union all "+retRdSql+") p group by cid;"
    records_sum_rd=db.executesql(records_sum_rd,as_dict = True)
    
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='12.2\n\n'
        myString=myString+'Item Wise Sales Statement Detail Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        myString+='Summary\n'
        
        
        myString+='Inv S.Qty,Inv B.Qty,Inv TP,Ret Qty,Ret B.Qty,Ret TP,RTN%,Net S.Qty,Net B.Qty,Net TP,SP.Disc,Reg.Disc,Vat,Net,NS%\n'
        
        rDisc=0
        for k in range(len(records_sum_rd)):
            record_sum_rd=records_sum_rd[k]
            rDisc=(record_sum_rd['invDisc']-record_sum_rd['retDisc'])
                  
               
        for j in range(len(records_sum)):
            record_sum=records_sum[j]
                             
            invQty=record_sum['invQty']            
            invBQty=record_sum['invBQty']
            invTp=float(record_sum['invTp'])
            
            retQty=record_sum['retQty']            
            retBQty=record_sum['retBQty']
            retTp=float(record_sum['retTp'])  
            
            rtnPer=retTp*100/invTp
            
            netSQty=invQty-retQty
            netSBQty=invBQty-retBQty
            netTp=invTp-retTp
            spDisc=record_sum['invItemSpDisc']-record_sum['retItemSpDisc']
            vat=record_sum['invVat']-record_sum['retVat']
            net=(netTp+vat)-(rDisc+spDisc)
            nsPer=netTp*100/invTp
            
                               
            myString+=str(round(invQty,2))+','+str(round(invBQty,2))+','+str(round(invTp,2))+','+str(round(retQty,2))+','+str(round(retBQty,2))+','+str(round(retTp,2))+','+str(round(rtnPer,2))+','+str(round(netSQty,2))+','+str(round(netSBQty,2))+','+str(round(netTp,2))+','+str(round(spDisc,2))+','+str(round(rDisc,2))+','+str(round(vat,2))+','+str(round(net,2))+','+str(round(nsPer,2))+'\n\n'
       
       
        
        myString+='Item,ItemName,Inv Count,Ret Count,Inv S.Qty,Inv B.Qty,Inv TP,Ret S.Qty,Ret B.Qty,Ret TP,RTN%,Net S.Qty,Net B.Qty,Net TP,Disc,Vat,Net,NS %\n'
       
        for k in range(len(records)):
            record=records[k]  
            
            item_idD=record['item_id']
            item_nameD=record['item_name']
            invSLD=record['invSL']
            retInvSLD=record['retInvSL']
            
            invQtyD=record['invQty']
            invBQtyD=record['invBQty']
            invTpD=float(record['invTp'])
            
            retQtyD=record['retQty']
            retBQtyD=record['retBQty']
            retTpD=float(record['retTp'])
            
            if invTpD>0:
                rtnPerD=retTpD*100/invTpD
            
            netSQtyD=invQtyD-retQtyD
            netSBQtyD=invBQtyD-retBQtyD
            netTpD=invTpD-retTpD
            spDiscD=record['invItemSpDisc']-record['retItemSpDisc']
            vatD=record['invVat']-record['retVat']
            netD=(netTpD+vatD)-(spDiscD)
            
            if invTpD>0:
                nsPerD=netTpD*100/invTpD
            
                                    
            
            myString+=str(item_idD)+','+str(item_nameD)+','+str(invSLD)+','+str(retInvSLD)+','+str(invQtyD)+','+str(invBQtyD)+','+\
            str(round(invTpD,2))+','+str(round(retQtyD,2))+','+str(round(retBQtyD,2))+','+str(retTpD)+','+str(round(rtnPerD,2))+','+\
            str(round(netSQtyD,2))+','+str(round(netSBQtyD,2))+','+str(round(netTpD,2))+','+str(round(spDiscD,2))+','+str(round(vatD,2))+','+str(round(netD,2))+','+str(round(nsPerD,2))+'\n'
       
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=itemWiseSalesStatementDetailPeriodic.csv'   
        return str(myString)




def salesClosingStockSBPeriodic():
    c_id=session.cid 
    response.title='B Sales Closing StockS Periodic'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    
    
    itemSql="Select cid,item_id,name as item_name,price as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as retQty,0 as retBQty,0 as retTp,0 as stockQty from sm_item where cid='"+c_id+"'"
        
    
    condition=''
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"    
    
    
    itemStockSql="Select cid,item_id,'' as item_name,0 as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as retQty,0 as retBQty,0 as retTp,quantity as stockQty from sm_depot_stock_balance where cid='"+c_id+"' and depot_id='"+depot_id+"' and store_id='"+store_id+"'"
    invSql=" (select cid, `item_id`,`item_name` as item_name,0 as recentPrice,sl as invSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,0 as retQty,0 as retBQty,0 as retTp,0 as stockQty from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" ) "
    retSql=" (select cid, `item_id`,`item_name` as item_name,0 as recentPrice,sl as invSL,0 as invQty,0 as invBQty,0 as invTp,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,0 as stockQty from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned'  "+condition+") "
    records="select cid, `item_id`,max(item_name) as item_name,sum(recentPrice) as recentPrice,invSL as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(stockQty) as stockQty  from ("+itemSql+" union all "+itemStockSql+" union all "+invSql+" union all "+retSql+") p group by item_id order by item_id;"

    records=db.executesql(records,as_dict = True)
    
    records_sum="select sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(stockQty) as stockQty  from ("+itemSql+" union all "+itemStockSql+" union all "+invSql+" union all "+retSql+") p group by cid;"
    
    records_sum=db.executesql(records_sum,as_dict = True)

    return dict(records=records,records_sum=records_sum,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name)
 

def salesClosingStockSBDPeriodic():
    c_id=session.cid 
    response.title='B Sales Closing StockS Periodic'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    dman_id=str(request.vars.dman_id).strip()
    dman_name=str(request.vars.dman_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()
    
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)  

    
    
    itemSql="Select cid,item_id,name as item_name,price as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as retQty,0 as retBQty,0 as retTp,0 as stockQty from sm_item where cid='"+c_id+"'"
        
    
    condition=''
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"    
    
    
    itemStockSql="Select cid,item_id,'' as item_name,0 as recentPrice,0 as invSL,0 as invQty,0 as invBQty,0 as invTp,0 as retQty,0 as retBQty,0 as retTp,quantity as stockQty from sm_depot_stock_balance where cid='"+c_id+"' and depot_id='"+depot_id+"' and store_id='"+store_id+"'"
    invSql=" (select cid, `item_id`,`item_name` as item_name,0 as recentPrice,sl as invSL,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,0 as retQty,0 as retBQty,0 as retTp,0 as stockQty from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" ) "
    retSql=" (select cid, `item_id`,`item_name` as item_name,0 as recentPrice,sl as invSL,0 as invQty,0 as invBQty,0 as invTp,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp,0 as stockQty from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned'  "+condition+") "
    records="select cid, `item_id`,max(item_name) as item_name,sum(recentPrice) as recentPrice,invSL as invSL,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(stockQty) as stockQty  from ("+itemSql+" union all "+itemStockSql+" union all "+invSql+" union all "+retSql+") p group by item_id order by item_id;"
    records=db.executesql(records,as_dict = True)
    
    records_sum="select sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invQty*invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retQty*retTp) as retTp,sum(stockQty) as stockQty  from ("+itemSql+" union all "+itemStockSql+" union all "+invSql+" union all "+retSql+") p group by cid;"
    
    records_sum=db.executesql(records_sum,as_dict = True)      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='B\n\n'
        myString=myString+'B Sales Closing StockS Periodic\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
                                
        myString+='Item,ItemName,S.TP,S.Qty after Return,TP*S.Qty,S.B Qty after Return,Closing stock Qty,Stock TP,TP*Closing stock Qty\n'
        
        
        
        totalStockTp=0             
          
        for k in range(len(records)):
            record=records[k]
              
            totalStockTp+=float(record['stockQty'])*record['recentPrice']
            
            if record['invQty']>0:
                item_id=record['item_id']
                item_name=record['item_name']
                recentPrice=record['recentPrice']
                sQtyAfterRet=record['invQty']-record['retQty']
                tpSqty=record['invTp']-record['retTp']
                sBQtyAfterRet=record['invBQty']-record['retBQty']         
                            
                stockQty=record['stockQty']
                closingStQty=float(record['stockQty'])*record['recentPrice']        
                                               
            
                myString+=str(item_id)+','+str(item_name)+','+str(recentPrice)+','+str(sQtyAfterRet)+','+str(tpSqty)+','+str(sBQtyAfterRet)+','+str(stockQty)+','+str(recentPrice)+','+str(closingStQty)+'\n'
        
        myString+='*Stock available but not sold within the period\n'
        
        for j in range(len(records)):
            record=records[j]  
            
            if record['invQty']==0:
                item_id=record['item_id']
                item_name=record['item_name']
                recentPrice=record['recentPrice']
                sQtyAfterRet=record['invQty']-record['retQty']
                tpSqty=record['invTp']-record['retTp']
                sBQtyAfterRet=record['invBQty']-record['retBQty']         
                            
                stockQty=record['stockQty']
                closingStQty=float(record['stockQty'])*record['recentPrice']        
                                               
            
                myString+=str(item_id)+','+str(item_name)+','+str(recentPrice)+','+str(sQtyAfterRet)+','+str(tpSqty)+','+str(sBQtyAfterRet)+','+str(stockQty)+','+str(recentPrice)+','+str(closingStQty)+'\n'
                               
        
        totalTp=0
        for i in range(len(records_sum)):
            record_sum=records_sum[i]
            totalTp=record_sum['invTp']-record_sum['retTp']
                               
        myString+=',,,,'+str(totalTp)+',,,,'+str(totalStockTp)+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=bSalesClosingStockPeriodic.csv'   
        return str(myString)

def customrInvoiceProductwiseSPeriodic():
    c_id=session.cid   
    response.title='10.6,11.3 Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
       
    
    condition=''
    
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
                
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"        
   
    if (rsm_id!=''):
        condition=condition+" AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+" AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+" AND item_id= '"+str(item_id)+"'"

    
    invSql=" (select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,0 as retQty,0 as retBQty,0 as retTp from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" ) "
    retSql=" (select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,0 as invQty,0 as invBQty,0 as invTp,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+" ) "
    records="select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retTp) as retTp  from ("+invSql+" union all "+retSql+") p group by client_id,depot_id,invoice_date,item_id order by client_id,depot_id,invoice_date,item_id;"
        
    records=db.executesql(records,as_dict = True)
        
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,store_id=store_id,store_name=store_name,customer_id=customer_id, customer_name=customer_name,  mso_id=mso_id, mso_name=mso_name,market_id=market_id,market_name=market_name,teritory_id=teritory_id,teritory_name=teritory_name,item_id=item_id,item_name=item_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name)


def customrInvoiceProductwiseSDPeriodic():
    c_id=session.cid   
    response.title='10.6,11.3 Customer-Invoice-Product Wise Sales Statement'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    store_id=str(request.vars.store_id).strip()
    store_name=str(request.vars.store_name).strip()
    customer_id=str(request.vars.customer_id).strip()
    customer_name=str(request.vars.customer_name).strip()
    
    teritory_id=str(request.vars.teritory_id).strip()
    teritory_name=str(request.vars.teritory_name).strip()
  
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    
    market_id=str(request.vars.market_id).strip()
    market_name=str(request.vars.market_name).strip()

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
    item_id=str(request.vars.item_id)
    item_name=str(request.vars.item_name)
    rsm_id=str(request.vars.rsm_id)
    rsm_name=str(request.vars.rsm_name)
    fm_id=str(request.vars.fm_id)
    fm_name=str(request.vars.fm_name)
    
    
    if teritory_id!='':
        pass
    else:
        if (rsm_id=='' and fm_id=='' and (item_id=='')):
            session.flash="Please select RSM or FM and Item"
            redirect(URL(c='report_sales',f='home'))
        if ((rsm_id!='' or fm_id!='') and (item_id=='')):
            session.flash="Please select Item"
            redirect(URL(c='report_sales',f='home'))
       
    
    condition=''
    
    if (depot_id!=''):
        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
    
    if (store_id!=''):
        condition=condition+" AND store_id = '"+str(store_id)+"'"
                
    if (customer_id!=''):
        condition=condition+" AND client_id = '"+str(customer_id)+"'"
        
    if (mso_id!=''):
        condition=condition+" AND rep_id = '"+str(mso_id)+"'"
        
    if (market_id!=''):
        condition=condition+" AND market_id = '"+str(market_id)+"'"
        
    if (teritory_id!=''):
        condition=condition+" AND area_id= '"+str(teritory_id)+"'"        
   
    if (rsm_id!=''):
        condition=condition+" AND level1_id= '"+str(rsm_id)+"'"
        
    if (fm_id!=''):
        condition=condition+" AND level2_id= '"+str(fm_id)+"'"
        
    if (item_id!=''):
        condition=condition+" AND item_id= '"+str(item_id)+"'"

    
    invSql=" (select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,quantity as invQty,bonus_qty as invBQty,actual_tp as invTp,0 as retQty,0 as retBQty,0 as retTp from sm_invoice where cid='"+c_id+"' and invoice_date>='"+date_from+"' and invoice_date<='"+date_to+"' and status='Invoiced' "+condition+" ) "
    retSql=" (select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,0 as invQty,0 as invBQty,0 as invTp,quantity as retQty,bonus_qty as retBQty,actual_tp as retTp from sm_return where cid='"+c_id+"' and return_date>='"+date_from+"' and return_date<='"+date_to+"' and status='Returned' "+condition+" ) "
    records="select cid,client_id,client_name,depot_id,sl,invoice_date,area_name,`item_id`,`item_name`,item_unit,sum(invQty) as invQty,sum(invBQty) as invBQty,sum(invTp) as invTp,sum(retQty) as retQty,sum(retBQty) as retBQty,sum(retTp) as retTp  from ("+invSql+" union all "+retSql+") p group by client_id,depot_id,invoice_date,item_id order by client_id,depot_id,invoice_date,item_id;"
    
    
    records=db.executesql(records,as_dict = True)      
    
    if not records:
        session.flash="Data Not Available"
        redirect(URL(c='report_sales',f='home'))        
    else:    
        myString='10.6 11.3\n\n'
        myString=myString+'Customer-Invoice-Product Wise Sales Statement\n'
        myString=myString+'Depot/Branch,'+date_from+'|'+date_to+'\n'
        myString=myString+'Depot/Branch,'+depot_id+'|'+depot_name+'\n'
        myString=myString+'Store,'+store_id+'|'+store_name+'\n'
        myString=myString+'Customer,'+customer_id+'|'+customer_name+'\n'
        myString=myString+'Teritory,'+teritory_id+'|'+teritory_name+'\n'
        myString=myString+'MSO,'+mso_id+'|'+mso_name+'\n\n'
        
        
        
                                
        myString+='ItemID,ItemName,UOM,UnitPrice,Ret%,Inv Qnty,Inv Bonus,Inv TradePrice,Ret Qnty,Ret Bonus,Ret TradePrice,Net Qnty,Net Bonus,Net TradePrice\n'
        
        retPer=0
        clientID=''
        invsl='' 
        totalInvTp=0
        totalRetTp=0 
        totalRetPer=0        
        for k in range(len(records)):
            record=records[k]
            
            item_id=record['item_id']
            item_name=record['item_name']
            item_unit=record['item_unit']
            invTp=record['invTp']
            retTp=record['retTp']
            
            if invTp>0:
                retPer=retTp*100/invTp
            else:
                retPer=0
                
            invQty=record['invQty']
            invBQty=record['invBQty']
            invTradePrice=float(record['invQty'])*record['invTp']
            
            retQty=record['retQty']
            retBQty=record['retBQty']
            retTradePrice=float(record['retQty'])*record['retTp']
            
            totalInvTp+=invTradePrice
            totalRetTp+=retTradePrice
            totalRetPer=totalRetTp*100/totalInvTp       
            
            if (clientID != record['client_id'] ):
                myString+=str(record['client_id'])+','+str(record['client_name'])+'\n' 
            
            if ((clientID != record['client_id']) & (invsl != record['sl']) ):
                myString+="INV"+str(record['depot_id'])+'-'+str(record['sl'])+','+str(record['invoice_date'])+','+str(record['area_name'])+'\n'                               
        
            myString+=str(item_id)+','+str(item_name)+','+str(item_unit)+','+str(invTp)+','+str(retPer)+','+str(invQty)+','+str(invBQty)+','+str(invTradePrice)+','+str(retQty)+','+str(retBQty)+','+str(retTradePrice)+','+str(invQty-retQty)+','+str(invBQty-retBQty)+','+str(invTradePrice-retTradePrice)+'\n'
            
            
            clientID=record['client_id']
            invsl=record['sl']
                                       
        myString+='Total,,,,'+str(totalRetPer)+',,,'+str(totalInvTp)+',,,'+str(totalRetTp)+',,,'+str(totalInvTp-totalRetTp)+'\n'
        
           
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=customerInvoiceProductWisePeriodic.csv'   
        return str(myString)    