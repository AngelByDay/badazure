echo Python deployment.


echo "Deployment Source: $DEPLOYMENT_SOURCE"
echo "Deployment Target: $DEPLOYMENT_TARGET"


# 1. KuduSync

if [[ "$IN_PLACE_DEPLOYMENT" -ne "1" ]]; then
  "$KUDU_SYNC_CMD" -v 50 -f "$DEPLOYMENT_SOURCE/badazure" -t "$DEPLOYMENT_TARGET" -n "$NEXT_MANIFEST_PATH" -p "$PREVIOUS_MANIFEST_PATH" -i ".git;.hg;.deployment;deploy.sh"
  #exitWithMessageOnError "Kudu Sync failed"
fi


#2. Install any dependencies

export ANTENV="antenv"
export PYTHON3="python3.7"

if [ "$WEBSITE_PYTHON_VERSION" = "3.6" ]; then
    export ANTENV="antenv3.6"
    export PYTHON3="python3.6"
fi


if [ -f "$DEPLOYMENT_TARGET/requirements.txt" ]; then
  echo "Found requirements.txt"
  echo "Python Virtual Environment: $ANTENV"
  echo "Python Version: $PYTHON3"

  cd "$DEPLOYMENT_TARGET"

  #2a. Setup virtual Environment
  echo "Create virtual environment"
  $PYTHON3 -m venv $ANTENV --copies

  #2b. Activate virtual environment
  echo "Activate virtual environment"
  source $ANTENV/bin/activate

  #2c. Install dependencies
  pip install -r requirements.txt

  echo "pip install finished"

fi

#3. Default Configuration

if [ ! -f "$DEPLOYMENT_TARGET/config.py" ]; then
  echo "Configuration file config.py does not exist, please create."
fi

echo "Deployment Complete"
