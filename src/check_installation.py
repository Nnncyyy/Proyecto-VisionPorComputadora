import sys


def check_import(package_name, import_name=None):
    import_name = import_name or package_name

    try:
        module = __import__(import_name)
        version = getattr(module, "__version__", "versión no disponible")
        print(f"[OK] {package_name}: {version}")
        return True
    except Exception as e:
        print(f"[ERROR] {package_name}: {e}")
        return False


def main():
    print("Verificación de entorno — Echomain")
    print("Python:", sys.version)

    checks = [
        ("opencv-python", "cv2"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib"),
        ("tqdm", "tqdm"),
        ("supervision", "supervision"),
        ("ultralytics", "ultralytics"),
    ]

    results = [check_import(pkg, imp) for pkg, imp in checks]

    if all(results):
        print("\nEntorno listo.")
    else:
        print("\nFaltan dependencias. Ejecuta:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()