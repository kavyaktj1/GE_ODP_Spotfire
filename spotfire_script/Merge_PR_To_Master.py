#!/usr/bin/python3
from github import Github
import os
import sys
import boto3
#####VARIABLE SECTION###########
merge_to_dev=''
approver_matched=''
approver_length=''
reviewer_str =''
success_merge_release_cnt=0
##################################

##print ("Total Number of PRs To Process are :" + str(pulls.totalCount))
def merge_feature_to_dev(pr):

    try:
        email=pr.user
        email=pr.user.login
        global pr_number
        global reviewer_str
        pr_number=pr.number
        review_requests = pr.get_review_requests()
        get_reviews=pr.get_reviews()
        review_state=''
        for reviews in get_reviews:
            #print("inside get_reviews")
            review_state=reviews.state
            review_state=review_state.strip()

        if review_state=='APPROVED' :
            feature_to_dev_merge_msg="Closing PR and merging via Git commands to avoid merge conflict"
            print_stmt="INFO:"+feature_to_dev_merge_msg
            feature_to_dev_commit_title="PR:"+str(pr_number)+" commit title"
            print_stmt=feature_to_dev_commit_title
            pull_done=pr.edit(title=feature_to_dev_commit_title, body=feature_to_dev_merge_msg, state='closed')
            return "Yes"
        else:
            return "None"
    
    except NameError as e:
        return e
        
    except Exception as e:
        return e


g = Github(base_url="https://github.build.ge.com/api/v3", login_or_token="9410aeef823911c5aa2814e7394dfe7334b53eb3")

repo = g.get_repo("DnA-ODP/ODP_Spotfire")


pulls = repo.get_pulls(state='open', sort='created', base='master')

if pulls.totalCount >0:
    for pr in pulls:
        pr_status = merge_feature_to_dev(pr)
        if pr_status=="Yes":
            branch_name = str(pr.head.label).split(':')[-1]
            print(branch_name)
        else:
            print(pr_status)
        break
 
else:
    print("None")
