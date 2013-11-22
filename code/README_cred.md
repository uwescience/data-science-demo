Configuring credentials
=======================

It is not safe to put credentials up on github. Instead, do the following:

1. Create the file `credentials.cfg` by copying the sample config file:

        cp credentials.cfg.sample credentials.cfg

2. Edit `credentials.cfg` to include your access token key and secret.

3. When you need to read the key and secret in your code, use the supplied `cred` module to parse the config file and extract the values.

Finally, DO NOT check `credentials.cfg` into git!
