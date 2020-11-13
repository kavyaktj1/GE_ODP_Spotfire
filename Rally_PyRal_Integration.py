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
from pyral import Rally, rallyWorkset, RallyRESTResponse
import base64
import string
from dateutil.relativedelta import relativedelta
import datetime

# Begining of main block
v_version = pyral.__version__
# print("v_version:" + str(v_version))

# Variable Declaration
list_of_csv = []
open_user_stories = []
feature = 'F3031'  # Feature id in rally perticulary for CICD Team
one_month_before_time = datetime.date.today() - relativedelta(months=1)  # gives 1 month old time from toaday
query_stmt = ''

# Params: Fetching Configuration file values -- rally_configuration.cfg
options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
args = [arg for arg in sys.argv[1:] if arg not in options]

# Connecting to Rally
server, user, password, apikey, workspace, project = rallyWorkset(options)
rally = Rally(server, user, password, apikey=apikey, workspace=workspace, project=project)

def pre_check_csv_files_in_repo():
    if os.path.isfile('export/spotfire_data.csv'):
        # print('Deleting spotfire_data.csv file as it is present')
        logFile.write('Deleting spotfire_data.csv file as it is present\n')
        os.system('rm export/spotfire_data.csv')
    else:
        # print('spotfire_data file is not present.Which is OK')
        logFile.write('spotfire_data file is not present.Which is OK\n')

    if os.path.isfile('export/spotfire_data_temp.csv'):
        os.system('rm export/spotfire_data_temp.csv')
        logFile.write('Deleting spotfire_data_temp.csv file as it is present\n')
        # print('Deleting spotfire_data_temp.csv file as it is present')
    else:
        # print('spotfire_data_temp file is not present.Which is OK')
        logFile.write('spotfire_data_temp file is not present.Which is OK\n')
    os.system('> export/user_story_list.csv')


def get_open_user_stories():
    user_stories = rally.get('HierarchicalRequirement', fetch=True)
    for user_story in user_stories:
        # filter the userstories according to Feature value and created time
        if (user_story.CreationDate[0:10] > str(one_month_before_time)):
            try:
                if (user_story.Feature.FormattedID == feature and len(
                        user_story.Tasks) == 0 and user_story.FlowState.Name != 'Completed'):
                    logFile.write('user_story.FormattedID = '+str(user_story.FormattedID)+"\n")
                    logFile.write('user_story.CreationDate[0:10] = '+str(user_story.CreationDate[0:10])+"\n")
                    logFile.write('user_story.FlowState.Name = ' + str(user_story.FlowState.Name) + "\n")
                    # print(user_story.FormattedID, user_story.CreationDate[0:10], user_story.FlowState.Name)
                    open_user_stories.append(user_story.FormattedID)
            except:
                continue
    return open_user_stories


# This function copy's csv content from UserStroy csv file to temporary csv file in jenkins workspace
def get_csv_attachment_content(query_stmt):
    logFile.write(query_stmt)
    response = rally.get('HierarchicalRequirement', query=query_stmt, order="FormattedID", pagesize=200, limit=400,
                              projectScopeDown=True)
    artifact = response.next()
    context, augments = rally.contextHelper.identifyContext()
    for att in artifact.Attachments:
        resp = rally._getResourceByOID(context, 'AttachmentContent', att.Content.oid, project=None)
        if resp.status_code not in [200, 201, 202]:
            break
        res = RallyRESTResponse(rally.session, context, "AttachmentContent.x", resp, "full", 1)
        if res.errors or res.resultCount != 1:
            logFile.write("breaking the for loop\n")
            # print("breaking the for loop")
        att_content = res.next()
        cont = att_content.Content
        x = base64.b64decode(cont)
        FileName = att.Name
        output = open(os.path.join('export', 'spotfire_data_temp.csv'), 'ab')
        output.write(x)
        output.close()
        list_of_csv.append(FileName)
        logFile.write('list_of_csv = ' + str(list_of_csv) + "\n")
        # print(list_of_csv)


def copy_temp_to_spotfire_csv():
    with open(os.path.join('export', 'spotfire_data_temp.csv'), 'r') as f:
        for line_no, line in enumerate(f):
            if line_no != 0 and 'OBJECT_NAME' in line:
                # print('should not print')
                pass
            else:
                output = open(os.path.join('export', 'spotfire_data.csv'), 'a')
                output.write(line)
                output.close()
    print('Deleting spotfire_data_temp.csv file')
    logFile.write("Deleting spotfire_data_temp.csv file\n")
    os.system('rm export/spotfire_data_temp.csv')

# will genearte log file of this script
if os.path.isfile('export/RallyLogFile.txt'):
    # print('Deleting RallyLogFile.txt file as it is present')
    os.system('rm export/RallyLogFile.txt')
logFile = open(os.path.join('export', 'RallyLogFile.txt'), 'a+')
logFile.write('\nPyRal python script Log File\n')
logFile.write("v_version:" + str(v_version)+"\n")

# check for manual run or Auto run 
if (len(args) != 0):
    usr_story_arg = args[0].strip()
    # print('UserStory passed manually = ',usr_story_arg)
    logFile.write('UserStory passed manually = '+str(usr_story_arg)+"\n")
    query_stmt = "FormattedID" + " = " + usr_story_arg
    # print ('query_stmt = ',query_stmt)
    pre_check_csv_files_in_repo()
    get_csv_attachment_content(query_stmt)
    copy_temp_to_spotfire_csv()
    logFile.close()
    print(usr_story_arg)

else:
    # Calling pre_check_csv_files_in_repo
    pre_check_csv_files_in_repo()

    # Get open Userstories from Rally
    open_user_stories = get_open_user_stories()
    # print('Number of open UserStories are = ', open_user_stories)
    logFile.write('Number of open UserStories are = '+str(open_user_stories) + "\n")
    if (len(open_user_stories) == 0):
        logFile.close()
        print('NULL')
        sys.exit(0)
    else:
        # check for csv attachemnet content for open userstories -- pick only one userstory for every run
        for user_story in open_user_stories:
            query_stmt = "FormattedID" + " = " + user_story
            # print('user_story = ', user_story)
            logFile.write('user_story =  '+ str(user_story) + "\n")
            get_csv_attachment_content(query_stmt)
            break
        # copy csv contents fron temporary file to spotfire_data.csv
        copy_temp_to_spotfire_csv()
        logFile.close()
        print(user_story)
