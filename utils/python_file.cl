cat tests/files/some_file.txt| sed -e "s/^#/# #/" \
    -e "/% All About Me/i\
    #!/usr/bin/env python3" \
    -e "/plain comment./a \
    print('hello, world')" > tests/files/some_code.py
