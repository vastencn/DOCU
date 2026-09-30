import os
import zipfile
import datetime
import sys

# Configuration
SOURCE_DIR = r"E:\DOCU"
BACKUP_DIR = os.path.join(SOURCE_DIR, "backups")
EXCLUDE_DIRS = {"node_modules", "backups", "results", ".git", ".idea", "dist", "build", "__pycache__"}
ALLOWED_EXTS = {".js", ".json", ".md", ".rs", ".html", ".css", ".ts", ".txt", ".ps1", ".py", ".glsl"}
MAX_PREFLIGHT_SIZE_MB = 50

def get_source_files():
    files_to_zip = []
    total_size = 0
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Mutate dirs in-place to prevent walking into excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            # Allow files with specific extensions or no extension
            if ext in ALLOWED_EXTS or not ext:
                full_path = os.path.join(root, file)
                size = os.path.getsize(full_path)
                files_to_zip.append(full_path)
                total_size += size
                
    return files_to_zip, total_size

def pre_flight_check():
    print("--- Starting Pre-flight Check ---")
    files, total_size = get_source_files()
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"Discovered {len(files)} source files.")
    print(f"Estimated uncompressed size: {total_size_mb:.2f} MB")
    
    if total_size_mb > MAX_PREFLIGHT_SIZE_MB:
        print(f"ERROR: Pre-flight failed! Size {total_size_mb:.2f} MB exceeds maximum {MAX_PREFLIGHT_SIZE_MB} MB.")
        sys.exit(1)
        
    print("Pre-flight check passed.")
    return files

def create_zip(files_to_zip, prefix="docu_src"):
    print("\n--- Generating ZIP Archive ---")
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    clean_prefix = prefix.strip().replace(" ", "_") if prefix else "docu_src"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{clean_prefix}_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_zip:
            rel_path = os.path.relpath(file_path, SOURCE_DIR)
            zf.write(file_path, rel_path)
            
    print(f"Archive generated at: {zip_path}")
    return zip_path

def verify_zip(zip_path):
    print("\n--- Verifying ZIP Archive ---")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            bad_file = zf.testzip()
            if bad_file:
                print(f"ERROR: ZIP validation failed. Corrupted file found: {bad_file}")
                sys.exit(1)
            
            manifest = zf.namelist()
            print(f"ZIP valid and contains {len(manifest)} files.")
            for f in manifest:
                parts = f.replace('\\', '/').split('/')
                if any(ex in parts for ex in EXCLUDE_DIRS):
                    print(f"ERROR: ZIP contains blacklisted directory! Offending file: {f}")
                    sys.exit(1)
                    
            print("Validation successful. Backup is pristine.")
    except zipfile.BadZipFile:
        print("ERROR: Generated ZIP file is invalid/corrupt.")
        sys.exit(1)

def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "docu_src"
    print(f"Initializing DOCU Backup & Verification Protocol (Target: {prefix})...\n")
    files_to_zip = pre_flight_check()
    zip_path = create_zip(files_to_zip, prefix=prefix)
    verify_zip(zip_path)
    print("\n--- Backup Process Completed Successfully ---")

if __name__ == "__main__":
    main()
