#!/usr/bin/env python

import iio

def main():
    contexts = iio.scan_contexts()
    if len(contexts) > 1:
        print('Multiple contexts found. Please select one using --uri:')
        for index, each in enumerate(contexts):
            print('\t%d: %s [%s]' % (index, contexts[each], each))
        return

    uri = next(iter(contexts), None)
        
    if uri is not None:

        ctx = iio.Context(uri)
        
        print(ctx.xml)
    else:
        print('No available contexts')

if __name__ == '__main__':
	main()
