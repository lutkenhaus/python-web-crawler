import time


def sleep(segundos):
    if segundos > 1:
        print("\nEsperando " + str(segundos) + " segundos...")
    else:
        print("\nEsperando " + str(segundos) + " segundo...")
    time.sleep(segundos)
