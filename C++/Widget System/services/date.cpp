// Import Important Modules
#include <chrono>
#include <ctime>
#include <string>
#include <iomanip>
#include <sstream>
#include <atomic>
#include <thread>
#include <functional>
#include <vector>

// Main Configuration
class DateService {
    public:
        using DateUpdateCallback = std::function<void(const std::string&)>;
        DateService() : running_(false) {}
        
        void start() {
            running_ = true;
            worker_thread_ = std::thread([this]() {
                while (running_) {
                    updateDate();
                    std::this_thread::sleep_for(std::chrono::seconds(60)); // Update every
                                                                           // 60 seconds
                }
            });
        }

        void stop() {
            running_ = false;
            if (worker_thread_.joinable()) {
                worker_thread_.join();
            }
        }

        void setUpdateCallback(DateUpdateCallback callback) {
            callback_ = callback;
        }

        std::string getCurrentDate() {
            auto now = std::chrono::system_clock::now();
            std::time_t time = std::chrono::system_clock::to_time_t(now);
            std::tm* tm = std::localtime(&time);

            std::stringstream ss;
            ss << std::put_time(tm, "%A, %B %d, %Y");
            return ss.str();
        }

        std::string getShortDate() {
            auto now = std::chrono::system_clock::now();
            std::time_t time = std::chrono::system_clock::to_time_t(now);
            std::tm* tm = std::localtime(&time);

            std::stringstream ss;
            ss << std::put_time(tm, "%Y-%m-%d");
            return ss.str();
        }

        std::string getWeekNumber() {
            auto now = std::chrono::system_clock::now();
            std::time_t time = std::chrono::system_clock::to_time_t(now);
            std::tm* tm = std::localtime(&time);

            char week[3];
            strftime(week, sizeof(week), "%V", tm);
            return std::string(week);
        }

private:
    void updateDate() {
        std::string date = getCurrentDate();
        if (callback_) {
            callback_(date);
        }
    }

    std::atomic<bool> running_;
    std::thread worker_thread_;
    DateUpdateCallback callback_;
};
