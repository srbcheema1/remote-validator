# Remote-Validator

A network interface to run vcf-validator as a service. To allow users to validate their own remote files, or even a dynamically generated VCF stream.

to validate the file:

    1. start the server
    2. run client with input the vcf stream from stdin you may use < operator

```
    ./client.py < vcf-file
```

