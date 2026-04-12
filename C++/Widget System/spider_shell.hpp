#pragma once
#include <memory>
#include <vector>
#include "wayland/display.hpp"
#include "hyprland/ipc.hpp"
#include "services/service_registry.hpp"
#include "modules/module.hpp"

class SpiderShell {
    public:
        static SpiderShell& instance();

        bool init();
        void run();
        void shutdown();

        WaylandDisplay* display() { return m_display.get(); }
        HyprlandIPC* ipc() { return m_ipc.get(); }
        Service_Registry* services() { return m_services.get(); }

        void addModule(std::unique_ptr<Module> module);

    private:
        SpiderShell() = default;
        std::unique_ptr<WaylandDisplay> m_display;
        std::unique_ptr<HyprlandIPC> m_ipc;
        std::unique_ptr<Service_Registry> m_services;
        std::vector<std::unique_ptr<Module>> m_modules;
};
