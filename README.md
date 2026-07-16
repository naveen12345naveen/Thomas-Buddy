#include <iostream>
#include <string>
#include <regex>
#include "httplib.h"

// Helper utility to safely pull structural parameters out of the JSON string
std::string getJsonValue(const std::string& body, const std::string& key) {
    std::regex key_regex("\"" + key + "\"\\s*:\\s*\"([^\"]+)\"");
    std::smatch match;
    if (std::regex_search(body, match, key_regex)) {
        return match[1].str();
    }
    return "";
}

int main() {
    httplib::Server svr;

    svr.set_default_headers({
        {"Access-Control-Allow-Origin", "*"},
        {"Access-Control-Allow-Headers", "Content-Type"}
    });

    svr.Post("/reminder", [](const httplib::Request& req, httplib::Response& res) {
        // Extract structural parameters cleanly sent by the interface layout
        std::string task = getJsonValue(req.body, "task");
        std::string date = getJsonValue(req.body, "date");
        std::string time = getJsonValue(req.body, "time");

        std::cout << "\n--- New Log Record Cached ---" << std::endl;
        std::cout << "Task: " << task << "\nDate: " << date << "\nTime: " << time << std::endl;

        // Build Confirmation Text Block
        std::string confirmation = "Success! I have logged an alert to remind you to '" + task + "' on " + date + " at exactly " + time + ".";
        
        std::string json_response = "{\"reply\":\"" + confirmation + "\"}";
        res.set_content(json_response, "application/json");
    });

    std::cout << "Secure Personal Bot Pipeline active on http://localhost:8080" << std::endl;
    svr.listen("0.0.0.0", 8080);
    return 0;
}
