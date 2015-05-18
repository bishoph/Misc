#!/bin/bash

# Simple config file check tool for Open-Xchange
# usage ./analyse_config.sh path_to_config_reference_file

# CONFIG OPTIONS

# output and debugging
# 0 = normal report
# 2 = more details whats going on
# 5 = all we have
DEBUG=0

# 0 = check config
# 1 = read current config and can be used with DEBUG=0 to create reference file (./analyse_config.sh > OX_7_6_2.STANDARDS)
CREATE_OUTPUT=0

# conf file directory
TARGET_DIR=/opt/open-xchange/etc/

#######################################

# do not touch
CHECK_CONFIG=()
STANDARDS=()

#######################################

function read_property_file() {
 local file=$1
 local i=${#file}
 i=$i+1
 local diff=()
 found=0
 if [[ $DEBUG > 1 ]]; then
  echo "reading $file"
 fi
 while read line
  do
    #line="$(echo -e "${line}" | sed -e 's/^[[:space:]]*//')"
    if  [[ $line == \#* ]] || [[ $line == "" ]]; then
     if [[ $DEBUG > 3  ]]; then
      echo "ignoring $line"
     fi
    else
     if [[ $CREATE_OUTPUT -eq 1 ]]; then
      echo "$file:$line"
     else
      check="$file:$line"
      oldIFS="$IFS"
      IFS="="
      read -a name_value <<< "$check"
      exists=0
      for var in "${STANDARDS[@]}"
       do
        read -a name_value_s <<< "$var"
        if [[ "${name_value[0]}" == "${name_value_s[0]}" ]]; then
         exists=1
         if [[ "${name_value[1]}" != "${name_value_s[1]}" ]]; then
          diff+=("<<< $line")
	  diff+=(">>> ${var:$i}")
          found=1
         fi
        fi
      done
      IFS="$oldIFS"
      if [[ $exists -eq 0 ]]; then
       diff+=("--- $line")
       found=1
      fi
     fi
    fi
 done < $1
 if [[ $found -eq 1 ]]; then
  echo "@ $file"
  for changes in "${diff[@]}"
   do
    echo "$changes"
  done
 fi
}

#######################################

if [[ $CREATE_OUTPUT -eq 0 ]]; then
 if [[ -e $1 ]]; then
  if [[ $DEBUG > 1 ]]; then
   echo "reading standard config files"
  fi
  while read line
   do
    STANDARDS+=("$line")
  done < "$1"
 else 
  echo "reference file not found!"
  exit 1
 fi
fi

for content in $(find $TARGET_DIR -name '*.properties');
 do
  CHECK_CONFIG+=("$content")
done

for file in "${CHECK_CONFIG[@]}"
 do
  if [[ $DEBUG > 1 ]]; then
   echo "processing $file"
  fi
  if  [[ $file =~ ".properties" ]]; then
   read_property_file $file
  fi
done 
