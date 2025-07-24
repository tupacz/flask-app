"""
Script para probar el nuevo sistema de votaciones
"""

from app.voting_manager import VotingManager
import json
from datetime import datetime

def test_voting_system():
    print("🧪 Probando el nuevo sistema de votaciones...")
    print("=" * 50)
    
    # Crear una instancia del gestor de votaciones para testing
    test_manager = VotingManager('test_votes.json')
    
    # Datos de prueba
    test_books = [
        "Cien años de soledad",
        "Don Quijote de la Mancha", 
        "El Principito",
        "1984",
        "Rayuela"
    ]
    
    print("📚 Libros de prueba:")
    for i, book in enumerate(test_books, 1):
        print(f"  {i}. {book}")
    
    print("\n🗳️ Simulando votos...")
    
    # Simular voto desde web
    success1, msg1 = test_manager.add_vote(
        ranking=["1984", "Cien años de soledad", "El Principito", "Rayuela", "Don Quijote de la Mancha"],
        username="usuario_web_1"
    )
    print(f"📝 Voto web 1: {'✅' if success1 else '❌'} {msg1}")
    
    # Simular voto desde Telegram
    fake_telegram_data = {
        'id': 123456789,
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'username': 'juanperez'
    }
    
    success2, msg2 = test_manager.add_vote(
        ranking=["El Principito", "1984", "Cien años de soledad", "Don Quijote de la Mancha", "Rayuela"],
        telegram_user_id="123456789",
        telegram_user_data=fake_telegram_data
    )
    print(f"📱 Voto Telegram 1: {'✅' if success2 else '❌'} {msg2}")
    
    # Simular otro voto desde web
    success3, msg3 = test_manager.add_vote(
        ranking=["Rayuela", "Cien años de soledad", "1984", "El Principito", "Don Quijote de la Mancha"],
        username="usuario_web_2"
    )
    print(f"📝 Voto web 2: {'✅' if success3 else '❌'} {msg3}")
    
    # Intentar votar dos veces con el mismo usuario
    success4, msg4 = test_manager.add_vote(
        ranking=["Don Quijote de la Mancha", "El Principito", "1984", "Rayuela", "Cien años de soledad"],
        username="usuario_web_1"
    )
    print(f"📝 Voto duplicado: {'✅' if success4 else '❌'} {msg4}")
    
    print("\n📊 Estadísticas del test:")
    summary = test_manager.export_votes_summary()
    print(f"  Total de votos: {summary['total_votes']}")
    print(f"  Votos web: {summary['web_votes']}")
    print(f"  Votos Telegram: {summary['telegram_votes']}")
    
    print("\n📋 Detalle de votos:")
    for i, vote in enumerate(summary['vote_details'], 1):
        source = "📱" if vote['source'] == 'telegram' else "🌐"
        print(f"  {i}. {source} {vote['display_name']}")
        print(f"     Ranking: {' > '.join(vote['ranking'])}")
    
    # Probar algoritmo de Condorcet
    print("\n🏆 Resultado de Condorcet:")
    try:
        from app.voting_condorcet import condorcet_winner
        rankings = test_manager.get_rankings_for_condorcet()
        result = condorcet_winner(rankings)
        print(f"  Ganador: {result['ganador_condorcet']}")
        print(f"  Total candidatos: {len(result['candidatos'])}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Limpiar archivo de test
    try:
        import os
        os.remove('test_votes.json')
        print(f"\n🧹 Archivo de test eliminado")
    except:
        pass
    
    print(f"\n✅ ¡Test completado!")

def test_json_structure():
    """Probar la estructura JSON del sistema"""
    print("\n🔍 Probando estructura JSON...")
    
    # Crear voto de ejemplo
    test_manager = VotingManager('test_structure.json')
    
    test_manager.add_vote(
        ranking=["Libro A", "Libro B", "Libro C"],
        telegram_user_id="987654321",
        telegram_user_data={
            'id': 987654321,
            'first_name': 'Ana',
            'last_name': 'García',
            'username': 'anagarcia',
            'language_code': 'es'
        }
    )
    
    # Leer y mostrar estructura
    with open('test_structure.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("📄 Estructura JSON generada:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # Limpiar
    import os
    os.remove('test_structure.json')

if __name__ == '__main__':
    test_voting_system()
    test_json_structure()
    
    print("\n" + "=" * 50)
    print("✨ Sistema de votaciones listo para usar!")
    print("📝 Los votos se guardan en: votes.json")
    print("🔧 Usa show_data_locations.py para ver estadísticas")
    print("💾 Usa el parámetro backup en show_data_locations.py para hacer respaldos")
