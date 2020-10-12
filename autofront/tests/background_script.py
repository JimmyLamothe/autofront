import time

with open('logger.txt', 'w') as logger:
    time.sleep(3)
    logger.write('time elapsed')
