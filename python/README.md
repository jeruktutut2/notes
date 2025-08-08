# PYTHON

## note
    cek installed python
    which python3
    type -a python3
    biasanya hasilnya
    python3 is /usr/local/bin/python3
    python3 is /usr/bin/python3

    jika ls -l /usr/local/bin/python3 dan hasilnya kira-kira lrwxr-xr-x  1 user  admin  37 Jul 27 14:13 /usr/local/bin/python3 -> ../Cellar/python@3.10/3.10.13/bin/python3 berarti itu symlink ke Homebrew.

    brew list python
    brew install python@3.10 install python3.10, untuk kebutuhan open-whisper
    buat symlink
    ln -sf /usr/local/opt/python@3.10/bin/python3 /usr/local/bin/python3
    ln -sf /usr/local/opt/python@3.10/bin/pip3 /usr/local/bin/pip3
    brew --prefix python@3.10 melihat path-nya yang benar