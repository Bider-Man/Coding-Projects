#include <iostream>

namespace first {
int x = 1;
}

namespace second {
int x = 2;
}

int main() {
  using namespace first;
  std::cout << x << '\n';
  std::cout << second::x; // If you type 'using namespace {identifier}'; then
                          // you can just leave the variable as it is. If you
                          // want to call the same variable in a different
                          // namespace, you use 'std::cout << {identifier}::x;'
  return 0;
}
