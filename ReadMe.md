# ReadMe


## Run code locally
In Terminal:

1. Active your virtual environment:

       `source env/bin/activate`

2. Run web server

       `python manage.py runserver`

3. Deactivate virtual environment:

       `deactivate`


## Upload to server


1. SSH to server

       `ssh `

2. Locate VCGtool folder

       `cd Desktop/VCGtool/`

3. allowed port (Not need every time)

       `sudo ufw allow 8070`

4. Active your virtual environment:

       `source env/bin/activate`

5. Run web server

       `nohup python manage.py runserver  http:// &`

6. Click Enter key

## Shutdown web server
1. Kill port 

       `sudo fuser -k 8070/tcp`

2. Deactivate virtual environment:

       `deactivate`

## Update conclusion
- 1.4.0 
  - Update the uploaded file on the frontend
  - Upload the file to the backend directly and save to `data`

- 1.3.0 
  - Add data support for a special situation of PhilipsECG FDATemplate v2.6 
  - Trying to change the other methord to read data

- 1.2.0 
  - Add data support for PhilipsECG FDATemplate

- 1.1.0 
  - Add data support for NL ECGToolkit

- 1.0.0 
  - Basic function completely finish,supported PhilipsECG