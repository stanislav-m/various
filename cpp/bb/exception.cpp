#include <iostream>

class A {
	public:
		A(): m_x(0)
		{
			std::cout << "constr A()" << std::endl;
		}
		A(int x) : m_x(x)
		{
			std::cout << "constr A(" << x << ")" << std::endl;
		}
		~A()
		{
			std::cout << "destr ~A(): " << m_x << std::endl;
		}
	private:
		int m_x;
};

class B {
	public:
		B()
		{
			std::cout << "constr B()" << std::endl;
		}
		~B()
		{
			std::cout << "destr ~B()" << std::endl;
		}
};

void f3()
{
	std::cout << "start of f3()" << std::endl;
	A a(3); 
	std::cout << "throw" << std::endl;
	throw 3;
	std::cout << "end of f3()" << std::endl;
}

void f2()
{
	std::cout << "start of f2()" << std::endl;
	A a(2);
	f3();
	std::cout << "end of f2()" << std::endl;
}
void f1()
{
	std::cout << "start of f1()" << std::endl;
	A a(1);
	f2();
	std::cout << "end of f1()" << std::endl;
}

int main()
{
	std::cout << "start of main()" << std::endl;
	A a;
	try
	{
		std::cout << "before f1()" << std::endl;
		B b;
		f1();
		std::cout << "after f1()" << std::endl;
	}
	catch (int ex)
	{
		std::cout << "cought exception: " << ex << std::endl;
	}

	std::cout << "end of main()" << std::endl;
	return 0;
}
