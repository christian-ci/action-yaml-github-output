#!/bin/sh -l

echo "Listing /github/workspace/"
ls -la /github/workspace/
ls -la /
ls -la /github/

python /main_action.py \
--file_path "$FILE_PATH" \
--format_type "$FORMAT_TYPE" \
--main_key "$MAIN_KEY" \
--sub_key "$SUB_KEY" \
--primary_key "$PRIMARY_KEY" \
--primary_value "$PRIMARY_VALUE"