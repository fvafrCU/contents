modul=excerpts
output_directory=codes_doxygen
mkdir ${output_directory} || true
for src in $(find ${modul}/ -name "*py") 
do 
    if test "$file" != "__init__"; then  
        output=${output_directory}/$(basename $src)
        python3 -m doxypypy.doxypypy -a -c $src > $output
    fi 
done
