modul=excerpts
mkdir doxy_codes || true
for src in $(find ${modul}/ -name "*py") 
do 
    if test "$file" != "__init__"; then  
        output=doxy_codes/$(basename $src)
        python3 -m doxypypy.doxypypy -a -c $src > $output
    fi 
done
