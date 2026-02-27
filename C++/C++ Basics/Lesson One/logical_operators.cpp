 include <iostream>

int main() {

    // &&: Check if two conditions are true (AND)
    // ||: Check if at least one of the conditions are true (OR)
    // !: Reverse the logical state of the operand. (NOT)

    int temp;

    std::cout << "Enter the temperature: ";
    std::cin >> temp;

    if (temp > 0 && temp < 30) {
        std::cout << "The temperature is good!";
    }
    else {
        std::cout << "The temperature is bad!";
    }

    return 0;
}
