#include <map>
#include <set>
#include <list>
#include <cmath>
#include <ctime>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <bitset>
#include <cstdio>
#include <limits>
#include <vector>
#include <climits>
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <numeric>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <unordered_map>

using namespace std;

long long count_inversions(vector<int> a) {
    long long res = 0;
    auto prev = a.begin();
    auto b = a.begin();
    auto e = a.end();
    for (auto it = b; it != e; ++it) {
        if (it == prev)
            continue;
        auto ins = std::upper_bound(b, prev, *it);
        prev = it;
        if ((ins != e) && (*it < *ins))  {
            auto d = std::distance(ins, it); 
            std::cerr << "ins=" << *ins << " it=" << *it <<  " d=" << d << std::endl;
            std::swap(*it, *ins);
            res += d;
        }
    }
    std::for_each(b, e, [&](int i){
       std::cerr << i << " ";
    });
    std::cerr << std::endl;
    return res;
}

int main(){
    int t;
    cin >> t;
    for(int a0 = 0; a0 < t; a0++){
        int n;
        cin >> n;
        vector<int> arr(n);
        for(int arr_i = 0;arr_i < n;arr_i++){
           cin >> arr[arr_i];
        }
        cout << count_inversions(arr) << endl;
    }
    return 0;
}
