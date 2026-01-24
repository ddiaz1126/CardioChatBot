# AI Server - tools/cardio_tools.py

"""
    Task: Need to have these functions run on the databases from /data
"""

# Database paths
DB_MAP = {
    1: 'data/client_1_cardio.db',
    2: 'data/client_2_cardio.db',
    3: 'data/client_3_cardio.db'
}

# ==========================================
# SESSION TOOLS
# ==========================================

def get_recent_cardio_sessions(client_id: int, limit: int = 10):
    """Get client's recent cardio sessions"""


def get_cardio_by_date(client_id: int, date: str):
    """Get cardio sessions on a specific date"""


def get_cardio_history(client_id: int, weeks_back: int = 12):
    """Get full cardio training history"""


def get_cardio_session_details(cardio_id: int):
    """Get detailed info for specific cardio session"""


def get_cardio_frequency(client_id: int, weeks: int = 4):
    """How often client does cardio per week"""

# ==========================================
# PERFORMANCE TOOLS
# ==========================================

def get_pace_progression(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track pace improvement over time"""

def get_heart_rate_trends(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track heart rate trends"""

def get_speed_progression(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track speed improvement over time"""


def get_cardio_personal_bests(client_id: int, cardio_type: str = None):
    """Get personal records for distance, pace, duration"""


def get_cardio_intensity_zones(client_id: int, cardio_type: str = None, weeks: int = 4):
    """Analyze heart rate zones and training intensity"""


def compare_cardio_sessions(cardio_id_1: int, cardio_id_2: int):
    """Compare two cardio sessions"""


# ==========================================
# DISTANCE & DURATION TOOLS
# ==========================================

def get_distance_trends(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track distance trends over time"""


def get_duration_trends(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track duration trends over time"""


def get_weekly_mileage(client_id: int, cardio_type: str = None, weeks: int = 4):
    """Get weekly distance totals"""


def get_monthly_volume(client_id: int, cardio_type: str = None, months: int = 3):
    """Get monthly cardio volume"""


def get_longest_sessions(client_id: int, cardio_type: str = None, limit: int = 5):
    """Get longest cardio sessions by distance or duration"""

# ==========================================
# SPLITS & PACING TOOLS
# ==========================================

def get_split_analysis(cardio_id: int):
    """Analyze splits for a specific session"""


def get_pacing_consistency(cardio_id: int):
    """Measure pacing consistency across splits"""


def get_negative_splits(client_id: int, cardio_type: str = None, weeks: int = 12):
    """Find sessions with negative splits (faster second half)"""


def get_fastest_splits(client_id: int, cardio_type: str = None, limit: int = 10):
    """Get fastest individual splits"""

# ==========================================
# ELEVATION TOOLS
# ==========================================

def get_elevation_gain_trends(client_id: int, cardio_type: str = None, weeks_back: int = 12):
    """Track elevation gain over time"""


def get_altitude_performance(client_id: int, cardio_type: str = None):
    """Compare performance at different altitudes"""


def get_hill_workouts(client_id: int, weeks: int = 12):
    """Get sessions with significant elevation gain"""


# ==========================================
# CARDIO TYPE TOOLS
# ==========================================

def get_cardio_type_distribution(client_id: int, weeks: int = 4):
    """Breakdown of cardio types (running, cycling, etc.)"""

def get_cardio_type_frequency(client_id: int, cardio_type: str, weeks: int = 4):
    """How often client does specific cardio type"""

def compare_cardio_types(cardio_type_1: str, cardio_type_2: str, client_id: int, weeks: int = 4):
    """Compare performance between two cardio types"""


