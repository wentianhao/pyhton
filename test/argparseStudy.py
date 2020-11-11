import argparse

parser = argparse.ArgumentParser(description='what')

parser.add_argument('-n','--name',default='WEN')
parser.add_argument('-y','--year',default='20')
args = parser.parse_args()
print(args)
name  = args.name
year = args.year
print('Hello {} {}'.format(name,year))