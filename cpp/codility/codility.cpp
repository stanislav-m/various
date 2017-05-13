#include <iostream>

int solution(int A, int B, int K)
{
	std:: cout << "A=" << A << " B=" << B << " K=" << K << std::endl;
	int first = -1; 

	if (A > 0)
	{
		for (int i=A; i<(A+K) && i<=B; ++i)
		{
			if ( i % K == 0)
			{
				first = i;
				break;
			}
		}
	}
	else
	if (A == 0)
	{
		first = 0;
	}
	if (first >= 0)
	{
		return (B-first)/K +1;
	}
	return 0;
}

int main ()
{
	std::cout << solution(2, 41, 5) << std::endl;
	std::cout << solution(0, 32, 7) << std::endl;
	std::cout << solution(11, 11, 11) << std::endl;
	std::cout << solution(12, 17, 18) << std::endl;
	std::cout << solution(0, 99, 113) << std::endl;
	return 0;
}
