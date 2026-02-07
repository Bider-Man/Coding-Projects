#include <iostream>

int main() {
  std::string name;
  int age;

  std::cout << "What is your age?: ";
  std::cin >> age;

  std::cout << "What is your full name?: ";
  std::getline(std::cin >> std::ws, name); // Use this for inputs with spaces std::ws gets rid of whitespaces from previous inputs.
  // std::cin >> name; - Easier way to input names.

  std::cout << "Hello, " << name << '\n';
  std::cout << "You are " << age << " years old!";
  return 0;
}
