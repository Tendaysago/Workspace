//http://www.deqnotes.net/acmicpc/2d_geometry/
//http://is2011.2-d.jp/moin/moin.cgi/amylase/icpc
//を参考
#include<bits/stdc++.h>
typedef complex<double> P;
typedef pair<P,double> Circle;
typedef vector<P> Polygon;
/*
complexの嬉しさ
1:実軸方向をx軸,虚軸方向をy軸と同様に見ることができる
2:四則演算,絶対値,ノルムが定義済み
3:
double x=a.real(),double y=a.imag(); x座標y座標
double length=abs(a)　ベクトルの絶対値
double distance=abs(a-b);2点A,B間の距離を求める
P b=a/abs(a) ベクトルaの単位ベクトルb
ベクトルaの二つの法線ベクトルn1,n2(n1は正の方向に90度回転,n2は負の方向に90度回転)
P n1=a*P(0,1); ex:(5,2i)*i=(-2,5i)
P n2=a*P(0,-1)

P un1=(a*P(0,+1))/abs(a);
P un2=(a*P(0,-1))/abs(a);
*/
#define EPS (1e-10)
#define EQ(a,b) (abs((a)-(b)) < EPS)

#define EQV(a,b)(EQ((a).real(),(b).real()) && EQ((a).imag(),(b).imag())
//a dot b   = a_x*b_x+a_y*b_y+a_z*b_z ⇄ |a||b|cosθ
//a cross b = (a_y*b_z-a_z*b_y , a_z*b_x-a_x*b_z , a_x*b_y-a_y*b_x) ⇄ |a||b|sinθ
//二次元の場合,z成分が全て0になると考えると良い.(結局第三要素の部分だけ残る:(0,0,a_x*b_y-a_y*b_x))
double dot(P a,P b)//内積
{
  return (a.real()*b.real()+a.imag()*b.imag());
}
double cross(P a,P b)//外積
{
  return (a.real()*b.imag()-a.imag()*b.real());
}
bool is_orthogonal(P a1,P a2,P b1,P b2)//直線a1a2と直線b1b2は垂直か?
{
  return EQ(dot(a1-a2,b1-b2),0,0);//cosθ=0に相当
}
bool is_parallel(P a1,P a2,P b1,P b2)//直線a1a2と直線b1b2は平行か?
{
  return EQ(cross(a1-a2,b1-b2),0,0);//sinθ=0に相当
}
bool is_point_on_line(P a,P b,P c)//点cは直線ab上にあるか?
{
  return EQ(cross(b-a,c-a),0.0);//sinθ=0に相当
}
bool is_point_on_seg(P a,P b,P c)//点cは線分ab上にあるか?
{
  return (abs(a-c)+abs(c-b)<abs(a-b)+EPS);
  //1行で済ませたいならこれ.直感的には,線分ab上に点cがあるなら,(aからcまでの距離+cからbまでの距離)=aからbまでの距離
}
double distance_l_p(P a,P b,P c)//直線と点の距離
{
  return abs(cross((b-a,c-a))/abs(b-a));
}
double dintance_s_p(P a,P b,P c)//線分と点の距離
{
  if(dot(b-a,c-a)<EPS) return abs(c-a);//bからみてaより更に向こう側にあるような状態
  if(dot(a-b,c-b)<EPS) return abs(c-b);//aからみてbより更に向こう側にあるような状態
  return abs(cross(b-a,c-a))/abs(b-a);//上二つの心配がないなら,点と直線の距離の手法と同じ(垂線)
}
bool is_intersected_seg(P a1,P a2,P b1,P b2)//a1,a2を端点とする線分とb1,b2を端点とする線分の交差判定
{
  //線分aからみて,b1,b2が線分aの両側に分布する事と,
  //線分bからみて,a1,a2が線分bの両側に分布する事が同時に起きると交差.
  return(cross(a2-a1,b1-a1)*cross(a2-a1,b2-a1)<EPS) &&
    (cross(b2-b1,a1-b1)*cross(b2-b1,a2-b1)<EPS);
}



int ccw(P a,P b,P c)//a→b→cと３点を進むときの進行方向
{
  b-=a;
  c-=a;
  //bは直線ab,cは直線acとなる
  if(cross(b,c)>0) return +1;//反時計回り
  if(cross(b,c)<0) return -1;//時計回り
  if(dot(b,c)<0) return +2;//a→bでUターンし,aを超えてcに　c--a--bの順.θ=180°になる状況
  if(norm(b)<norm(c)) return -2;//a--b--cの順ならaからcまでの長さの方が,aからbまでの長さより長い.または,a==bの状況
  return 0;//その他.a--c--bの順や,a==c,b==cなど(cが線分ab上にあるかの判定にも使える)
}

//交差判定系 接する場合も交差すると考える

bool isecLP(P a1,P a2,P p)//直線VS点
{
  return abs(ccw(a1,a2,p))!=1;//ccwのp--a1--a2や,a1--a2--pや,a1--p--a2になれる状況
}

bool isecLL(P a1,P a2,P b1,P b2)//直線VS直線
{
  return !isecLP(a2-a1,b2-b1,0) || isecLP(a1,b1,b2);
}

bool isecLS(P a1,P a2,P b1,P b2)//直線VS線分(bの方が線分とする)
{
  return cross(a2-a1,b1-a1)*cross(a2-a1,b2-a1)<EPS;
  //b1とb2で,直線aを境として互いに違う領域にあれば,上記の外積の掛け算が負になるぞ.
}

bool isecSS(P a1,P a2,P b1,P b2)//線分VS線分
{
  return ccw(a1,a2,b1)*ccw(a1,a2,b2)<=0 && ccw(b1,b2,a1)*ccw(b1,b2,a2)<=0;
  //重なりが確かにある事が大事.線分aからみてbの2点がaをまたいで別々の方向にあっても,
  //それだけではまだaと離れたところにある可能性がある.
  //しかし,そのような場合だと,線分bから見た時にaの2点はbをまたいで同じ方向にあるように見える.
}

P projection(P a1,P a2,P p)//点pの直線aへの射影点
{
  return a1+dot(a2-a1,p-a1)/norm(a2-a1)*(a2-a1);
}

P reflection(P a1,P a2,P p)//点pが直線aによる反射点
{
  return 2.0*projection(a1,a2,p)-p;
}

//交点を求める系列
P intersection_seg(P a1,P a2,P b1,P b2)//線分VS線分の交点を求める
{
  P b=b2-b1;
  double d1=abs(cross(b,a1-b1));
  double d2=abs(cross(b,a2-b1));
  double t=d1 / (d1+d2);
  return a1+(a2-a1)*t;
}

P intersection_lin(P a1,P a2, P b1,P b2)//直線VS直線の交点
{
  P a=a2-a1;
  P b=b2-b1;
  P c(cross(a,a1),cross(b,b1));
  return P(cross(c,P(a.real(),b.real())),cross(c,P(a.imag(),b.imag()))/cross(a,b);
}
vector<P> intersection_circle_line(P a1,P a2,circle c)//円VS直線の交点(2点or0点)
{
  vector<P> ret;
  double di=distance_l_p(a1,a2,c.first);
  double r=c.second;
  if(di+1e-9>r) return ret;
  P v=(a2-a1);
  v/=abs(v);
  P rv=v*P(0,1);
  rv*=di;
  if(distance_l_p(a1,a2,c.first+rv)>di+1e-9) rv=-rv;
  v*=sqrt(r*r-di*di);
  ret.push_back(c.first+rv-v);
  ret.push_back(c.first+rv+v);
  return ret;
}