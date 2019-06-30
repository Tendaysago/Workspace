#include<bits/stdc++.h>
typedef long long ll;
using namespace std;
const int MOD=1e9+7;
const int MAX_N=1e7;
ll gcd(ll a, ll b)
{
    if(b==0) return a;
    return gcd(b,a%b);
}
ll extgcd(ll a, ll b,ll& x,ll& y)
{
 ll d=a;
 if(b!=0)
 {
  d=extgcd(b,a%b,y,x);
  y-=(a/b)*x;
 }
 else
 {
  x=1;y=0;
 }
 return d;
}
ll mod_pow(ll x,ll n,ll mod)
{
    ll res=1;
    while(n>0)
    {
        if(n&1) res=res*x%mod;
        x=x*x%mod;
        n >>=1;
    }
    return res;
}
ll comb[2005][2005];
void combinit()
{
  for(int i=0;i<=2000;i++)
  {
    for(int j=0;j<=i;j++)
    {
      if(j==0 || j==i) comb[i][j]=1;
      else
      {
        comb[i][j]=(comb[i-1][j-1]+comb[i-1][j])%MOD;
      }

    }
  }
}
bool judge_prime(ll n)
{
 for(ll i=2;i*i<=n;i++)
 {
  if(n%i==0) return false;
 }
 return n!=1;
}

vector<ll> divisor(ll n)
{
 vector<ll> res;
 for(ll i=1;i*i<=n;i++)
 {
  if(n%i==0)
  {
   res.push_back(i);
   if(i!=n/i) res.push_back(n/i);
  }
 }
 return res;
}

map<ll,ll> prime_factor(ll n)
{
 map<ll,ll> res;
 for(ll i=2;i*i<=n;i++)
 {
  while(n%i==0)
  {
   ++res[i];
   n/=i;
  }
 }
 if(n!=1) res[n]=1;
 return res;
}

ll prime[MAX_N];
bool is_prime[MAX_N+5];

ll sieve(ll n)
{
 ll p=0;
 for(ll i=0;i<=n;i++) is_prime[i]=true;
 is_prime[0]=is_prime[1]=false;
 for(ll i=2;i<=n;i++)
 {
  if(is_prime[i])
  {
   prime[p++]=i;
   for(ll j=2*i;j<=n;j+=i) is_prime[j]=false;
  }
 }
 return p;
}
 
