#include<bits/stdc++.h>
//螺旋本を基に実装.実によくあるベルマンフォード法.
using namespace std;
const int inf=1e9+5;
const int maxn=100000;
typedef vector<int> vi;
typedef long long ll;
#define fi first
#define se second
typedef pair<int,int> P;
//今回firstはその地点での距離,secondは行き先だが,
//構造体やクラスでも表現できるようになると表現の幅が広がるぞ.
int d[maxn+5];
//この実装では,「その地点でのスタートからの最短距離」だが,
//そのほかの形式で状態を与えられる事もある.
//状態を考慮し,ある種のDPと捉えて解決できるようにしよう.
bool visited[maxn+5];
//↑も,ある状態を訪れたかどうかで与えられる事もある.
int v,e,r;

struct Edge
{
  int cost,to;
  Edge(int _cost,int _to):cost(_cost),to(_to){}
};

vector<Edge> adj[maxn];
bool nega=false;
void bellman_ford(int n,int s)
{
  for(int i=0;i<n;i++)
  {
    d[i]=inf;
  }
  d[s]=0;
  //priority_queueによる枝刈りは無く,ある種の全探索と言える.
  //素直に全点からそれにつながる点を列挙しつつコストが下がるながらコストを減らす動きをとるが,
  //↑の手順でいくらでもコストを下げられる場合はn回↑の手順を行なってもコストが減り続けるので
  //負の辺を含んでいる.
  for(int i=0;i<n;i++)
  {
    for(int v=0;v<n;v++)
    {
      for(int k=0;k<adj[v].size();k++)
      {
        Edge e=adj[v][k];
        if(d[v]!= inf && d[e.to]>d[v]+e.cost)
        {
          d[e.to]=d[v]+e.cost;
          if(i==n-1) 
          {
            nega=true;
            return;
          }
        }
      }
    }
  }
  return;
}


int main(void)
{
  cin >> v >> e>> r;
  for(int i=0;i<e;i++)
  {
    int s,t,d;
    cin >> s >> t >> d;
    adj[s].push_back(Edge(d,t));
    //Edge[t].push_back(P(d,s));
  }
  bellman_ford(v,r);
  if(nega)
  {
    cout << "NEGATIVE CYCLE" << endl;
    return 0;
  }
  else
  {
    for(int i=0;i<v;i++)
    {
      if(d[i]==inf)
      {
        cout << "INF" << endl;
      }
      else cout << d[i] << endl;
    }
  }
  return 0;
}
