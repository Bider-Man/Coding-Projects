#include <iostream>

namespace first {
int y = 1;
}

namespace second {
int y = 2;
}

int main() {

  // This is a comment.
  /*
   * This is a multi-line
   * comment
   */

  std::cout << "I love spinach!" << '\n';
  std::cout << "It's really good!" << '\n';

  int x; // Declaraing the variable
  x = 5; // Assigning the variable
  int age = 23;
  std::cout << x << '\n';

  // Doubles are used instead of floats
  double price = 10.99;
  double gpa = 4.0;
  double temp = 25.1;

  std::cout << price << '\n';
  std::cout << gpa << '\n';
  std::cout << temp;

  // Single characters are called "char", remember to use single quotes for
  // these
  char grade = 'A';
  char initial = 'B';

  std::cout << grade << '\n';
  std::cout << initial << '\n';

  // Booleans (true or false)
  bool student = true;
  bool light = false;

  std::cout << student << '\n';
  std::cout << light << '\n';

  // Strings are the same as in python
  std::string name = "Karthik";

  std::cout << "Hello, " << name << '\n';
  std::cout << "You are " << age << " years old" << '\n';

  // Const will tell the compiler to not change the value
  // So it's read-only
  const double pi = 3.14159;
  double radius = 10;
  double circumference = 2 * pi * radius;

  std::cout << circumference << " cm" << '\n';

  // Namespaces allow for same name variables to exist, long as their Namespaces
  // are different.

  using namespace first;

  std::cout << y;

  return 0;
}
