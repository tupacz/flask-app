"""
Módulo para gestionar las votaciones de usuarios
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid

class VotingManager:
    def __init__(self, votes_file: str = 'votes.json'):
        """
        Inicializa el gestor de votaciones
        
        Args:
            votes_file: Ruta al archivo JSON donde se guardan los votos
        """
        self.votes_file = votes_file
        self._ensure_votes_file_exists()
    
    def _ensure_votes_file_exists(self):
        """Crea el archivo de votos si no existe"""
        if not os.path.exists(self.votes_file):
            with open(self.votes_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def _load_votes(self) -> Dict:
        """Carga todos los votos desde el archivo JSON"""
        try:
            with open(self.votes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_votes(self, votes: Dict):
        """Guarda todos los votos al archivo JSON"""
        with open(self.votes_file, 'w', encoding='utf-8') as f:
            json.dump(votes, f, ensure_ascii=False, indent=2)
    
    def user_has_voted(self, user_id: Optional[str] = None, username: Optional[str] = None) -> bool:
        """
        Verifica si un usuario ya ha votado
        
        Args:
            user_id: ID de Telegram del usuario (para usuarios de Telegram)
            username: Nombre del usuario (para usuarios web)
            
        Returns:
            True si el usuario ya votó, False en caso contrario
        """
        votes = self._load_votes()
        
        for vote in votes.values():
            # Verificar por ID de Telegram (prioritario)
            if user_id and vote.get('telegram_user_id') == str(user_id):
                return True
            
            # Verificar por nombre de usuario (fallback para usuarios web)
            if username and vote.get('username') == username and not vote.get('telegram_user_id'):
                return True
        
        return False
    
    def add_vote(self, 
                 ranking: List[str], 
                 telegram_user_id: Optional[str] = None,
                 telegram_user_data: Optional[Dict] = None,
                 username: Optional[str] = None) -> Tuple[bool, str]:
        """
        Añade un nuevo voto
        
        Args:
            ranking: Lista ordenada de títulos de libros (del favorito al menos favorito)
            telegram_user_id: ID de usuario de Telegram
            telegram_user_data: Datos completos del usuario de Telegram
            username: Nombre de usuario (para usuarios web)
            
        Returns:
            Tuple (success: bool, message: str)
        """
        # Verificar si el usuario ya votó
        if self.user_has_voted(telegram_user_id, username):
            user_display = telegram_user_data.get('first_name', username) if telegram_user_data else username
            return False, f"{user_display} ya votó anteriormente"
        
        # Crear entrada del voto
        vote_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        vote_entry = {
            'vote_id': vote_id,
            'timestamp': timestamp,
            'ranking': ranking,
            'vote_source': 'telegram' if telegram_user_id else 'web'
        }
        
        # Agregar información del usuario de Telegram si está disponible
        if telegram_user_id:
            vote_entry['telegram_user_id'] = str(telegram_user_id)
            if telegram_user_data:
                vote_entry['telegram_user_data'] = {
                    'first_name': telegram_user_data.get('first_name'),
                    'last_name': telegram_user_data.get('last_name'),
                    'username': telegram_user_data.get('username'),
                    'language_code': telegram_user_data.get('language_code')
                }
                vote_entry['display_name'] = self._get_display_name(telegram_user_data)
        else:
            vote_entry['username'] = username
            vote_entry['display_name'] = username
        
        # Guardar el voto
        votes = self._load_votes()
        votes[vote_id] = vote_entry
        self._save_votes(votes)
        
        return True, "Voto guardado correctamente"
    
    def _get_display_name(self, telegram_user_data: Dict) -> str:
        """Genera un nombre para mostrar a partir de los datos de Telegram"""
        first_name = telegram_user_data.get('first_name', '')
        last_name = telegram_user_data.get('last_name', '')
        username = telegram_user_data.get('username', '')
        
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif username:
            return f"@{username}"
        else:
            return f"Usuario {telegram_user_data.get('id', 'Desconocido')}"
    
    def get_all_votes(self) -> Dict:
        """Obtiene todos los votos"""
        return self._load_votes()
    
    def get_vote_count(self) -> int:
        """Obtiene el número total de votos"""
        return len(self._load_votes())
    
    def get_telegram_votes_count(self) -> int:
        """Obtiene el número de votos desde Telegram"""
        votes = self._load_votes()
        return sum(1 for vote in votes.values() if vote.get('vote_source') == 'telegram')
    
    def get_web_votes_count(self) -> int:
        """Obtiene el número de votos desde la web"""
        votes = self._load_votes()
        return sum(1 for vote in votes.values() if vote.get('vote_source') == 'web')
    
    def get_rankings_for_condorcet(self) -> List[List[str]]:
        """
        Obtiene todas las clasificaciones en formato para el algoritmo de Condorcet
        
        Returns:
            Lista de listas, donde cada sublista es un ranking de libros
        """
        votes = self._load_votes()
        return [vote['ranking'] for vote in votes.values()]
    
    def export_votes_summary(self) -> Dict:
        """
        Exporta un resumen de los votos para análisis
        
        Returns:
            Diccionario con estadísticas y datos de votos
        """
        votes = self._load_votes()
        
        summary = {
            'total_votes': len(votes),
            'telegram_votes': self.get_telegram_votes_count(),
            'web_votes': self.get_web_votes_count(),
            'vote_details': []
        }
        
        for vote in votes.values():
            vote_detail = {
                'timestamp': vote['timestamp'],
                'source': vote['vote_source'],
                'display_name': vote.get('display_name', 'Anónimo'),
                'ranking': vote['ranking']
            }
            summary['vote_details'].append(vote_detail)
        
        # Ordenar por timestamp
        summary['vote_details'].sort(key=lambda x: x['timestamp'])
        
        return summary
