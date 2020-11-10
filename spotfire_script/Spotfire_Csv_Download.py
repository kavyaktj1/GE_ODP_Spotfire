#!/usr/bin/python3
from github import Github
import os
import re
import sys
import boto3
import subprocess
from datetime import datetime
import pytz 
import time
import requests
import pyral
from pyral import Rally, rallyWorkset,RallyRESTResponse
import base64 
import string

#####VARIABLE SECTION###########
merge_to_dev=''
approver_matched=''
approver_length=''
reviewer_str =''
success_merge_release_cnt=0
usr_str_not_found=''
##################################


#Begining of main block
v_version=pyral.__version__
print ("v_version:"+str(v_version))

list_of_csv=[]

options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
args    = [arg for arg in sys.argv[1:] if arg not in options]
print (args)
print (args[0])
print ( "checking for the argument")
query_stmt= "FormattedID"+ " = "+args[0]
print (type(query_stmt))
print (len(query_stmt))
print ("special char query_stmt")
literal_string = repr(query_stmt)
print (literal_string)
print ("query_stmt Valid") if re.match("^[a-zA-Z0-9]*$", query_stmt) else print ("query_stmt Invalid")
usr_story_arg=args[0].strip()
print ("after striping ")
print (type(usr_story_arg))
print (len(usr_story_arg))
print ("special char usr_story_arg")
literal_string = repr(usr_story_arg)
print (literal_string)
print ("usr_story_arg Valid") if re.match("^[a-zA-Z0-9]*$", usr_story_arg) else print ("usr_story_arg Invalid")
server, user, password, apikey, workspace, project = rallyWorkset(options)
#rally = Rally(server, user, password, apikey='_ERnpK4RQNCn0kTdcoyyhKGQFsgeEb1jNurFTBgvWw', workspace='BI Build', project='ODP Services Migration')
rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)

if os.path.isfile('export/spotfire_data.csv'):
    print ('Deleting spotfire_data.csv file as it is present')
    os.system('rm export/spotfire_data.csv')
else :
    print ('spotfire_data file is not present.Which is OK')
    
if os.path.isfile('export/spotfire_data_temp.csv'):
    print ('Deleting spotfire_data_temp.csv file as it is present')
    os.system('rm export/spotfire_data_temp.csv')
else :
    print ('spotfire_data_temp file is not present.Which is OK')
os.system('> export/user_story_list.csv')

'''
state1=rally.getStates('US74407')
criterion = 'FormattedID = US74407'
response = rally.get('UserStory', fetch=True, query=criterion)
if not response.errors:
    for story in response:
        for task in story.Tasks:
            print (task.oid, task.Name)
            att=
            print (
   
   
   



PROJECT = 'ODP Services Migration'
project_req = rally.get('Project', fetch=True, query='Name = "%s"' % (PROJECT))
project = project_req.next()

user_stories = rally.get('HierarchicalRequirement', fetch=True, query='Project = %s' % (project.ref))
counter=0




with open(os.path.join('export','user_story_list.csv'), 'r') as f:
    Lines = f.readlines() 
    for line in Lines:
        usr_story_temp=line.split(',') 
        if usr_story_arg in usr_story_temp[0]:
            if 'Defined' in usr_story_temp[1]:
                print (line)
                print("The user story :"+str(usr_story_arg) +" is there.So, not proceeding further.Hence Exiting")
                sys.exit()
        else :
                
                usr_str_not_found=1
if usr_str_not_found == 1:
    print("The user story :"+str(usr_story_arg) +" is not there in the list.So,appending it.And proceeding.") 
    for user_story in user_stories:
        foid=user_story.FormattedID
        if usr_story_arg == foid :
            #att=user_story.attributes()
            #foid=user_story.FormattedID
            #name=user_story.Name
            #oid=user_story.ObjectID
            #own=user_story.Owner
            #parent=user_story.Parent
            #cr_at=user_story._CreatedAt
            #dash_name=user_story.c_DashboardName
            #us_acpt_dt=user_story.c_USAcceptedDate
            #us_release_dt=user_story.c_USReleasedDate
            #us_notes=user_story.c_UserStoryNotes
            #defect=user_story.DefectStatus
            #ready=user_story.Ready
            schedule=user_story.ScheduleState
            #t_actual=user_story.TaskActualTotal
            #t_estimate=user_story.TaskEstimateTotal
            #t_remain=user_story.TaskRemainingTotal
            #t_status=user_story.TaskStatus
            #t=user_story.Tasks
            
            fields    = "FormattedID,State,Name"
            #criterion = 'State != Closed'
            #criterion = 'iteration = /iteration/20502967321'
            criterion = 'iteration.Name = \"iteration 5\"'
            
            #response = rally.get('Task', fetch=fields, query=criterion, order="FormattedID",pagesize=200, limit=400)
                                    
            #print (foid,name,oid,own,parent,dash_name,us_acpt_dt,us_release_dt,us_notes,defect,ready,schedule,t_actual,t_estimate,t_remain,t_status,t)
            with open(os.path.join('export','user_story_list.csv'), 'a') as f:
                ustr_schedule=foid+","+schedule+"\n"
                f.write(ustr_schedule)
            #counter=counter+1
            #foid = user_story.FormattedID
            #state = user_story.State
            #print (counter,foid,state)

'''
'''
workspaces = rally.getWorkspaces()
for wksp in workspaces:
    print (wksp.oid,wksp.Name)
    projects = rally.getProjects(workspace=wksp.Name)
    for proj in projects:
        print (proj.oid,proj.Name)
#csvname=rally.getAttachmentNames('US75163')
#print (csvname)


project_req = rally.get('Project', fetch=True, query='Name = "%s"' % ('ODP Services Migration'))
project = project_req.next()

user_stories = rally.get('HierarchicalRequirement', fetch=True, query='Project = %s' % (project.ref))

response = rally.get('UserStory', fetch=True, query=query_stmt)
#story1 = response.next()
#print (response.details())
for item in response :
    name=item.Name
    children = item.Children
    parent = item.Parent
    foid = item.FormattedID
    attachment = item.Attachments[0]
    print(name,children,parent,foid,attachment)
'''

################

criterion = 'FormattedID = US74407'
print (type(criterion))
print (len(criterion))

print ("special char criterion")
literal_string = repr(criterion)
print (criterion)
print ("criterion Valid") if re.match("^[a-zA-Z0-9]*$", criterion) else print ("criterion Invalid")

#criterion = 'FormattedID = '+args[0]+"'"
#criterion = "'"+"FormattedID "+ " = "+args[0].strip()+"'"
#criterion=criterion.strip()
response = rally.get('HierarchicalRequirement',  query=query_stmt, order="FormattedID",pagesize=200, limit=400, projectScopeDown=True)
	
artifact = response.next()
context, augments = rally.contextHelper.identifyContext()
for att in artifact.Attachments:
    resp = rally._getResourceByOID(context, 'AttachmentContent', att.Content.oid, project=None)
    if resp.status_code not in [200, 201, 202]:
        break
    res = RallyRESTResponse(rally.session, context, "AttachmentContent.x", resp, "full", 1)
    if res.errors or res.resultCount != 1:
        print("breaking the for loop")
    att_content = res.next()
    cont = att_content.Content
    x = base64.b64decode(cont)
    FileName=att.Name
    output = open(os.path.join('export','spotfire_data_temp.csv'), 'ab') 
    output.write(x)
    output.close()
    list_of_csv.append(FileName)
    print (list_of_csv)
    #with open(os.path.join('export','list_of_csv.txt'), 'w') as f:
        #for item in list_of_csv:
            #f.write("%s\n" % item)



with open(os.path.join('export','spotfire_data_temp.csv'), 'r') as f:
    for line_no, line in enumerate(f):
        if   line_no != 0 and 'OBJECT_NAME' in line:
             print ('should not print')
             pass
        else :
            #with open(os.path.join('export','spotfire_data.csv'), 'a') as f1:
                #f1.write(line)
            
            output = open(os.path.join('export','spotfire_data.csv'), 'a') 
            output.write(line)
            output.close()
print ('Deleting spotfire_data_temp.csv file')
os.system('rm export/spotfire_data_temp.csv')

