#!/usr/bin/bash

option="$1"
env_path="$3"

activate() {
    env_dir="${env_path:-ocr-env}"
    env_loc="$env_dir/bin/activate"

    [ ! -f "$env_loc" ] && {
        echo "Missing virtual environment: $env_loc"
        exit 1
    }
    # shellcheck disable=SC1090
    source "$env_loc"
}

if [[ $option = "--run" ]]; then
    activate

    if [ -z "$2" ]; then
        main_file="app.py"

        [ ! -f $main_file ] && {
            echo "Missing main file: $main_file"
            exit 1
        }
        python $main_file
    else
        python "$2"
    fi
    exit 0
elif [[ $option = "--install" ]]; then
    activate
    
    if [ -z "$2" ]; then
        req_file="requirements.txt"

        [ ! -f $req_file ] && {
            echo "Missing file: $req_file"
            exit 1
        }
        pip install -r $req_file --timeout 1000 --retries 10
    else
        pip install "$2" --timeout 1000 --retries 10
    fi
    exit 0
elif [[ $option = "--activate" ]]; then
    activate

    echo "Virtual environment successfully activated"
    exit 0
else
    echo "Unrecognized option '$option'"
    exit 1
fi