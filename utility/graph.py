import networkx as nx
from networkx.algorithms import community
import pandas as pd

class Graph_reader(object):

    def __init__(self,path,type=1):
        super(Graph_reader,self).__init__()

        if(type==1):
            self.df = pd.read_csv(path, sep="\s+", skiprows=0,  usecols=[0,1],names=['id_u','id_c'])
            self.g = nx.from_pandas_edgelist(self.df,source='id_u',target='id_c')
        else:
            self.df = pd.read_csv(path, sep="\s+", skiprows=1,  usecols=[0,1],names=['id_u','id_c'])
            self.g = nx.from_pandas_edgelist(self.df,source='id_u',target='id_c')

        self.communities = community.louvain_communities(self.g,seed=420)

    def find_top_k(self,user,list_follow,k):
        for i in range(len(self.communities)):
            if user in self.communities[i]:
                comm=i
                break
        
        top_k=[]
        follow_in_commu = [f for f in list_follow if f in self.communities[comm]]
        for u in follow_in_commu:
            nb_followers = len(self.df.loc[self.df["id_u"==u,"id_c"]])
            top_k.append([u,nb_followers])
        
        top_k.sort(key=get_nb_follow,reverse=True)

        if len(top_k<k):
            return top_k
        else:
            return top_k[:k]
        
    def get_nb_follow(elem):
        return elem[1]