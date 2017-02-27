import networkx as nx
from itertools import combinations as cmbs
import cPickle as pickle
import graphviz as pgv

TRANSFER = 0
LOAN = 1
ALL = 2

COUNTRY = 0
CLUB = 1

CLIQUE = 0
COMMUNITY = 1

#transfersData - list of jsons transfer Data dicts {name, type, OrigTeam, DestTeam, Origcountry, DestCountry, price}
#transferType - TRANSFER, LOAN OR ALL data - int indicator of data filtering
#countryOrClub - COUNTRY, CLUB- int, indicator of club data or country data relevance
def createGraph(transfersData, countryOrClub, transferType):
    moneyGraphWeights = False
    transferGraph = nx.Graph()
    for transfer in transfersData:
        if transferType == LOAN:
            if transfer["type"] != "Loan":
                continue

        elif transferType == TRANSFER:
            if transfer["type"] == "Loan" or transfer["type"] == "Free":
                continue

        nodeDataFrom = transfer["OrigTeam"]
        nodeDataTo = transfer["DestTeam"]
        if countryOrClub == COUNTRY:
            nodeDataFrom = transfer["OrigCountry"]
            nodeDataTo = transfer["DestCountry"]

        if not transferGraph.has_node(nodeDataFrom):
            transferGraph.add_node(nodeDataFrom)

        if not transferGraph.has_node(nodeDataTo):
            transferGraph.add_node(nodeDataTo)

        if nodeDataFrom == nodeDataTo:
            continue

        if transferGraph.has_edge(nodeDataFrom, nodeDataTo):
            transferGraph[nodeDataFrom][nodeDataTo]['weight'] += 1
            try:
                transferGraph[nodeDataFrom][nodeDataTo]['price'] += float(transfer['price'])
            except:
                continue
        else:
            price = transfer['price']
            if price is None:
                price = 0.0
            transferGraph.add_edge(nodeDataFrom, nodeDataTo, weight=1, price=price)

    return transferGraph

def filterNodesNotInClique(graph, nodesInClique):
    nodesInCliqueSet = []
    for clique in nodesInClique:
        for team in clique:
            if team not in nodesInCliqueSet:
                nodesInCliqueSet.append(team)
    filteredGraph = graph.copy()
    for node in graph.nodes():
        if node not in nodesInCliqueSet:
            filteredGraph.remove_node(node)
    return filteredGraph



#@param - groupList - clique list or community list, CliqueOrComm - indicator for clique or comm graph export
# builds graph from nodes that are nodes in clique or in community
def buildCliqueOrCommunityGraph(groupList, CliqueOrComm, countryOrClub):
    groupGraph = nx.Graph()
    for group in groupList:
        for team in group:
            groupGraph.add_node(team)
        for teamA in group:
            for teamB in group:
                if teamA == teamB or groupGraph.has_edge(teamA, teamB):
                    continue
                groupGraph.add_edge(teamA, teamB)
    if countryOrClub == COUNTRY:
        if CliqueOrComm == COMMUNITY:
            nx.write_graphml(groupGraph, "commCountryGraph.graphml")
        else:
            nx.write_graphml(groupGraph, "cliqueCountryGraph.graphml")
    else:
        if CliqueOrComm == COMMUNITY:
            nx.write_graphml(groupGraph, "commClubGraph.graphml")
        else:
            nx.write_graphml(groupGraph, "cliqueClubGraph.graphml")

#@param transferGraph - graph
# filter the edges  and nodes in the graph according to the number of transfers between two nodes and the amount of
#  money that was spent
def filterEdges(transferGraph):
    for nodeA, nodeB  in transferGraph.edges():
        edgeData = transferGraph.get_edge_data(nodeA, nodeB)
        if edgeData['weight'] < 2 or edgeData['price'] < 3:
            transferGraph.remove_edge(nodeA, nodeB)

    to_remove = []
    for cc in nx.connected_components(transferGraph):
        if len(cc) == 1:
            to_remove.append(list(cc)[0])

    transferGraph.remove_nodes_from(to_remove)

#@param cliqueList - list of lists, transfergraph - teams Graph, K - number of strong cliques to return
#@returns the K most significant cliques from each clique size by the number of player transfers between them
def k_strongestCliques_From_Each_Size(transferGraph, cliqueList, k):

    cliqueSize = len(cliqueList[0])
    curSizeClique = []
    kstrongestCliques = []

    cliqueList.sort(key=lambda x: len(x))
    for clique in cliqueList:
        if len(clique) != cliqueSize:
            cliqueSize += 1
            curSizeClique.sort(key=lambda x: -x[1])
            kstrongestCliques.append(curSizeClique[:k])
            curSizeClique = []
        curSizeClique.append((tuple(clique), cliqueStrength(clique, transferGraph), calcCliqueMoney(clique, transferGraph)))
    return kstrongestCliques

#@param clique - list, transfergraph - teams Graph
#@returns the number of player transfers between teams in the clique
def cliqueStrength(clique, transferGraph):
    cliqueStength = 0
    for cliqueCouple in cmbs(clique, 2):
        cliqueStength += transferGraph[cliqueCouple[0]][cliqueCouple[1]]['weight']
    return cliqueStength

#@param clique - list, transfergraph - teams Graph
#@returns the sum of money that was transfered between teams in he clique
def calcCliqueMoney(clique, transferGraph):
    cliqueMoney = 0.0
    for cliqueCouple in cmbs(clique, 2):
        try:
            price = float(transferGraph.get_edge_data(cliqueCouple[0], cliqueCouple[1])['price'])
        except:
            price = 0.0
        cliqueMoney += price
    return cliqueMoney


def extractTeamInCliques(team, cliques):
    teamInCliques = []
    numOfTeamsInSameCliques = 0
    for i in range(len(cliques)):
        if team in cliques[i]:
            teamInCliques.append(i)
    # if len(teamInCliques) == 0:
    #     return -1
    return teamInCliques

def isTeamInSameClique(transferTeam, indexesOfCliques,cliques):
    for cliqueIndex in indexesOfCliques:
        if transferTeam in cliques[cliqueIndex]:
            return True
    return False

def calcMean(transferGraph):
    teamTransferNumber = []
    for team in nx.nodes(transferGraph):
        sumTransfers = 0
        transfers = nx.edges(transferGraph, team)
        for transfer in transfers:
            sumTransfers += transferGraph.get_edge_data(transfer[0], transfer[1])['weight']
        teamTransferNumber.append(sumTransfers)
    return sorted(teamTransferNumber)[int(len(teamTransferNumber) / 2)]


def calcStatistics(transferGraph, cliques):
    cliquesTeamStrengths = []
    for clique in cliques:
        allAndCommunityTransfer = []
        for team in clique:
            sumAllTransfers = 0
            transfersInClique = 0
            teamTransfers = nx.edges(transferGraph, team)
            numOfTeamsInSameCliques = 0
            for transfer in teamTransfers:
                edgeWeight = transferGraph.get_edge_data(transfer[0], transfer[1])['weight']
                if transfer[1] in clique:
                    transfersInClique += edgeWeight
                    numOfTeamsInSameCliques += 1
                sumAllTransfers += edgeWeight

            allAndCommunityTransfer.append((team, (sumAllTransfers - transfersInClique), len(teamTransfers) - numOfTeamsInSameCliques, transfersInClique, numOfTeamsInSameCliques))

        cliquesTeamStrengths.append(allAndCommunityTransfer)
    return cliquesTeamStrengths



if __name__ == "__main__":
    transfersData = pickle.load(open("transferDataArray.p", "rb"))
    clubNumTransferGraph = createGraph(transfersData, CLUB, TRANSFER)
    origtransferGraph = clubNumTransferGraph.copy()
    print("-----------------------FULL DATA GRAPH----------------------------------------------------")
    print("The number of nodes in the graph is: ", clubNumTransferGraph.number_of_nodes())
    print("The number of edges in the graph is: ", clubNumTransferGraph.number_of_edges())
    print("The number of connected component in the graph is: ", nx.number_connected_components(clubNumTransferGraph))

    print("--------------------------------NUM TRANSFERS DATA-------------------------------------------")

    filterEdges(clubNumTransferGraph)
    print("The number of nodes in the NUM TRANSFERS graph is: ", clubNumTransferGraph.number_of_nodes())
    print("The number of edges in the NUM TRANSFERS graph is: ", clubNumTransferGraph.number_of_edges())
    print("The number of connected component in the NUM TRANSFERS graph is: ", nx.number_connected_components(clubNumTransferGraph))

    # extract all max Cliques From The Graph
    cliqueList = list(nx.find_cliques(clubNumTransferGraph))
    print("The number of cliques is: ", len(cliqueList))

    # Filter The Less Significant Cliques arrange them by size and print the significant Cliques
    strongestCliques = k_strongestCliques_From_Each_Size(clubNumTransferGraph, cliqueList, 5)
    for clique in strongestCliques:
        print (clique)

    #unify all cliques in one list
    allStrongestCliques = []
    for sublist in strongestCliques:
        for clique in sublist:
            allStrongestCliques.append(clique[0])

    nodesInCliquesGraph = filterNodesNotInClique(clubNumTransferGraph, allStrongestCliques)
    nx.write_graphml(nodesInCliquesGraph, "filteredCountryGraph.graphml")
    #build significant clique Graph
    buildCliqueOrCommunityGraph(allStrongestCliques, CLIQUE, COUNTRY)

    print("----------------------------The Communities are:----------------------------------------------")

    # extract communities from the graph by the most significant cliques
    communityList = list(nx.k_clique_communities(clubNumTransferGraph, 3, allStrongestCliques))
    for community in communityList:
        print (community, calcCliqueMoney(community, clubNumTransferGraph))


    print("------------------------------------statistics-----------------------------------------------------")

    cliqueAfterFilter = calcStatistics(clubNumTransferGraph, allStrongestCliques)

    print("means Before:", calcMean(origtransferGraph))
    print("means After:", calcMean(clubNumTransferGraph))

    print("-----------------------after filtering community ratio:-----------------------------")
    sumAvg = 0
    counter = 0
    cliqueAvg = 0
    for clique in cliqueAfterFilter:
        print("clique: ", clique)
        for team in clique:
            teamCliqueAvg = team[3]/float(team[4])
            teamnotCliqueAvg = team[1]/float(team[2])
            sumAvg += teamCliqueAvg / teamnotCliqueAvg
            cliqueAvg += teamCliqueAvg / teamnotCliqueAvg
            counter += 1
            print(team[0], teamCliqueAvg, teamnotCliqueAvg, teamCliqueAvg / teamnotCliqueAvg)
        print("clique Average:", cliqueAvg/len(clique))
        cliqueAvg = 0
    print("----------AVG AFTER: ", sumAvg / float(counter), "------------------")

    #build community graph
    buildCliqueOrCommunityGraph(communityList, COMMUNITY, COUNTRY)


    nx.write_graphml(clubNumTransferGraph, "transferCountryGraph.graphml")