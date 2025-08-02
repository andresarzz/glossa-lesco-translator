"""
Configuración de estilos y colores para GLOSSA
"""

class DesignSystem:
    """Sistema de diseño profesional para GLOSSA"""
    
    # Paleta de colores profesional
    COLORS = {
        # Colores primarios
        'primary': '#2563eb',
        'primary_hover': '#1d4ed8', 
        'primary_light': '#dbeafe',
        
        # Colores secundarios
        'secondary': '#64748b',
        'secondary_light': '#f1f5f9',
        
        # Colores de estado
        'success': '#10b981',
        'success_light': '#d1fae5',
        'warning': '#f59e0b', 
        'warning_light': '#fef3c7',
        'danger': '#ef4444',
        'danger_light': '#fee2e2',
        
        # Neutrales
        'white': '#ffffff',
        'gray_50': '#f8fafc',
        'gray_100': '#f1f5f9',
        'gray_200': '#e2e8f0',
        'gray_300': '#cbd5e1',
        'gray_400': '#94a3b8',
        'gray_500': '#64748b',
        'gray_600': '#475569',
        'gray_700': '#334155',
        'gray_800': '#1e293b',
        'gray_900': '#0f172a',
    }
    
    # Tipografía
    FONTS = {
        'primary': 'Segoe UI',
        'secondary': 'Segoe UI',
        'monospace': 'Consolas',
        'emoji': 'Segoe UI Emoji'
    }
    
    # Tamaños de fuente
    FONT_SIZES = {
        'xs': 10,
        'sm': 11,
        'base': 12,
        'lg': 14,
        'xl': 16,
        '2xl': 20,
        '3xl': 24,
        '4xl': 32
    }
    
    # Espaciado
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        '2xl': 48
    }
    
    # Radios de borde
    BORDER_RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16
    }
    
    # Sombras
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
    }
