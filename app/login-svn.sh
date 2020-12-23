#!/bin/bash

user_name="${SVN_USER_NAME}"
pass_word="${SVN_PASS_WORD}"
deploy_url="${SVN_DEPLOY_URL}"

expect << EOF
spawn svn ls --username ${user_name} --password ${pass_word} ${deploy_url}
expect "(R)eject, accept (t)emporarily or accept (p)ermanently? "
exit
EOF

