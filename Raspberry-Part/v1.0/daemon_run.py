import os
import sys
import time
from random import randint

from daemon import Daemon
from param import DAEMON_SLEEP_TIME, LOG_PATH

class MyTestDaemon(Daemon):
    steps = 6000

    def run(self):
        sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        while True:
            sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
            sys.stdout.flush()

            filelist = [f for f in os.listdir(self.filepath) if os.path.isfile(os.path.join(self.filepath, f))]
            filelist.sort()

            # if len(filelist) >= 10:
            #     fn = os.path.join(self.filepath, filelist[0])
            #     os.remove(fn)
            #     sys.stdout.write('Delete log file: ' + fn + '\n')
            #     sys.stdout.flush()

            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            fn = self.filepath + str(localtime) + ".log"
            fo = open(fn, "w+")
            print("Create file, filename is: ", fo.name)
            
            band_time = str(localtime) + "#"

            self.steps = self.steps +randint(0, 100)
            steps = str(self.steps) + "#"
            
            heart_rate = str(randint(60, 80)) + "#"
            
            str_in = band_time + steps + heart_rate
            fo.write(str_in)
            fo.close()

            sys.stdout.write('Create log file: '+fn+'\n')
            sys.stdout.flush()

            time.sleep(DAEMON_SLEEP_TIME)


if __name__ == '__main__':
    PIDFILE = '/tmp/daemon-example.pid'
    LOG = '/tmp/daemon-example.log'
    daemon = MyTestDaemon(pidfile=PIDFILE, stdout=LOG, stderr=LOG, filepath=LOG_PATH)

    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if 'start' == sys.argv[1]:
        daemon.start()
    elif 'stop' == sys.argv[1]:
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        daemon.restart()
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
