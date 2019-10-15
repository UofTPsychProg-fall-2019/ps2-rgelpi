#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil
import csv

#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    folder_name = 'testingroom' + room
    source = './' + folder_name + '/experiment_data.csv'
    shutil.copyfile(source,'./rawdata/experiment_data_' + room + '.csv')


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0, 5))
for room in testingrooms:
    with open('./rawdata/experiment_data_' + room + '.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for line in file:
            row = line.strip('\n').split(',')
            np_row = np.array(row)
            data = np.vstack((data,row))
print(data)


#%%
# calculate overall average accuracy and average median RT
#
data = data.astype(np.float)
acc_avg = data[:,3].mean(axis=0)   # 91.48%
print(acc_avg)
mrt_avg = data[:,4].mean(axis=0)   # 477.3ms
print(mrt_avg)


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
words_data = np.empty((0, 5))
faces_data = np.empty((0, 5))
for room in testingrooms:
    with open('./rawdata/experiment_data_' + room + '.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for line in file:
            row = line.strip('\n').split(',')
            if row[1] == '1':
                print('Adding to words.')
                np_row = np.array(row)
                words_data = np.vstack((words_data, row))
            else:
                print('Adding to faces.')
                np_row = np.array(row)
                faces_data = np.vstack((faces_data, row))

words_data = words_data.astype(np.float)
words_acc_avg = round(words_data[:,3].mean(axis=0),3)
print('Words: '+str(words_acc_avg*100)+'%')
words_mrt_avg = round(words_data[:,4].mean(axis=0),1)
print(str(words_mrt_avg)+'ms')
# words: 88.6%, 489.4ms
faces_data = faces_data.astype(np.float)
faces_acc_avg = round(faces_data[:,3].mean(axis=0),3)
print('Faces: '+str(faces_acc_avg*100)+'%')
faces_mrt_avg = round(faces_data[:,4].mean(axis=0),1)
print(str(faces_mrt_avg)+'ms')
# faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
pleasant_index = np.reshape(data[:,2],92).astype(int)
print(pleasant_index)
count = 0
acc_wp_sum = 0
acc_bp_sum = 0
mrt_wp_sum = 0
mrt_bp_sum = 0
wp = 0
for index in pleasant_index:
    if index == 1:
        wp += 1
        acc_wp_sum+=data[count,3]
        mrt_wp_sum+=data[count,4]
    else:
        acc_bp_sum+=data[count,3]
        mrt_bp_sum+=data[count,4]
    count += 1
acc_wp = round(acc_wp_sum/wp*100,3)
print(acc_wp)  # 94.0%
acc_bp = round(acc_bp_sum/wp*100,3)
print(acc_bp)  # 88.9%
mrt_wp = round(mrt_wp_sum/wp,1)
print(mrt_wp)  # 469.6ms
mrt_bp = round(mrt_bp_sum/wp,1)
print(mrt_bp)  # 485.1ms


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#

wordsp_index = np.reshape(words_data[:,2],46).astype(int)
facesp_index = np.reshape(faces_data[:,2],46).astype(int)
count = 0
words_wp_sum = 0
words_bp_sum = 0
faces_wp_sum = 0
faces_bp_sum = 0
wp = 0
# For use with scipy below.
words_wp_array = []
words_bp_array = []
faces_wp_array = []
faces_bp_array = []
for index in wordsp_index:
    if index == 1:
        wp += 1
        words_wp_sum+=words_data[count,4]
        words_wp_array.append(words_data[count,4])
    else:
        words_bp_sum+=words_data[count,4]
        words_bp_array.append(words_data[count, 4])
    count += 1
count = 0
wp = 0
for index in facesp_index:
    if index == 1:
        wp += 1
        faces_wp_sum+=faces_data[count,4]
        faces_wp_array.append(faces_data[count, 4])
    else:
        faces_bp_sum+=faces_data[count,4]
        faces_bp_array.append(faces_data[count, 4])
    count += 1

words_wp = round(words_wp_sum/wp,1)
print(words_wp)  # words - white/pleasant: 478.4ms
words_bp = round(words_bp_sum/wp,1)
print(words_bp)  # words - black/pleasant: 500.3ms
faces_wp = round(faces_wp_sum/wp,1)
print(faces_wp)  # faces - white/pleasant: 460.8ms
faces_bp = round(faces_bp_sum/wp,1)
print(faces_bp)  # faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats as stats

wordsttest = stats.ttest_rel(words_wp_array,words_bp_array)
print(wordsttest)
# words: t=-5.36, p=2.19e-5
facesttest = stats.ttest_rel(faces_wp_array,faces_bp_array)
print(facesttest)
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(acc_avg*100,mrt_avg))
print('WORDS: {:.2f}%, {:.1f} ms'.format(words_acc_avg*100,words_mrt_avg))
print('FACES: {:.2f}%, {:.1f} ms'.format(faces_acc_avg*100,faces_mrt_avg))
print('\nWORDS (WP mean: {:.1f} ms ≠ BP mean: {:.1f} ms): t = {:.2f}, p = {:.5f}'.format(words_wp,words_bp,wordsttest.statistic,wordsttest.pvalue))
print('FACES (WP mean: {:.1f} ms ≠ BP mean: {:.1f} ms): t = {:.2f}, p = {:.2f}'.format(faces_wp,faces_bp,facesttest.statistic,facesttest.pvalue))
