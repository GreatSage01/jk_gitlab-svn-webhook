#!/usr/bin/env python3
# encoding: utf-8
#

import os

# GITLAB
GITLAB_URL = os.environ.get("GITLAB_URL", "http://git.fjfuyu.net")
GITLAB_PRIVATE_TOKEN = os.environ.get("GITLAB_PRIVATE_TOKEN", "9jAzgpnqiXgxqbKu1KF2")

# SVN
JAVA_DEPLOY_URL = os.environ.get("JAVA_DEPLAY_URL", "http://fy-svn.fjfuyu.net/svn/Deploy/test")
FRONTEND_DEPLOY_URL = os.environ.get("FRONTEND_DEPLOY_URL", "http://fy-svn.fjfuyu.net/svn/Deploy/test")
SVN_USER_NAME = os.environ.get("SVN_USER_NAME", "jk_read-only")
SVN_PASS_WORD = os.environ.get("SVN_PASS_WORD", "jk_read-only@fjfuyu.net")

# JENKSIN
JENKINS_URL = os.environ.get("JENKINS_URL", "http://jenkins.fjfuyu.net")
JENKINS_USER_NAME = os.environ.get("JENKINS_USER_NAME", "webhook")
JENKINS_API_TOKEN = os.environ.get("JENKINS_API_TOKEN", "11bcfb90b2eafd71c2addb615f17131cdc")
JENKINS_JOB_NAME = os.environ.get("JENKINS_JOB_NAME", {"dotnet_Com": "dotnet-new-pipeline",
                                                        "dotnet_AB": "dotnet-AB-pipeline",
                                                        "frontend_Com": "frontend-git-pipeline",
                                                        "java_Com": "java-git-pipeline"})

# WEBHOOK
WEBHOOK_BRANCHER = os.environ.get("WEBHOOK_BRANCHER",{ "Com" : [ "master" , "dev"],
                                                        "AB": ["t0","t1","t2"]})

WEBHOOK_VERIFY_TOKEN = os.environ.get("WEBHOOK_VERIFY_TOKEN", "8d87ab776829647ffbaa4d39abbbffc5")

WEBHOOK_GIT_GROUP = os.environ.get("WEBHOOK_GIT_GROUP", {"dotnet": "server-side", "frontend": "frontend", "java": "java"})

#Harbor
HARBOR_URL=os.environ.get("HARBOR_URL", "http://hub.xueerqin.net")
HARBOR_USER_NAME = os.environ.get("HARBOR_USER_NAME", "admin")
HARBOR_PASS_WORD = os.environ.get("HARBOR_PASS_WORD", "Fyinfo@123")

#Mysql
MYSQL_CONN=os.environ.get("MYSQL_CONN",{"prod":{"mysql_ip" : "172.16.0.27",
                                                "mysql_port" : 3306,
                                                 "mysql_user":"fyjy",
                                                 "mysql_passwd":"FYJY@yyinfo1205",
                                                 "mysql_charset":"utf8"},
                                        "uat":{"mysql_ip" : "172.16.0.232",
                                                "mysql_port" : 30837,
                                                 "mysql_user":"root",
                                                 "mysql_passwd":"Fyinfo@123",
                                                 "mysql_charset":"utf8"}
                                        }
                          )
MYSQL_EXCLUDE=os.environ.get("MYSQL_EXCLUDE",['information_schema','mysql','performance_schema','sys'])
