#include<bits/stdc++.h>
//螺旋本を基に実装した関節点の導出
using namespace std;
typedef long long ll;
typedef vector<int> vi;
#define first fi
#define second se
const int MAX=100005;
const int inf=1e9;
vi G[MAX];
int N;
bool visited[MAX];
int prenum[MAX];//任意の頂点を視点としてDFSを行い,各頂点uの訪問の順番をprenum[u]に記録する
int parent[MAX];//DFSで生成された木Tにおけるuの親をparent[u]に記録する.
int lowest[MAX];//各頂点uについて,以下の3候補のうちの最小値
//1:prenum[u]
//2:GのBackedge(u,v)が存在するとき,頂点vにおけるprenum[v]
//Backedge(u,v)とは,頂点uからTに属する頂点vに向かうTに属さないGのエッジ.
//(↑このようなものがでる理由は,閉路などが含まる無向グラフから,DFSで恣意的に木を生成しているから!)
//(↑直感的には,無向グラフのエッジの内,Tのエッジに使われていないものがBackedgeと考えると良い)
//3:Tに属する頂点uの全ての子xに対するlowest[x];

//上記を用いて,関節点は以下のように決定される.
//1.Tの根rが二つ以上の子を持つとき(必要十分条件),rは関節点(根限定)
//2.各頂点uにおいて,uの親をpとすると,prenum[p]<=lowest[u]ならpは関節点
//2を満たしていると,頂点uと(Tにおけるuの子孫)から頂点pへのエッジがないことを表す.
int timer;

void dfs(int current,int prev)
{
  prenum[current]=lowest[current]=timer;
  //prenumは行きがけ順なので,timerをそのまま代入
  //lowestは普段は帰りがけ順のポジションだが,↑の式を使うのでちょっとminだらけに
  timer++;

  visited[current]=true;
  int next;
  for(int i=0;i<G[current].size();i++)
  {
    next=G[current][i];
    if(!visited[next])
    {
      //ノードnextへ向かう直前
      parent[next]=current;
      dfs(next,current);
      //ノードnextの探索が終わった後.
      //lowest[next]の決着もついたぞ.
      lowest[current]=min(lowest[current],lowest[next]);
    }
    else if(next!=prev)
    {
      //エッジcurrent->nextがBack-Edgeの場合
      //Back-Edgeの場合は訪問はしないので,lowest[next]は不要.
      //prenum[next]との比較だけで良い.
      lowest[current]=min(lowest[current],prenum[next]);
    }
  }
}

void art_points()
{
  timer=1;
  dfs(0,-1);
  set<int> ap;
  int np=0;
  for(int i=1;i<N;i++)
  {
    int p=parent[i];
    if(p==0) np++;
    else if(prenum[p]<=lowest[i]) ap.insert(p);
  }
  if(np>1) ap.insert(0);
  for(set<int>::iterator it =ap.begin();it!=ap.end();it++)
  {
    cout << *it << endl;
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
  art_points();
}

