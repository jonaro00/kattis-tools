#!/bin/bash

# Usage: ./rustrunner.sh a
# Place 'a.zip' containing testcases in project root

# cargo install cargo-watch

if [ -z "$1" ]; then
    echo "Provide a binary name to test."
    exit 1
fi

if [ "$1" != "--run" ]; then
    cargo watch -qc -i tests -s "/bin/bash rustrunner.sh --run $1"
    exit
fi


# TEST RUNNER
code=$2
if ! cargo build --bin $code; then
    exit
fi
echo
echo "Running tests for $code.rs:"
testdir="tests"
target="$testdir/$code"
zip="$code.zip"
if [ ! -d "$target" ]; then
    if [ ! -f "$zip" ]; then
        echo "No zip file found: $zip"
        exit 1
    fi
    mkdir -p "$testdir"
    unzip "$zip" -d "$target"
fi
for test in $(find "$target" -name '*.in' | sort); do
    echo -n "Testing $test... "
    ans=$(cat "$(echo $test | cut -d'.' -f1).ans")
    out=$(timeout 5 cargo run -q --bin "$code" < $test)
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
