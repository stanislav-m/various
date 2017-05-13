#include <map>
#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

class Contact
{
public:
    void add(const std::string& name)
    {
      m_data.insert(std::pair<std::string, int>(name, name.size()));
    }
    int find(const std::string& name)
    {
			auto ret = m_data.equal_range(name);
			return std::distance(ret.first, ret.second);
    }
private:
    std::map<std::string, int> m_data;
};

int main(){
    Contact cnt;
    int n;
    cin >> n;
    for(int a0 = 0; a0 < n; a0++){
        string op;
        string contact;
        cin >> op >> contact;
        if (op == "add")
        {
            cnt.add(contact);    
        }
        else
        if (op == "find")
        {
            cout << cnt.find(contact) << endl;    
        }
    }
    return 0;
}

