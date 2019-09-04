import pandas as pd
import numpy as np
import re
import requests
import json
import os

os.chdir('F:/005_Works/CV/scraper/bytedance')

TYPE_PRODUCT = 874
TYPE_OPERATION = 877

sess = requests.Session()
json_url = "https://job.bytedance.com/api/recruitment/position/list/?type=1&summary_id=&sequence=&city=128&q1=%E6%95%B0%E6%8D%AE&name=&limit=100&offset=0&position_type=&_signature=oX4IGAAgEANJpCplnoZ2BKF-CAAAPwf"
resp = sess.get(json_url).text
resp_json = json.loads(resp)

columns = ['requirement','sub_name','sequence','position_id','create_time','type','position_advertisement_id','id','category','salary_min','salary_max','stage_time_stat','summary_id','description','city','expiry','work_year','hc','name','position_type','summary','channel_id','hot_flag','qualification','category_id']
job_df = pd.concat([pd.DataFrame(list(job.values())) for job in resp_json['positions']],axis = 1)
job_df = job_df.T
job_df.columns = columns
job_df.id = job_df.id.astype(str)
job_df['url'] = "https://job.bytedance.com/job/detail/" + job_df.id


mask = (job_df.summary_id.isin([TYPE_PRODUCT, TYPE_OPERATION])) & (job_df.work_year <= 5) & (~job_df.name.str.contains('资深|高级|专家|经理')) & (~job_df.requirement.str.contains('hadoop|spark'))
target_jobs = job_df[mask]
select_cols = ['name','requirement','description','work_year','sub_name','summary','category', 'url']

target_jobs[select_cols].to_excel('target_jobs.xlsx', encoding = 'GBK', index = False)
