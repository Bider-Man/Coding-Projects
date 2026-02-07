#include <iostream>

// typedef std::string text_t; // This is kind of old.

using text_t = std::string; // This is more modern

int main() {
  text_t firstName = "Karthik";
  std::cout << firstName << '\n';

  // int students = 20;
  //  students += 1;
  //  students++; // increment operator if you only need to add one

  // students -= 1;
  // students--; // decrement operator if you only need to decrease one

  // students *= 2;

  // students /= 3;

  // int remainder = students % 7;
  // std::cout << remainder;

  int correct = 8;
  int questions = 10;

  double score = correct / (double)questions * 100;

  std::cout << score << "%";

  return 0;
}
