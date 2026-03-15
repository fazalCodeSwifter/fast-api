from prisma import Prisma

class PrismaConnection:
    def __init__(self):
        self.prisma = Prisma()

    async def connect(self):
        try:
            await self.prisma.connect()
            print('implement prisma connections')
        except Exception as error:
            raise error
    def db(self):
        return self.prisma
    
    async def disconnect(self):
        try:
            await self.prisma.disconnect()
        except Exception as error:
            raise error
        
db = PrismaConnection()