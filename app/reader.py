import asyncio

PERIOD = 0.5


def endless():
    num = 0
    while True:
        yield num
        num += 1

a = endless()


async def readline():
    while True:
        num = next(a)
        return num



'''
@asyncio.coroutine
def readline():
    with open('test.txt') as f:
        while True:
            data = f.readline()

            if data:
                return data
            yield from asyncio.sleep(PERIOD)'''

