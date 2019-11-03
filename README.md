# Thinking Machines Data Engineering Exam Solution

By: John Clinton Buzon

## Part 2: Soft(ware) skills

### Decrypt the PGP-encrypted data

Decrypt data successful.

### Clean the data and load it to your choice of database

Upon checking the decrypted `dailycheckins.csv` file, I noticed that 2 things need to be cleaned.

1. Empty user
2. Dirty timestamps

I created the script `generate_sqlite_file.py` which does the cleaning and creation of database file. Main function which does the cleaning would be `clean_timestamp(timestamp)`

I chose to use `sqlite` database for its simplicity and portability since the data to be inserted isn't that much. This is also the default database of choice for the web app to be created later(python django).

### Create a web service that displays a per-user filtered view of the checkins

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
