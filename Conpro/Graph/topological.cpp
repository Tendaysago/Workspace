#include<bits/stdc++.h>
//トポロジカルソート
using namespace std;
typedef long long ll;
typedef vector<int> vi;
#define first fi
#define second se
const int MAX=100000;
const int inf=1e9;
vi G[MAX];
list<int> out;
bool V[MAX];
int indeg[MAX];
int v,e;
void bfs(int s)
{
  queue<int> q;
  q.push(s);
  V[s]=true;
  while(!q.empty())
  {
    int u=q.front();q.pop();
    out.push_back(u);
    for(int i=0;i<G[u].size();i++)
    {
      int v=G[u][i];
      indeg[v]--;
      if(indeg[v]==0 && !V[v])
      {
        V[v]=true;
        q.push(v);
      }
    }
  }
}
void tsort()
{
  for(int i=0;i<v;i++)
  {
    indeg[i]=0;
  }
  for(int u=0;u<v;u++)
  {
    for(int i=0;i<G[u].size();i++)
    {
      int v=G[u][i];
      indeg[v]++;
    }
  }
  for(int u=0;u<v;u++)
  {
    if(indeg[u]==0 && !V[u]) bfs(u);
  }
  for(list<int>::iterator it=out.begin();it!=out.end();it++)
  {
    cout << *it << endl;
  }
}
int main(void)
{
  cin >> v >> e;
  for(int i=0;i<v;i++)
  {
    V[i]=false;
  }
  for(int i=0;i<e;i++)
  {
    int s,t;
    cin >> s>> t;
    G[s].push_back(t);
  }
  tsort();
}

