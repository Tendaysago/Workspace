#include<bits/stdc++.h>
//螺旋本を基に実装.実によくあるダイクストラ法.
using namespace std;
const int inf=1e9+5;
const int maxn=100000;
typedef vector<int> vi;
typedef long long ll;
#define fi first
#define se second
typedef pair<int,int> P;
vector<pair<int,int> > Edge[maxn+5];
//今回firstはその地点での距離,secondは行き先だが,
//構造体やクラスでも表現できるようになると表現の幅が広がるぞ.
int d[maxn+5];
//この実装では,「その地点でのスタートからの最短距離」だが,
//そのほかの形式で状態を与えられる事もある.
//状態を考慮し,ある種のDPと捉えて解決できるようにしよう.
bool visited[maxn+5];
//↑も,ある状態を訪れたかどうかで与えられる事もある.
int v,e,r;

void dijkstra(int s)
{
  memset(visited,false,sizeof(visited));
  for(int i=0;i<maxn+5;i++)
  {
    d[i]=inf;
  }
  priority_queue<P,vector<P>,greater<P> > que;
  //greater<型>をクラスや構造体で使えるようにするのは難しい.
  //pair<距離(int),状態>と表現しておけば困らずにすみそうなので,状態に距離の情報は入れないでおこう.
  d[s]=0;
  que.push(P(0,s));
  while(!que.empty())
  {
    P f=que.top();que.pop();
    int u=f.se;
    visited[u]=true;
    if(d[u]<f.fi) continue;
    for(int j=0;j<Edge[u].size();j++)
    {
      int v=Edge[u][j].se;
      if(visited[v]) continue;
      if(d[v]>d[u]+Edge[u][j].fi)
      {
        d[v]=d[u]+Edge[u][j].fi;
        que.push(P(d[v],v));
      }
    }
  }
  for(int i=0;i<v;i++)
  {
    if(d[i]==inf)
    {
      cout << "INF" << endl;
    }
    else
    {
      cout << d[i] << endl;
    }
  }
}

int main(void)
{
  cin >> v >> e>> r;
  for(int i=0;i<e;i++)
  {
    int s,t,d;
    cin >> s >> t >> d;
    Edge[s].push_back(P(d,t));
    //Edge[t].push_back(P(d,s));
  }
  dijkstra(r);
}
