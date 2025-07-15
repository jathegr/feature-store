import importlib
import subprocess
import sys
import importlib.util
import site # Import the site module

def install_module(module_name: str) -> bool:
    """
    Installs a Python module using pip.

    Args:
        module_name (str): The name of the module to install.

    Returns:
        bool: True if the module was successfully installed or already present, False otherwise.
    """
    # Check if the module is already installed
    if importlib.util.find_spec(module_name):
        print(f"Module '{module_name}' is already installed.")
        return True

    print(f"Attempting to install module: '{module_name}'...")
    try:
        # Use subprocess to run the pip install command
        # sys.executable ensures pip is run with the same Python interpreter
        # as the script, which is good practice.
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"Successfully installed module: '{module_name}'")
       
        # Invalidate caches to ensure importlib recognizes the newly installed module
        importlib.invalidate_caches()
        print(f"Refreshed module cache for '{module_name}'.")
       
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing module '{module_name}': {e}")
        print("Please make sure pip is installed and accessible, or try installing manually.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during installation of '{module_name}': {e}")
        return False

def import_module_dynamically(module_name: str):
    """
    Imports a Python module dynamically given its name.

    Args:
        module_name (str): The name of the module to import (e.g., 'math', 'os').

    Returns:
        module: The imported module object, or None if the import fails.
    """
    # Ensure user site-packages are in sys.path
    # This is important when pip installs to a user-specific directory (e.g., due to permissions)
    user_site_packages = site.getusersitepackages()
    if user_site_packages not in sys.path:
        sys.path.insert(0, user_site_packages) # Add it to the beginning of the path
        print(f"Added user site-packages to sys.path: {user_site_packages}")

    try:
        module = importlib.import_module(module_name)
        print(f"Successfully imported module: '{module_name}'")
        return module
    except ImportError:
        print(f"Error: Module '{module_name}' not found after attempting to install.")
        print(f"Current sys.path: {sys.path}") # Print sys.path for debugging
        return None
    except Exception as e:
        print(f"An unexpected error occurred while importing '{module_name}': {e}")
        return None

# --- Main part of the script to ask the user and process ---

if __name__ == "__main__":
    print("Welcome to the Python Module Importer!")
    print("This program can help you install and then import a Python module.")
    print("You can also type 'pip' to update pip itself.")

    while True:
        user_input = input("\nEnter the name of the module you want to install and import (or type 'pip' to update pip, or 'exit' to quit): ").strip()

        if user_input.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        if not user_input:
            print("Module name cannot be empty. Please try again.")
            continue

        if user_input.lower() == 'pip':
            print("\n--- Updating pip ---")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                print("pip updated successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Error updating pip: {e}")
                print("Please check your internet connection or try updating pip manually.")
            except Exception as e:
                print(f"An unexpected error occurred while updating pip: {e}")
            print("-" * 50)
            continue # Go back to the start of the loop
       
        # If not 'pip' or 'exit', proceed with module installation/import
        # First, try to install the module
        if install_module(user_input):
            # If installation (or existing check) was successful, try to import
            print(f"\nAttempting to import '{user_input}'...")
            imported_module = import_module_dynamically(user_input)
            if imported_module:
                print(f"You can now use '{user_input}' in your program.")
            else:
                print(f"Could not import '{user_input}' even after attempting installation. There might be an issue.")
        else:
            print(f"Could not install '{user_input}'. Cannot proceed with import.")
        print("-" * 50)