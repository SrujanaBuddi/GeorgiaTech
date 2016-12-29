#include <iostream>
#include <vector>


vector<int> rotateArray(vector<int> &A, int B) {
	vector<int> ret; 
	for (int i = 0; i < A.size(); i++) {
		ret.push_back(A[i + B]);
	}
	for (int i=0;i<B;i++)
{	ret.push_back(A[i])
	}
	return ret; 
}

int main()
{
std::vector <int> myvector;
for (int i=0;i<10;i++) 
myvector.push_back(i)

myvector = rotateArray(myvector, 3);
                                                 
  std::cout << "myvector contains:";
  for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    std::cout << ' ' << *it;
  std::cout << '\n';

  return 0;
}

