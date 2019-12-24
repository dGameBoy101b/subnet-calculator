from subnetter import SubnetterV4
from subnet import SubnetV4

class Console():
    '''the console interface for the subnet calculator'''
    EXIT = 'close'
    HELP = 'help'
    PROMPT = '>>> '
    IN_PROMPT = '?> '
    ERR_PROMPT = '!> '
    OUT_PROMPT = '#> '

    def help():
        '''print a help message'''
        print(Console.PROMPT+'Input an IPv4 network address with a slash notation mask first as the allocated network address space for the requested sub-networks (*0-255*.*0-255*.*0-255*.*0-255*/*mask*).\n'
              +'Then add a list of the required number of hosts for each sub-network separated by spaces (*sub_hosts* *sub_hosts* ...).\n'
              +repr(Console.EXIT)+' can be entered instead to close this program, or '+repr(Console.HELP)+' to display this help message again.\n')

    def close():
        '''close the program with a farewell message'''
        print(Console.PROMPT+'Thank you for using the Mader Subnet Calculator.')
        raise SystemExit()

    def open():
        '''open the program with a welcome message and the help message'''
        print(Console.PROMPT+'Welcome to the Mader Subnet Calculator.\n')
        Console.help()

    def main():
        '''the main interaction loop'''
        Console.open()
        while True:
            com = input(Console.IN_PROMPT).strip()
            if com == Console.EXIT:
                Console.close()
            elif com == Console.HELP:
                Console.help()
            else:
                args = Console.interpret(com)
                if args != None:
                    res = Console.calculate(args)
                    if res != None:
                        Console.display(res)

    def interpret(inp: str) -> (SubnetV4, [int]):
        '''interpret an input string'''
        args = inp.split(' ')
        try:
            addr = SubnetV4.strToSubnetV4(args[0])
        except Exception as e:
            print(Console.ERR_PROMPT+'Invalid network address or slash notation mask: '+str(e)+'\n')
            return
        hosts = []
        for i in range(1, len(args)):
            try:
                host = int(args[i])
            except Exception as e:
                print(Console.ERR_PROMPT+'Invalid subnet host count requirement: '+str(e)+'\n')
                return
            hosts.append(host)
        return (addr, hosts)

    def calculate(args: (SubnetV4, [int])) -> ([SubnetV4], int):
        '''calculate the subnets for an input'''
        try:
            subnetter = SubnetterV4(*args)
        except Exception as e:
            print(Console.ERR_PROMPT+'Invalid input: '+str(e)+'\n')
            return
        try:
            return (subnetter.calcSubnets(), subnetter.calcRemaining())
        except Exception as e:
            print(Console.ERR_PROMPT+'Impossible subnetting request: '+str(e)+'\n')
            return

    def display(results: ([SubnetV4], int)):
        '''display the resulting subnets'''
        for subnet in results[0]:
            print(Console.OUT_PROMPT+str(subnet)+' with '+str(subnet.useableAddr())+' usable network addresses.')
        print(Console.OUT_PROMPT+'With '+str(results[1])+' network addresses remaining.\n')

if __name__ == '__main__':
    Console.main()
