#!/usr/bin/env bash
set -e
DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$DIR"

SCREEN_SESSION=mlflow
export MLFLOW_AUTH_CONFIG_PATH="${DIR}/auth_config.ini"

export OPENBLAS_NUM_THREADS=1

send_to_screen(){
    # Replace occurrences of $ with \$ to prevent variable substitution:
    string="${1//$/\\$}"
    screen -xr $SCREEN_SESSION -X stuff "$string\r"
}

# start a detached screen session
screen -dmS $SCREEN_SESSION

ulimit -Sv unlimited

send_to_screen "date"
send_to_screen "echo \$PWD"
send_to_screen "echo \$MLFLOW_AUTH_CONFIG_PATH"
send_to_screen "source /hpc/uwork/fe1ai/VenvPy3.11/bin/activate"
send_to_screen "mlflow server --app-name basic-auth --backend-store-uri \"sqlite:///${DIR}/mlflow.db\" --artifacts-destination \"${DIR}/mlflow-artifacts\" --workers 10 --host 0.0.0.0 --port 5000"
echo "Started mlflow in a detached screen session."
echo "Enter \`screen -xr $SCREEN_SESSION\` to attach."
echo "Then press 'ctrl+a d' to detach."
