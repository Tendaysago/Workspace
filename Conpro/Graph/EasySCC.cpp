#include<bits/stdc++.h>
//蟻本を基にした
//強連結成分分解(比較的実装しやすい方)
//2-SAT(xかつyの充足判定)への利用や,有向グラフを縮約してDAGにする効果がある.
//DAGになればDPやトポロジカルソートができるようになる.
using namespace std;
typedef long long ll;
const int MAXV=1e5+5;
int V;//頂点数
bool visited[MAXV];
vector<int> G[MAXV];//有向グラフの隣接リスト表現
vector<int> rG[MAXV];//↑のグラフの辺を逆向きにしたグラフ
vector<int> vs; //帰りがけ順の並び
int cmp[MAXV];//属する強連結成分のトポロジカル順序
void add_edge(int from,int to)
{
  G[from].push_back(to);
  rG[to].push_back(from);
}

void dfs(int v)
{
  visited[v]=true;
  for(int i=0;i<G[v].size();i++)
    {
      if(!visited[G[v][i]]) dfs(G[v][i]);
    }
  vs.push_back(v);
}

void rdfs(int v,int k)
{
  visited[v]=true;
  cmp[v]=k;
  for(int i=0;i<rG[v].size();i++)
    {
      if(!visited[rG[v][i]]) rdfs(rG[v][i],k);
    }
}

int scc()
{
  memset(visited,0,sizeof(visited));
  vs.clear();
  for (int v = 0; v < V; ++v)
    {
      //全点網羅できるようにDFSだ!
      if(!visited[v])dfs(v);
    }
  memset(visited,-1,sizeof(visited));
  int k=0;
  for(int i=vs.size()-1;i>=0;i--)
    {
      //直感的には,強連結成分の集合は[辺が逆になっても到達できる集団]だ.
      //ただの一方通行では辺が逆になると互いに行き来できなくなる.
      //互いに行き来できるのは閉路のような形に限られる.
      if(!visited[vs[i]])rdfs(vs[i],k++);
    }
  return k;//kは,強連結成分の集団の個数を表している.
}

int main(void)
{
  int E,Q;
  memset(cmp,0,sizeof(cmp));
  cin >> V >> E;
  for(int i=0;i<MAXV;i++)
    {
      G[i].clear();
      rG[i].clear();
    }
  for (int i = 0; i < E; ++i)
    {
      int fro,to;
      cin >> fro >> to;
      add_edge(fro,to);
    }
  scc();
  cin >> Q;
  for(int i=0;i<Q;i++)
    {
      int u,v;
      cin >> u >> v;
      if(cmp[u]==cmp[v]) cout << 1 << endl;
      else cout << 0 << endl;
    }
}

