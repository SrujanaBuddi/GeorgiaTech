vector<int> Solution::allFactors(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector <int> factors;int i;
    for (i=1;i<=sqrt(int(A));i++)
    {
        if (A%i==0)
        {
            factors.push_back(i);
            if (i!=1 && i!=sqrt(int(A)))
            factors.push_back(A/i);
        }
    }
    if (A!=1)
    factors.push_back(A);
    std::sort(A.begin(),A.end());
    return factors;
}
-----------------------------------------------------------------------------------------------------
int Solution::isPrime(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int limit = sqrt(A);int i;
    if(A==1)
    {return 0;}
    for(i=2;i<=limit;i++)
    {
        if (A%i==0)
        return 0;
    }
    return 1;
}
--------------------------------------------------------------------------------------------------------

vector<int> Solution::sieve(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector <int> prime;int arr[A+1];int i,j;
    for (i=0;i<=A;i++)
        arr[i]=i;
    arr[1]=0;
    for (i=2;i<=A;i++)
    {
        if (arr[i]!=0)
        {
            for(int j=2;i*j<=A;j++)
                arr[i*j]=0;
        }
    }
    for (i=0;i<=A;i++)
    {
        if (arr[i]!=0)
            prime.push_back(i);
    }
    return prime;
}
----------------------------------------------------------------------------------------------------------
string Solution::findDigitsInBinary(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    string binary;
    if (A<=0)
        binary  +='0';
    int a = A;
    while(a>0)
    {
        if (a%2==1)
            binary+= '1';
        else 
            binary += '0';
        a /=2;
    }
    std::reverse(binary.begin(), binary.end());
    return binary;
}

-------------------------------------------------------------------------------------------------------------

vector<int> Solution::primesum(int A) {
    vector <int> primes;
        int i,j,a=A,b=A,arr[A+1];
        for (i=0;i<=A;i++)
            arr[i]=i;
        arr[1]=0;
        for (i=2;i<=A;i++)
        {
            if (arr[i]!=0)
            {
                for (j=2;i*j<=A;j++)
                    arr[i*j]=0;
            }
        }
      for(i=1;i<=A;i++)
    {
        if (arr[i]!=0 && arr[A-i]!=0 && i<=a && A-i<b && i<=A-i)
        {
            a=i;
            b=A-i;
        }
    }
    primes.push_back(a);
    primes.push_back(b);
    return primes;
}
--------------------------------------------------------------------------------------------------------------
bool Solution::isPower(int A) {
    if (A==1)
    return true;
    int n=int(sqrt(A));
    for (int i=n;i>=2;i--)
    {
        for(int j=2;j<=log2(A);j++)
        {
            int x = pow(i,j);
            if (x==A)
            return true;
        }
    }
    return false;
}
-----------------------------------------------------------------------------------------------------------
bool Solution::isPower(int A) {
    if (A==1)
    return true;
    int n=int(sqrt(A));
    for (int i=n;i>=2;i--)
    {
        for(int j=2;j<=log2(A);j++)
        {
            int x = pow(i,j);
            if (x==A)
            return true;
        }
    }
    return false;
}
-------------------------------------------------------------------------------------------------------------
int Solution::titleToNumber(string A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int score=0;
    int l = A.length();
    int x= 0;
    if (l>1)
        x=1;
    for(int i = 0;i<l;i++)
    {
       score = (A[i]-'A'+1)+ score*26;
    }
    return score;
}
----------------------------------------------------------------------------------------------------------------
string Solution::convertToTitle(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int n = A;
    string z;
    while(n>0)
    {
        int x = n%26;
        char c = char('A'+x-1);
        z.push_back(c);
        n = n/26;
    }
    std::reverse(z.begin(),z.end());
    return z;
}
--------------------------------------------------------------------------------------------------------
bool Solution::isPalindrome(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    string Ac = std::to_string(A);
    int l = Ac.length();
    int arr[l];
    int i=0;
    while(A>0)
    {
     arr[l-1-i]=A%10;
     i++;
     A=int(A/10);
    }
    for(int i=0;i<l/2;i++)
    {
        if(arr[i]!=arr[l-i-1])
        return false;
    }
    return true;
}
---------------------------------------------------------------------------------------------------------------
int Solution::reverse(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int sign = 1;
    if (A<0)
     {sign = -1;A=-A;}
    if (A>INT_MAX or A<INT_MIN)
    return 0;
    int l = std::to_string(A).length();
    int i=0,ans=0;
    while (A>0)
    {
        if(ans+(pow(10,l-i-1)*(A%10))>INT_MAX)
            return 0;
        ans = ans+(pow(10,l-i-1)*(A%10));
        A=int(A/10);
        i++;
    }
    ans = ans*sign;
    return ans;
}
------------------------------------------------------------------------------------------------------------------
int Solution::gcd(int A, int B) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int a =int(sqrt(A)), b= int(sqrt(B)),gcd=0;
    //if(A==0 or B==0)
    //return 0;
    if(A==0)
    return B;
    if(B==0)
    return A;
    if(A%B==0)
    return B;
    if(B%A==0)
    return A;
    vector <int> factorsa,factorsb;
    for (int i=1;i<=a;i++)
    {
        if (A%i==0)
        {factorsa.push_back(i);
        factorsa.push_back(A/i);}
    }
    for(int i=1;i<=b;i++)
    {
        if(B%i==0){
        factorsb.push_back(i);
        factorsb.push_back(B/i);}
    }
    for(int i =0;i<factorsa.size();i++)
    {
        int ca=factorsa[i];
        for(int j=0;j<factorsb.size();j++)
        {
            int cb = factorsb[j];
            if (ca==cb && ca>gcd)
            gcd =ca;
        }
    }
    return gcd;
}
------------------------------------------------------------------
-------------------------------------------------------
int Solution::gcd(int A, int B) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int gcd=0,a,b,q;
    if(A==0)
    return B;
    if(B==0)
    return A;
    if(A%B==0)
    return B;
    if(B%A==0)
    return A;
    if(A>B)
    {
        a=A;
        b=B;
    }
    else
    {
        a=B;
        b=A;
    }
    q=a;
    while(q!=0)
    {
        q=a%b;
        if(q==0)
            {gcd=b;}
        a=b;
        b=q;
    }
    return gcd;
}
-------------------------------------------------------------------------------------------------------------------------
int Solution::trailingZeroes(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int z=0,i=5;
    while(i<=A)
    {
        z= z+A/i;
        i=i*5;
    }
    return z;
}
---------------------------------------------------------------------------------------------------------------------
int Solution::cpFact(int A, int B) {
    int gcd=A,a,b,q,cpfact;
    while(gcd!=1)
    {
    if(A>B)
    {
        a=A;
        b=B;
    }
    else
    {
        a=B;
        b=A;
    }
    q=a;
    while(q!=0)
    {
        q=a%b;
        if(q==0)
            {gcd=b;}
        a=b;
        b=q;
    }
    A=A/gcd;
    }
    cpfact=A;
    return cpfact;
}
------------------------------------------------------------------------------------------------------------------------
int Solution::findRank(string A) {
    int l=A.length(),rank=0;
    string A_copy=A;
    std::sort(A.begin(),A.end());
    map<char, int> words = {};
    for (int j=0;j<l;j++)
    {
    words[A[j]]=j+1;
    }
for(int i=0;i<l;i++)
{
    int f=1;
    for(int k=1;k<l-i;k++)
        f=f*k;
    if (l-1-i==0)
        f=0;
    rank = rank+(words[A_copy[i]]-1)*f;
    words={};
    int temp=0;
    for (int j=0;j<l;j++)
    {
    if(A[j]!=A_copy[i])
    {words[A[j]]=temp+1;temp++;}
    }
}
rank = rank+1;
return rank%1000003;
}
------------------------------------------------------------------------------------------------------------------
int Solution::uniquePaths(int A, int B) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int k=A+B-2,n=1,d=1,steps=1;
    if(A-1==0 or B-1==0)
        {return 1;}
    for(int i=1;i<A;i++,k--)
    {
        steps*=k;
        steps/=i;
    }
    return steps;
}
-------------------------------------------------------------------------------------------------------------------------
// Input : X and Y co-ordinates of the points in order. 
// Each point is represented by (X[i], Y[i])
int Solution::coverPoints(vector<int> &X, vector<int> &Y) {
    int steps=0;int curr_steps=0,curr_x,next_x,curr_y,next_y;
    for(int i=0;i<X.size()-1;i++)
    {
        curr_steps=0;
        curr_x=X[i];
        next_x=X[i+1];
        curr_y=Y[i];
        next_y=Y[i+1];
        if(abs(curr_x-next_x)==abs(curr_y-next_y))
            curr_steps=abs(curr_x-next_x);
        else if(curr_x==next_x or curr_y==next_y)
            curr_steps=abs(curr_y-next_y)+abs(curr_x-next_x);
        else
            {
                int d = abs(curr_x-next_x)>abs(curr_y-next_y)? abs(curr_x-next_x): abs(curr_y-next_y);
                curr_steps=curr_steps+d;
            }
        steps=steps+curr_steps;
    }
    return steps;
}
-----------------------------------------------------------------------------------------------------------------------------
vector<int> Solution::plusOne(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int i=1,l=A.size();vector <int> B=A;
    B[l-1]+=1;
    if (B[l-1]==10)
        B[l-1]=0;
    while(A[l-i]==9)
    {
        B[l-i-1]+=1;
        if (B[l-i-1]==10)
            B[l-i-1]=0;
        i++;
    }
    return B;
}
-----------------------------------------------------------------------------------------------------------------------------
int Solution::maxSubArray(const vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int l=A.size(),max=INT_MIN,max_id=0;
    for(int i=0;i<l;i++)
    {
        int sum[l-i];
        for(int x=0;x<l-i;x++)
            sum[x]=0;
        sum[0]=A[i];
        if (sum[0]>max)
        {
            max=sum[0];
        }
        for(int j=i+1;j<l;j++)
        {
            sum[j-i+1]=sum[j-i]+A[j];
            if(sum[j-i+1]>max)
            {
             max=sum[j-i+1];
             max_id=i;
            }
        }
    }
    return max;
}
-----------------------------------------------------------------------------------------------------------------------------
int Solution::maxArr(vector<int> &A) {
    int l=A.size(),max1=INT_MIN,max2=INT_MIN,min1=INT_MAX,min2=INT_MAX,res;
    for(int i=0;i<l;i++)
    {
        if(A[i]-i>max1)
            max1=A[i]-i;
        if(A[i]-i<min1)
            min1=A[i]-i;
        if(A[i]+i>max2)
            max2=A[i]+i;
        if(A[i]+i<min2)
            min2=A[i]+i;
    }
    int r1=max1-min1;
    int r2=max2-min2;
    res=(r1>r2)?r1:r2;
    return res;
}
-----------------------------------------------------------------------------------------------------------------------------
vector<int> Solution::repeatedNumber(const vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    long long int sum=0,esum,sqsum=0,esqsum; int a=0,b=0,l=A.size();vector <int> res;
    esum = 0.5*l*(l+1);
    esqsum= (l)*(l+1)*(2*l+1)/6;
    for(int i=0;i<A.size();i++)
    {
        sum =sum+A[i];
        sqsum=sqsum+(A[i]*A[i]);
    }
    int diff= esum-sum;
    long long int sqdiff = esqsum-sqsum;
    int sum1= sqdiff/diff;
    a=(sum1+diff)/2;
    b=(sum1-diff)/2;
    res.push_back(b);
    res.push_back(a);
    return res;
}
-----------------------------------------------------------------------------------------------------------------------------
void Solution::setZeroes(vector<vector<int> > &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int rows=A.size(),cols=A[0].size();vector <int> r,c;
    for(int i=0;i<rows;i++)
    {
        for(int j=0;j<cols;j++)
        {
            if (A[i][j]==0)
            {
                r.push_back(i);
                c.push_back(j);
            }
        }
    }
    for(int i=0;i<r.size();i++)
    {
        int row=r[i];
        for(int j=0;j<cols;j++)
            A[row][j]=0;
    }
    for(int i=0;i<c.size();i++)
    {
        int col=c[i];
        for(int j=0;j<rows;j++)
            A[j][col]=0;
    }
}
-----------------------------------------------------------------------------------------------------------------------------
vector<vector<int> > Solution::generate(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector <vector <int> > tri;vector <int> temp;
    if (A<=0)
        return tri;
    temp.push_back(1);
    tri.push_back(temp);
   for(int i=1;i<A;i++)
    {
        temp.erase(temp.begin(),temp.end());
        temp.push_back(1);
        for(int j=1;j<i;j++)
        {
            temp.push_back(tri[i-1][j]+tri[i-1][j-1]);
        }
        temp.push_back(1);
        tri.push_back(temp);
    }
    return tri;
}
--------------------------------------------------------------------------------------------------------------------------------
vector<int> Solution::maxset(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector<int> curr_arr,subarr;int max=INT_MIN;long long int sum=0;
    for (int i=0;i<A.size();i++)
    {
        if(A[i]>=0)
        {
            if(sum+A[i]<INT_MAX)
            sum+=A[i];
            else
            sum=INT_MAX;
            curr_arr.push_back(A[i]);
            //printf("%d %d\n",sum,A[i]);
        if (sum==max and curr_arr.size()>subarr.size())
            {
            subarr=curr_arr;
            }
        if (sum>max)
            {
            subarr=curr_arr;
            max=sum;
            }
        }
        if(A[i]<0)
        {
            curr_arr.erase(curr_arr.begin(),curr_arr.end());
            sum=0;
        }
    }
    return subarr;
}
--------------------------------------------------------------------------------------------------------------------------------
int Solution::firstMissingPositive(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int l=A.size(),miss;
    for(int i=0;i<l;i++)
    {
        if(A[i]>0 and A[i]<=l)
        {
            if(A[i]-1 !=i and A[A[i]-1]!=A[i])
            {
                int temp=A[A[i]-1];
                    A[A[i]-1]=A[i];
                    A[i]=temp;
                    i--;
            }
        }
    }
     for(int i=0;i<l;i++)
            if(A[i]!=i+1)
                return i+1;
return l+1;
}
--------------------------------------------------------------------------------------------------------------------------------
bool Solution::hotel(vector<int> &arrive, vector<int> &depart, int K) {
    std::map<int,int>guests;
    for(int i=0;i<arrive.size();i++)
    {
        int a=arrive[i],d=depart[i];
        for(int x=a;x<d;x++)
        {
            guests[x]+=1;
            if (guests[x]>K)
                return false;
        }
    }
    return true;
}
--------------------------------------------------------------------------------------------------------------------------------
vector<int> Solution::wave(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    std::sort(A.begin(),A.end());int i=0;
    while(i<A.size()-1)
    {
        int temp=A[i];
        A[i]=A[i+1];
        A[i+1]=temp;
        i=i+2;
    }
    return A;
}
--------------------------------------------------------------------------------------------------------------------------------
int Solution::maximumGap(const vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    int max=INT_MIN,diff=-1;
    if(A.size()<=1)
        return 0;
    for(int i=0;i<A.size();i++)
    {
        for(int j=i+1;j<A.size();j++)
        {
            if((A[j]-A[i])>=max and j-i>diff)
            {
                max=A[j]-A[i];
                diff=j-i;
            }
        }
    }
    return diff;
}
--------------------------------------------------------------------------------------------------------------------------------
int Solution::maximumGap(const vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector <int> A_copy=A;int l=A.size(),s=l,e;
    std::sort(A_copy.begin(),A_copy.end());
    for(int i=0;i<l;i++)
    {
        if(A_copy[0]==A[i] and i<s)
            s=i;
        if(A_copy[l-1]==A[i])
            e=i;
    }
    if (s-e>0)
        return e-s;
    else
        return 0;
}
---------------------------------------------------------------------------------------------------------------------------------
vector<vector<int> > Solution::prettyPrint(int A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout www.interviewbit.com/pages/sample_codes/ for more details
    vector <vector <int>> matrix;
    vector <int> temp;
    for(int i=0;i<2*A-1;i++)
        temp.push_back(A);
    for(int i=0;i<2*A-1;i++)
        matrix.push_back(temp);   
    for(int i=0;i<A;i++)
    {
        for (int j=i;j<2*A-i-1;j++)
        {
         int m=i<j?i:j;
         matrix[i][j]=A-m;
         matrix[j][i]=A-m;
         matrix[2*A-2-i][j]= A-m;
         matrix[j][2*A-2-i]= A-m;
        }
    }
    //matrix[2*A-1][2*A-1]=A-1;
  return matrix;  
}
---------------------------------------------------------------------------------------------------------------------------------

