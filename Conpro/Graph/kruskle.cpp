#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef vector<int> vi;
#define first fi
#define second se
const int MAX=100000;
const int inf=1e9;
//最小全域木(クラスカル法)
//UnionFindはもちろん必須!(なのでUnionFindも同封のつもり)
//これに載せているのは,サイズ付き標準UnionFind.
vi G[MAX];
list<int> out;
bool V[MAX];
int indeg[MAX];
int v,e;

const int MAX_N=1e5+5;
class UnionFind
{
    int par[MAX_N];
    int rnk[MAX_N];
    int sizes[MAX_N];
    public:
    void init(int n)
    {
        for(int i=0;i<n;i++)
        {
            par[i]=i;
            rnk[i]=0;
            sizes[i]=1;
        }
    }
    int find(int x)
    {
        if(par[x]==x)
        {
            return x;
        }
        else
        {
            return par[x]=find(par[x]);
        }
    }
    void unite(int x,int y)
    {
        x=find(x);
        y=find(y);
        if(x==y) return;
        if(rnk[x]<rnk[y]) swap(x,y);
        par[y]=x;
        if(rnk[x]==rnk[y]) rnk[x]++;
        sizes[x]+=sizes[y];
    }
    bool same(int x,int y)
    {
        return find(x)==find(y);
    }
    int size(int x)
    {
        return sizes[find(x)];
    }
};

class Edge
{
  public:
  int source,target,cost;
  Edge(int source=0,int target=0,int cost=0):
  source(source),target(target),cost(cost){}
  bool operator < (const Edge &e ) const
  {
    return cost < e.cost;
  }
};

int kruskal(int N,vector<Edge> edges)
{
  int totalCost=0;
  sort(edges.begin(),edges.end());
  UnionFind uf;
  uf.init(N+1);
  for(int i=0;i<edges.size();i++)
  {
    Edge e=edges[i];
    if(!uf.same(e.source,e.target) )
    {
      totalCost+=e.cost;
      uf.unite(e.source,e.target);
    }
  }
  return totalCost;
}


int main(void)
{
  int N,M,cost;
  int source,target;
  cin >> N >> M;
  vector<Edge> edges;
  for(int i=0;i<M;i++)
  {
    cin >> source >> target >> cost;
    edges.push_back(Edge(source,target,cost));
  }
  cout << kruskal(N,edges) << endl;
  return 0;
}

