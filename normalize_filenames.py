import os
import unicodedata

# Cambia aquí si tus archivos están en otra carpeta
root_dir = "notebooks"

def remove_accents(text):
    """Remueve acentos de un texto"""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

count = 0
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        # Solo procesar archivos con tildes
        if 'á' in filename or 'é' in filename or 'í' in filename or 'ó' in filename or 'ú' in filename:
            # Crear nombre sin tildes
            clean_name = remove_accents(filename)
            
            # Solo renombrar si el archivo limpio no existe
            src = os.path.join(dirpath, filename)
            dst = os.path.join(dirpath, clean_name)
            
            if not os.path.exists(dst):
                try:
                    os.rename(src, dst)
                    print(f"✅ Renamed: {filename} → {clean_name}")
                    count += 1
                except OSError as e:
                    print(f"❌ Error renaming {filename}: {e}")
            else:
                print(f"⚠️  File already exists: {clean_name}")

print(f"\nTotal files renamed: {count}")
print("\n🔧 Files renamed successfully! Now update your README files to use the new filenames.")
