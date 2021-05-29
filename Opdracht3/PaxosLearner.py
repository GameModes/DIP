class Computer:  # Machines performing a simulation to receive consensus, and learn new data
    def __init__(self, net, acc=None, lea=None):
        self.failed = False #if failed the computer is unusable. Default is Not Failed
        self.network = net #Connects the computer to the network
        self.acceptors = acc #Knows the acceptors to send a message to
        self.learners = lea #Knows the learners to send succes messages to
        self.prior = False #Tells if the computer has priority of sending a message. Default is False
        self.changed = False #Tells if the computer has changed during the simulation. Default is false
        self.accepted = 0 #Tells the amount of accepted messages. Default is 0
        self.rejected = 0 #Tells the amount of rejected messages. Default is 0
        self.promise = 0 #Tells the amount of promised messagees. Default is 0
        self.consensus = False #?
        self.initval = None #?
        self.value = None #Tells the value it holds if it needs to send a messag
        self.maxID = 0 #?
        self.matrices = None #?
        self.predicted = 0 #?

    def DeliverMessage(self, m):  # Performs an action based on the message type
        """
        Sends a Prepare message type to all acceptor with the Message() function during the Propose type of the Message
        Else if during the Prepare type of the message, send a promise message.
        Else if Promise message, send accept
        Else if Accept message, send reject or accepted depending on the ID used.
        Else determines if proposal is successful
        :param m: The Message that needs to be sended
        """
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
        elif m.type == 'SUCCESS':
            # Learner saves accepted value in respective matrix and sends predicted message to simulation
            if not self.matrices:  # Makes matrices if they dont exist
                matrixnl = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in
                            'abcdefghijklmnopqrstuvwxyz $'}
                matrixen = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in
                            'abcdefghijklmnopqrstuvwxyz $'}
                self.matrices = {'nl': matrixnl, 'en': matrixen}
            value = m.value
            value = value.split(':')
            if len(value[1]) < 2:  # Adds missing space lost in conversion
                value[1] += ' '
            # Saves bigram based on language and combination
            self.matrices[value[0]][value[1][0]][value[1][1]] += 1
            self.predicted += 1
            # Resets amount of proposals passed for next round
            proposal = 0
            mn = Message()
            mn.type = 'PREDICTED'
            mn.src = m.dst
            mn.dst = None
            mn.value = None
            mn.proposalID = self.predicted
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
                    # If there are learners, send success message to learners
                    for i in self.learners:
                        mn = Message()
                        mn.type = 'SUCCESS'
                        mn.src = m.dst
                        mn.dst = i
                        mn.value = m.value
                        mn.proposalID = m.proposalID
                        self.network.Queue_Message(mn)
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

    def Extract_Message(self):
        # Takes first message in queue if source and destination are not failed, or contain a learner
        for m in self.queue:
            if 'L' in m.src or 'L' in m.dst:
                self.queue.remove(m)
                return m
            elif self.computers[m.src].failed is False and self.computers[m.dst].failed is False:
                self.queue.remove(m)
                return m
        return None


def Simulate(n_p, n_a, n_l, tmax, E):  # Runs Paxos simulation with given events
    ticklen = len(str(tmax))  # Length of tickstring for padding
    finished = False  # Indicator to see if current round is finished or not
    # Initialise computers and network
    N = Network()
    A = {'A' + str((i + 1)): Computer(N) for i in range(n_a)}
    L = {'L' + str((i + 1)): Computer(N) for i in range(n_l)}
    P = {'P' + str((i + 1)): Computer(N, A.keys(), L.keys()) for i in range(n_p)}
    C = {**P, **A, **L}
    N.computers = C
    global proposal
    proposal = 0

    for t in range(0, tmax):
        if len(N.queue) == 0 and len(E) == 0:
            # If there are no messages or events, the simulation ends.
            if not finished:  # If round is not finished, print current consensus
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
                print('{}: ** {} kapot **'.format(str(t).zfill(ticklen), c))
                C[c].failed = True
            for c in R:
                print('{}: ** {} gerepareerd **'.format(str(t).zfill(ticklen), c))
                C[c].failed = False
            if pi_v is not None and pi_c is not None:
                finished = False
                m = Message()
                m.type = 'PROPOSE'
                m.src = None  # PROPOSE-message starts outside network.
                m.dst = pi_c
                m.value = pi_v
                print('{}:    -> {}  PROPOSE v={}'.format(str(t).zfill(ticklen), m.dst, m.value))
                C[pi_c].DeliverMessage(m)
        else:
            m = N.Extract_Message()
            if m is not None:  # Messages get printed and delivered based on type
                if m.type == 'PREPARE':
                    print('{}: {} -> {}  PREPARE n={}'.format(str(t).zfill(ticklen), m.src, m.dst, m.proposalID))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'PROMISE':
                    if C[m.src].prior:
                        print(
                            '{}: {} -> {}  PROMISE n={} (Prior: n={}, v={})'.format(str(t).zfill(ticklen), m.src, m.dst,
                                                                                    m.proposalID, C[m.src].maxID,
                                                                                    C[m.src].value))
                    else:
                        print('{}: {} -> {}  PROMISE n={} (Prior: None)'.format(str(t).zfill(ticklen), m.src, m.dst,
                                                                                m.proposalID))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPT':
                    print('{}: {} -> {}  ACCEPT n={} v={}'.format(str(t).zfill(ticklen), m.src, m.dst, m.proposalID,
                                                                  m.value))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPTED':
                    print('{}: {} -> {}  ACCEPTED n={} v={}'.format(str(t).zfill(ticklen), m.src, m.dst, m.proposalID,
                                                                    m.value))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'REJECTED':
                    print('{}: {} -> {}  REJECTED n={}'.format(str(t).zfill(ticklen), m.src, m.dst, m.proposalID))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'SUCCESS':
                    print('{}: {} -> {}  SUCCESS n={} v={}'.format(str(t).zfill(ticklen), m.src, m.dst, m.proposalID,
                                                                   m.value))
                    C[m.dst].DeliverMessage(m)
                elif m.type == 'PREDICTED':
                    finished = True
                    print('{}: {} ->     PREDICTED n={}'.format(str(t).zfill(ticklen), m.src, m.proposalID))
                    for i in A.keys():  # Resets acceptors for new round
                        A[i].maxID = 0
                        A[i].value = None
                        A[i].prior = False

                    print()
                    for key in P.keys():  # Prints consensus and resets proposers for new round
                        print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                                  P[key].value))
                        P[key].consensus = False
                        P[key].initval = None
                        P[key].value = None
                    print()
            else:
                print('{}:'.format(str(t).zfill(ticklen)))

    # Prints consensus if tmax was reached
    for key in P.keys():
        if P[key].consensus:
            print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                      P[key].value))
        else:
            print('{} heeft geen consensus.'.format(key))


def main(file):  # Converts input and initialises simulation
    file = open(file, 'r')
    file = file.read().splitlines()

    start = file[0].split(' ')
    file = file[1:-1]
    n_p = int(start[0])
    n_a = int(start[1])
    n_l = int(start[2])
    tmax = int(start[3])
    E = []

    current = None
    for i in file:
        i = i.split(' ')
        if current is None:
            current = [int(i[0]), [], [], None, None]
        if int(i[0]) != current[0]:
            E.append(current)
            current = [int(i[0]), [], [], None, None]

        if 'FAIL' in i:
            if 'PROPOSER' in i:
                current[1].append('P{}'.format(i[-1]))
            else:
                current[1].append('A{}'.format(i[-1]))
        elif 'RECOVER' in i:
            if 'PROPOSER' in i:
                current[2].append('P{}'.format(i[-1]))
            else:
                current[2].append('A{}'.format(i[-1]))
        elif 'PROPOSE' in i:
            current[3] = 'P' + i[2]
            current[4] = ' '.join(i).split(' {} '.format(i[2]))[-1]
    E.append(current)

    Simulate(n_p, n_a, n_l, tmax, E)


if __name__ == '__main__':
    main('testinputPaxos2.txt')