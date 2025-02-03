# HTTP2-Conformance-Tests
 
python -m venv .venv

pip install -r requirements.txt

in http_test.py, change the following variables based on your needs:
CLIENT_WORKER
CLIENT_PORT
SERVER_WORKER
SERVER_IP
SERVER_PORT
MASTER

The following command will run all test cases (test_cases.json) sequentially and log the results in a txt file:
python http_test.py
