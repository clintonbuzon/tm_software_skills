# Thinking Machines Data Engineering Exam Solution

By: John Clinton Buzon

## Part 2: Soft(ware) skills

### Solutions

Cleaned database: `dailycheckins.db`

Solution website: http://ec2-13-229-64-171.ap-southeast-1.compute.amazonaws.com:8000/

### Details below

#### Decrypt the PGP-encrypted data

Decrypt data successful.

#### Clean the data and load it to your choice of database

I created the script `generate_sqlite_file.py` which does the cleaning and creation of database file. Main function which does the cleaning would be `clean_timestamp(timestamp)`.

I chose to use `sqlite` database for its simplicity and portability since the data to be inserted isn't that much. This is also the default database of choice for the web app to be created later(python django).

##### Cleaning

Upon checking the decrypted `dailycheckins.csv` file, I noticed that 2 things need to be cleaned.

1. Empty user
2. Dirty timestamps

For empty user values, I hard coded them to be `<blank>` so that they could be identified on the web app. 

For dirty timestamps, the following cleaning were done. Assumption: all timestamps on the file are in UTC.

1. Check if timestamp has provided timezone, if not append UTC tag at the end.
2. Check if timestamp contains russian date/month. If yes, we replace it with english version.
3. Convert the string to datetime object using dateutil.parser.
4. Return uniform formatted timestamp as string.

The cleaned timestamp would then be added on to a new row `cleaned_timestamp` to retain raw uncleaned column for future reference. The cleaned timestamp is also in string format due to the limitation of `sqlite` when storing timestamps. `sqlite` timestamp only stores till precision `YYYY-MM-DD HH:MM:SS.SSS` but the data provided contains precision `YYYY-MM-DD HH:MM:SS.SSSSSS`. Since the exam does not require timestamp calculations, I opted to store them as string with complete details avoiding loss of data. For future improvements, we can easily truncate this as sqlite timestamp.

##### Load it to your choice of database

The script `generate_sqlite_file.py` would generate a sqlite database file `dailycheckins.db`. You can use this to check if data looks good. The created db file is also copied to `mysite/db.sqlite3` to be used by the web app in the next step.

#### Create a web service that displays a per-user filtered view of the checkins

My solution for this is to create a python web app using `Django` python framework installed in an AWS EC2 instance (free-tier).

##### Django details

I already created the django website as  `mysite` folder. A lot of setup is done on django framework but majority of my code changes would be on the following scripts:

- `mysite/viewcheckins/views.py`
- `mysite/viewcheckins/models.py`
- `mysite/viewcheckins/templates/viewcheckins/index.html`

##### AWS EC2 details and setup

1. Create EC2 instace. [Documentation here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html).
2. Add [inbound](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html) rule to your EC2 security group. Inbound rule should allow Type: `Custom TCP Rule` Port: `8000` Source: `0.0.0.0/0`. This would be the connection to be used later.
3. [Connect to EC2 instance.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html)
4. Install all required items on EC2 by performing the following commands.

```bash
sudo yum update
sudo yum install python3
sudo yum install sqlite
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
pip install python-dateutil --user
pip install Django==2.1.* --user
```

5. Upload everyting in this repository to EC2. You may use your FTP tool of your choice (I used winscp).
6. Execute `chmod 775 generate_sqlite_file.py start_server_local.sh` to provide execute permissions for the scripts to be executed.
7. Execute `python3 ./generate_sqlite_file.py`. This cleans the data from `dailycheckins.csv` and creates `dailycheckins.db` & `mysite/db.sqlite3`
8. Execute `./start_server_local.sh` to enable website. Take note this is starting for development server.
9. On AWS EC2 page, look for your `Public DNS (IPv4)` and open that link to any browser with `:8000` at the end of the link. In my case, link is http://ec2-13-229-64-171.ap-southeast-1.compute.amazonaws.com:8000/

