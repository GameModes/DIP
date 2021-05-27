class Computer:
    def __init__(self, id, net, acc=None):
        self.id = id
        self.failed = False
        self.network = net
        self.acceptors = acc
        self.prior = False
        self.accepted = 0
        self.rejected = 0
        self.consensus = False
        self.initval = 0
        self.maxval = 0
        self.maxID = 0

    def DeliverMessage(self, m):
        """
        A message given from Simulation
        :param m: Message
        """
        #         print('im gonna deliver')
        global proposal
        if m.type == 'PROPOSE':
            proposal +=1
            self.initval = m.value
            self.maxval = m.value
            for i in self.acceptors.keys():
                mn = Message()
                mn.type = 'PREPARE'
                mn.src = m.dst
                mn.dst = i
                mn.value = m.value
                mn.proposalID = proposal
                self.network.Queue_Message(mn)

        elif m.type == 'PREPARE':
            if self.maxval < m.value:
                self.maxval = m.value
            mn = Message()
            mn.type = 'PROMISE'
            mn.src = m.dst
            mn.dst = m.src
            mn.value = self.maxval
            mn.proposalID = m.proposalID
            self.network.Queue_Message(mn)
        elif m.type == 'PROMISE':
            if self.maxval < m.value:
                self.maxval = m.value
            mn = Message()
            mn.type = 'ACCEPT'
            mn.src = m.dst
            mn.dst = m.src
            mn.value = m.value
            mn.proposalID = m.proposalID
            #             print(mn.type, mn.src, mn.dst, mn.value)

            self.network.Queue_Message(mn)
        elif m.type == 'ACCEPT':
            if self.prior:
                if m.proposalID < self.maxID:
                    mn = Message()
                    mn.type = 'REJECTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
                else:
                    self.maxID = m.proposalID
                    mn = Message()
                    mn.type = 'ACCEPTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
            else:
                self.prior = True
                self.maxID = m.proposalID
                mn = Message()
                mn.type = 'ACCEPTED'
                mn.src = m.dst
                mn.dst = m.src
                mn.value = m.value
                mn.proposalID = m.proposalID
                self.network.Queue_Message(mn)
        else:
            if m.type == 'ACCEPTED':
                self.accepted += 1
            else:
                self.rejected += 1
            if self.accepted + self.rejected == len(self.acceptors.keys()):
                if self.accepted > self.rejected:
                    self.consensus = True
                else:
                    self.accepted = 0
                    self.rejected = 0
                    proposal += 1
                    self.maxval = m.value
                    for i in self.acceptors.keys():
                        mn = Message()
                        mn.type = 'PREPARE'
                        mn.src = m.dst
                        mn.dst = i
                        mn.value = m.value
                        mn.proposalID = proposal
                        self.network.Queue_Message(mn)


class Message:
    def __init__(self):
        self.src = None
        self.dst = None
        self.type = None
        self.value = None
        self.proposalID = None


class Network:
    def __init__(self):
        self.queue = []
        self.proposers = None
        self.acceptors = None

    def Queue_Message(self, m):
        self.queue.append(m)

    def Extract_Message(self):
        for m in self.queue:
            if 'P' in m.src:
                if self.proposers[m.src].failed == False and self.acceptors[m.dst].failed == False:
                    self.queue.remove(m)
                    return m
            else:
                if self.acceptors[m.src].failed == False and self.proposers[m.dst].failed == False:
                    self.queue.remove(m)
                    return m
        return None


def Simulate(n_p, n_a, tmax, E):
    #   /* Initializeer Proposer and Acceptor sets, maak netwerk aan*/
    N = Network()
    A = {'A' + str((i + 1)): Computer('A' + str((i + 1)), N) for i in range(n_a)}
    P = {'P' + str((i + 1)): Computer('P' + str((i + 1)), N, A) for i in range(n_p)}
    N.proposers = P
    N.acceptors = A
    #     comps = P+A
    global proposal
    proposal = 0

    for t in range(0, tmax):
        #         print(len(E))
        #         print(len(N.queue) == 0 or len(E) == 0)
        if len(N.queue) == 0 and len(E) == 0:
            #             print('empty')
            # Als er geen berichten of zijn of events, dan is de simulatie afgelopen.
            print()
            for key in P.keys():
                if P[key].consensus:
                    print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                              P[key].maxval))
                else:
                    print('{} heeft geen consensus.'.format(key))
            return
        # Verwerk event e (als dat tenminste bestaat)
        e = [i for i in E if i[0] == t]
        e = None if e == [] else e[0]
        if e is not None:
            E.remove(e)
            #             print(e)
            (t, F, R, pi_c, pi_v) = e
            #             print((t, F, R, pi_c, pi_v))
            for c in F:
                print('{}: ** {} kapot **'.format('%03d' % t, c))
                if 'P' in c:
                    P[c].failed = True
                else:
                    A[c].failed = True
            for c in R:
                print('{}: ** {} gerepareerd **'.format('%03d' % t, c))
                if 'P' in c:
                    P[c].failed = False
                else:
                    A[c].failed = False
            if pi_v is not None and pi_c is not None:
                m = Message()
                m.type = 'PROPOSE'
                m.src = None  # PROPOSE-bericht beginnen buiten het netwerk.
                m.dst = pi_c
                m.value = pi_v
                print('{}:    -> {}  PROPOSE v={}'.format('%03d' % t, m.dst, m.value))
                P[pi_c].DeliverMessage(m)
        else:
            m = N.Extract_Message()
            if m is not None:
                #                 if m.type = 'PROPOSE':
                #                     print('{}:    -> P{}  PROPOSE v={}'.format(t, m.dst, m.value))
                if m.type == 'PREPARE':
                    print('{}: {} -> {}  PREPARE n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    A[m.dst].DeliverMessage(m)
                elif m.type == 'PROMISE':
                    if A[m.src].prior:
                        print('{}: {} -> {}  PROMISE n={} (Prior: n={}, v={})'.format('%03d' % t, m.src, m.dst,
                                                                                      m.proposalID, A[m.src].maxID,
                                                                                      A[m.src].maxval))
                    else:
                        print('{}: {} -> {}  PROMISE n={} (Prior: None)'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    P[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPT':
                    print('{}: {} -> {}  ACCEPT n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    A[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPTED':
                    print('{}: {} -> {}  ACCEPTED n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    P[m.dst].DeliverMessage(m)
                elif m.type == 'REJECTED':
                    print('{}: {} -> {}  REJECTED n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    P[m.dst].DeliverMessage(m)
            #                 if m.type in ['PREPARE', 'ACCEPT']:
            #                     A[m.dst].DeliverMessage(m)
            #                 else:
            #                     P[m.dst].DeliverMessage(m)
            #                 DeliverMessage(m.dst, m)
            else:
                print('{}:'.format('%03d' % t))



def main(file):
    file = open(file, 'r')
    file = file.read().splitlines()

    start = file[0].split(' ')
    file = file[1:-1]
    n_p = int(start[0])
    n_a = int(start[1])
    tmax = int(start[2])
    #     print(file)
    E = []

    current = None
    for i in file:
        i = i.split(' ')
        if current == None:
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
            current[3] = 'P' + i[-2]
            current[4] = int(i[-1])
    E.append(current)
    #     print(E)

    Simulate(n_p, n_a, tmax, E)

main('testinputPaxos1.txt')