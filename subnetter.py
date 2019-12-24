from subnet import SubnetV4

class ImpossibleSubnetError(Exception):
    '''impossible to fulfil subnetting requirements'''
    def __init__(self, root: SubnetV4, hosts: [int]):
        if not isinstance(root, SubnetV4):
            raise TypeError('\'root\' must be a SubnetV4, not a ' + str(type(root)))
        if not isinstance(hosts, list):
            raise TypeError('\'hosts\' must be a list, not a ' + str(type(hosts)))
        if len(hosts) < 1:
            raise IndexError('\'hosts\' must contain at least 1 item, not ' + str(len(hosts)))
        for host in hosts:
            if not isinstance(host, int):
                raise TypeError('every element in \'hosts\' must be an integer, not a ' + str(type(host)))
            if host < 1:
                raise ValueError('every element in \'hosts\' must be greater than 0, not ' + str(host))
        self.root = root
        self.hosts = hosts
        hosts_str = ''
        for host in hosts:
            hosts_str += str(host) + ', '
        hosts_str = hosts_str[0:-2]
        self.mes = ('Cannot fit all sub-networks with required network address spaces ('+hosts_str+') into allocated address space ('+str(root)+')!')

    def __str__(self) -> str:
        return self.mes

class SubnetterV4():
    '''a calculator for subnetting'''
    
    def __init__(self, root: SubnetV4 = SubnetV4(), hosts: [int] = [1]):
        if not isinstance(root, SubnetV4):
            raise TypeError('\'root\' must be a SubnetV4, not a ' + str(type(root)))
        if not isinstance(hosts, list):
            raise TypeError('\'hosts\' must be a list, not a ' + str(type(hosts)))
        if len(hosts) < 1:
            raise IndexError('\'hosts\' must contain at least 1 item, not ' + str(len(hosts)))
        for host in hosts:
            if not isinstance(host, int):
                raise TypeError('every element in \'hosts\' must be an integer, not a ' + str(type(host)))
            if host < 1:
                raise ValueError('every element in \'hosts\' must be greater than 0, not ' + str(host))
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

    def calcSubnets(self) -> [SubnetV4]:
        '''calculate the network addresses and subnet masks for creating sub networks
        from a root network address and subnet mask
        and a list of host quantities for each sub network'''
        hosts = self.hosts.copy()
        hosts.sort()
        hosts.reverse()
        addr = self.root.networkAddr()
        subnets = []
        for host in hosts:
            bit = SubnetterV4.requiredBits(host + 2)
            mask = SubnetV4.MAX_BITS - bit
            subnet = SubnetV4(addr, mask)
            if subnet.broadcastAddr() > self.root.broadcastAddr():
                raise ImpossibleSubnetError(self.root, self.hosts)
            subnets.append(subnet)
            addr += 2 ** bit
        return subnets

    def requiredBits(x: int) -> int:
        '''claculate the number of bits required to store an unsigned integer'''
        if not isinstance(x, int):
            raise TypeError('\'x\' must be an integer, not a ' +str(type(x)))
        if x < 0:
            raise ValueError('\'x\' must be greater than or equal to 0, not ' + str(x))
        elif x == 0:
            return 0
        bits = 1
        while x > 2 ** bits:
            bits += 1
        return bits

    def calcRemaining(self) -> int:
        '''calculate the number of free network addresses in the root network after subnetting'''
        subnets = self.calcSubnets()
        used = 0
        for subnet in subnets:
            used += subnet.totalAddr()
        return self.root.totalAddr() - used

assert SubnetterV4() == SubnetterV4()
assert SubnetterV4.requiredBits(0) == 0
assert SubnetterV4.requiredBits(1) == 1
assert SubnetterV4.requiredBits(2) == 1
assert repr(SubnetterV4()) == 'SubnetterV4('+repr(SubnetV4())+',[1])'
assert SubnetterV4(SubnetV4.strToSubnetV4('192.168.1.0/29'), [2,2]).calcSubnets() == [SubnetV4.strToSubnetV4('192.168.1.0/30'), SubnetV4.strToSubnetV4('192.168.1.4/30')]
assert SubnetterV4(SubnetV4.strToSubnetV4('192.168.1.0/29'), [2,2]).calcRemaining() == 0
