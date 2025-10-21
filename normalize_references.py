import os
import re
import unicodedata

def remove_accents(text):
    """Remueve acentos de un texto"""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def normalize_file_references(file_path):
    """Normaliza las referencias de imágenes en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Buscar y reemplazar referencias con tildes en rutas de imágenes
        # Patrón para encontrar referencias de imágenes con tildes
        pattern = r'!\[([^\]]*)\]\(([^)]*)\)'
        
        def replace_reference(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Solo procesar si el path contiene tildes
            if 'á' in image_path or 'é' in image_path or 'í' in image_path or 'ó' in image_path or 'ú' in image_path:
                # Remover tildes del path
                clean_path = remove_accents(image_path)
                return f'![{alt_text}]({clean_path})'
            else:
                return match.group(0)  # No cambiar si no tiene tildes
        
        content = re.sub(pattern, replace_reference, content)
        
        # Si hubo cambios, escribir el archivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"ℹ️  No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

# Buscar todos los archivos README
root_dir = "notebooks"
updated_count = 0

print("🔧 Normalizing image references in README files...")
print("=" * 50)

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.md'):
            file_path = os.path.join(dirpath, filename)
            if normalize_file_references(file_path):
                updated_count += 1

print("=" * 50)
print(f"Total files updated: {updated_count}")
print("🔧 All image references have been normalized!")
print("\nNow run 'jupyter-book build .' to test the changes.")
