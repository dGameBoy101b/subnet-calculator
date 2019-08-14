from subnet import SubnetV4

class SubnetterV4():
    '''a calculator of subnetting'''
    
    def __init__(self, root: SubnetV4 = SubnetV4(), hosts: list = [1]):
        if not isinstance(root, SubnetV4):
            raise TypeError('\'subnet\' must be a SubnetV4, not a ' + str(type(subnet)))
        if not isinstance(hosts, list):
            raise TypeError('\'hosts\' must be a list, not a ' + str(type(subnet)))
        for host in hosts:
            if not isinstance(host, int):
                raise TypeError('every element in \'hosts\' must be an integer, not a ' + str(type(host)))
            if host < 0:
                raise ValueError('every element in \'hosts\' must be greater than 0, not ' + str(host))
        hosts = self.trimList(hosts, 0)
        if len(hosts) < 1:
            raise IndexError('\'hosts\' must contain at least 1 item, not ' + str(len(hosts)))
        self.root = root
        self.hosts = hosts
        return

    def __eq__(self, other) -> bool:
        if isinstance(other, SubnetterV4):
            return self.root == other.root and self.hosts.sort() == other.hosts.sort()
        else:
            return False

    def __repr__(self) -> str:
        return 'SubnetterV4(' + repr(self.root) + ',' + repr(self.hosts) + ')'

    def calcSubnets(self) -> list:
        '''calculate the network addresses and subnet masks for creating sub networks
        from a root network address and subnet mask
        and a list of host quantities for each sub network'''
        hosts = self.hosts.copy().sort()
        subnets = []
        addr = self.root.firstAddr()
        for item in hosts:
            bits = requiredBits(item)
            mask = SubnetV4.MAX_BITS - bits
            if mask > self.root.slashMask():
                raise Exception('root mask too small')
            pass
            subnets.append(SubnetV4(addr, SubnetV4.MAX_BITS -

    def requiredBits(self, x: int) -> int:
        '''claculate the number of bits required to store an unsigned integer'''
        if not isinstance(x, int):
            raise TypeError('\'x\' must be an integer, not a ' +str(type(x)))
        if x < 0:
            raise ValueError('\'x\' must be greater than or equal to 0, not ' + str(x))
        bits = 1
        while x >= 2 ** bits:
            bits += 1
        return bits

    def trimList(self, x: list, targ: int) -> list:
        '''remove every occurrance of targ in x'''
        while True:
            try:
                x.remove(targ)
            except ValueError:
                return x

assert SubnetterV4() == SubnetterV4()
assert SubnetterV4().trimList([10,1,20,1,30],1) == [10,20,30]
assert SubnetterV4().trimList([10,30,0,23],2) == [10,30,0,23]
assert SubnetterV4().requiredBits(8) == 4
assert SubnetterV4().requiredBits(0) == 1
assert repr(SubnetterV4()) == 'SubnetterV4('+repr(SubnetV4())+',[1])'
