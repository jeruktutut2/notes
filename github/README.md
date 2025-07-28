# GITHUB

## if got error 
    error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400
    send-pack: unexpected disconnect while reading sideband packet
    Writing objects: 100% (97/97), 2.83 MiB | 3.60 MiB/s, done.
    Total 97 (delta 26), reused 0 (delta 0), pack-reused 0
    fatal: the remote end hung up unexpectedly

1. Files (can be) too big 

Github has limit in term of file size, please check it before pushing it:  

    git lfs track "*.ext"

or make sure there is no file with big size using:  

    git count-objects -vH

2. Connection problem  

try to push again with verbose opstion:  

    GIT_CURL_VERBOSE=1 git push origin main

3. Problem with authentication  

if using Https, make sure the token still valid (because github no longer support username and password authentication)  

    gh auth login

or if using SSH, make sure SSH key is correct:  

    ssh -T git@github.com

4. Problem with HTP Configuration in Git  

Try to add these configurations to increase the limit buffer:  

    git config --global http.postBuffer 524288000
    git config --global http.lowSpeedLimit 0
    git config --global http.lowSpeedTime 999999

5. Push too many files in one push  

try to push in a smaller batch  

    git push origin main --force --no-thin