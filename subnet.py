class SubnetV4():
    '''a representation of a subnetwork using IPv4'''
    MAX_BITS = 32
    ADDR_DIVISIONS = 4
    ADDR_SEP = '.'
    MASK_SEP = '/'
    
    def __init__(self, net_addr: int = 0, mask: int = 32):
        if not isinstance(net_addr, int):
            raise TypeError('\'net_addr\' must be an integer, not a ' + str(type(net_addr)))
        if not isinstance(mask, int):
            raise TypeError('\'mask\' must be an integer, not a ' + str(type(mask)))
        if net_addr >= 2 ** SubnetV4.MAX_BITS:
            raise ValueError('\'net_addr\' must be less than ' + str(2 ** SubnetV4.MAX_BITS) + ', not ' + str(part))
        if net_addr < 0:
            raise ValueError('\'net_addr\' must ge greater than or equal to 0, not ' +str(net_addr))
        if mask > SubnetV4.MAX_BITS:
            raise ValueError('\'mask\' must be less than ' + str(SubnetV4.MAX_BITS) + ', not ' + str(mask))
        self.net_addr = net_addr
        self.mask = mask
        return

    def __eq__(self, other) -> bool:
        if isinstance(other, SubnetV4):
            return self.net_addr == other.net_addr and self.mask == other.mask
        else:
            return False

    def __repr__(self) -> str:
        return 'SubnetV4(' + repr(self.net_addr) + ',' + repr(self.mask) + ')'

    def __str__(self) -> str:
        addr_parts = self.intToAddr(self.net_addr)
        string = ''
        i = 0
        while i < len(addr_parts):
            string += str(addr_parts[i]) + SubnetV4.ADDR_SEP
            i += 1
        return string[0:-len(SubnetV4.ADDR_SEP)] + SubnetV4.MASK_SEP + str(self.mask)

    def strToSubnetV4(self, x: str):
        '''convert a string into a SubnetV4'''
        if not isinstance(x, str):
            raise TypeError('\'x\' must be a string, not a ' + str(type(x)))
        if x.count(SubnetV4.MASK_SEP) != 1:
            raise ValueError('\'x\' must contain exactly one ' + str(SubnetV4.MASK_SEP) + ', not ' + str(x.count(SubnetV4.MASK_SEP)))
        mask = int(x.partition(SubnetV4.MASK_SEP)[2])
        net_addr = self.addrToInt(self.strToAddr(x.partition(SubnetV4.MASK_SEP)[0]))
        return SubnetV4(net_addr, mask)

    def strToAddr(self, x: str) -> tuple:
        '''convert a string into a suitable representation of an address'''
        if not isinstance(x, str):
            raise TypeError('\'x\' must be a string, not a ' + str(type(x)))
        if x.count(SubnetV4.ADDR_SEP) != SubnetV4.ADDR_DIVISIONS - 1:
            raise ValueError('\'x\' must contain exactly ' + str(SubnetV4.ADDR_DIVISIONS - 1) + repr(SubnetV4.ADDR_SEP) + ', not ' + str(x.count(SubnetV4.ADDR_SEP)))
        addr_parts = x.split(SubnetV4.ADDR_SEP)
        addr = []
        for part in addr_parts:
            if int(part) > 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS):
                raise ValueError('\'x\' must contain integers less than ' + str(2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS)) + ', not ' + part)
            addr.append(int(part))
        return tuple(addr)

    def intToAddr(self, x: int) -> tuple:
        '''convert an integer into a suitable representation of an address'''
        if not isinstance(x, int):
            raise TypeError('\'x\' must be an integer, not a ' + str(type(x)))
        if x < 0:
            raise ValueError('\'x\' must be greater than or equal to 0, not ' + str(x))
        if x >= 2 ** SubnetV4.MAX_BITS:
            raise ValueError('\'x\' must be lesser than ' + str(2 ** SubnetV4.MAX_BITS) + ', not ' + str(x))
        base = 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS)
        i = SubnetV4.ADDR_DIVISIONS - 1
        addr = []
        while i >= 0:
            num = x // (base ** i)
            addr.append(num)
            x -= num * base ** i
            i -= 1
        return tuple(addr)

    def addrToInt(self, x: tuple) -> int:
        '''convert a tuple address to an integer'''
        if not isinstance(x, tuple):
            raise TypeError('\'x\' must be a tuple, not a ' + str(type(x)))
        if len(x) != SubnetV4.ADDR_DIVISIONS:
            raise IndexError('\'x\' must be ' + str(SubnetV4.ADDR_DIVISIONS) + ' long, not ' + str(len(x)))
        x = list(x)
        x.reverse()
        base = 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS)
        i = 0
        addr = 0
        while i < SubnetV4.ADDR_DIVISIONS:
            if not isinstance(x[i], int):
                raise TypeError('every element of \'x\' must be an integer, not a ' + str(type(x[i])))
            if x[i] >= base:
                raise ValueError('every element of \'x\' must be less than ' + str(base) + ', not ' + str(x[i]))
            if x[i] < 0:
                raise ValueError('every element of \'x\' must be greater than 0, not ' + str(x[i]))
            num = x[i] * base ** i
            addr += num
            i += 1
        return addr

    def lastAddr(self) -> int:
        '''the last address in this sub network (aka broadcast address)'''
        return self.net_addr + self.totalAddr() - 1

    def firstAddr(self) -> int:
        '''the first address in this sub network (aka network address)'''
        return self.net_addr
        
    def totalAddr(self) -> int:
        '''the total number of addresses that can be used in this subnetwork'''
        return 2 ** (SubnetV4.MAX_BITS - self.mask)

    def useableAddr(self) -> int:
        '''the number of addresses that can be used for hosts in this subnetwork'''
        return self.totalAddr() - 2

assert SubnetV4() == SubnetV4()
assert repr(SubnetV4(255,24)) == 'SubnetV4(255,24)'
assert SubnetV4().strToAddr('255.255.255.255') == (255,255,255,255)
assert SubnetV4().addrToInt((255,255,255,0)) == int('0b' + '1' * 24 + '0' * 8, 2)
assert SubnetV4().intToAddr(int('0b' + '1' * 24 + '0' * 8, 2)) == (255,255,255,0)
assert SubnetV4().strToSubnetV4('255.255.255.0/24') == SubnetV4(int('0b'+'1'*24+'0'*8,2),24)
assert str(SubnetV4(255,24)) == '0.0.0.255/24'
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).totalAddr() == 2 ** (SubnetV4.MAX_BITS - 24)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).useableAddr() == 2 ** (SubnetV4.MAX_BITS - 24) - 2
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).lastAddr() == int('0b'+'1'*32,2)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).firstAddr() == int('0b'+'1'*24+'0'*8,2)
