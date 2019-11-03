# Thinking Machines Data Engineering Exam Solution

By: John Clinton Buzon

## Part 2: Soft(ware) skills

### Decrypt the PGP-encrypted data

Decrypt data successful.

### Clean the data and load it to your choice of database

I created the script `generate_sqlite_file.py` which does the cleaning and creation of database file. Main function which does the cleaning would be `clean_timestamp(timestamp)`.

I chose to use `sqlite` database for its simplicity and portability since the data to be inserted isn't that much. This is also the default database of choice for the web app to be created later(python django).

#### Cleaning

Upon checking the decrypted `dailycheckins.csv` file, I noticed that 2 things need to be cleaned.

1. Empty user
2. Dirty timestamps

For empty user values, I hard coded them to be `<blank>` so that they could be identified on the web app. 

For dirty timestamps, the following cleaning were done. Assumption: all timestamps on the file are in UTC.

1. Check if timestamp has provided timezone, if not append UTC tag at the end.
2. Check if timestamp contains russian date/month. If yes, we replace it with english version.
3. Convert the string to datetime object using dateutil.parser.
4. Return uniform formatted timestamp as string.

The cleaned timestamp would then be added on to a new row `cleaned_timestamp` to retain raw uncleaned column for future reference. The cleaned timestamp is also in string format due to the limitation of `sqlite` when storing timestamps. `sqlite` timestamp only stores till precision `YYYY-MM-DD HH:MM:SS.SSS` but the data provided contains precision `YYYY-MM-DD HH:MM:SS.SSSSSS`. Since exam does not require timestamp calculations, I opted to store them as string with complete details avoiding loss of data. For future improvements, we can easily truncate this as sqlite timestamp.

#### Load it to your choice of database

The script `generate_sqlite_file.py` would generate a sqlite database file `dailycheckins.db`. You can use this to check if data looks good. The created db file is also copied to `mysite/db.sqlite3` to be used by the web app in the next step.

### Create a web service that displays a per-user filtered view of the checkins

My solution for this is to create a python web app using `Django` installed in an AWS EC2 instance (free-tier).




Bonus points for:

- Python
- A publicly accessible deployment of your service
- Documentation
- Tests
- Diagrams

We value:

- Communication
- Reproducibility
- Pragmatism
- Code hygiene

## Submission

Submit your code by sharing a __private repo__ to the following users:

- https://github.com/marksteve/
- https://github.com/florobarotjr/
- https://github.com/syk0saje/
- https://github.com/nhuber
