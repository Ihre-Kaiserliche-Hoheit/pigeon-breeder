#include <iostream>

int main() {
    World w;
    
    return 0;
}

void print(std::string newString) {
    // If you want to complain about this you can kindly fuck off
    std::cout << newString << "\n";
}

class World {
    public:
        int getMonth() {
            return month;
        }

        void setMonth(int newMonth) {
            month = newMonth;
        }

        int getYear() {
            return year;
        }

        void setYear(int newYear) {
            year = newYear;
        }

        std::string getDate() {
            return std::to_string(month) + "/" + std::to_string(year); // This simple trick is HATED by Rust programmers! Just add three strings together.
        }

        void setWorldname(std::string newWorldname) {
            worldname = newWorldname;
        }

        std::string getWorldname() {
            return worldname;
        }

    private:
        std::string worldname;

        int month = 1;
        int year = 0;
        int wealth = 50;


};
