#include<iostream>
#include<vector>
#include<string>
#include<cstring>
#include<iomanip>
#include<algorithm>
#include<list>
#include<queue>
#include<set>
using namespace std;
typedef long long ll;
typedef vector<int> vi;
const int MAX=100005;
const int inf=1e9;
vi G[MAX];
int N;
bool visited[MAX];
typedef pair<int,int> P;
int prenum[MAX],parent[MAX],lowest[MAX],timer;
vector<P> bridge;
void dfs(int current,int prev)
{
  prenum[current]=lowest[current]=timer;
  timer++;

  visited[current]=true;
  int next;
  for(int i=0;i<G[current].size();i++)
  {
    next=G[current][i];
    if(!visited[next])
    {
      parent[next]=current;
      dfs(next,current);
      lowest[current]=min(lowest[current],lowest[next]);
      if(prenum[current]<lowest[next]) bridge.push_back(P(min(current,next),max(current,next)));
    }
    else if(next!=prev)
    {
      lowest[current]=min(lowest[current],prenum[next]);
    }
  }
}

void bridge_points()
{
  timer=1;
  dfs(0,-1);
  sort(bridge.begin(),bridge.end());
  for(int i=0;i<bridge.size();i++)
  {
    cout << bridge[i].first << ' ' << bridge[i].second << endl;
  }
}

int main(void)
{
  int m;
  cin >> N >> m;
  memset(visited,false,sizeof(visited));
  for(int i=0;i<m;i++)
  {
    int s,t;
    cin >> s>> t;
    G[s].push_back(t);
    G[t].push_back(s);
  }
  bridge_points();
}

