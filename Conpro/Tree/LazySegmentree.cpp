#include<bits/stdc++.h>
using namespace std;
const int INF=1e9;
typedef long long ll;
//区間加算,区間和を行えるセグメントツリー
//遅延評価あり
struct LazySegmentTree
{
private:
    int n;
    vector<ll> node,lazy;

public:
    LazySegmentTree(vector<ll> v)
    {
        int sz=v.size();
        n=1;while(n<sz) n*=2;
        node.resize(2*n-1);
        lazy.resize(2*n-1,0);

        for(int i=0;i<sz;i++) node[i+n-1]=v[i];
        for(int i=n-2;i>=0;i--) node[i]=min(node[2*i+1],node[2*i+2]);
    }
    //k番目のノードについて遅延評価を行う
    void eval(int k,int l,int r)
    {
        //遅延配列が空でない場合,自ノード及び子ノードへの値の伝播が起こる
        if(lazy[k]!=0)
        {
            node[k]+=lazy[k];
            //最下段かどうかの確認
            //子ノードは親ノードの1/2の範囲なので,
            //遅延配列の値を伝播させる時は半分にして伝播する.
            if(r-l>1)
            {
                lazy[2*k+1]+=lazy[k]/2;
                lazy[2*k+2]+=lazy[k]/2;
            }
            //伝播し終わったら,自ノードの遅延配列を0にする
            lazy[k]=0;
        }
    }
    void update(int x,int val)
    {
        x+=(n-1);
        node[x]=val;
        while(x>0)
        {
            x=(x-1)/2;
            node[x]=min(node[2*x+1],node[2*x+2]);
        }
    }
    // k := 自分がいるノードのインデックス
    // 対象区間は [l, r) にあたる
    //区間加算
    void add(int a,int b,ll x,int k=0,int l=0,int r=-1)
    {
        //最初に呼び出された時の対象区間は[0,n)
        if(r<0) r=n;
        //k番目のノードに対して遅延評価を行う
        eval(k,l,r);
        //要求区間と対象区間が交わらないなら何もしない
        if(r<=a || b<=l) return;
        //要求区間が対象区間を完全に被覆しているなら,
        //遅延配列に値を入れた後に評価
        if(a<=l && r<=b) 
        {
            lazy[k]+=(r-l)*x;
            eval(k,l,r);
        }
        //要求区間が対象区間の一部を被覆している場合は,
        //子ノードの値を再帰的に計算して,
        //計算ずみの値をもらってくる.
        else
        {
            add(a,b,x,2*k+1,l,(l+r)/2);
            add(a,b,x,2*k+2,(l+r)/2,r);
            node[k]=node[2*k+1]+node[2*k+2];
        }
    }
    //区間話の取得
    ll getsum(int a,int b,int k=0,int l=0,int r=-1)
    {
        if(r<0) r=n;
        if(r<=a || b<=l) return 0;
        //被覆し得たら遅延評価からスタート.
        eval(k,l,r);
        if(a<=l && r<=b)return node[k];
        ll vl=getsum(a,b,2*k+1,l,(l+r)/2);
        ll vr=getsum(a,b,2*k+2,(l+r)/2,r);
        return vl+vr;
    }
};

int main(void)
{
    int N,Q,query,s,t,x;
    cin >> N >> Q;
    LazySegmentTree seg(vector<ll>(N,0));
    for(int i=0;i<Q;i++)
    {
        cin >> query;
        if(query==0)
        {
            cin >> s >> t >> x;
            seg.add(s-1,t,x);
        }
        else
        {
            cin >> s >> t;
            cout << seg.getsum(s-1,t) << endl;
        }
        
    }
}

