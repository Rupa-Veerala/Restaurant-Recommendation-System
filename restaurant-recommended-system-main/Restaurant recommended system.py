# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 21:20:03 2023

@author: MOHID BABU SHAIK
"""

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import string

filtered_res=pickle.load(open('filtered_res.pkl','rb'))
popularity=pickle.load(open('popularity.pkl','rb'))
output=pickle.load(open('output.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
filtered_res_out=pickle.load(open('filtered_res_out.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home_main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommendations',methods=['GET','POST'])
def recommendations():
    if request.method=='POST':
        loc = request.form.get('location', 'all')
        res = request.form.get('restaurant_name', 'all')
        res_type = request.form.get('restaurant_type', 'all')
        
        punc_to_remove=string.punctuation
        def remove_punctuation(text):
          return text.translate(str.maketrans('', '', punc_to_remove))
        res = remove_punctuation(res)
        res=res.replace(' ', '')
        def recommend_main(res,loc,res_type):
            if res!='all' and res not in filtered_res_out['name'].unique():
                res_output = pd.DataFrame()
                return res_output #print("Data Not Available")
            elif(res=='all' and res_type=='all'):
                res_output = pd.DataFrame()
                top5=popularity[popularity['location']==loc][:6]
                for i in range(len(top5)):
                    temp_df = top5.iloc[i]
                    temp_res = pd.DataFrame({
                        'name': [temp_df['name']],
                        'location': [temp_df['location']],
                        'rating': [temp_df['Rating']],
                        'cost': [temp_df['Cost']],
                        'rest_type': [temp_df['rest_type']],
                        'book_table': [temp_df['book_table']],
                        'online_order': [temp_df['online_order']],
                        'phone': [temp_df['phone']],
                        'address': [temp_df['address']]
                        })
                    res_output = pd.concat([res_output, temp_res], ignore_index=True)
                return res_output
            elif(loc=='all' and res_type=='all'):
                res_output = pd.DataFrame()
                matching_res=filtered_res_out[filtered_res_out['name']==res]
                if not matching_res.empty:
                    index = matching_res.index[0:]
                    if len(index)>0:
                        print(f"{len(index)} {res} restaurants is available in different location")
                        for i in range(len(index)):
                            location=filtered_res['location'][index[i]]
                            print(f"{res} at {location}")
                            distance=sorted(list(enumerate(similarity[index[i]])),reverse=True,key=lambda x:x[1])
                            print()
                            for i in distance[0:5]:
                                temp_df = output.iloc[i[0]]
                                temp_res = pd.DataFrame({
                                    'name': [temp_df['name']],
                                    'location': [temp_df['location']],
                                    'rating': [temp_df['Rating']],
                                    'cost': [temp_df['Cost']],
                                    'rest_type': [temp_df['rest_type']],
                                    'book_table': [temp_df['book_table']],
                                    'online_order': [temp_df['online_order']],
                                    'phone': [temp_df['phone']],
                                    'address': [temp_df['address']]
                                    })
                                res_output = pd.concat([res_output, temp_res], ignore_index=True)
                        return res_output
                    else:
                        return res_output
            
            elif(res !='all' and res_type == 'all'):
                res_output = pd.DataFrame()
                detail=popularity[(popularity['location'] == loc) & (popularity['name'] == res)]
                # print(detail.iloc[0, 0:])
                # print()
                # print("Related_restaurants")
                # print()
                # # res_output=detail
                temp=detail.iloc[0, 0:]
                det_tem=pd.DataFrame({
                    'name': [temp['name']],
                    'location': [temp['location']],
                    'rating': [temp['Rating']],
                    'cost': [temp['Cost']],
                    'rest_type': [temp['rest_type']],
                    'book_table': [temp['book_table']],
                    'online_order': [temp['online_order']],
                    'phone': [temp['phone']],
                    'address': [temp['address']]
                    })
                res_output = pd.concat([res_output, det_tem], ignore_index=True)
                matching_res=filtered_res_out[(filtered_res_out['location'] == loc) & (filtered_res_out['name'] == res)]
                if not matching_res.empty:
                    index = matching_res.index[0]
                    distance=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
                    for i in distance[1:6]:
                        temp_df = output.iloc[i[0]]
                        temp_res = pd.DataFrame({
                            'name': [temp_df['name']],
                            'location': [temp_df['location']],
                            'rating': [temp_df['Rating']],
                            'cost': [temp_df['Cost']],
                            'rest_type': [temp_df['rest_type']],
                            'book_table': [temp_df['book_table']],
                            'online_order': [temp_df['online_order']],
                            'phone': [temp_df['phone']],
                            'address': [temp_df['address']]
                            })
                        res_output = pd.concat([res_output, temp_res], ignore_index=True)
                    return res_output# 1 means return nothing there no res in the location
            elif(res == 'all' and loc != 'all' and res_type !='all'):
                res_output = pd.DataFrame()
                res_loc_details=popularity[(popularity['location'] == loc) & (popularity['rest_type'].isin([res_type]))]
                if not res_loc_details.empty:
                    for i in range(0,len(res_loc_details)):
                        temp_df = res_loc_details.iloc[i]
                        temp_res = pd.DataFrame({
                            'name': [temp_df['name']],
                            'location': [temp_df['location']],
                            'rating': [temp_df['Rating']],
                            'cost': [temp_df['Cost']],
                            'rest_type': [temp_df['rest_type']],
                            'book_table': [temp_df['book_table']],
                            'online_order': [temp_df['online_order']],
                            'phone': [temp_df['phone']],
                            'address': [temp_df['address']]
                            })
                        res_output = pd.concat([res_output, temp_res], ignore_index=True)
                    return res_output
                else:
                    top5=popularity[popularity['location']==loc][:10]
                    for i in range(len(top5)):
                        temp_df = top5.iloc[i]
                        temp_res = pd.DataFrame({
                            'name': [temp_df['name']],
                            'location': [temp_df['location']],
                            'rating': [temp_df['Rating']],
                            'cost': [temp_df['Cost']],
                            'rest_type': [temp_df['rest_type']],
                            'book_table': [temp_df['book_table']],
                            'online_order': [temp_df['online_order']],
                            'phone': [temp_df['phone']],
                            'address': [temp_df['address']]
                            })
                        res_output = pd.concat([res_output, temp_res], ignore_index=True)
                    return res_output
            else:
                res_output = pd.DataFrame()
                return res_output
        res_output=recommend_main(res, loc, res_type)
        return render_template('recommends_of_res.html',res=res,loc=loc,res_type=res_type,res_output=res_output)      
    return render_template('recommendations.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/signin')
def sign_in():
    return render_template('sign_in.html')

if __name__=='__main__':
    app.run(debug=True)