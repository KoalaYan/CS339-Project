import os
import sys
import time
from random import randint

from daemon import Daemon

class MyTestDaemon(Daemon):
    def run(self):
        sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        while True:
            sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
            sys.stdout.flush()
            filelist = [f for f in os.listdir(self.filepath) if os.path.isfile(os.path.join(self.filepath, f))]
            filenum = randint(0, len(filelist)-1)
            fn = os.path.join(self.filepath, filelist[filenum])
            fo = open(fn,'r')
            all_txt = fo.read()
            fo.close()

            fn = os.path.splitext(filelist[filenum])[0] + '_copy' + os.path.splitext(filelist[filenum])[1]
            fn = os.path.join(self.filepath, fn)
            fo = open(fn, "w+")
            str_in = 'This is the copy file.\n' + all_txt
            fo.write(str_in)
            fo.close()
            
            sys.stdout.write('Copy file: '+fn+'\n')
            sys.stdout.flush()

            time.sleep(5)

if __name__ == '__main__':
    PIDFILE = '/tmp/daemon-example.pid'
    LOG = '/tmp/daemon-example.log'
    FILEPATH = '/usr/test/'
    daemon = MyTestDaemon(pidfile=PIDFILE, stdout=LOG, stderr=LOG, filepath=FILEPATH)

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