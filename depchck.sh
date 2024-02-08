#!/bin/bash

OWASPDC_DIRECTORY=$HOME/OWASP-Dependency-Check
DATA_DIRECTORY="$OWASPDC_DIRECTORY/data"
#REPORT_DIRECTORY="$OWASPDC_DIRECTORY/reports"
REPORT DIRECTORY="$(pwd)/security/reports"

PROJECT_NAME=${1:-Unknown}

USER_PARAMS=$@
if [ ! -d "$DATA_DIRECTORY" ]; then
fi
echo "Initially creating persistent directories" mkdir -p "$DATA_DIRECTORY"
chmod R 755 "$DATA_DIRECTORY"
if [ ! -d "$REPORT DIRECTORY" ]; 
then mkdir -p "$REPORT_DIRECTORY"

fi

# Make sure we are using the latest version 
docker pull owasp/dependency-check

docker run --rm --user $(id -u jenkins): $(id -g jenkins) \ 
--volume $(pwd): /src\
--volume "$DATA_DIRECTORY":/usr/share/dependency-check/data\ 
--volume "$REPORT_DIRECTORY":/report \ owasp/dependency-check \
--scan /src\
--exclude .scannerwork --exclude .git --exclude .npm \
--disableNodeAuditCache --nodeAuditSkip DevDependencies \
--format HTML --format JSON
--project "$PROJECT_NAME" \
--out /report \
--failOnCVSS 7 \
$USER_PARAMS
