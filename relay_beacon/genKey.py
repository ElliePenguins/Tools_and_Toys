#!/bin/python3

# Gen a one time password key and output it to the console.
# put this key in the client & server python script.
# they must be the same to work.

import pyotp

print(pyotp.random_base32());
