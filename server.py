import asyncio
import crcmod
import binascii

crcFunction = crcmod.predefined.mkPredefinedCrcFun("crc-16")


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self._peer = transport.get_extra_info('peername')
        print('Connection from {}'.format(self._peer))
        self.transport = transport

    def data_received(self, data):
        print('recv: {}'.format(binascii.hexlify(data)))
        #two first bytes of crc always zero
        crc_remote = binascii.hexlify(data[-2:]).decode()
        crc_local = str(hex(crcFunction(data[8:-4])))[2:]
        print('CRC from msg: {}'.format(crc_remote))
        print('CRC calculated: {}'.format(crc_local))
        if crc_remote == crc_local:
            print('msg is ok =):')
            self.transport.write(b'ok')
        else:
            print('msg is bad =(:')
            self.transport.write(b'reject')
    def connection_lost(self, transport):
        print('Lost connection with {}'.format(self._peer))
        

async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
