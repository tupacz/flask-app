"""
Script para mostrar las ubicaciones y estadísticas de los datos de votación
"""

import json
import os
from pathlib import Path
from datetime import datetime

def show_data_locations():
    print("📂 Ubicaciones de datos de la aplicación:")
    print("=" * 60)
    
    # Directorio actual
    current_dir = Path.cwd()
    print(f"📁 Directorio de la app: {current_dir}")
    
    # Archivos de datos importantes
    data_files = {
        'votes.json': 'Votaciones de usuarios',
        'app/data/books.json': 'Lista de libros',
        '.env': 'Variables de entorno',
        'config.py': 'Configuración de la app'
    }
    
    print(f"\n📋 Archivos de datos:")
    for file, description in data_files.items():
        file_path = current_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            print(f"✅ {file}")
            print(f"   📝 {description}")
            print(f"   📁 {file_path}")
            print(f"   📊 {size} bytes, modificado: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ {file}: No existe")
        print()
    
    # Analizar archivo de votos
    analyze_votes_file()

def analyze_votes_file():
    print("\n�️ Análisis del archivo de votos:")
    print("=" * 40)
    
    try:
        # Importar aquí para evitar problemas de importación circular
        from app.voting_manager import VotingManager
        
        voting_manager = VotingManager('votes.json')
        summary = voting_manager.export_votes_summary()
        
        print(f"📊 Total de votos: {summary['total_votes']}")
        print(f"📱 Votos desde Telegram: {summary['telegram_votes']}")
        print(f"🌐 Votos desde Web: {summary['web_votes']}")
        
        if summary['vote_details']:
            print(f"\n📅 Primer voto: {summary['vote_details'][0]['timestamp']}")
            print(f"📅 Último voto: {summary['vote_details'][-1]['timestamp']}")
            
            print(f"\n📋 Últimos 3 votos:")
            for i, vote in enumerate(summary['vote_details'][-3:], 1):
                try:
                    timestamp = datetime.fromisoformat(vote['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = vote['timestamp']
                source = "📱" if vote['source'] == 'telegram' else "🌐"
                print(f"  {i}. {source} {vote['display_name']} - {timestamp}")
                print(f"     Ranking: {' > '.join(vote['ranking'][:3])}{'...' if len(vote['ranking']) > 3 else ''}")
        else:
            print("📭 No hay votos registrados aún")
            
    except ImportError:
        print("⚠️ No se puede importar VotingManager. Analizando directamente el JSON...")
        analyze_votes_json_direct()
    except Exception as e:
        print(f"❌ Error analizando votos: {e}")

def analyze_votes_json_direct():
    """Análisis directo del archivo JSON cuando no se puede importar VotingManager"""
    votes_file = Path('votes.json')
    if not votes_file.exists():
        print("📭 No hay archivo de votos aún")
        return
    
    try:
        with open(votes_file, 'r', encoding='utf-8') as f:
            votes = json.load(f)
        
        print(f"📊 Total de votos: {len(votes)}")
        
        if votes:
            # Contar por fuente
            telegram_count = sum(1 for v in votes.values() if v.get('vote_source') == 'telegram')
            web_count = len(votes) - telegram_count
            
            print(f"📱 Votos desde Telegram: {telegram_count}")
            print(f"🌐 Votos desde Web: {web_count}")
            
            # Mostrar ejemplo de voto
            sample_vote = list(votes.values())[0]
            print(f"\n📋 Estructura de un voto:")
            for key, value in sample_vote.items():
                if isinstance(value, list) and len(value) > 3:
                    print(f"   {key}: [{', '.join(map(str, value[:3]))}, ...]")
                elif isinstance(value, dict):
                    print(f"   {key}: {{...}}")
                else:
                    print(f"   {key}: {value}")
                    
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")

def backup_votes():
    """Crear backup del archivo de votos"""
    print("\n💾 Creando backup de votos...")
    
    votes_file = Path('votes.json')
    if not votes_file.exists():
        print("❌ No hay archivo de votos para respaldar")
        return
    
    # Crear directorio de backups
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Nombre del backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'votes_backup_{timestamp}.json'
    
    # Copiar archivo
    import shutil
    shutil.copy2(votes_file, backup_file)
    
    print(f"✅ Backup creado: {backup_file}")
    
    # Mostrar estadísticas del backup
    with open(votes_file, 'r', encoding='utf-8') as f:
        votes = json.load(f)
    print(f"📊 Votos respaldados: {len(votes)}")

def main():
    print("🔍 Analizando datos de la aplicación de votación...")
    print()
    
    show_data_locations()
    
    # Preguntar si crear backup
    try:
        response = input("\n❓ ¿Crear backup de los votos? (y/N): ").strip().lower()
        if response == 'y':
            backup_votes()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")

if __name__ == '__main__':
    main()