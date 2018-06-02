from linepy import *


client = LINE()
client.log("Auth Token : " + str(client.authToken))

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if op.param1 not in JoinedGroups:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
                group = client.getGroup(op.param1)
                targets = []
                for g in group.members:
                    targets.append(g.mid)
                if targets == []:
                    client.leaveGroup(op.param1)
                    JoinedGroups.removm(op.param1)
                else:
                    for target in targets:
                        try:
                           client.kickoutFromGroup(op.param1,[target])
                           print (op.param1,[g.mid])
                        except:
                           client.leaveGroup(op.param1)
                           JoinedGroups.remove(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return
    
oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})


while True:
    oepoll.trace()
