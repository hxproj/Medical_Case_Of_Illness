#! /bin/sh

#PATH=${WORKSPACE}/venv/bin:$PATH

COVER=coverage
#
#if [ ! -d "venv" ]; then
#	virtualenv venv
#fi
#chmod +x ./venv/bin/activate

./venv/bin/activate
pip install --trusted-host scmesos06 -i http://scmesos06:3141/simple -r requirements_dev.txt --cache-dir=/tmp/${JOB_NAME}

${COVER} run --source netscaler_sentinel -m unittest discover --start-directory test --pattern test_*.py

[ $? -gt 0 ] && exit 1

${COVER} xml