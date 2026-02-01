import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Union


def get_application_path() -> Path:
    """
    Get the directory where the executable is located.
    Works for both development and bundled executables.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = Path(sys.executable).parent
    else:
        # Running in development environment
        application_path = Path(__file__).parent

    return application_path


def load_app_settings(config_filename: str = "app_settings.json") -> Dict[str, Any]:
    """
    Load all application settings from JSON file.

    Args:
        config_filename: Name of the configuration file

    Returns:
        Dictionary containing all settings (xpaths and attributes)
    """
    # Get the directory where the executable is located
    app_dir = get_application_path()
    config_path = app_dir / config_filename

    # Default settings
    default_settings = {
        "xpaths": {
            "acc_data": "//Файл/Документ/СвСчФакт/@ДатаДок",
            "acc_num": "//Файл/Документ/СвСчФакт/@НомерДок",
            "acc_org_name": "//Файл/Документ/@НаимЭконСубСост",
            "goods": "//Файл/Документ/ТаблСчФакт/СведТов",
            "row_num": "@НомСтр",
            "name": "@НаимТов",
            "price": "@ЦенаТов",
            "amount": "@КолТов",
            "id_mark": "ДопСведТов/НомСредИдентТов/КИЗ/text()"
        },
        "attributes": {
            "acc_data": {"column": "ДатаДок", "width": 10},
            "acc_num": {"column": "НомерДок", "width": 15},
            "acc_org_name": {"column": "НаимЭконСубСост", "width": 50},
            "id_mark": {"column": "КИЗ", "width": 40},
            "row_num": {"column": "НомСтр", "width": 8},
            "name": {"column": "НаимТов", "width": 40},
            "price": {"column": "ЦенаТов", "width": 10},
            "amount": {"column": "КолТов", "width": 7}
        }
    }

    # Check if settings file exists
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            # Update settings with any new defaults (for backward compatibility)
            updated = False

            # Handle xpaths section
            if "xpaths" not in settings:
                settings["xpaths"] = {}
            for key, value in default_settings["xpaths"].items():
                if key not in settings["xpaths"]:
                    settings["xpaths"][key] = value
                    updated = True

            # Handle attributes section
            if "attributes" not in settings:
                settings["attributes"] = {}
            for key, value in default_settings["attributes"].items():
                if key not in settings["attributes"]:
                    settings["attributes"][key] = value
                    updated = True

            # Save back if there were updates
            if updated:
                save_app_settings(settings, config_path)

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading settings file: {e}. Using default settings.")
            settings = default_settings.copy()
    else:
        # Create settings file with default values
        settings = default_settings.copy()
        save_app_settings(settings, config_path)
        print(f"Created default settings file: {config_path}")

    return settings


def save_app_settings(settings: Dict[str, Any], config_path: Path):
    """
    Save all application settings to JSON file.

    Args:
        settings: Dictionary containing all settings
        config_path: Path object to the configuration file
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_xpath_settings(config_filename: str = "app_settings.json") -> Dict[str, str]:
    """
    Get only the XPath settings.

    Args:
        config_filename: Name of the configuration file

    Returns:
        Dictionary containing XPath settings
    """
    settings = load_app_settings(config_filename)
    return settings.get("xpaths", {})


def get_attribute_settings(config_filename: str = "app_settings.json") -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Get only the attribute settings.

    Args:
        config_filename: Name of the configuration file

    Returns:
        Dictionary containing attribute settings
    """
    settings = load_app_settings(config_filename)
    return settings.get("attributes", {})


# Example usage in your PyQt5 application
class YourApp:
    def __init__(self):
        # Load all settings
        self.all_settings = load_app_settings()
        self.xpath_settings = self.all_settings["xpaths"]
        self.attribute_settings = self.all_settings["attributes"]

        # Now you can use both sets of settings
        self.acc_data_xpath = self.xpath_settings["acc_data"]
        self.goods_xpath = self.xpath_settings["goods"]

        # Access attribute settings
        self.name_column = self.attribute_settings["name"]["column"]
        self.name_width = self.attribute_settings["name"]["width"]


# For direct usage
if __name__ == "__main__":
    # Load all settings
    app_settings = load_app_settings()

    print("XPath Settings:")
    for key, value in app_settings["xpaths"].items():
        print(f"  {key}: {value}")

    print("\nAttribute Settings:")
    for key, value in app_settings["attributes"].items():
        print(f"  {key}: {value}")

    print(f"\nExecutable directory: {get_application_path()}")