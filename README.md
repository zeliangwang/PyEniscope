## An example Python script for retrieving Eniscope metering data using Eniscope Core API

To use Eniscope Core API, type your `<API Key>`, `<Username>` and `<Password>` in the example scripy:
```python
# API header
headers = {'X-Eniscope-API': "<API Key>", 
            'Accept': "/",
            'Host': "core.eniscope.com"}
# API usename and password
auth = HTTPBasicAuth('<Username>', '<Password>')  
```

Note that the script has been tested working under `Python 3.6`. For the retrieved data samples, please see the [results/](results/) directory.

For further details, please refer to [ENISCOPE API Documents](https://help.bestsupportdesk.com/en/support/tickets/archived/232597)


