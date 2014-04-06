#!/usr/bin/env python

import argparse
import csv
import json

__author__ = 'Martijn Reening'
__version__ = '0.0.1'

# Warning: hack-ish code ahead. It just werks(TM)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert CSV files to JSON')
    parser.add_argument('input')
    parser.add_argument('-p', '--pretty', action='store_true', help='Pretty print JSON')
    parser.add_argument('-o', '--output', help='Output to a file')
    args = parser.parse_args()

    with open(args.input, 'r') as csvfile:
        reader = csv.reader(csvfile)

        output = []

        items = list(reader)
        headers = items[0]
        for item in items[1:]:
            # Some hackery to get the proper data types
            for i in range(len(item)):
                field = item[i]
                new = field

                # Do nothing (infinity bug)
                if field.lower() in ['-infinity', 'infinity']:
                    continue
    

                if field.lower() in ['true', 'yes']:
                    item[i] = True
                    continue

                if field.lower() in ['false', 'no']:
                    item[i] = False
                    continue

                try:
                    item[i] = int(field)
                    continue
                except:
                    pass
    
                try:
                    item[i] = float(field)
                    continue
                except:
                    pass
    
            output.append(dict(zip(headers, item)))

        if args.pretty:
            output = json.dumps(output[:-1], indent=4, separators=(',', ': '))
        else:
            output = json.dumps(output[:-1])

        if args.output:
            with open(args.output, 'w') as fh:
                fh.write(output)
        else:
            print output

