# flake.nix
{
  description = "Spider Shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    hyprtoolkit.url = "github:hyprwm/hyprtoolkit";
  };

  outputs = { self, nixpkgs, flake-utils, hyprtoolkit }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        hyprtoolkit-pkg = hyprtoolkit.packages.${system}.default;
      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            cmake
            pkg-config
            gcc13
            gdb
            wayland
            wayland-protocols
            wayland-scanner
            libGL
            libxml2
            dbus
            nlohmann_json
            hyprtoolkit-pkg
          ];
          shellHook = ''
            echo "Spider Shell dev environment"
          '';
        };
      });
}
