import time
import hashlib
class Block:
    def __init__(self, index, proof, previoushash, transactions):
        self.index = index
        self.proof = proof
        self.previoushash = previoushash
        self.transactions = transactions
        self.timestamp = time.time()
    @property
    def getblockhash(self):
        blockstring = "{}{}{}{}{}".format(self.index, self.proof, self.previoushash, self.transactions, self.timestamp)
        return hashlib.sha256(blockstring.encode()).hexdigest()
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof, self.previoushash, self.transactions, self.timestamp)


class BlockChain:
    def __init__(self):
        self.chain=[]
        self.currentnodetransactions=[]
        self.nodes=set()
        self.createfirstblock()

    def createfirstblock(self):
        self.createnewblock(proof=0,previoushash=0)

    def createnewblock(self,proof,previoushash):
        block = Block(
            index=len(self.chain),
            proof=proof,
            previoushash=previoushash,
            transactions=self.currentnodetransactions
        )
        self.currentnodetransactions=[]  
        self.chain.append(block)
        return block

    def createnewtransaction(self,sender,recipient,amount):
        self.currentnodetransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return True

    @staticmethod
    def createproofofwork(previousproof):
        proof=previousproof + 1
        while not BlockChain.isvalidproof(proof,previousproof):
            proof=proof+1

        return proof

    @staticmethod
    def isvalidproof(proof, previousproof):
        return (proof + previousproof) % 7 == 0

    @property
    def getlastblock(self):
        return self.chain[-1]

    def mine(self,sendingperson,transamount,mineraddress):
        self.createnewtransaction(
            sender=sendingperson,
            recipient=mineraddress,
            amount=transamount,
        )
        lastblock=self.getlastblock
        lastproof=lastblock.proof
        proof=self.createproofofwork(lastproof)
        lasthash=lastblock.getblockhash
        block=self.createnewblock(proof,lasthash)

blockchain=BlockChain()
blockchain.mine("alice",25,"bob")
blockchain.mine("alice",30,"tom")
print(blockchain.chain)

  
