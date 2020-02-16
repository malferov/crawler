# install dependencies
```
sudo yum -y install python36 python36-devel chromium
sudo pip3.6 install -r requirements
curl -O https://sites.google.com/a/chromium.org/chromedriver/home
unzip chromedriver.zip
sudo cp chromedriver /usr/local/bin/chromedriver
sudo chmod o+w /usr/lib/python3.6/site-packages/tldextract
```
# init
```
mkdir dat
echo '{"lock":0}' > dat/status.json
```
# run
```
# add -d flag for debug mode
./runner.py
```
