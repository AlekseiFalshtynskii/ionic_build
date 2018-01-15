#!/usr/bin/env python
#coding: utf-8

import sys
import json
import codecs
import requests
import pystache

page = sys.argv[1]
branch = sys.argv[2]

confluence_url = "http://confluence/rest/api/content/" + page

response = requests.get(
	confluence_url,
	headers = {
		"Content-Type": "application/json"
	}
)
data = json.loads(response.content)
title = data["title"]
space = data["space"]
version = data["version"]["number"] + 1

response = requests.get(
	confluence_url,
	params = {
		"expand": "ancestors"
	},
	headers = {
		"Content-Type": "application/json"
	}
)
data = json.loads(response.content)
ancestors = [
  {
    "id": data["ancestors"][len(data["ancestors"]) - 1]["id"]
  }
]

try:
  with open("build/data/builds.json") as json_data:
    builds = json.load(json_data)
except IOError as e:
  print "Error: Couldn't read \"build/data/builds.json\""
  exit()

try:
  file = codecs.open("build/common/publish/confluence/page.mustache", "r", "utf-8")
  template = file.read()
except IOError as e:
  print "Error: Couldn't read \"build/common/publish/confluence/page.mustache\""
  exit()

def stand_comparator(left, right):
  if left == "shell":
    return -1
  elif right == "shell":
    return 1
  elif left == "online":
    return 1
  elif right == "online":
    return -1
  elif left == "qatar":
    return -1
  elif right == "qatar":
    return 1
  else:
    return 0

stands = []

for stand in builds[branch]:
  stands.append(stand)

stands.sort(stand_comparator)

params = {"stand": []}

for stand in stands:
  standJson = {
    "name": stand,
    "mode": []
  }
  for mode in builds[branch][stand]:
    for platform in builds[branch][stand][mode]:
      modeJson = {
        "name": mode,
        "platform": platform,
        "date": builds[branch][stand][mode][platform]["date"],
        "revision": builds[branch][stand][mode][platform]["revision"],
        "urls": []
      }
      for url in builds[branch][stand][mode][platform]["urls"]:
        modeJson["urls"].append({
          "url": url
        });
      standJson["mode"].append(modeJson)
  params["stand"].append(standJson)

splitLines = pystache.render(template, params).splitlines()

body = ""

for splitLine in splitLines:
  body += splitLine.strip()

response = requests.put(
  confluence_url,
  headers = {
    "Authorization": "Basic QWxla3NlaSBGYWxzaHRz",
    "Content-Type": "application/json"
  },
  data = json.dumps({
    "id": page,
    "type": "page",
    "title": branch,
    "space": space,
    "ancestors": ancestors,
    "body": {
      "storage": {
        "value": body,
        "representation": "storage"
      }
    },
    "version": {
      "number": version
    }
  })
)
print response.status_code
