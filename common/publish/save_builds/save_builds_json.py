#!/usr/bin/env python
#coding: utf-8

import os
import sys
import json
import requests
import dateutil.parser
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

def checkUrl(url, stand, mode, platform):
    if platform == "ios":
      return ".plist" in url and stand in url and (mode == "debug" and "-d" in url or mode == "release" and "-d" not in url)
    else:
      return ".apk" in url and stand in url and mode in url

private_token = "37q8yNj5cc5yrd6CkQ5m"
branch = sys.argv[1]
configs = sys.argv[2].strip().split("#")
dropboxUrls = sys.argv[3].strip().split("#")
today = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M")

try:
  os.remove("build/data/builds_current.json")
except OSError as e:
  print "Warning: Didn't delete \"build/data/builds_current.json\""

response = requests.get(
	"http://git.dos.softlab.ru/api/v4/projects/81/repository/commits",
	headers = {
		"Content-Type": "application/json"
	},
	params = {
	  "private_token": private_token,
	  "ref_name": branch
	}
)
commit_list = json.loads(response.content)
last_commit = commit_list[0]["short_id"]

try:
  with open("build/data/builds.json") as json_data:
    builds = json.load(json_data)
except IOError as e:
  builds = {}
builds_current = {}

response = requests.get(
	"http://git.dos.softlab.ru/api/v4/projects/81/merge_requests",
	headers = {
		"Content-Type": "application/json"
	},
	params = {
	  "private_token": private_token,
	  "per_page": 100,
	  "state": "merged",
	  "order_by": "updated_at"
	}
)
merged_100_merge_request_list = json.loads(response.content)

response = requests.get(
	"http://git.dos.softlab.ru/api/v4/projects/81/merge_requests",
	headers = {
		"Content-Type": "application/json"
	},
	params = {
    "private_token": private_token,
    "per_page": 100,
    "state": "opened"
  }
)
opened_100_merge_request_list = json.loads(response.content)

for config in configs:
  split = config.strip().split("_")
  stand = split[0]
  mode = split[1]
  platform = split[2]
  merged_merge_request_list = []
  opened_merge_request_list = []
  last_merge_request_id = 0

  if branch not in builds_current:
    builds_current[branch] = {}
    builds_current[branch][stand] = {}
    builds_current[branch][stand][mode] = {}
    builds_current[branch][stand][mode][platform] = {}
  elif stand not in builds_current[branch]:
    builds_current[branch][stand] = {}
    builds_current[branch][stand][mode] = {}
    builds_current[branch][stand][mode][platform] = {}
  elif mode not in builds_current[branch][stand]:
    builds_current[branch][stand][mode] = {}
    builds_current[branch][stand][mode][platform] = {}
  elif platform not in builds_current[branch][stand][mode]:
    builds_current[branch][stand][mode][platform] = {}

  if branch not in builds:
    builds[branch] = {}
    builds[branch][stand] = {}
    builds[branch][stand][mode] = {}
    builds[branch][stand][mode][platform] = {}
  elif stand not in builds[branch]:
    builds[branch][stand] = {}
    builds[branch][stand][mode] = {}
    builds[branch][stand][mode][platform] = {}
  elif mode not in builds[branch][stand]:
    builds[branch][stand][mode] = {}
    builds[branch][stand][mode][platform] = {}
  elif platform not in builds[branch][stand][mode]:
    builds[branch][stand][mode][platform] = {}
  else:
    last_merge_request_id = builds[branch][stand][mode][platform]["last_merge_request_id"]

  for merge_request in merged_100_merge_request_list:
    # цикл по мерджам до последнего участвовавшего в сборке
    if merge_request["id"] > last_merge_request_id:
      # если мердж в собираемую ветку - включаем сразу
      if merge_request["target_branch"] == branch and merge_request["title"] not in merged_merge_request_list:
        merged_merge_request_list.append(merge_request["title"])
    else:
      break
  builds[branch][stand][mode][platform]["last_merge_request_id"] = merged_100_merge_request_list[0]["id"]
  builds_current[branch][stand][mode][platform]["last_merge_request_id"] = merged_100_merge_request_list[0]["id"]

  opened_merge_request_list = []
  for merge_request in opened_100_merge_request_list:
    if merge_request["target_branch"] == branch:
      opened_merge_request_list.append(merge_request["title"])

  builds[branch][stand][mode][platform]["date"] = today
  builds[branch][stand][mode][platform]["revision"] = last_commit
  builds[branch][stand][mode][platform]["merged_merge_request_list"] = merged_merge_request_list
  builds[branch][stand][mode][platform]["opened_merge_request_list"] = opened_merge_request_list
  builds_current[branch][stand][mode][platform]["date"] = today
  builds_current[branch][stand][mode][platform]["revision"] = last_commit
  builds_current[branch][stand][mode][platform]["merged_merge_request_list"] = merged_merge_request_list
  builds_current[branch][stand][mode][platform]["opened_merge_request_list"] = opened_merge_request_list

  builds[branch][stand][mode][platform]["urls"] = []
  builds_current[branch][stand][mode][platform]["urls"] = []
  for url in dropboxUrls:
    if checkUrl(url, stand, mode, platform):
      builds[branch][stand][mode][platform]["urls"].append(url)
      builds_current[branch][stand][mode][platform]["urls"].append(url)

with open("build/data/builds.json", "w") as outfile:
  json.dump(builds, outfile)
with open("build/data/builds_current.json", "w") as outfile:
  json.dump(builds_current, outfile)
