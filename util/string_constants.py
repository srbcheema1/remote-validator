vcf_path = "./bin/vcf_validator"

debug = 0

if (debug == 1):
    vcf_path = "./bin/demo"
if (debug == 2):
    vcf_path = "./bin/even"

end_of_report = "According to the VCF specification, the input file is valid"
end_of_report_neg = "According to the VCF specification, the input file is not valid"

default_ip = 'localhost'
default_port = 12321

connection_timeout = 10
