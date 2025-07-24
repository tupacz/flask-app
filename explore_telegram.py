import telegram
print(f"Versión: {telegram.__version__}")
print("\nExplorando módulos disponibles:")

# Explorar qué hay en el módulo principal
main_items = [item for item in dir(telegram) if not item.startswith('_')]
print(f"\nElementos en telegram: {len(main_items)}")
for item in sorted(main_items):
    if 'web' in item.lower() or 'app' in item.lower():
        print(f"  🔍 {item}")

# Buscar en submódulos
try:
    import telegram.constants
    print(f"\nConstantes disponibles:")
    constants = [item for item in dir(telegram.constants) if 'WEB' in item or 'APP' in item]
    for const in constants:
        print(f"  📋 {const}")
except:
    pass

# Verificar qué está en InlineKeyboardButton
try:
    from telegram import InlineKeyboardButton
    print(f"\nInlineKeyboardButton parameters:")
    import inspect
    sig = inspect.signature(InlineKeyboardButton.__init__)
    for param in sig.parameters:
        if 'web' in param.lower():
            print(f"  🔘 {param}")
except Exception as e:
    print(f"Error explorando InlineKeyboardButton: {e}")

# Buscar en todos los submódulos
import pkgutil
print(f"\nSubmódulos de telegram:")
for importer, modname, ispkg in pkgutil.iter_modules(telegram.__path__):
    if 'web' in modname.lower():
        print(f"  📦 {modname}")