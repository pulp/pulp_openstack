# to get pulp.devel and friends
# TODO: this may be avoidable in pip 1.5, via "subdirectory=" option
git clone https://github.com/pulp/pulp
git clone https://github.com/pulp/nectar.git
cd pulp
pip install ./devel
pip install ./server
pip install ./common
pip install ./client_lib
pip install ./bindings
cd ..
rm -rf pulp

pushd nectar
python setup.py install
popd
rm -rf nectar

#this should go in requirements.txt
pip install blinker
pip install flake8
pip install pymongo
pip install iniparse
pip install isodate
pip install celery
pip install okaara
pip install coverage
pip install python-glanceclient
pip install python-keystoneclient

sudo mkdir -p /etc/pulp
sudo cp fake-server.conf /etc/pulp/server.conf

./manage_setup_pys.sh install

