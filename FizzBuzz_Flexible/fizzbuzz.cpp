#include <iostream>

int fizzbuzz(int fizznum, int buzznum, int iterations)
{
	for(int i=1; i<iterations+1; i++)
	{
		if((i % fizznum != 0) && (i % buzznum != 0))
		{
			std::cout << i << std::endl;
		} else 
		{
			if(i%fizznum==0)
			{
				std::cout << "Fizz";
			}
			if(i%buzznum==0)
			{
				std::cout << "Buzz";
			}
			std::cout << std::endl;
		}
	}
}

int main()
{
	while(true)
	{
		int fizznum;
		int buzznum;
		int iterations;
		
		std::cout << "Fizznumber?" << std::endl;
		std::cin >> fizznum;
		std::cout << "Buzznumber?" << std::endl;
		std::cin >> buzznum;
		std::cout << "Number of iterations" << std::endl;
		std::cin >> iterations;
		fizzbuzz(fizznum, buzznum, iterations);		
	}
}
