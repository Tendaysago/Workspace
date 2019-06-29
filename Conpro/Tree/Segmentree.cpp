#include<bits/stdc++.h>
using namespace std;
const int INF=1e9;
//区間の最小値の更新や,区間の和が出せる最も基本的なセグメントツリー
//遅延評価なし
struct SegmentTree
{
private:
    int n;
    vector<int> node;

public:
    SegmentTree(vector<int> v)
    {
        int sz=v.size();
        n=1;while(n<sz) n*=2;
        node.resize(2*n-1,INF);

        for(int i=0;i<sz;i++) node[i+n-1]=v[i];
        for(int i=n-2;i>=0;i--) node[i]=min(node[2*i+1],node[2*i+2]);
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

    void add(int k,int val)
    {
        k+=(n-1);
        node[k]+=val;
        while(k>0)
        {
            k=(k-1)/2;
            node[k]=node[2*k+1]+node[2*k+2];
        }
    }
    // 要求区間 [a, b) 中の要素の最小値を答える
    // k := 自分がいるノードのインデックス
    // 対象区間は [l, r) にあたる

    int getmin(int a,int b,int k=0,int l=0,int r=-1)
    {
        //最初に呼び出された時の対象区間は[0,n)
        if(r<0) r=n;
        //要求区間と対象区間が交わらない
        if(r<=a || b<=l) return INF;
        //要求区間が対象区間を完全に被覆
        if(a<=l && r<=b) return node[k];
        //要求区間が対象区間の一部を被覆
        int vl=getmin(a,b,2*k+1,l,(l+r)/2);
        int vr=getmin(a,b,2*k+2,(l+r)/2,r);
        return min(vl,vr);
    }
    int getsum(int a,int b,int k=0,int l=0,int r=-1)
    {
        if(r<0) r=n;
        if(r<=a || b<=l) return 0;
        if(a<=l && r<=b)return node[k];
        int vl=getsum(a,b,2*k+1,l,(l+r)/2);
        int vr=getsum(a,b,2*k+2,(l+r)/2,r);
        return vl+vr;
    }
};


