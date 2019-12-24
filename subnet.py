class MaskSepCountError(ValueError):
    '''incorrect number of mask separators'''
    def __init__(self, count: int, targ: int):
        if not isinstance(count, int):
            raise TypeError('\'count\' must be an integer, not a '+str(type(count)))
        if count < 0:
            raise ValueError('\'count\' must be 0 or greater, not '+str(count))
        if not isinstance(targ, int):
            raise TypeError('\'targ\' must be an integer, not a '+str(type(targ)))
        if targ == count:
            raise ValueError('\'count\' and \'targ\' cannot be equal if there is indeed an error')
        self.count = count
        self.targ = targ
        mes = ('There must be exactly '+str(targ)+' occurance',' of the mask separator ('+SubnetV4.MASK_SEP+') but '+str(count)+' ',' found!')
        if targ != 1:
            mes = ('s'.join(mes[:2]), mes[2])
        else:
            mes = (''.join(mes[:2]), mes[2])
        if count != 1:
            mes = 'were'.join(mes)
        else:
            mes = 'was'.join(mes)
        self.mes = mes

    def __str__(self) -> str:
        return self.mes

class MaskTooBigError(ValueError):
    '''mask exceeds address bit capacity'''
    def __init__(self, mask: int):
        if not isinstance(mask, int):
            raise TypeError('\'mask\' must be an integer, not a '+str(type(mask)))
        if mask < SubnetV4.MAX_BITS:
            raise ValueError('\'mask\' must be greater than or equal to '+str(SubnetV4.MAX_BITS)+' if there is indeed an error, not '+str(mask))
        self.mask = mask
        self.mes = ('The slash notation mask must be less than the maximum number of bits in an address ('
                   +str(SubnetV4.MAX_BITS)+') for there to be both network and host bits; '+str(mask)+' is too big!')

    def __str__(self) -> str:
        return self.mes

class MaskTooSmallError(ValueError):
    '''mask is negative or 0'''
    def __init__(self, mask: int):
        if not isinstance(mask, int):
            raise TypeError('\'mask\' must be an integer, not a '+str(type(mask)))
        if mask > 0:
            raise ValueError('\'mask\' must be 0 or lesser if there is indeed an error, not '+str(mask))
        self.mask = mask
        self.mes = 'The slash notation mask must be greater than 0 for there to be both network and host bits; '+str(mask)+' is too small!'

    def __str__(self) -> str:
        return self.mes

class AddrSepCountError(ValueError):
    '''incorrect number of address separators'''
    def __init__(self, count: int, targ: int):
        if not isinstance(count, int):
            raise TypeError('\'count\' must be an integer, not a '+str(type(count)))
        if count < 0:
            raise ValueError('\'count\' must be 0 or greater, not '+str(count))
        if not isinstance(targ, int):
            raise TypeError('\'targ\' must be an integer, not a '+str(type(targ)))
        if count == targ:
            raise ValueError('\'mask\' and \'targ\' cannot be equal if there is indeed an error')
        self.count = count
        self.targ = targ
        mes = ('There must be exactly '+str(targ)+' occurance',' of the address separator ('+SubnetV4.ADDR_SEP+') but '+str(count)+' ',' found!')
        if targ != 1:
            mes = (''.join(mes[:2]), mes[2])
        else:
            mes = ('s'.join(mes[:2]), mes[2])
        if count != 1:
            mes = 'were'.join(mes)
        else:
            mes = 'was'.join(mes)
        self.mes = mes

    def __str__(self) -> str:
        return self.mes

class AddrTooBigError(ValueError):
    '''integer address exceeds bit capacity'''
    def __init__(self, addr: int):
        if not isinstance(addr, int):
            raise TypeError('\'addr\' must be an integer, not a '+str(type(addr)))
        if addr < 2 ** SubnetV4.MAX_BITS:
            raise ValueError('\'addr\' must be '+str(2**SubnetV4.MAX_BITS)+' or greater if there is indeed an error, not '+str(addr))
        self.addr = addr
        ValueError('The integer value of an address must be less than '+str(2**SubnetV4.MAX_BITS)
                   +' for it to fit in the allocated bits ('+str(SubnetV4.MAX_BITS)+'); '+str(addr)+' is too big!')        

class AddrTooSmallError(ValueError):
    '''integer address is negative'''
    def __init__(self, addr: int):
        if not isinstance(addr, int):
            raise TypeError('\'addr\' must be an integer, not a '+str(type(addr)))
        if addr >= 0:
            raise ValueError('\'addr\' must be lesser than 0 if there is indeed an error, not '+str(addr))
        self.addr = addr
        self.mes = 'The integer value of an address must be 0 or greater for it to be unsigned; '+str(addr)+' is too small!'

    def __str__(self) -> str:
        return self.mes

class AddrPartTooBigError(ValueError):
    '''part of an address exceeds limit'''
    def __init__(self, addr_part: int):
        if not isinstance(addr_part, int):
            raise TypeError('\'addr_part\' must be an integer, not a '+str(type(addr_part)))
        if addr_part < 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS):
            raise ValueError('\'addr_part\' must be '+str(2**(SubnetV4.MAX_BITS//SubnetV4.ADDR_DIVISIONS))
                             +' or greater if there is indeed an error, not '+str(addr_part))
        self.addr_part = addr_part
        self.mes = ('Every part of an IPv4 network address must be lesser than '+str(2**(SubnetV4.MAX_BITS//SubnetV4.ADDR_DIVISIONS))
                   +' for the entire address to fit in the allocated bits; '+str(addr_part)+' is too big!')

    def __str__(self) -> str:
        return self.mes

class AddrPartTooSmallError(ValueError):
    '''part of an address is negative'''
    def __init__(self, addr_part: int):
        if not isinstance(addr_part, int):
            raise TypeError('\'addr_part\' must be an integer, not a '+str(type(addr_part)))
        if addr_part >= 0:
            raise ValueError('\'addr_part\' must be less than 0 if there is indeed an error, not '+str(addr_part))
        self.addr_part = addr_part
        self.mes = ('Every part of an IPv4 network address must be 0 or greater for it to be unsigned; '
                   +str(addr_part)+' is too small!')

    def __str__(self) -> str:
        return self.mes

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
            raise AddrTooBigError(net_addr)
        if net_addr < 0:
            raise AddrTooSmallError(net_addr)
        if mask > SubnetV4.MAX_BITS:
            raise MaskTooBigError(mask)
        if mask < 0:
            raise MaskTooSmallError(mask)
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
        addr_parts = SubnetV4.intToAddr(self.net_addr)
        string = ''
        i = 0
        for i in range(0,len(addr_parts)):
            string += str(addr_parts[i]) + SubnetV4.ADDR_SEP
        return string[0:-len(SubnetV4.ADDR_SEP)] + SubnetV4.MASK_SEP + str(self.mask)

    def strToSubnetV4(x: str):
        '''convert a string into a SubnetV4'''
        if not isinstance(x, str):
            raise TypeError('\'x\' must be a string, not a ' + str(type(x)))
        if x.count(SubnetV4.MASK_SEP) != 1:
            raise MaskSepCountError(x.count(SubnetV4.MASK_SEP), 1)
        mask = int(x.partition(SubnetV4.MASK_SEP)[2])
        net_addr = SubnetV4.addrToInt(SubnetV4.strToAddr(x.partition(SubnetV4.MASK_SEP)[0]))
        return SubnetV4(net_addr, mask)

    def strToAddr(x: str) -> tuple:
        '''convert a string into a suitable representation of an address'''
        if not isinstance(x, str):
            raise TypeError('\'x\' must be a string, not a ' + str(type(x)))
        if x.count(SubnetV4.ADDR_SEP) != SubnetV4.ADDR_DIVISIONS - 1:
            raise AddrSepCountError(x.count(SubnetV4.ADDR_SEP), SubnetV4.ADDR_DIVISIONS - 1)
        addr_parts = x.split(SubnetV4.ADDR_SEP)
        addr = []
        for part in addr_parts:
            if int(part) > 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS):
                raise AddrPartTooBigError(int(part))
            if int(part) < 0:
                raise AddrPartTooSmallError(int(part))
            addr.append(int(part))
        return tuple(addr)

    def intToAddr(x: int) -> tuple:
        '''convert an integer into a suitable representation of an address'''
        if not isinstance(x, int):
            raise TypeError('\'x\' must be an integer, not a ' + str(type(x)))
        if x < 0:
            raise AddrTooSmallError(x)
        if x >= 2 ** SubnetV4.MAX_BITS:
            raise AddrTooBigError(x)
        base = 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS)
        i = SubnetV4.ADDR_DIVISIONS - 1
        addr = []
        while i >= 0:
            num = x // (base ** i)
            addr.append(num)
            x -= num * base ** i
            i -= 1
        return tuple(addr)

    def addrToInt(x: tuple) -> int:
        '''convert a tuple address to an integer'''
        if not isinstance(x, tuple):
            raise TypeError('\'x\' must be a tuple, not a ' + str(type(x)))
        if len(x) != SubnetV4.ADDR_DIVISIONS:
            raise ValueError('\'x\' must be ' + str(SubnetV4.ADDR_DIVISIONS) + ' long, not ' + str(len(x)))
        x = list(x)
        x.reverse()
        base = 2 ** (SubnetV4.MAX_BITS // SubnetV4.ADDR_DIVISIONS)
        i = 0
        addr = 0
        while i < SubnetV4.ADDR_DIVISIONS:
            if not isinstance(x[i], int):
                raise TypeError('every element of \'x\' must be an integer, not a ' + str(type(x[i])))
            if x[i] >= base:
                raise AddrPartTooBigError(x[i])
            if x[i] < 0:
                raise AddrPartTooSmallError(x[i])
            num = x[i] * base ** i
            addr += num
            i += 1
        return addr

    def broadcastAddr(self) -> int:
        '''the last address in this sub network (aka broadcast address)'''
        return self.net_addr + self.totalAddr() - 1

    def networkAddr(self) -> int:
        '''the first address in this sub network (aka network address)'''
        return self.net_addr

    def firstAddr(self) -> int:
        '''the first usable address in this sub network'''
        return self.net_addr + 1

    def lastAddr(self) -> int:
        '''the last usable address in this sub network'''
        return self.net_addr + self.totalAddr() - 2
        
    def totalAddr(self) -> int:
        '''the total number of addresses that can be used in this subnetwork'''
        return 2 ** (SubnetV4.MAX_BITS - self.mask)

    def useableAddr(self) -> int:
        '''the number of addresses that can be used for hosts in this subnetwork'''
        return self.totalAddr() - 2

    def slashMask(self) -> int:
        '''the number of bits used for the network part of the address'''
        return self.mask

    def addrMask(self) -> tuple:
        '''the mask using IPv4 notation'''
        return SubnetV4.intToAddr(int('0b' + '1' * self.mask + '0' * (SubnetV4.MAX_BITS - self.mask), 2))

assert SubnetV4() == SubnetV4()
assert repr(SubnetV4(255,24)) == 'SubnetV4(255,24)'
assert SubnetV4.strToAddr('255.255.255.255') == (255,255,255,255)
assert SubnetV4.addrToInt((255,255,255,0)) == int('0b' + '1' * 24 + '0' * 8, 2)
assert SubnetV4.intToAddr(int('0b' + '1' * 24 + '0' * 8, 2)) == (255,255,255,0)
assert SubnetV4.strToSubnetV4('255.255.255.0/24') == SubnetV4(int('0b'+'1'*24+'0'*8,2),24)
assert str(SubnetV4(255,24)) == '0.0.0.255/24'
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).totalAddr() == 2 ** (SubnetV4.MAX_BITS - 24)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).useableAddr() == 2 ** (SubnetV4.MAX_BITS - 24) - 2
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).broadcastAddr() == int('0b'+'1'*32,2)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).networkAddr() == int('0b'+'1'*24+'0'*8,2)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).firstAddr() == int('0b'+'1'*24+'0'*7+'1',2)
assert SubnetV4(int('0b'+'1'*24+'0'*8,2),24).lastAddr() == int('0b'+'1'*31+'0',2)
assert SubnetV4.strToSubnetV4('123.244.0.1/16').slashMask() == 16
assert SubnetV4.strToSubnetV4('123.244.0.1/16').addrMask() == (255,255,0,0)
