#include <iostream>

int main() {
    int age;

    std::cout << "Enter your age: ";
    std::cin >> age;

    if(age < 0) {
        std::cout << "You haven't even born yet!";
    }

    else if(age >= 100) {
        std::cout << "You're too old to enter the club!";
    }

    else if(age >= 18) {
        std::cout << "Welcome to the club!";
    }

    else{
        std::cout << "You are too young to enter.";
    }

    return 0;
}
