FROM python:3.6-alpine

# 设置环境变量
ARG VER_GLIBC=2.31-r0
ARG GLIBC_DOWNLOAD_URL=https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${VER_GLIBC}
ENV SVN_DEPLOY_URL="http://fy-svn.fjfuyu.net/svn/Deploy/"
ENV SVN_USER_NAME="jk_read-only"
ENV SVN_PASS_WORD="jk_read-only@fjfuyu.net"
ENV LANG=en_US.UTF8

# 定义工作目录
WORKDIR /app

# 更换国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 上传flask程序
ADD ./app /app

# 安装常用软件
RUN apk upgrade --no-cache &&\
    apk add --no-cache bash ca-certificates openssl tzdata tcpdump wget curl net-tools musl git subversion expect &&\
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo "Asia/Shanghai" > /etc/timezone 

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub 
#    wget ${GLIBC_DOWNLOAD_URL}/glibc-${VER_GLIBC}.apk 

#RUN  wget ${GLIBC_DOWNLOAD_URL}/glibc-bin-${VER_GLIBC}.apk &&\
#    wget ${GLIBC_DOWNLOAD_URL}/glibc-i18n-${VER_GLIBC}.apk 

COPY glibc-*.apk  /usr/local/glibc/

RUN   cd  /usr/local/glibc/ &&  apk add glibc-${VER_GLIBC}.apk glibc-bin-${VER_GLIBC}.apk glibc-i18n-${VER_GLIBC}.apk &&\
    /usr/glibc-compat/bin/localedef -i en_US -f UTF-8 en_US.UTF-8 

RUN  which pip &&   pip install --upgrade pip  -i https://mirrors.aliyun.com/pypi/simple

RUN  pip install flask python-jenkins python-gitlab svn pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple &&\
    rm -rf /tmp/* /var/cache/apk/*

# 添加svn服务器证书信任
RUN cp -a /app/svnSelfSignedRootCA.crt /usr/local/share/ca-certificates/ && update-ca-certificates &&\
    chmod a+x /app/login-svn.sh && sh /app/login-svn.sh

EXPOSE 8888

ENTRYPOINT ["python", "manage.py"]
