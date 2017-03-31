#!/bin/sh
git_tags=$(git log --tags --simplify-by-decoration --pretty="format:%d")
last_version=$(echo $git_tags| head -1 | cut -f2 -d" " | sed -e 's/[,)]$//')
version=$(grep version setup.py | cut -f2 -d"'")
if test $last_version != $version; 
then
    git tag -a $version
fi
