#!/usr/bin/env python3
"""
Build configuration and automation script for TC LED Table project.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a command and print output."""
    print(f"Running: {' '.join(cmd)}")
    if cwd:
        print(f"Working directory: {cwd}")
    
    result = subprocess.run(cmd, cwd=cwd, check=check)
    return result.returncode == 0


def setup_build_dir(build_dir, cmake_args=None):
    """Create and configure build directory."""
    build_dir = Path(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    
    cmake_cmd = ["cmake", ".."]
    if cmake_args:
        cmake_cmd.extend(cmake_args)
    
    return run_command(cmake_cmd, cwd=build_dir)


def build_project(build_dir, target=None, config="Release"):
    """Build the project."""
    build_cmd = ["cmake", "--build", ".", "--config", config]
    if target:
        build_cmd.extend(["--target", target])
    
    return run_command(build_cmd, cwd=build_dir)


def run_tests(build_dir):
    """Run tests."""
    return run_command(["ctest", "--output-on-failure"], cwd=build_dir)


def install_python_dependencies():
    """Install Python dependencies from requirements.txt."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("⚠️  requirements.txt not found, skipping Python dependencies")
        return True
    
    print("🐍 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False):
        print("⚠️  Failed to upgrade pip, continuing anyway...")
    
    # Install requirements
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
    
    if not run_command(cmd, check=False):
        print("❌ Failed to install some Python dependencies")
        print("You may need to install them manually:")
        print(f"  pip install -r {requirements_file}")
        return False
    
    print("✅ Python dependencies installed successfully")
    return True


def install_python_package(dev_mode=True):
    """Install Python package."""
    cmd = [sys.executable, "-m", "pip", "install"]
    if dev_mode:
        cmd.append("-e")
    cmd.append(".")
    
    return run_command(cmd)


def clean_build(build_dir):
    """Clean build directory."""
    import shutil
    build_path = Path(build_dir)
    if build_path.exists():
        shutil.rmtree(build_path)
        print(f"Cleaned {build_path}")
    return True


def build_libartnet():
    """Build libartnet from source if needed."""
    libartnet_path = Path("external/libartnet")
    
    if not libartnet_path.exists():
        print("⚠️  libartnet submodule not found. Skipping Art-Net support.")
        return True
    
    # Check if already built
    install_dir = Path("build/external/libartnet")
    if (install_dir / "lib" / "libartnet.so").exists() or (install_dir / "lib" / "libartnet.a").exists():
        print("ℹ️  libartnet already built")
        return True
    
    print("🔨 Building libartnet from source...")
    
    # libartnet uses autotools, not CMake
    build_dir = Path("build/external/libartnet")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for autotools dependencies
    autotools_deps = ["autoconf", "automake", "libtoolize", "make", "gcc"]
    missing_deps = []
    
    for dep in autotools_deps:
        try:
            subprocess.run([dep, "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Missing autotools dependencies: {', '.join(missing_deps)}")
        print("🔄 Attempting to install autotools dependencies...")
        
        if install_system_dependencies():
            # Re-check after installation
            still_missing = []
            for dep in missing_deps:
                try:
                    subprocess.run([dep, "--version"], capture_output=True, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    still_missing.append(dep)
            
            if still_missing:
                print(f"❌ Still missing autotools: {', '.join(still_missing)}")
                print("Install manually: sudo apt-get install build-essential autoconf automake libtool")
                return False
        else:
            print("Install manually: sudo apt-get install build-essential autoconf automake libtool")
            return False
    
    # Build libartnet
    try:
        # Run autogen.sh if it exists, otherwise autoreconf
        if (libartnet_path / "autogen.sh").exists():
            if not run_command(["./autogen.sh"], cwd=libartnet_path):
                return False
        else:
            if not run_command(["autoreconf", "-fiv"], cwd=libartnet_path):
                return False
        
        # Configure
        configure_cmd = [
            str((libartnet_path / "configure").absolute()),
            f"--prefix={build_dir.absolute()}",
            "--enable-static",
            "--disable-shared",  # Build static library for easier linking
            "CFLAGS=-g -O2 -fPIC -Wno-error"  # Add -fPIC for shared library compatibility
        ]
        
        if not run_command(configure_cmd, cwd=build_dir):
            return False
        
        # Build and install
        if not run_command(["make", "-j", str(os.cpu_count() or 4)], cwd=build_dir):
            return False
        
        if not run_command(["make", "install"], cwd=build_dir):
            return False
        
        print("✅ libartnet built successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error building libartnet: {e}")
        return False


def install_system_dependencies():
    """Install required system dependencies automatically."""
    print("🔧 Checking and installing system dependencies...")
    
    # Detect package manager
    package_managers = {
        "apt-get": ["ubuntu", "debian", "mint"],
        "yum": ["centos", "rhel", "fedora"],
        "dnf": ["fedora"],
        "pacman": ["arch", "manjaro"],
        "zypper": ["opensuse", "suse"]
    }
    
    # Try to detect distribution
    distro = None
    try:
        with open("/etc/os-release", "r") as f:
            content = f.read().lower()
            for pm, distros in package_managers.items():
                for d in distros:
                    if d in content:
                        distro = pm
                        break
                if distro:
                    break
    except FileNotFoundError:
        pass
    
    if not distro:
        # Fallback: try to find available package manager
        for pm in package_managers.keys():
            try:
                subprocess.run([pm, "--version"], capture_output=True, check=True)
                distro = pm
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    if not distro:
        print("❌ Could not detect package manager. Please install dependencies manually:")
        print("  - build-essential (or equivalent)")
        print("  - cmake")
        print("  - git")
        print("  - autoconf automake libtool")
        return False
    
    # Define packages for each package manager
    package_sets = {
        "apt-get": {
            "base": ["build-essential", "cmake", "git"],
            "autotools": ["autoconf", "automake", "libtool"],
            "python": ["python3-dev", "python3-pip", "python3-venv"]
        },
        "yum": {
            "base": ["gcc", "gcc-c++", "make", "cmake", "git"],
            "autotools": ["autoconf", "automake", "libtool"],
            "python": ["python3-devel", "python3-pip"]
        },
        "dnf": {
            "base": ["gcc", "gcc-c++", "make", "cmake", "git"],
            "autotools": ["autoconf", "automake", "libtool"],
            "python": ["python3-devel", "python3-pip"]
        },
        "pacman": {
            "base": ["base-devel", "cmake", "git"],
            "autotools": ["autoconf", "automake", "libtool"],
            "python": ["python", "python-pip"]
        },
        "zypper": {
            "base": ["gcc", "gcc-c++", "make", "cmake", "git"],
            "autotools": ["autoconf", "automake", "libtool"],
            "python": ["python3-devel", "python3-pip"]
        }
    }
    
    packages = package_sets.get(distro, package_sets["apt-get"])
    
    # Install packages
    install_commands = {
        "apt-get": ["sudo", "apt-get", "install", "-y"],
        "yum": ["sudo", "yum", "install", "-y"],
        "dnf": ["sudo", "dnf", "install", "-y"],
        "pacman": ["sudo", "pacman", "-S", "--noconfirm"],
        "zypper": ["sudo", "zypper", "install", "-y"]
    }
    
    base_cmd = install_commands[distro]
    
    # Update package cache first
    if distro == "apt-get":
        print("📦 Updating package cache...")
        if not run_command(["sudo", "apt-get", "update"], check=False):
            print("⚠️  Failed to update package cache, continuing anyway...")
    
    # Install base dependencies
    all_packages = packages["base"] + packages["autotools"] + packages["python"]
    
    if all_packages:
        print(f"📦 Installing packages: {' '.join(all_packages)}")
        install_cmd = base_cmd + all_packages
        
        if not run_command(install_cmd, check=False):
            print("❌ Failed to install some packages. Please install manually:")
            print(f"   {' '.join(install_cmd)}")
            return False
    
    print("✅ System dependencies installed successfully")
    return True


def check_dependencies(auto_install=True):
    """Check if required dependencies are available."""
    dependencies = ["cmake", "git"]
    missing = []
    
    for dep in dependencies:
        try:
            subprocess.run([dep, "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(dep)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        
        if auto_install:
            print("🔄 Attempting to install missing dependencies...")
            if install_system_dependencies():
                # Re-check after installation
                still_missing = []
                for dep in missing:
                    try:
                        subprocess.run([dep, "--version"], capture_output=True, check=True)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        still_missing.append(dep)
                
                if still_missing:
                    print(f"❌ Still missing after installation: {', '.join(still_missing)}")
                    return False
                else:
                    print("✅ All dependencies now available")
                    return True
            else:
                return False
        else:
            print("Please install them before proceeding.")
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Build automation for TC LED Table")
    parser.add_argument("--build-dir", default="build", help="Build directory")
    parser.add_argument("--config", default="Release", choices=["Debug", "Release"],
                       help="Build configuration")
    parser.add_argument("--clean", action="store_true", help="Clean build directory")
    parser.add_argument("--tests", action="store_true", help="Build and run tests")
    parser.add_argument("--python-only", action="store_true", 
                       help="Only install Python package")
    parser.add_argument("--no-python", action="store_true",
                       help="Skip Python bindings")
    parser.add_argument("--skip-external", action="store_true",
                       help="Skip building external dependencies")
    parser.add_argument("--no-auto-install", action="store_true",
                       help="Don't automatically install missing dependencies")
    parser.add_argument("--target", help="Specific target to build")
    parser.add_argument("--install", action="store_true", help="Install after building")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not check_dependencies(auto_install=not args.no_auto_install):
        sys.exit(1)
    
    if args.clean:
        clean_build(args.build_dir)
        return
    
    if args.python_only:
        success = install_python_package(dev_mode=True)
        sys.exit(0 if success else 1)
    
    # Check if this is the restructured version
    if not Path("src/tc_led_table").exists():
        print("❌ This appears to be the old project structure.")
        print("Please run the migration first or use the old CMakeLists.txt in cpplib/")
        print("For old structure: cd cpplib && mkdir build && cd build && cmake .. && make")
        sys.exit(1)
    
    # Prepare CMake arguments
    cmake_args = [
        f"-DCMAKE_BUILD_TYPE={args.config}",
        "-DTCLEDTABLE_BUILD_TESTS=ON" if args.tests else "-DTCLEDTABLE_BUILD_TESTS=OFF",
        "-DTCLEDTABLE_BUILD_PYTHON_BINDINGS=OFF" if args.no_python else "-DTCLEDTABLE_BUILD_PYTHON_BINDINGS=ON",
    ]
    
    # Add libartnet paths if built
    libartnet_install = Path("build/external/libartnet")
    if libartnet_install.exists():
        cmake_args.extend([
            f"-DLIBARTNET_ROOT={libartnet_install.absolute()}",
            f"-DLIBARTNET_INCLUDE_DIR={libartnet_install.absolute()}/include",
            f"-DLIBARTNET_LIBRARY={libartnet_install.absolute()}/lib/libartnet.a"
        ])
    
    if args.verbose:
        cmake_args.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
    
    # Setup and build
    success = True
    
    # Build external dependencies first
    if not args.skip_external:
        print("🔨 Building external dependencies...")
        if not build_libartnet():
            print("❌ libartnet build failed")
            success = False
    else:
        print("⏭️  Skipping external dependencies build")
    
    if success:
        print("🔨 Configuring project...")
        if not setup_build_dir(args.build_dir, cmake_args):
            print("❌ CMake configuration failed")
            success = False
    
    if success:
        print("🔨 Building project...")
        if not build_project(args.build_dir, args.target, args.config):
            print("❌ Build failed")
            success = False
    
    if success and args.tests:
        print("🧪 Running tests...")
        if not run_tests(args.build_dir):
            print("❌ Tests failed")
            success = False
    
    if success and not args.no_python:
        print("🐍 Installing Python dependencies...")
        if not install_python_dependencies():
            print("❌ Python dependencies installation failed")
            success = False
        
        if success:
            print("🐍 Installing Python package...")
            if not install_python_package(dev_mode=True):
                print("❌ Python package installation failed")
                success = False
    
    if success and args.install:
        print("📦 Installing...")
        if not run_command(["cmake", "--install", "."], cwd=args.build_dir):
            print("❌ Installation failed")
            success = False
    
    if success:
        print("✅ Build completed successfully!")
        print("\nNext steps:")
        print("- Test the Python bindings: python -c 'import tc_led_table; print(\"Import successful!\")'")
        if not args.no_python:
            print("- Run examples: python python/examples/")
        print("- Check documentation: docs/")
    else:
        print("❌ Build failed!")
        print("\nTroubleshooting:")
        print("- Check that all dependencies are installed")
        print("- Install autotools: sudo apt-get install build-essential autoconf automake libtool")
        print("- For the old structure, use: cd cpplib && mkdir build && cd build && cmake .. && make")
        print("- Run with --verbose for more details")
        print("- Use --skip-external to skip building libartnet")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
