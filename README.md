#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <mutex>
#include <sstream>

// Structure to store reminder details
struct Reminder {
    std::string message;
    std::chrono::steady_clock::time_point triggerTime;
};

// Global variables for thread safety
std::vector<Reminder> reminders;
std::mutex reminderMutex;
bool running = true;

// Background worker thread to monitor and trigger reminders
void reminderWorker() {
    while (running) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        auto now = std::chrono::steady_clock::now();
        
        std::lock_guard<std::mutex> lock(reminderMutex);
        for (auto it = reminders.begin(); it != reminders.end(); ) {
            if (now >= it->triggerTime) {
                std::cout << "\n\a[REMINDER]: " << it->message << "\n> " << std::flush;
                it = reminders.erase(it); // Remove triggered reminder
            } else {
                ++it;
            }
        }
    }
}

int main() {
    // Start background thread
    std::thread worker(reminderWorker);
    
    std::cout << "=== C++ Reminder Chatbot ===\n";
    std::cout << "Format: <seconds> <message>\n";
    std::cout << "Example: 10 Take out the trash\n";
    std::cout << "Type 'exit' to quit.\n\n";

    std::string line;
    while (true) {
        std::cout << "> ";
        if (!std::getline(std::cin, line) || line == "exit") {
            break;
        }

        std::stringstream ss(line);
        int seconds;
        std::string message;

        // Parse seconds and the remaining text string
        if (ss >> seconds) {
            std::getline(ss >> std::ws, message); // Read rest of line ignoring leading whitespace
            
            if (message.empty()) {
                std::cout << "Bot: Please provide a message for the reminder.\n";
                continue;
            }

            // Calculate exact trigger time point
            auto trigger = std::chrono::steady_clock::now() + std::chrono::seconds(seconds);

            // Thread-safe insertion
            {
                std::lock_guard<std::mutex> lock(reminderMutex);
                reminders.push_back({message, trigger});
            }

            std::cout << "Bot: Saved! I will remind you about '" << message << "' in " << seconds << " seconds.\n";
        } else {
            std::cout << "Bot: Invalid format. Use: <seconds> <message>\n";
        }
    }

    // Clean shutdown
    running = false;
    if (worker.joinable()) {
        worker.join();
    }
    return 0;
}

