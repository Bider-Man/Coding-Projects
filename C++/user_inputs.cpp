#include <iostream>

int main() {
  std::string name;
  std::cout << "What is your name?: ";
  std::cin >> name;

  std::cout << "Hello, " << name;
  return 0;
}
