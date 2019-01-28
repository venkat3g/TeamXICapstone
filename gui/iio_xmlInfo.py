#!/usr/bin/env python

import iio


def getIIOContext():
    ctx = iio.XMLContext("pluto.xml")

    return ctx


def main():
        
    ctx = iio.XMLContext('pluto.xml')

    print('IIO context at XML: pluto.xml')

    print('IIO context created: ' + ctx.name)
    print('Backend version: %u.%u (git tag: %s)' % ctx.version)
    print('Backend description string: ' + ctx.description)

    if len(ctx.attrs) > 0:
        print('IIO context has %u attributes:' % len(ctx.attrs))
    for attr, value in ctx.attrs.items():
        print('\t' + attr + ': ' + value)

    print('IIO context has %u devices:' % len(ctx.devices))

    for dev in ctx.devices:
        print('\t' + dev.id + ': ' + dev.name)

    if dev is iio.Trigger:
        print('Found trigger! Rate: %u Hz' % dev.frequency)

    print('\t\t%u channels found:' % len(dev.channels))

    for chn in dev.channels:
        print('\t\t\t%s: %s (%s)' % (chn.id, chn.name or "", 'output' if chn.output else 'input'))

        if len(chn.attrs) != 0:
            print('\t\t\t%u channel-specific attributes found:' % len(chn.attrs))

        for attr in chn.attrs:
            try:
                print('\t\t\t\t' + attr + ', value: ' + chn.attrs[attr].value)
            except OSError as e:
                print('Unable to read ' + attr + ': ' + e.strerror)

    if len(dev.attrs) != 0:
        print('\t\t%u device-specific attributes found:' % len(dev.attrs))

    for attr in dev.attrs:
        try:
            print('\t\t\t' + attr + ', value: ' + dev.attrs[attr].value)
        except OSError as e:
            print('Unable to read ' + attr + ': ' + e.strerror)

    if len(dev.debug_attrs) != 0:
        print('\t\t%u debug attributes found:' % len(dev.debug_attrs))

    for attr in dev.debug_attrs:
        try:
            print('\t\t\t' + attr + ', value: ' + dev.debug_attrs[attr].value)
        except OSError as e:
            print('Unable to read ' + attr + ': ' + e.strerror)
    
if __name__ == '__main__':
	main()
