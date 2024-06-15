import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px
import requests


mydb = mysql.connector.connect(
 host="127.0.0.1",
 user="root",
 password="Leema",
 database="Phonepe",
 port="3306"
 )

print(mydb)
mycursor = mydb.cursor(buffered=True)

#SQL la irrunthu insert panna datava get paniruke:
mycursor.execute("SELECT * FROM aggregated_transaction")

result=mycursor.fetchall()

aggregated1=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "Transaction_type",
                               "Transaction_count",
                               "Transaction_amount"])

#SQL la irrunthu insert panna datava get paniruke:
mycursor.execute("SELECT * FROM aggregated_users")

result=mycursor.fetchall()

aggregated2=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "brands",
                               "Transaction_count",
                               "Percentage"])


mycursor.execute("SELECT * FROM aggre_map_trans")

result=mycursor.fetchall()

map1=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "Districts",
                               "Transaction_count",
                               "Transaction_amount"])


mycursor.execute("SELECT * FROM aggre_map_user")

result=mycursor.fetchall()

map2=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "Districts",
                               "registeredusers",
                               "appopens"])


mycursor.execute("SELECT * FROM top_trans_list")

result=mycursor.fetchall()

top1=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "Pincode",
                               "Transaction_amount",
                               "Transaction_count"])


mycursor.execute("SELECT * FROM top_users_list")

result=mycursor.fetchall()

top2=pd.DataFrame(result, columns=["States",
                               "Years",
                               "Quarter",
                               "Pincode",
                               "RegisteredUsers"])


#AGGREGATEDE TRANSACTION YEAR ANALYSIS:
def Transaction_amount_count_Y(df, year):

    tran_amo_year = df[df["Years"] == year]#Particular year matu yeduka
    tran_amo_year.reset_index(drop=True, inplace=True)#actual index value change panna

    group = tran_amo_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        amount=px.area(group,x="States",y="Transaction_amount",title=f"{year} Transaction Amount",
                   color_discrete_sequence=px.colors.sequential.RdBu_r,height=650,width=800)
        st.plotly_chart(amount)
    with col2:
        count=px.area(group,x="States",y="Transaction_count",title=f"{year} Transaction Count",
                  color_discrete_sequence=px.colors.sequential.RdBu_r,height=650,width=800)
        st.plotly_chart(count)


    col1,col2=st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)

        state_name=[]
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])

        state_name.sort()

        india=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="Reds",
                            range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                            hover_name="States",title=f"{year} Transaction_amount",fitbounds="locations",
                            height=650,width=600)
        
        india.update_geos(visible=False)
        st.plotly_chart(india)

    with col2:
        india_1=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="Reds",
                            range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                            hover_name="States",title=f"{year} Transaction_count",fitbounds="locations",
                            height=650,width=600)
        
        india_1.update_geos(visible=False)
        st.plotly_chart(india_1)

    return tran_amo_year

#AGGREGATED TRANSACTION QUARTER ANALYSIS:
def Transaction_Quarter(df, quarter):
    tran_amo_year=df[df["Quarter"] == quarter]#Particular year matu yeduka
    tran_amo_year.reset_index(drop=True, inplace=True)#actual index value change panna

    group=tran_amo_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
       #CHART 1:
        amount=px.bar(group,x="States",y="Transaction_amount",title=f"{tran_amo_year['Years'].max()} YEAR {quarter} Quarter Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        
        st.plotly_chart(amount)
    with col2:
        #CHART 2:
        count=px.bar(group,x="States",y="Transaction_count",title=f"{tran_amo_year['Years'].max()} YEAR {quarter} Quarter Transaction Count",
                    color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=600)
        
        st.plotly_chart(count)

        #Geo Visulation plot India Map:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)

        state_name=[]
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])

        state_name.sort()
    col1,col2=st.columns(2)

    with col1:
        india=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="Reds",
                            range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                            hover_name="States",title=f"{tran_amo_year['Years'].max()} YEAR {quarter} Quarter Transaction Amount",fitbounds="locations",
                            height=650,width=600)
        
        india.update_geos(visible=False)
        
        st.plotly_chart(india)
    with col2:
        india_1=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="Reds",
                            range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                            hover_name="States",title=f"{tran_amo_year['Years'].max()} YEAR {quarter} Quarter Transaction Count",fitbounds="locations",
                            height=650,width=600)
        
        india_1.update_geos(visible=False)
        
        st.plotly_chart(india_1)

        return tran_amo_year

#AGGREGATED TRANSACION TYPE YEAR ANALAYSIS:
def agg_transaction_type_year(df,year):
    agg_tran_type_year=df[df["Years"]==year]

    group=agg_tran_type_year.groupby("Transaction_type")[["Transaction_amount","Transaction_count"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        pie_chart=px.pie(data_frame= group, names="Transaction_type",values="Transaction_amount",
                        width=600,title="TRANSACTION AMOUNT")

        st.plotly_chart(pie_chart)
    with col2:
        pie_chart_1=px.pie(data_frame= group, names="Transaction_type",values="Transaction_count",
                        width=600,title="TRANSACTION COUNT")

        st.plotly_chart(pie_chart_1)
        
        return agg_tran_type_year

#AGGREGATED TRANSACTION TYPE DISTRIC ANALYSIS:
def agg_tran_transaction_type(df,state):

    tran_amo_year=df[df["States"] == state]#Particular year matu yeduka
    tran_amo_year.reset_index(drop=True, inplace=True)#actual index value change panna

    group=tran_amo_year.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        pie_chart=px.pie(data_frame= group, names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT")

        st.plotly_chart(pie_chart)

    #Transaction_count:
    with col2:
        pie_chart_1=px.pie(data_frame= group, names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT")

        st.plotly_chart(pie_chart_1)

    return tran_amo_year

#AGGREGATED USER YEAR ANALYSIS:
def agge_user_plot(df,year):
    Agge_user_year=df[df['Years']==year]
    Agge_user_year.reset_index(drop=True, inplace=True)#rows ah aline panni order ah show agum

    Agge_user_year_gr=pd.DataFrame(Agge_user_year.groupby("brands")["Transaction_count"].sum())
    Agge_user_year_gr.reset_index(inplace=True)


    agg_us_bar=px.bar(Agge_user_year_gr,x="brands",y="Transaction_count",
                    title=f"{year}Brands and Transaction Count",width=800,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(agg_us_bar)

    return Agge_user_year

#Aggre_User_Quarter analysis:
def agg_user_qu(df,quarter):
    Agge_user_qu=df[df['Quarter']==quarter]
    Agge_user_qu.reset_index(drop=True, inplace=True)#rows ah aline panni order ah show agum

    Agge_user_qu_gro=pd.DataFrame(Agge_user_qu.groupby("brands")["Transaction_count"].sum())
    Agge_user_qu_gro.reset_index(inplace=True)

    agg_us_bar_1=px.bar(Agge_user_qu_gro,x="brands",y="Transaction_count",
                    title=f"{quarter} Quarter Brands and Transaction Count",width=800,color_discrete_sequence=px.colors.sequential.Rainbow)
    
    st.plotly_chart(agg_us_bar_1)
   
    return Agge_user_qu

#Aggregated User State Analysis:
def agg_user_state(df,state):
    agg_use_year_qu_sta=df[df["States"]==state]
    agg_use_year_qu_sta.reset_index(drop=True,inplace=True)


    line_chart=px.bar(agg_use_year_qu_sta,x="brands", y="Transaction_count",title=f"{state} Transaction Count and State",width=800)
    st.plotly_chart(line_chart)


#Map Transction Year Analysis:
def map_transaction_year(df,year):
    map_transaction=df[df["Years"]==year]
    map_transaction.reset_index(drop=True,inplace=True)

    group=map_transaction.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    #Map Transaction Amount:
    col1,col2=st.columns(2)

    with col1:
        map_amount=px.bar(group,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",height=650,width=800)
        st.plotly_chart(map_amount)
        #Map_Transaction Count:
    with col2:
        map_count=px.bar(group,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",height=650,width=800)
        st.plotly_chart(map_count)

        #Geo Visulation plot India Map:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)

        state_name=[]
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])

        state_name.sort()

    col1,col2=st.columns(2)

    with col1:
        india_2=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="Reds",
                            range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                            title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",height=650,width=800)
        india_2.update_geos(visible=False)
        st.plotly_chart(india_2)
    with col2:
        india_3=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="Reds",
                            range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                            title=f"{year}TRANSACTION COUNT",fitbounds="locations",height=650,width=800)
        india_3.update_geos(visible=False)
        st.plotly_chart(india_3)

        return map_transaction


# Map Transaction Quarter:

def map_tran_year_qua(df,quarter):
    map_year=df[df["Quarter"] == quarter]#Particular year matu yeduka
    map_year.reset_index(drop=True, inplace=True)#actual index value change panna

    group=map_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        amount=px.bar(group,x="States",y="Transaction_amount",title=f"{map_year ['Years'].max()} YEAR {quarter} Quarter Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=800)
        st.plotly_chart(amount)
    
    with col2:
        amount=px.bar(group,x="States",y="Transaction_count",title=f"{map_year ['Years'].max()} YEAR {quarter} Quarter Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=800)
        st.plotly_chart(amount)

        #Geo Visulation plot India Map:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)

        state_name=[]
        for feature in data["features"]:
            state_name.append(feature["properties"]["ST_NM"])

        state_name.sort()

    col1,col2=st.columns(2)

    with col1:
        india=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Reds",
                                range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                                hover_name="States",title=f"{map_year ['Years'].max()} YEAR {quarter} Quarter Transaction Amount",fitbounds="locations",
                                height=650,width=800)

        india.update_geos(visible=False)
        st.plotly_chart(india)
    with col2:
        india_1=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Reds",
                                range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                                hover_name="States",title=f"{map_year ['Years'].max()} YEAR {quarter} Quarter Transaction Count",fitbounds="locations",
                                height=650,width=800)

        india_1.update_geos(visible=False)
        st.plotly_chart(india_1)

        return map_year

#Map_Transaction District Chart:

def map_trans_distr(df,State):
    map_tran_distr=df[df["States"] == State]
    map_tran_distr.reset_index(drop=True, inplace=True)
    group=map_tran_distr.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        pie_chart=px.line(data_frame= group, x="Districts",y="Transaction_amount",
                            title=f"{map_tran_distr ["Years"].max()} STATE {State} TRANSACTION AMOUNT")

        st.plotly_chart(pie_chart)
    with col2:
        pie_chart_1=px.line(data_frame= group, x="Districts",y="Transaction_count",
                            title=f"{map_tran_distr ["Years"].max()} STATE {State}  TRANSACTION COUNT")

        st.plotly_chart(pie_chart_1)

#Map_user_chart 01:

def map_user_year(df,year):
    map_user=df[df['Years']==year]
    map_user.reset_index(drop=True, inplace=True)

    map_user_gru=map_user.groupby("States")[["registeredusers","appopens"]].sum()
    map_user_gru.reset_index(inplace=True)

    map_user_bar=px.line(map_user_gru,x="States",y=["registeredusers","appopens"],
                    title=f"{year} REGISTERED USER AND APP OPENS",width=800,height=600)
    st.plotly_chart(map_user_bar)

    return map_user

#Map User Quarter wise:
def map_user_Y_Quar(df,quarter):
    map_user_quar=df[df['Quarter']==quarter]
    map_user_quar.reset_index(drop=True, inplace=True)

    map_user_quar_gr=map_user_quar.groupby("States")[["registeredusers","appopens"]].sum()
    map_user_quar_gr.reset_index(inplace=True)

    map_user_quar_bar=px.bar(map_user_quar_gr,x="States",y=["registeredusers","appopens"],
                    title=f"{df['Years'].min()} YEAR {quarter} Quarter REGISTERED USER AND APP OPENS",width=800,height=600)
    st.plotly_chart(map_user_quar_bar)
    
    return map_user_quar

#Map user District chart:

def map_user_distric(df,state):
    map_use_year_qu_sta=df[df["States"]==state]
    map_use_year_qu_sta.reset_index(drop=True,inplace=True)

    group=map_use_year_qu_sta.groupby("Districts")[["registeredusers","appopens"]].sum()
    group.reset_index(inplace= True)

    col1,col2=st.columns(2)
    with col1:
        line_chart=px.bar(data_frame=group,x="Districts", y="registeredusers",title=f"{map_use_year_qu_sta["Years"].max()} STATE {state} REGISTERED USER",
                        width=800)
        st.plotly_chart(line_chart)
    with col2:
        pie_chart_1=px.bar(data_frame=group, x="Districts",y="appopens",
                            title=f"{map_use_year_qu_sta ["Years"].max()} STATE {state}  APP USERS",width=800)

        st.plotly_chart(pie_chart_1)

        return map_use_year_qu_sta


#Top Transaction year wise:
def top_transa_year(df,year):
    top_transaction=df[df["Years"]==year]
    top_transaction.reset_index(drop=True,inplace=True)

    top_trans_grp=top_transaction.groupby("States")[["Transaction_amount","Transaction_count"]].sum()
    top_trans_grp.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        top_transa_year1=px.line(top_trans_grp, x="States", y="Transaction_amount", title=f"{year} YEAR TRANSACTION AMOUNT",
                            height=650, width=800)
        
        st.plotly_chart(top_transa_year1)
    with col2:
        top_transa_year2=px.line(top_trans_grp, x="States", y="Transaction_count",title=f"{year} YEAR TRANSACTION COUNT",
                                height=650, width=800)
        
        st.plotly_chart(top_transa_year2)

    #Geo Visulation plot India Map:
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]
    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()

    col1,col2=st.columns(2)
    with col1:
        india=px.choropleth(top_trans_grp, geojson=data, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Reds",
                                range_color=(top_trans_grp["Transaction_amount"].min(),top_trans_grp["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} YEAR TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=800)

        india.update_geos(visible=False)
        st.plotly_chart(india)
    
    with col2:
        india_1=px.choropleth(top_trans_grp, geojson=data, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Reds",
                                range_color=(top_trans_grp["Transaction_count"].min(),top_trans_grp["Transaction_count"].max()),
                                hover_name="States",title=f"{year} YEAR TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=800)

        india_1.update_geos(visible=False)
        st.plotly_chart(india_1)

        return top_transaction

#TOP TRANSACTION YEAR AND QUARTER CHART:
def top_transaction_y_qu(df,quarter):
    top_transa_state=df[df["Quarter"] == quarter]#Particular year matu yeduka
    top_transa_state.reset_index(drop=True, inplace=True)#actual index value change panna

    group=top_transa_state.groupby("States")[["Transaction_amount","Transaction_count"]].sum()
    group.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        #top_Transaction_amount:
        top_trans_qu=px.bar(group,x="States",y="Transaction_amount",title=f"{top_transa_state ['Years'].max()} YEAR {quarter} Quarter Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=800)
        
        st.plotly_chart(top_trans_qu)
    with col2:
        #top_Transaction_count:
        top_trans_qu=px.bar(group,x="States",y="Transaction_count",title=f"{top_transa_state['Years'].max()} YEAR {quarter} Quarter Transaction Count",
                        color_discrete_sequence=px.colors.sequential.Viridis,height=650,width=800)
        
        st.plotly_chart(top_trans_qu)
        
        return top_transa_state

#Top Transaction Pincode Chart:
def top_trans_Y_Qu_pin(df,state):
    top_tran_Ye_Sta=df[df["States"] == state]
    top_tran_Ye_Sta.reset_index(drop=True, inplace=True)
    
    group=top_tran_Ye_Sta.groupby("Pincode")[["Transaction_amount","Transaction_count"]].sum()
    group.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        pie_chart=px.pie(data_frame= group, names="Pincode",values="Transaction_amount",
                        width=600,title=f"{state} TRANSACTION AMOUNT")

        st.plotly_chart(pie_chart)
    with col2:

        pie_chart_1=px.pie(data_frame= group, names="Pincode",values="Transaction_count",
                        width=600,title=f"{state} TRANSACTION COUNT")

        st.plotly_chart(pie_chart_1)

#Top User Analysis:
def top_user_ye(df,year):
    top_user_year=df[df['Years']==year]
    top_user_year.reset_index(drop=True,inplace=True)

    group=top_user_year.groupby("States")[["RegisteredUsers"]].sum()
    group.reset_index(inplace=True)

    top_user_bar=px.histogram(top_user_year,x="States",y="RegisteredUsers",title=f"{year} YEAR TOP REGISTERED USERS",width=800,height=600)
    st.plotly_chart(top_user_bar)

    return top_user_year


#Top User Quarter analysis:
def top_user_Ye_Quar(df,quarter):
    top_user_year_qu=df[df['Quarter']==quarter]
    top_user_year_qu.reset_index(drop=True,inplace=True)

    group=top_user_year_qu.groupby("States")[["RegisteredUsers"]].sum()
    group.reset_index(inplace=True)

    top_user_Q_bar=px.line(top_user_year_qu,x="States",y="RegisteredUsers",title=f"{df['Years'].min()} YEAR {quarter} QUARTER TOP REGISTERED USERS",width=800,height=600)
    st.plotly_chart(top_user_Q_bar)

    return top_user_year_qu

#Top User Pincode analysis:
def top_user_pincode(df,state):
    top_user_Ye_Sta=df[df["States"] == state]
    top_user_Ye_Sta.reset_index(drop=True, inplace=True)

    top_user_pin=px.bar(top_user_Ye_Sta,x="Quarter",y="RegisteredUsers",title="REGISTERED USERS PINCODE AND QUARTER",
                        width=800,height=650,color="RegisteredUsers",hover_data="Pincode",color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(top_user_pin)

    return top_user_Ye_Sta

#Final Charts Transaction Amount:
#Qustion No 01,02,03:
def Top_chart_trans_amount(table_name):
    query2=f'''select States, sum(Transaction_amount) as Transaction_Amount
                from {table_name}
                group by States
                order by Transaction_amount
                limit 10 ;'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("State","Transaction Amount"))

    amount=px.bar(df_2,x="State",y="Transaction Amount",title="TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    #Chart 03:

    query3=f'''select States, avg(Transaction_amount) as Transaction_Amount
                from {table_name}
                group by States
                order by Transaction_amount'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("State","Transaction Amount"))

    amount=px.pie(df_3,names="State",values="Transaction Amount",title="TRANSACTION AMOUNT AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Final CHART TRANSACTION COUNT:
#Qustion No:01,02,03,04:
def Top_chart_trans_count(table_name):
    query2=f'''select States, sum(Transaction_count) as Transaction_Count
                from {table_name}
                group by States
                order by Transaction_count
                limit 10 ;'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("State","Transaction count"))

    amount=px.bar(df_2,x="State",y="Transaction count",title="TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    #Chart 02:

    query3=f'''select States, avg(Transaction_count) as Transaction_Count
                from {table_name}
                group by States
                order by Transaction_count'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("State","Transaction count"))

    amount=px.pie(df_3,names="State",values="Transaction count",title="TRANSACTION COUNT AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Qustion no 05: REGISTERED USER PLOT
def Top_chart_registered_user(table_name,state):
    query2=f'''select Districts, sum(registeredusers) as Registered_User from {table_name}
                where States = '{state}'
                group by Districts 
                order by Registered_User
                limit 10'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("Districts","Registered_User"))

    amount=px.bar(df_2,x="Districts",y="Registered_User",title="REGISTERED USER",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    #Chart 02:

    query3=f'''select Districts, avg(registeredusers) as Registered_User from {table_name}
                where States = '{state}'
                group by Districts 
                order by Registered_User
                limit 10'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("Districts","Registered_User"))

    amount=px.pie(df_3,names="Districts",values="Registered_User",title="REGISTERED USER AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Question 06: REGISTERED USER PLOT
def Top_chart_app_open(table_name,state):
    query2=f'''select Districts, sum(appopens) as App_Opens from {table_name}
                where States = '{state}'
                group by Districts 
                order by App_Opens
                limit 10'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("Districts","App_Opens"))

    amount=px.bar(df_2,x="Districts",y="App_Opens",title="APP OPENS",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    #Chart 03:

    query3=f'''select Districts, avg(appopens) as App_Opens from {table_name}
                where States = '{state}'
                group by Districts 
                order by App_Opens
                limit 10'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("Districts","App_Opens"))

    amount=px.pie(df_3,names="Districts",values="App_Opens",title="APP OPENS AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Question 07: REGISTERED USER FROM TOP USER PLOT
def Top_chart_registered_user_top_user(table_name):
    query2=f'''select States, sum(RegisteredUsers) as RegisteredUsers from {table_name}
                group by States 
                order by RegisteredUsers desc
                limit 10'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("States","RegisteredUsers"))

    amount=px.bar(df_2,x="States",y="RegisteredUsers",title="REGISTERED USER FROM TOP USER",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    #Chart 03:

    query3=f'''select States, avg(RegisteredUsers) as RegisteredUsers from {table_name}
                group by States 
                order by RegisteredUsers
                '''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("States","RegisteredUsers"))

    amount=px.pie(df_3,names="States",values="RegisteredUsers",title="REGISTERED USER FROM TOP USER AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Qustion 08: REGISTERED USER QUARTER FROM AGG USER PLOT
def agg_map_user_qu(table_name,District):
    query2=f'''select Quarter,sum(registeredusers) as registered_users 
                from {table_name}
                where States='{District}'
                group by Quarter 
                order by registered_users;'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("Quarter","registered_users"))

    amount=px.bar(df_2,x="Quarter",y="registered_users",title="REGISTERED USER QUARTER FROM TOP USER",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    # #Chart 03:

    query3=f'''select Quarter,avg(registeredusers) as registered_users 
                from {table_name}
                where States='{District}'
                group by Quarter 
                order by registered_users;'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("Quarter","registered_users"))

    amount=px.pie(df_3,names="Quarter",values="registered_users",title="REGISTERED USER QUARTER FROM TOP USER AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Question 09: REGISTERED USER QUARTER FROM MAP USER APP OPENS PLOT
def agg_map_user_app(table_name,District):
    query2=f'''select Quarter,sum(appopens) as appopens FROM {table_name}
                where States ='{District}'
                group by Quarter
                order by appopens;'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("Quarter","appopens"))

    amount=px.bar(df_2,x="Quarter",y="appopens",title="REGISTERED USER QUARTER FROM APP OPENS",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    # #Chart 03:

    query3=f'''select Quarter,avg(appopens) as appopens FROM {table_name}
                where States ='{District}'
                group by Quarter
                order by appopens;'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("Quarter","appopens"))

    amount=px.pie(df_3,names="Quarter",values="appopens",title="REGISTERED USER QUARTER FROM APP OPENS AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

#Question 10:BRANT WISE AGGREGATED USER PLOT
def agg_user_brand(table_name,District):
    query2=f'''select brands,sum(Transaction_count) as Transaction_count from {table_name}
                where States = '{District}'
                group by brands 
                order by Transaction_count
                limit 10;'''

    mycursor.execute(query2)
    table_1=mycursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_1,columns=("brands","Transaction_count"))

    amount=px.bar(df_2,x="brands",y="Transaction_count",title="BRANDS WISE TRANSACTION COUNT ASCENDING ORDER",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)

    # #Chart 03:

    query3=f'''select brands,avg(Transaction_count) as Transaction_count from {table_name}
                where States = '{District}'
                group by brands 
                order by Transaction_count
                limit 10;'''

    mycursor.execute(query3)
    table_2=mycursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_2,columns=("brands","Transaction_count"))

    amount=px.pie(df_3,names="brands",values="Transaction_count",title="BRANDS WISE TRANSACTION COUNT AVERAGE",
                    color_discrete_sequence=px.colors.sequential.Magenta,height=650,width=800)
    st.plotly_chart(amount)


#HOME PAGE AGGREGATE TRANSACTION:
def agg_transaction_map(df, year):
    tran_amo_year=df[df["Years"] == year]#Particular year matu yeduka
    tran_amo_year.reset_index(drop=True, inplace=True)#actual index value change panna

    group=tran_amo_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    #Geo Visulation plot India Map:
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]
    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()
    col1,col2=st.columns(2)
    
    with col1:
        india=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="Viridis",
                            range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                            hover_name="States",title=f"{year} AGGREGATED TRANSACTION AMOUNT",fitbounds="locations",
                            height=650,width=650)
        
        india.update_geos(visible=False)
        st.plotly_chart(india)
    with col2:
        india_1=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="Viridis",
                            range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                            hover_name="States",title=f"{year} AGGREGATED TRANSACTION COUNT",fitbounds="locations",
                            height=650,width=650)
        
        india_1.update_geos(visible=False)
        st.plotly_chart(india_1)

#Map Transction Year Analysis:
def map_transaction_map(df,year):
    map_transaction=df[df["Years"]==year]
    map_transaction.reset_index(drop=True,inplace=True)

    group=map_transaction.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group.reset_index(inplace=True)

    #Geo Visulation plot India Map:
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]
    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()
    col1,col2=st.columns(2)
    with col1:
        india_2=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_amount",color_continuous_scale="Plasma",
                            range_color=(group["Transaction_amount"].min(),group["Transaction_amount"].max()),
                            title=f"{year} MAP TRANSACTION AMOUNT",fitbounds="locations",height=650,width=800)
        india_2.update_geos(visible=False)
        st.plotly_chart(india_2)
    
    with col2:
        india_3=px.choropleth(group,geojson=data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_count",color_continuous_scale="Plasma",
                            range_color=(group["Transaction_count"].min(),group["Transaction_count"].max()),
                            title=f"{year} MAP TRANSACTION COUNT",fitbounds="locations",height=650,width=800)
        india_3.update_geos(visible=False)
        st.plotly_chart(india_3)

#Top Transaction year analysis:
def top_transa_map(df,year):
    top_transaction=df[df["Years"]==year]
    top_transaction.reset_index(drop=True,inplace=True)

    top_trans_grp=top_transaction.groupby("States")[["Transaction_amount","Transaction_count"]].sum()
    top_trans_grp.reset_index(inplace=True)

    #Geo Visulation plot India Map:
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)

    state_name=[]
    for feature in data["features"]:
        state_name.append(feature["properties"]["ST_NM"])

    state_name.sort()
    col1,col2=st.columns(2)
    with col1:
        india=px.choropleth(top_trans_grp, geojson=data, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Inferno",
                                range_color=(top_trans_grp["Transaction_amount"].min(),top_trans_grp["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} YEAR TOP TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=800)

        india.update_geos(visible=False)
        st.plotly_chart(india)
    with col2:
        india_1=px.choropleth(top_trans_grp, geojson=data, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Inferno",
                                range_color=(top_trans_grp["Transaction_count"].min(),top_trans_grp["Transaction_count"].max()),
                                hover_name="States",title=f"{year} YEAR TOP TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=800)

        india_1.update_geos(visible=False)
        st.plotly_chart(india_1)


#Streamlit Part
# Comfiguring Streamlit:
st.set_page_config(layout='wide',
                   page_icon=":trophy:")

# Title
st.header(':rainbow[Phonepe Pulse Data Visualization]')
st.write("***Phonepe Data Analysis***")

# Select tab
tab,tab1,tab2, tab3, tab4 = st.tabs(['**Geo Visulation**','**Aggregated**','**Map**','**Top**','**Top Chart**'])

#GEO VISULATION PART:
with tab:
    col1,col2=st.columns(2)
    with col1:
        method=st.image("https://entrackr.com/storage/2017/08/phone-pay-image.jpg",width=650)
    with col2:
        method=st.image("https://sarkaripariksha.com/daily-news-images/1676025622-news.jpeg",width=650)
    
    method=st.radio("SELECT METHOD",["AGGREGATED TRANSACTION","MAP TRANSACTION","TOP TRANSACTION"])
    
    if method =="AGGREGATED TRANSACTION":
        years=st.selectbox("SELECT THE YEAR AGGREGATED TRANSACTION",aggregated1['Years'].unique())
        agg_transaction_map(aggregated1,years)

    elif method =="MAP TRANSACTION":
        years=st.selectbox("SELECT THE YEAR MAP TRANSACTION",map1['Years'].unique())
        map_transaction_map(map1,years)

    elif method =="TOP TRANSACTION":
        years=st.selectbox("SELECT THE TRANSACTION TOP",top1['Years'].unique())
        top_transa_map(top1, years)

#AGGREGATED PART:
with tab1:
    method=st.radio("Select The Method",["Aggregated Transaction","Aggregated User"]) 

    if method=="Aggregated Transaction":

        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Year",aggregated1['Years'].unique())
        frame_agg_tran=Transaction_amount_count_Y(aggregated1,years)

        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarter",frame_agg_tran["Quarter"].unique())
        frame_agg_tran_q=Transaction_Quarter(frame_agg_tran,quarter)

        
        col1,col2=st.columns(2)
        with col1:
            
            State=st.selectbox("Select The Year_Transaction Type", aggregated1['Years'].unique())
        agg_transaction_type_year(aggregated1,State)

        col1,col2=st.columns(2)
        with col1:
            
            states=st.selectbox("Select The State", frame_agg_tran['States'].unique())
        agg_tran_transaction_type(frame_agg_tran,states)

#AGGREGATED USER PART:
    elif method=="Aggregated User":
        
        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Year",aggregated2['Years'].unique())
        Agg_user_year=agge_user_plot(aggregated2,years)
        
        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarter",Agg_user_year["Quarter"].unique())
        Agg_user_year_quar=agg_user_qu(Agg_user_year,quarter) 

        col1,col2=st.columns(2)
        with col1:
            
            states=st.selectbox("Select The State Type", Agg_user_year_quar['States'].unique())
        agg_user_state(Agg_user_year_quar,states)

#MAP TRANSACTION PART:
with tab2:

    method_2=st.radio("Select The Method",["Map Transaction","Map User"])

    if method_2=="Map Transaction":

        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Years",map1['Years'].unique())
        map_tran_year=map_transaction_year(map1,years)
        
        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarters",map_tran_year["Quarter"].unique())
        map_trans_ye_qu=map_tran_year_qua(map_tran_year,quarter)

        col1,col2=st.columns(2)
        with col1:

            distric=st.selectbox("Select The States",map_trans_ye_qu["States"].unique())
        map_trans_dist=map_trans_distr(map_trans_ye_qu, distric)

    elif method_2=="Map User":

        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Year_map_user",map2['Years'].unique())
        map_user_Y=map_user_year(map2,years)

        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarter_map_user",map_user_Y["Quarter"].unique())
        map_user_quar_df=map_user_Y_Quar(map_user_Y,quarter)

        col1,col2=st.columns(2)
        with col1:

            distric=st.selectbox("Select The States_map_user",map_user_quar_df["States"].unique())
        map_trans_dist=map_user_distric(map_user_quar_df, distric)

#TOP TRANSACTION:
with tab3:

    method_3=st.radio("Select The Method",["Top Transaction","Top Users"])

    if method_3=="Top Transaction":

        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Years Top Transaction",top1['Years'].unique())
        top_transaction_year=top_transa_year(top1, years)

        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarter Top Transaction",top_transaction_year["Quarter"].unique())
        top_trans_ye_qu=Transaction_Quarter(top_transaction_year,quarter)
        
        col1,col2=st.columns(2)
        with col1:
            pincode=st.selectbox("Select The States Top Transaction",top1["States"].unique())
        top_trans_pin=top_trans_Y_Qu_pin(top1, pincode)


    elif method_3=="Top Users":

        col1,col2= st.columns(2)
        with col1:

            years=st.selectbox("Select The Year Top User",top2['Years'].unique())
        top_user_year_df=top_user_ye(top2,years)

        col1,col2=st.columns(2)
        with col1:

            quarter=st.selectbox("Select The Quarter Top User",top_user_year_df["Quarter"].unique())
        top_user_ye_quar_df=top_user_Ye_Quar(top_user_year_df, quarter) 

        col1,col2=st.columns(2)
        with col1:
            states=st.selectbox("Select The States Top User",top_user_year_df["States"].unique())
        top_user_pin=top_user_pincode(top_user_year_df, states)

#QUESTION ANSWERS:
with tab4:
    question=st.selectbox("Select the questions",["1.What are the Aggregated Transaction of Amount and Count",
                                                    "2.What are the Map Transaction of Amount and Count",
                                                    "3.What are the Top Transaction of Amount and Count",
                                                    "4.What are the Transaction Count of Aggregated user",
                                                    "5.What are the Registered Users of Map User From District wise",
                                                    "6.What are the App Opens of Map User",
                                                    "7.What are the Registered Users of Top User",
                                                    "8.Quater wise Registered users of Map User",
                                                    "9.App opens from Quarter wise map users",
                                                    "10.Aggregated user from Brands"])


    if question == "1.What are the Aggregated Transaction of Amount and Count":
        Top_chart_trans_amount("aggregated_transaction")
        Top_chart_trans_count("aggregated_transaction")

    elif question == "2.What are the Map Transaction of Amount and Count":
        Top_chart_trans_amount("aggre_map_trans")
        Top_chart_trans_count("aggre_map_trans")

    elif question == "3.What are the Top Transaction of Amount and Count":
        Top_chart_trans_amount("top_trans_list")
        Top_chart_trans_count("top_trans_list")

    elif question == "4.What are the Transaction Count of Aggregated user":
        Top_chart_trans_count("aggregated_users")

    elif question =="5.What are the Registered Users of Map User From District wise":
        state=st.selectbox("Select the State",  map2['States'].unique())
        Top_chart_registered_user("aggre_map_user", state)

    elif question =="6.What are the App Opens of Map User":
        state=st.selectbox("Select the State",  map2['States'].unique())
        Top_chart_app_open("aggre_map_user", state)

    elif question =="7.What are the Registered Users of Top User":
        state=st.selectbox("Select the State",  top2['States'].unique())
        Top_chart_registered_user_top_user("top_users_list")

    elif question =="8.Quater wise Registered users of Map User":
        distric=st.selectbox("Select the State",map2['States'].unique())
        agg_map_user_qu("aggre_map_user",distric)

    elif question == "9.App opens from Quarter wise map users":
        distric=st.selectbox("Select the State",map2['States'].unique())
        agg_map_user_app("aggre_map_user",distric)

    elif question == "10.Aggregated user from Brands":
        distric=st.selectbox("Select the State",aggregated2['States'].unique())
        agg_user_brand("aggregated_users",distric)