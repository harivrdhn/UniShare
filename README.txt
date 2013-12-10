To run the server:

1. Extract the whole RAR file into Python27 folder.
2. Change the last line of test.py as needed:

run(host='localhost', port=8080)

3. Make sure your mongo connection and the connection url in test.py are the same.

connection = Connection('localhost', 27017)

4. Run mongod.exe
5. Run test.py
6. Open Browser to "http://localhost:8080/index"
7. Play Around!!