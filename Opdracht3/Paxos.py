class Computer:  # Machines performing a simulation to receive consensus
    def __init__(self, net, acc=None):
        self.failed = False
        self.network = net
        self.acceptors = acc
        self.prior = False
        self.changed = False
        self.accepted = 0
        self.rejected = 0
        self.promise = 0
        self.consensus = False
        self.initval = 0
        self.value = 0
        self.maxID = 0

    def DeliverMessage(self, m):  # Performs an action based on the message type
        global proposal
        if m.type == 'PROPOSE':  # Proposer sends a prepare message to all acceptors
            proposal += 1
            self.initval = m.value
            self.value = m.value
            for acceptor in self.acceptors:
                mn = Message()
                mn.type = 'PREPARE'
                mn.src = m.dst
                mn.dst = acceptor
                mn.value = m.value
                mn.proposalID = proposal
                self.network.Queue_Message(mn)

        elif m.type == 'PREPARE':  # Acceptors send a Promise message to source proposer
            mn = Message()
            mn.type = 'PROMISE'
            mn.src = m.dst
            mn.dst = m.src
            if self.prior:  # If there was prior data, change the current message data to that
                mn.value = self.value
            else:
                mn.value = m.value
            mn.proposalID = m.proposalID
            self.network.Queue_Message(mn)
        elif m.type == 'PROMISE':  # Proposer sends a accept messages to all acceptors
            self.promise += 1
            # If the message value is different and the first different, change own value
            if self.value != m.value and not self.changed:
                self.value = m.value
                self.changed = True
            if self.promise == len(self.acceptors):  # If all messages received, send messages with own value
                for acceptor in self.acceptors:
                    mn = Message()
                    mn.type = 'ACCEPT'
                    mn.src = m.dst
                    mn.dst = acceptor
                    mn.value = self.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
        elif m.type == 'ACCEPT':  # Acceptor sends an accepted or rejected message to source proposer
            if self.prior:  # If there is prior data, check request
                if m.proposalID < self.maxID:  # If request is outdated, reject request
                    mn = Message()
                    mn.type = 'REJECTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
                else:  # If request is not outdated, accept request
                    self.maxID = m.proposalID
                    self.value = m.value
                    mn = Message()
                    mn.type = 'ACCEPTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
            else:  # If there is no prior data, save current data and accept proposal
                self.prior = True
                self.maxID = m.proposalID
                self.value = m.value
                mn = Message()
                mn.type = 'ACCEPTED'
                mn.src = m.dst
                mn.dst = m.src
                mn.value = m.value
                mn.proposalID = m.proposalID
                self.network.Queue_Message(mn)
        else:  # Proposer receives accepted or rejected messages, and determines if proposal is successful
            if m.type == 'ACCEPTED':  # Save response from acceptors
                self.accepted += 1
            else:
                self.rejected += 1
            if self.accepted + self.rejected == len(self.acceptors):  # If all received, determine if successful
                if self.accepted > self.rejected:  # If more accepted, reset values from this run and change consensus
                    self.accepted = 0
                    self.rejected = 0
                    self.changed = False
                    self.promise = 0
                    self.consensus = True
                else:  # If more rejected, reset values from this run and send new prepare messages
                    self.accepted = 0
                    self.rejected = 0
                    self.changed = False
                    self.promise = 0
                    proposal += 1
                    self.value = m.value
                    for acceptor in self.acceptors:
                        mn = Message()
                        mn.type = 'PREPARE'
                        mn.src = m.dst
                        mn.dst = acceptor
                        mn.value = m.value
                        mn.proposalID = proposal
                        self.network.Queue_Message(mn)


class Message:  # Message sent between computers or the simulation
    def __init__(self):
        self.src = None
        self.dst = None
        self.type = None
        self.value = None
        self.proposalID = None


class Network:  # Container containing messages from computers
    def __init__(self):
        self.queue = []
        self.computers = None

    def Queue_Message(self, m):  # Adds message to queue
        self.queue.append(m)

    def Extract_Message(self):  # Takes first message in queue if source and destination are not failed
        for m in self.queue:
            if self.computers[m.src].failed is False and self.computers[m.dst].failed is False:
                self.queue.remove(m)
                return m
        return None


def Simulation(n_p, n_a, tmax, E):  # Runs Paxos simulation with given events
    # Initialise computers and network
    N = Network()
    A = {'A' + str((i + 1)): Computer(N) for i in range(n_a)}
    P = {'P' + str((i + 1)): Computer(N, A.keys()) for i in range(n_p)}
    C = {**P, **A}
    N.computers = C
    global proposal
    proposal = 0

    for t in range(0, tmax):
        if len(N.queue) == 0 and len(E) == 0:
            # If there are no messages or events, the simulation ends.
            print()
            for key in P.keys():
                if P[key].consensus:
                    print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                              P[key].value))
                else:
                    print('{} heeft geen consensus.'.format(key))
            return
        # Process event e (if it exists)
        e = [i for i in E if i[0] == t]
        e = None if e == [] else e[0]
        if e is not None:
            E.remove(e)
            (t, F, R, pi_c, pi_v) = e
            for c in F:
                print('{}: ** {} kapot **'.format('%03d' % t, c))
                C[c].failed = True
            for c in R:
                print('{}: ** {} gerepareerd **'.format('%03d' % t, c))
                C[c].failed = False
            if pi_v is not None and pi_c is not None:
                m = Message()
                m.type = 'PROPOSE'
                m.src = None  # PROPOSE-message starts outside network.
                m.dst = pi_c
                m.value = pi_v
                print('{}:    -> {}  PROPOSE v={}'.format('%03d' % t, m.dst, m.value))
                C[pi_c].DeliverMessage(m)
        else:
            m = N.Extract_Message()
            if m is not None:  # Messages get printed and delivered based on type
                if m.type == 'PREPARE':
                    print('{}: {} -> {}  PREPARE n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'PROMISE':
                    if C[m.src].prior:
                        print('{}: {} -> {}  PROMISE n={} (Prior: n={}, v={})'.format('%03d' % t, m.src, m.dst,
                                                                                      m.proposalID, C[m.src].maxID,
                                                                                      C[m.src].value))
                    else:
                        print('{}: {} -> {}  PROMISE n={} (Prior: None)'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPT':
                    print('{}: {} -> {}  ACCEPT n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPTED':
                    print('{}: {} -> {}  ACCEPTED n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'REJECTED':
                    print('{}: {} -> {}  REJECTED n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    C[m.dst].DeliverMessage(m)
            else:
                print('{}:'.format('%03d' % t))

    # Prints consensus if tmax was reached
    for key in P.keys():
        if P[key].consensus:
            print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                      P[key].value))
        else:
            print('{} heeft geen consensus.'.format(key))



def main(file):
    """
    Reads the file, splits first line and the rest.
    The first line is being splitted into proposers, acceptors and the maximum ticks
    The rest is being used in a for loop where each line is a executeLine.
    After that the executeLine will go through multiple if statements to determine the line.
    Then the event will be saved in E and after all lines are implemented in E, it will be used
    in Simulation(n_p, n_a, tmax, E).
    The order of the functions are: main -> Simulation ->

    :param file: the text file with commands
    """
    file = open(file, 'r')
    file = file.read().splitlines()

    firstLine = file[0].split(' ')
    n_p, n_a, tmax= firstLine
    n_p, n_a, tmax = int(n_p), int(n_a), int(tmax)

    E = []
    current_e = None #current event
    executeLines = file[1:-1]
    for executeLine in executeLines:
        executeLine = executeLine.split(' ') #to split every word in line
        executeLine[0] = int(executeLine[0]) #convert the tick of the line from a string to an integer
        if current_e == None: #this will be executed only the first time
            current_e = [executeLine[0], [], [], None, None] #create empty template with tick as first element
        if executeLine[0] != current_e[0]:#this will be executed only NOT the first time
            E.append(current_e) #to save the formerly event in list E
            current_e = [executeLine[0], [], [], None, None] #create empty template with tick as first element

        if 'FAIL' in executeLine:
            if 'PROPOSER' in executeLine: #so the line is FAIL PROPOSER
                current_e[1].append('P{}'.format(executeLine[-1])) #adds failing proposer to second element of current E aka F
            else: #so the line is FAIL ACCEPTOR
                current_e[1].append('A{}'.format(executeLine[-1])) #adds failing acceptor to second element of current E aka F
        elif 'RECOVER' in executeLine:
            if 'PROPOSER' in executeLine: #so the line is RECOVER PROPOSER
                current_e[2].append('P{}'.format(executeLine[-1])) #adds recovering proposer to third element of current E aka R
            else:#so the line is RECOVER ACCEPTOR
                current_e[2].append('A{}'.format(executeLine[-1])) #adds recovering acceptor to third element of current E aka R
        elif 'PROPOSE' in executeLine:#so the line is PROPOSE
            current_e[3] = 'P' + executeLine[-2] #add proposer to 4th element of current E aka msg_p
            current_e[4] = int(executeLine[-1]) #add value to 5th/last element of current E aka msg_v
    E.append(current_e) #to add the last one to E
    Simulation(n_p, n_a, tmax, E) #runs simulation with the input, firstline and all the Events in E

main('testinputPaxos1.txt')