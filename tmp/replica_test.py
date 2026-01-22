import numpy as np
import statistics
from statistics import geometric_mean

def calc_chat(x, y):
    out=0
    for i in range(0, len(x)):
        xx=x[i]
        yy=y[i]
        out+=(xx/yy)
    out=out/len(x)
    return out


def calc_true(x, y):
    values = []
    for bck in y:
        for sig in x:
            values.append(sig / bck)
    out = statistics.mean(values)
    return out


np.random.seed(1277653)
bck_loc=17
sig_loc=13
diff=sig_loc/bck_loc
print(diff)
no_of_true=0
no_of_iter=10000
diff_trues=[]
diff_falses=[]
diff_geos=[]
diff_chat=[]

for n in range(0,no_of_iter):
    bck_no=10
    sig_no=10
    background=np.random.normal(loc=bck_loc, scale=3.0, size=bck_no)
    signal=np.random.normal(loc=sig_loc, scale=2.0, size=sig_no)

    false_diff=statistics.mean(signal) / statistics.mean(background)
    chat_diff=calc_chat(signal, background)

    geo_sig=geometric_mean(signal)
    geo_bck=geometric_mean(background)
    geo_diff=geo_sig/geo_bck

    true_diff =calc_true(signal, background)
    s=str(false_diff) + '; ' + str(true_diff)

    x = (diff-false_diff)**2
    y = (diff - true_diff) ** 2
    z = (diff-geo_diff)**2
    v = (diff-chat_diff)**2
    # x = (diff - false_diff)
    # y = (diff - true_diff)
    # z = (diff - geo_diff)
    # v = (diff - chat_diff)
    diff_falses.append(x ** 0.5)
    diff_trues.append(y ** 0.5)
    diff_geos.append(z ** 0.5)
    diff_chat.append(v**0.5)


    #print(s)
    if x==y:
        print('???')
    elif x<y:
        pass
        #print('False!')
    else:
        no_of_true+=1
        #print('True!')

print('no of true:' + str(no_of_true/no_of_iter))
print ('trues_offtarget: '+ str(statistics.mean(diff_trues)))
print ('falses_offtarget: '+ str(statistics.mean(diff_falses)))
print ('geos_offtarget: '+ str(statistics.mean(diff_geos)))
print ('chat_offtarget: '+ str(statistics.mean(diff_chat)))



