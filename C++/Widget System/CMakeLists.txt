cmake_minimum_required(VERSION 3.20)
project(spider-shell VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(WAYLAND_CLIENT REQUIRED wayland-client)
pkg_check_modules(WAYLAND_PROTOCOLS REQUIRED wayland-protocols)
pkg_check_modules(EGL REQUIRED egl)
pkg_check_modules(GLESv2 REQUIRED glesv2)
pkg_check_modules(LIBXML2 REQUIRED libxml-2.0)
pkg_check_modules(DBUS REQUIRED dbus-1)
pkg_check_modules(THREADS REQUIRED threads)

# hyprtoolkit is not pkg-config based; we find it via CMake
find_package(hyprtoolkit REQUIRED)

# Wayland scanner setup (same as before)
find_program(WAYLAND_SCANNER_EXECUTABLE NAMES wayland-scanner)
set(PROTOCOL_XML_DIR ${WAYLAND_PROTOCOLS_PREFIX}/share/wayland-protocols)
set(GENERATED_SOURCES_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)

function(generate_protocol protocol_file)
    # ... (identical to previous implementation)
endfunction()

generate_protocol(${PROTOCOL_XML_DIR}/stable/xdg-shell/xdg-shell.xml)
generate_protocol(${PROTOCOL_XML_DIR}/staging/ext-idle-notify/ext-idle-notify-v1.xml)
# Assuming wlr-layer-shell xml is in protocols/
generate_protocol(${CMAKE_SOURCE_DIR}/protocols/wlr-layer-shell-unstable-v1.xml)

# Gather sources
file(GLOB_RECURSE SOURCES
    "src/*.cpp"
    "modules/*.cpp"
    "services/*.cpp"
    "system/*.cpp"
)

add_executable(${PROJECT_NAME} ${SOURCES} ${GENERATED_SOURCES})

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/modules
    ${CMAKE_CURRENT_SOURCE_DIR}/services
    ${CMAKE_CURRENT_SOURCE_DIR}/system
    ${WAYLAND_CLIENT_INCLUDE_DIRS}
    ${hyprtoolkit_INCLUDE_DIRS}
)

target_link_libraries(${PROJECT_NAME}
    ${WAYLAND_CLIENT_LIBRARIES}
    ${EGL_LIBRARIES}
    ${GLESv2_LIBRARIES}
    ${LIBXML2_LIBRARIES}
    ${DBUS_LIBRARIES}
    ${CMAKE_THREAD_LIBS_INIT}
    m
    wayland-egl
    hyprtoolkit::hyprtoolkit
    nlohmann_json::nlohmann_json
)
