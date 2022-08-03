service strace-docker restart

docker run --rm -v "$PWD":/home/ -w /home/ mylowriter bash -c "sleep 1; lowriter --convert-to pdf *.doc;"
docker run --rm -v "$PWD":/home/ -w /home/ mylowriter bash -c "sleep 1; lowriter --convert-to pdf *.odt;"
docker run --rm -v "$PWD":/home/ -w /home/ mylowriter bash -c "sleep 1; lowriter --convert-to 'txt:Text (encoded):UTF8' *.doc;"

