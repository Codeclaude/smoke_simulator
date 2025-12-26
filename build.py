#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

class Builder:
    def __init__(self):
        self.root = Path(__file__).parent.resolve()
        self.platform = sys.platform

        # Compilateur
        self.compiler = "clang++"

        # Drapeaux de compilation
        self.flags = [
            "-std=c++17",
            "-O2",
            "-g",
            "-Wall",
            "-Wextra"
        ]

        # Dossiers
        self.src_dir = self.root / "src"
        self.build_dir = self.root / "build"
        self.thirdparty_dir = self.root / "thirdparty"

        # Nom du binaire
        self.binary = "application.exe" if self.platform == "win32" else "application"

        # Création du dossier build
        self.build_dir.mkdir(exist_ok=True)

    # 🔍 Recherche de tous les .cpp
    def find_sources(self):
        return [str(p) for p in self.src_dir.rglob("*.cpp")]

    # 📂 Includes
    def get_includes(self):
        includes = [
            f"-I{self.src_dir}",
            f"-I{self.src_dir / 'Core'}",
            f"-I{self.src_dir / 'Utils'}",
            f"-I{self.thirdparty_dir}"
        ]

        # ImGui (si présent)
        imgui = self.thirdparty_dir / "imgui"
        if imgui.exists():
            includes.append(f"-I{imgui}")

        return includes

    # 📚 Librairies
    def get_libraries(self):
        if self.platform == "win32":
            return [
                "-lSDL3",
                "-limm32",
                "-loleaut32"
            ]
        else:
            return [
                "-lSDL3",
                "-ldl",
                "-lpthread"
            ]

    # 🏗️ Build
    def build(self):
        sources = self.find_sources()
        if not sources:
            print("❌ Aucun fichier .cpp trouvé")
            sys.exit(1)

        cmd = [
            self.compiler,
            *self.flags,
            *self.get_includes(),
            *sources,
            *self.get_libraries(),
            "-o", str(self.build_dir / self.binary)
        ]

        print("🔧 Compilation...")
        print(" ".join(cmd))

        subprocess.run(cmd, check=True)
        print("✅ Build terminé")

    # ▶️ Exécution
    def run(self):
        exe = self.build_dir / self.binary
        if not exe.exists():
            print("❌ Binaire introuvable, lance d'abord le build")
            return

        print("🚀 Lancement de l'application")
        subprocess.run([str(exe)])

if __name__ == "__main__":
    builder = Builder()

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        builder.run()
    else:
        builder.build()
