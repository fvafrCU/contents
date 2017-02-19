modul=excerpts
for src in $(find ${modul}/ -name "*py") 
do 
    file=$(basename $src .py) 
    if test "$file" != "__init__"; then  
        python3 -m pydoc -w ${modul}.$file
    fi 
done
python3 -m pydoc -w ${modul}
mv ${modul}*.html docs/
