#!/usr/bin/env python3
# encoding: utf-8
#

import json
import jenkins
import gitlab
import svn.remote
import svn.exception
import requests
import pymysql
from flask import Blueprint, request, jsonify, current_app as app
from requests.auth import HTTPBasicAuth

my_common_api = Blueprint('my_common_api', __name__)


#git仓库子目录
@my_common_api.route('/gitlab', methods=['GET'])
def get_dotnet_projects():
    if request.method == 'GET':
        token = request.args.get("token")
        groupname = request.args.get("groupname")
        projects_list = []
        try:
            client = gitlab.Gitlab(url=app.config["GITLAB_URL"], private_token=token)
            group = client.groups.get(groupname,all=True, as_list=False)
            projects = group.projects.list(all=True)
            for p in projects:
                projects_list.append(p.name)
        except Exception as err:
            print(err)
        projects_str = '\n'.join(projects_list)
        # print(projects_str)
        return projects_str

#获取svn项目目录
@my_common_api.route('/subversion', methods=['GET'])
def get_subversion_projects():
    if request.method == 'GET':
        deploy_url = request.args.get("url")
        projects_list = []
        try:
            client = svn.remote.RemoteClient(url=deploy_url, username=app.config["SVN_USER_NAME"],
                                             password=app.config["SVN_PASS_WORD"], trust_cert=True)
            projects = client.list()
            projects_list = []
            for p in projects:
                projects_list.append(p.replace('/', ''))
        except svn.exception.SvnException as err:
            print(err)
        projects_str = '\n'.join(projects_list)
        # print(projects_str)
        return projects_str

#git推送webhook到jenkins
@my_common_api.route('/webhook', methods=['POST'])
def web_hook():
    print("git webhook 开始！")
    def get_keys(i,j):
        y=[]
        for a in range(len(j)):
           if i in list(j.values())[a]:
               x=list(j.keys())[a]
               y.append(x)
        return y
    if request.method == 'POST':
        verify_token = request.headers.get('X-Gitlab-Token')
        if verify_token in app.config["WEBHOOK_VERIFY_TOKEN"]:
            data = request.get_data()
            dict_data = json.loads(data.decode("utf-8"))
            #提取有用参数
            prject_namespace= dict_data['project']['namespace']
            project_branch = dict_data['ref'].split('/')[2]
            project_name = dict_data['project']['name']
            user_name = dict_data['user_name']
            try:
                jenkins_group=get_keys(prject_namespace,app.config["WEBHOOK_GIT_GROUP"])[0]
                jenkins_brancher_group=get_keys(project_branch,app.config["WEBHOOK_BRANCHER"])[0]
                jenkins_jobName=app.config["JENKINS_JOB_NAME"][jenkins_group+"_"+jenkins_brancher_group]
            except  Exception as e:
                print(e)
                return jsonify({'status': prject_namespace+'的所属gitlab项目：'+project_name+',gitlab项目还未在jenins上设置JOB任务，请设置'}), 401
            deployEnv=''
            if project_branch == "dev":
                deployEnv="dev"
            elif project_branch == "master":
                deployEnv="pre"
            print("prject_namespace: {0}".format(prject_namespace))
            print("project_branch: {0}".format(project_branch))
            print("project_name: {0}".format(project_name))
            print("user_name: {0}".format(user_name))
            print("jenkins_jobName: {0}".format(jenkins_jobName))

            params = {'project_name': project_name, 'deployEnv': deployEnv, 'user_name': user_name}
            server = jenkins.Jenkins(url=app.config["JENKINS_URL"], username=app.config["JENKINS_USER_NAME"], password=app.config["JENKINS_API_TOKEN"])
            server.build_job(name=jenkins_jobName, parameters=params)

            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401
    else:
        print("methods 是：{0}".format(request.method))

#获取镜像最新tag
@my_common_api.route('/harbor_tag', methods=['GET'])
def harbor_tag_latest():
    if request.method == 'GET':
        harbor_repo_name = request.args.get("repo_name")
        harbor_repo_tag=[]
        harbor_url="{0}/api/repositories/{1}/tags?detail=false".format(app.config["HARBOR_URL"],harbor_repo_name)
        try:
            harbor_r=requests.get(url=harbor_url,auth=HTTPBasicAuth(app.config["HARBOR_USER_NAME"],app.config["HARBOR_PASS_WORD"]))
            for i in harbor_r.json():
                harbor_repo_tag.append(int(i['name']))
        except Exception as e:
            print(e)
        harbor_repo_tag.sort(reverse=True)
        print(harbor_repo_tag)
        harbor_repo_tag_latest=str(harbor_repo_tag[0])
        return harbor_repo_tag_latest

#获取生产MySQL全部数据库
@my_common_api.route('/prod_mysql', methods=['GET'])
def prod_mysql():
    if request.method == 'GET':
        env = request.args.get("env")
        mysql_conn=app.config["MYSQL_CONN"]
        if env not in mysql_conn.keys():
            return jsonify({"没有{0}这个环境的mysql配置".format(env)}), 401
        host=mysql_conn[env]["mysql_ip"]
        port=mysql_conn[env]["mysql_port"]
        user = mysql_conn[env]["mysql_user"]
        passwd = mysql_conn[env]["mysql_passwd"]
        charset= mysql_conn[env]["mysql_charset"]
        #连接数据库
        try:
            conn = pymysql.connect(host=host, port=port, user=user, password=passwd, charset=charset)
            cursor = conn.cursor()
            # 定义要执行的SQL语句
            sql = """
                show databases
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            dbs_list = []
            exclude_dbs=app.config["MYSQL_EXCLUDE"]
            for i in result:
                if i[0] not in exclude_dbs:
                    dbs_list.append(i[0])
            cursor.close()
            conn.close()
            dbs_str = '\n'.join(dbs_list)
            return dbs_str
        except Exception as e:
            return jsonify({e}), 401