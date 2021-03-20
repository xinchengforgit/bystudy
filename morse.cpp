#include <windows.h>
#include <map>
#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <ctime> 
#include  <algorithm>
using namespace std;
map<char, string> m;
string rec, po;
//初始化摩斯密码与字符的map 
void init()
{
    m['A'] = ".- ", m['B'] = "-... ", m['C'] = "-.-. ", m['D'] = "-..", m['E'] = ". ", m['F'] = "..-. ", m['G'] = "--. ", m['H'] = ".... ", m['I'] = ".. ",
    m['J'] = ".--- ", m['K'] = "-.- ", m['L'] = ".-.. ", m['M'] = "-- ", m['N'] = "-. ", m['O'] = "--- ", m['P'] = ".--. ", m['Q'] = "--.- ", m['R'] = ".-. ",
    m['S'] = "... ", m['T'] = "- ", m['U'] = "..- ", m['V'] = "...- ", m['W'] = ".-- ", m['X'] = ".-- ", m['Y'] = "-.-- ", m['Z'] = "--.. ", m['1'] = ".---- ",
    m['2'] = "..--- ", m['3'] = "...-- ", m['4'] = "....- ", m['5'] = "..... ", m['6'] = "-.... ", m['7'] = "--... ", m['8'] = "---.. ", m['9'] = "----. ", m['0'] = "----- ";
}
string upper(string str)
{
	  for( int i=0;i<str.size();i++)
    {
    	if(str[i]>='a'&&str[i]<='z')
    	str[i]=str[i]+'A'-'a';
	}
	return str;
}
void mycin()
{
	string temp;
	rec="";
	while(cin>>temp)
	{
		if(temp=="K"){
			rec+=temp;
			break;}
		rec+=temp;
		rec+="   ";
	}
}
void imitate_human(string s)
{
	int r1,r2,r3;//随机数r1用来模拟人类发报时的随机抖动;随机数r2用来模拟人类发报时可能产生的错误  
	 s=upper(s);
    for (int i = 0; i < s.size(); i++){
    	if(s[i]==' ')
    	po+=' ';
    	else
    	po+=m.find(s[i])->second;
	}
   	int t1=528,s_time=333;
   	char op;
   	printf("请问是否需要手动调节频率(1代表低，2代表中，3代表高)，时间(1代表快，2代表慢).\n输入(Y/N)\n");
   	cin>>op;
   	if(op=='Y'||op=='y'){
   		int n1,n2;
		cin>>n1>>n2;
		if(n1==1)	t1=400;
		if(n1==2)   t1=528;
		if(n1==3)   t1=800;
		if(n2==1)   s_time=200;
		if(n2==2)   s_time=333;
	   }
	int mark=-1;//当i==mark时表示人此时发现自己已经有字母的摩斯电码发错了 
	//模拟人类发报的过程 
   	for(int i=0;i<po.size();i++)
   	{
   		if(i==mark){
   			for(int j=1;j<=8;j++){
   				cout<<'.';
   				Beep(t1,300);
			   }
			cout<<"   ";
			Sleep(1000);
			i=0,mark=-1; //重置i重新发送摩斯密码 
		   }
   		if(po[i]=='.'){
   			//r2是一个随机数，如果r2==1则表示人类此时出现了错误,此处是为了模拟时间增长，人犯错的概率增大
   			r2=rand()%(200-(int)(i*0.4)); 
   			if(r2==1){
   			r3=rand()%3+1; 
   			mark=min(r3+i,(int)po.size());
   			cout<<'-';
   			Beep(t1,600);
			   }
			else{
			cout<<po[i];
   			Beep(t1,300);}}
   		else if(po[i]=='-'){
   			r2=rand()%(200-(int)(i*0.4));
   			if(r2==1){
   			r3=rand()%3+1; 
   			if(mark>0)
   				//如果之前已有一个字母发错，且还未发现,此时又按错了一个键,那么再度随机出来的mark必须要<=那个mark
   				mark=min(min(mark,r3+i),(int)po.size()); 
			else
				mark=min(r3+i,(int)po.size()); 
			   cout<<'.';
			   Beep(t1,300);}
			else{
   			cout<<po[i];
   			Beep(t1,600);}}
   		else{
   			cout<<" "; 
   			r1=rand()%5;
   			Sleep(s_time+r1*100);}
	   }
}
int main()
{
	srand((unsigned int)time(NULL)); 
	mycin();
	init();
   	imitate_human(rec);
    system("pause");
}
