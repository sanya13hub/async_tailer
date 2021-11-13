import os
import sys
import asyncio

# async Modified Source - https://github.com/kasun/python-tail


class Tail(object):
    ''' Represents a tail command. '''

    def __init__(self, tailed_file):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                tailed_file - File to be followed. '''

        self.check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write

    async def follow(self, s=1):
        ''' Do a tail follow. If a callback function is registered it is called with every new line.
        Else printed to standard out.

        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1. '''

        with open(self.tailed_file, 'rb') as file_:

            # try print last few lines of file
            cnt = 0
            file_.seek(0, 2)

            try:    # catch OSError in case of cnt > lines count
                while cnt != 10:
                    if file_.read(1) == b'\n':
                        cnt += 1
                    file_.seek(-2, os.SEEK_CUR)
            except OSError:
                file_.seek(0)

            lines = file_.readlines()
            for line in lines:
                yield line.decode("utf-8")

            # Go to the end of file
            file_.seek(0, 2)
            while True:
                curr_position = file_.tell()
                line = file_.readline().decode("utf-8")
                if not line:
                    file_.seek(curr_position)
                    await asyncio.sleep(s)
                else:
                    #self.callback(line)
                    yield line

    def register_callback(self, func):
        ''' Overrides default callback function to provided function. '''
        self.callback = func

    def check_file_validity(self, file_):
        ''' Check whether the a given file exists, readable and is a file '''
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))


class TailError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


if __name__ == '__main__':
    t = Tail('../test.txt')
    t.register_callback(print)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(t.follow())
