import proxyfinder

bgproxy = []
if proxyfinder.find_bg_proxy(bgproxy):
    print('bg proxy details: ip: {0} port: {1} type: {2} sll: {3}'.format(bgproxy[0][0], bgproxy[0][1], bgproxy[0][2], bgproxy[0][3]))
else:
    print('Cannot find working proxy.')

