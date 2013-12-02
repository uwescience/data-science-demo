import ConfigParser

import os
DEFAULT_FILE = os.path.join(os.path.dirname(__file__), 'credentials.cfg')

def read_credentials(filename=DEFAULT_FILE):
    config = ConfigParser.ConfigParser()
    config.read(filename)
    return dict(config.items('Twitter'))

if __name__ == "__main__":
    test_file = os.path.join(os.path.dirname(__file__), \
            'credentials.cfg.sample')
    print read_credentials(test_file)

