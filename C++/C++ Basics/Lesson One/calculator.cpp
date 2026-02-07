#include <iostream>
#include <cmath>

int main() {
    double a;
    double b;
    double x, y, z;
    double result;

    // Ask user to input values for a and b
    std::cout << "What value would you like for a?: ";
    std::cin >> a;

    std::cout << "What value would you like for b?: ";
    std::cin >> b;

    // Calculate a^2 and b^2
    x = pow(a, 2);
    y = pow(b, 2);

    // Calculate sqrt of x and y
    z = x + y;
    result = sqrt(z);

    // Print the final answer
    std::cout << "The final answer is: " << result;
    
    return 0;
}
