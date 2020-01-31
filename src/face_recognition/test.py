# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from ytDownloader import ytDownloader
from threading import Thread


import gc

from concurrent.futures import ThreadPoolExecutor

gc.set_debug(gc.DEBUG_UNCOLLECTABLE)

def callback(d):
    print('CALLBACK: video finished', d['filename'])

#original
#test = ['https://www.youtube.com/watch?v=nlg_tQ3aWxE']

#2020
test = ['https://www.youtube.com/watch?v=ogC1XQjBUfE']

ytd = ytDownloader(callback)

executor = ThreadPoolExecutor(max_workers=24)
executor.map(ytd.download, test, timeout=None)





#ytd.download('https://www.youtube.com/watch?v=nlg_tQ3aWxE')

#threads = [Thread(target=ytd.download, args=[vid]) for vid in videos]

#for thread in threads:
#    thread.start()

#for thread in threads:
#    thread.join()
