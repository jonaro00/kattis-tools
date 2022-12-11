#!/bin/bash

# sudo apt install entr # inotify-tools
# https://github.com/eradman/entr#docker-and-wsl
# Can be upgraded when https://github.com/microsoft/WSL/issues/4739 is resolved...

if [ -z "$1" ]; then
    echo "Provide a file to test."
    exit 1
fi

if [ "$1" != "--run" ]; then
    if [ ! -f "$1" ]; then
        echo "$1 not found"
        exit 1
    fi
    #ls *.py | env ENTR_INOTIFY_WORKAROUND=1 entr -r /bin/bash pyrunner.sh --run /_
    #ls *.py | entr -r /bin/bash pyrunner.sh --run /_
    echo "$1" | entr -r /bin/bash pyrunner.sh --run /_
    exit
fi

# TEST RUNNER
code=$2
echo
echo "Running tests for $code :"
#fn=$(echo $code | cut -d'.' -f1)
fn=$(basename $code .py)
testdir="tests"
target="$testdir/$fn"
zip="$fn.zip"
if [ ! -d "$target" ]; then
    if [ ! -f "$zip" ]; then
        echo "No zip file found: $zip"
        exit 1
    fi
    mkdir -p "$testdir"
    unzip "$zip" -d "$target"
fi
for test in $(find "$target" -name '*.in'); do
    echo -n "Testing $test... "
    ans=$(cat "$(echo $test | cut -d'.' -f1).ans")
    out=$(timeout 5 python3 "$code" < $test)
    if [ "$out" = "$ans" ]; then
        echo "✅"
    else
        echo "❌"
        echo "---- Input:     ----"
        cat "$test"
        echo "---- Expected:  ----"
        echo "$ans"
        echo "---- Got:       ----"
        echo "$out"
    fi
done
