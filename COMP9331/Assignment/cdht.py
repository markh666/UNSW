import sys
import threading
import socket
import time
import os
import numpy as np 

LOCALHOST = '127.0.0.1'


class CDHT():
    def __init__(self, peer, succ1, succ2, MSS, droprate):

        self.peer = peer
        self.succ1 = succ1
        self.succ2 = succ2
        self.pred1 = -1
        self.pred2 = -1
        self.MSS = MSS
        self.dropRate = droprate
        self.fileLength = 0
        self.fileDest = -1
        self.run = True
        self.start_time = time.time()

        self.threadPing = threading.Thread(target=self.Ping)
        self.threadTCP = threading.Thread(target=self.TCP)
        self.threadInput = threading.Thread(target=self.user_input)
        self.threadFile = threading.Thread(target=self.receiveFile)
        self.threadFile.start()
        self.threadPing.start()
        self.threadTCP.start()
        self.threadInput.start()

    def Ping(self):
        global LeavePeer
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)  # set time out
        sock.bind((LOCALHOST, 32698+self.peer))

        lastPingTime = 0
        seq = 0
        succ1Ack = 0
        succ2Ack = 0
        succ1_no_reply = False
        succ2_no_reply = False

        while self.run:
            if time.time() - lastPingTime > 10.0: 
                if self.succ1 != 'Leave':
                    self.sendPingMessage(seq, self.peer, 32698+self.succ1, 'request')
                if self.succ2 != 'Leave':
                    self.sendPingMessage(seq, self.peer, 32698+self.succ2, 'request')
                lastPingTime = time.time()
                seq += 1
            if succ1_no_reply and self.succ1 != 'Leave':
                succ1Ack = seq
                succ1_no_reply = False
            if succ2_no_reply and self.succ2 != 'Leave':
                succ2Ack = seq
                succ2_no_reply = False
            if self.succ1 != 'Leave' and seq - succ1Ack >= 5:
                print(f'Peer {self.succ1} is no longer alive.')
                LeavePeer = self.succ1
                self.succ1 = 'Leave'
                succ1_no_reply = True
                self.sendTCPMessage('ask', self.peer, 32698+self.succ2, 'search',
                                    succ1=0, succ2=0)
            if self.succ2 != 'Leave' and seq - succ2Ack >= 5:
                print(f'Peer {self.succ2} is no longer alive.')
                LeavePeer = self.succ2
                self.succ2 = 'Leave'
                succ2_no_reply = True
                self.sendTCPMessage('ask', self.peer, 32698+self.succ1, 'search',
                                    succ1=0, succ2=0)
            try:
                message = sock.recvfrom(1024)[0]
                sender, seqR, messageType = message.decode().split()

                if messageType == 'request':
                    print(f'A ping request message was received from Peer {sender}.')
                    if all([self.pred1 != -1, self.pred2 != -1, sender != self.pred1, sender != self.pred2]):
                        self.pred1 = -1
                        self.pred2 = -1
                    if self.pred1 == -1:
                        self.pred1 = int(sender)
                    elif self.pred2 == -1 and int(sender) != self.pred1:
                        self.pred2 = int(sender)

                    self.sendPingMessage(seqR, self.peer, 32698+int(sender), 'response')
                else:
                    if int(sender) == self.succ1:
                        succ1Ack = int(seqR)
                    elif int(sender) == self.succ2:
                        succ2Ack = int(seqR)
                    print(f'A ping response message was received from Peer {sender}.')
            except Exception:
                continue

    def TCP(self):
        global LeavePeer
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((LOCALHOST, 32698+self.peer))
        sock.listen(1)
        while self.run:
            try:
                conn = sock.accept()[0]
                while True:
                    message = conn.recv(1024)
                    if not message:
                        break
                    sender = message.decode().split()[2]
                    message = message.decode()
                    if message.split()[0] == 'ask':
                        if message.split()[1] == 'quit':
                            newSucc1, newSucc2 = message.split()[3:5]
                            if int(sender) == self.succ1:
                                self.succ1, self.succ2 = int(newSucc1), int(newSucc2)
                            elif int(sender) == self.succ2:
                                self.succ1, self.succ2 = self.succ1, int(newSucc1)
                            print(f'Peer {sender} will depart from the network.')
                            print(f'My first successor is now peer {self.succ1}.')
                            print(f'My second successor is now peer {self.succ2}.')

                        elif message.split()[1] == 'search':
                            self.sendTCPMessage('ask', self.peer, 32698+int(sender), 'response', succ1=self.succ1, succ2=self.succ2)

                        elif message.split()[1] == 'response':
                            newSucc1, newSucc2 = message.split()[3:5]
                            if self.succ1 == 'Leave':
                                self.succ1, self.succ2 = int(self.succ2), int(newSucc1)
                            elif self.succ2 == 'Leave':
                                if newSucc1 == str(LeavePeer) or newSucc1 == 'Leave':
                                    self.succ2 = int(newSucc2)
                                else :
                                    self.succ2 =int(newSucc1)
                            if self.succ1 == 'Leave' or self.succ2 == 'Leave':
                                continue
                            print(f'My first successor is now peer {self.succ1}.')
                            print(f'My second successor is now peer {self.succ2}.')
                    # found the file
                    elif message.split()[0] == 'found':
                        print(f'Received a response message from peer {sender}, which has the file {message.split()[3]}.')
                        print('We now start receiving the file...')
                        self.fileDest = int(sender)
                        # print('fileDest is :', self.fileDest)

                    elif message.split()[0] == 'file':
                        # find the file
                        fileHash = message.split()[1]
                        fileName = message.split()[3]
                        original = message.split()[4]
                        file_location = self.fileLocation(fileHash)

                        if file_location:
                            print(f'File {fileName} is here.')
                            self.sendTCPMessage('found', self.peer, 32698+int(original), int(fileHash)%256, fileName=fileName, original=original)
                            print(f'A response message, destined for peer {original}, has been sent.')
                            print(f'We now start sending the file...')
                            self.fileDest = int(original)
                            self.sendFile('hello', fileNum=fileName)
                            # print('fileDest is :', self.fileDest)

                        if not file_location:
                            print(f'File {fileName} is not stored here.')
                            self.sendTCPMessage('file', self.peer, 32698+self.succ1,int(fileHash)%256, fileName=fileName, original=original)
                            print(f'File request message has been forwarded to my successor.')
                conn.close()
            except Exception:
                pass

    def sendPingMessage(self, seq, source, dest, status):
        message = f'{source} {seq} {status}'
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.0)
            sock.sendto(message.encode(), (LOCALHOST, dest))
        except Exception:
            pass

    def sendTCPMessage(self, request, source, port, status, succ1=None, succ2=None, fileName=None,
                       original=None):
        if request == 'ask':
            message = f'ask {status} {source} {succ1} {succ2}'
        elif request == 'file':
            message = f'file {status} {source} {fileName} {original}'
        elif request == 'found':
            message = f'found {status} {source} {fileName} {original}'
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOCALHOST, port))
            sock.send(message.encode())
        except Exception:
            pass
        finally:
            sock.close()

    def fileLocation(self, fileNum):
        fileHash = int(fileNum) % 256
        if fileHash > 255:
            return False
        if self.succ1 < self.peer < fileHash:
            return True
        if abs(self.succ1 - fileHash) > abs(self.peer-fileHash) and abs(int(self.pred1)-fileHash) > abs(self.peer-fileHash):
            return True
        return False
                
    def sendFile(self, request, fileNum=None, seq=1, ack=0):
        fileName = fileNum+'.pdf'
        # print(request)
        if request == 'hello':
            filesize = str(os.path.getsize(fileName))
            message = f'filesize {filesize} {fileNum}'
            message = message.encode()

        elif request == 'connect':
            message = f'request {fileNum} {seq} {ack}'
            message = message.encode()

        elif request == 'received':
            message = f'next {fileNum} {seq} {ack}'
            message = message.encode()
        
        elif request == 'complete':
            message = f'finished {fileNum} {seq} {ack}'
            message = message.encode()

        elif request == 'file':    
            filesize = str(os.path.getsize(fileName))
            header = f'{seq} {ack} {self.MSS} '
            size = self.MSS - len(header)
            f = open(fileName, 'rb')
            p = f.read(self.fileLength)
            l = f.read(size)
            f.close()
            self.fileLength += size
            message = header.encode() + l

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(message, (LOCALHOST, 9331+self.fileDest))
            # print('send:', message)

        except Exception:
            pass

    def receiveFile(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.bind((LOCALHOST, 9331+self.peer))

        seq = 1
        ack = 0
        nbd = self.MSS
        fileNum = None
        fileName = None
        running = True
        
        while running:
            try:
                message, addr = sock.recvfrom(1024)
                c = len(str(seq))+len(str(ack))+len(str(self.MSS))+3
                # print(message)

                if len(message) < 30:
                    if message.decode().split()[0] == 'filesize':
                        filesize = int(message.decode().split()[1])
                        fileNum = message.decode().split()[2]
                        fileName = fileNum+'.pdf'
                        f = open('received_file.pdf', 'wb')
                        log = open('requesting_log.txt', 'w')
                        f.close()
                        log.close()
                        self.sendFile('connect', fileNum)

                    elif message.decode().split()[0] == 'request':
                        fileNum = message.decode().split()[1]
                        fileName = fileNum+'.pdf'
                        filesize = str(os.path.getsize(fileName))
                        r = open('responding_log.txt', 'w')
                        self.sendFile('file', fileNum)
                        T= round(float(time.time())-float(self.start_time),2)
                        nbd = self.MSS
                        content = f'snd    {T}      {seq}       {nbd}       {ack}\n'
                        r.write(content)
                        r.close()
                        ack = seq + nbd
                        seq = 0

                    elif message.decode().split()[0] == 'finished':
                        r = open('responding_log.txt', 'a')
                        T= round(float(time.time())-float(self.start_time),2)
                        nbd = self.MSS
                        content = f'rcv    {T}      {seq}       {nbd}       {ack}\n'
                        r.write(content)
                        running = False
                        print('The file is sent.')

                    elif message.decode().split()[0] == 'next':
                        r = open('responding_log.txt', 'a')
                        T= round(float(time.time())-float(self.start_time),2)
                        nbd = self.MSS
                        content = f'rcv    {T}      {seq}       {nbd}       {ack}\n'
                        r.write(content)
                        seq = ack
                        ack = 0

                        if np.random.random() > self.dropRate:
                            self.sendFile('file', fileNum, seq, ack)
                            T= round(float(time.time())-float(self.start_time),2)
                            nbd = self.MSS
                            content = f'snd    {T}      {seq}       {nbd}       {ack}\n'
                            r.write(content)
                            r.close()
                            ack = seq + nbd
                            seq = 0
                        else:
                            T= round(float(time.time())-float(self.start_time),2)
                            nbd = min(int(nbd), int(filesize))
                            content = f'drop   {T}      {seq}       {nbd}       {ack}\n'
                            r.write(content)
                            self.sendFile('file', fileNum)
                            T= round(float(time.time())-float(self.start_time),2)
                            nbd = self.MSS
                            content = f'RTX    {T}      {seq}       {nbd}       {ack}\n'
                            r.write(content)
                            ack = seq + nbd
                            seq = 0
                            r.close()

                elif len(message) > 5:
                    f = open('received_file.pdf', 'ab')
                    log = open('requesting_log.txt', 'a')
                    data = message[c:]
                    filesize -= (self.MSS-c)
                    f.write(data)
                    f.close()

                    T= round(float(time.time())-float(self.start_time),2)
                    nbd = len(message)
                    content = f'rcv    {T}      {seq}       {nbd}       {ack}\n'
                    log.write(content)
                    log.close()
                    ack = seq + nbd
                    seq = 0
                    if filesize <= 0:
                        self.sendFile('complete', fileNum)
                        T= round(float(time.time())-float(self.start_time),2)
                        content = f'snd    {T}      {seq}       {nbd}       {ack}\n'
                        log = open('requesting_log.txt', 'a')
                        log.write(content)
                        running = False
                        log.close()
                        print('The file is received.')
                    else:
                        self.sendFile('received', fileNum)
                        T= round(float(time.time())-float(self.start_time),2)
                        content = f'snd    {T}      {seq}       {nbd}       {ack}\n'
                        log = open('requesting_log.txt', 'a')
                        log.write(content)
                        log.close()
                        seq += ack
                        ack = 0
            except Exception:
                continue
        sock.close()    
        
    def user_input(self):
        while self.run:
            command = input()
            if command.split()[0] == 'request':
                try:
                    if len(command.split()[1]) != 4:
                        raise ValueError('\nERROR: Invalid filename provided.\n')
                    fileName = int(command.split()[1])
                    if not 0<=fileName<=9999:
                        raise ValueError('\nERROR: Invalid filename provided.\n')
                except:
                    print('\nERROR: Invalid request parameters.\n')
                    continue
                file_location = self.fileLocation(fileName)
                if file_location:
                    print(f'File {fileName} is here.')
                    
                elif not file_location:
                    self.sendTCPMessage('file', self.peer, 32698+self.succ1, int(fileName)%256, fileName=fileName, original=self.peer)
                    print(f'File {fileName} is not stored here.')
                    print(f'File request message has been forwarded to my successor.')

            elif command.split()[0] == 'quit':
                self.sendTCPMessage('ask', self.peer, 32698+self.pred1, 'quit', succ1=self.succ1, succ2=self.succ2)
                self.sendTCPMessage('ask', self.peer, 32698+self.pred2, 'quit', succ1=self.succ1, succ2=self.succ2)
                self.run = False


if __name__ == '__main__':
    instance = CDHT(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]))
