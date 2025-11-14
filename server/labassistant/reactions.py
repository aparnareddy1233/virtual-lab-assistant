# utils/reactions.py

REACTIONS_DB = {
    frozenset(['HCl', 'NaOH']): {
        'reaction': "HCl + NaOH → NaCl + H₂O 💧",
        'type': 'Neutralization',
        'balanced': True,
    },
    frozenset(['AgNO3', 'NaCl']): {
        'reaction': "AgNO₃ + NaCl → AgCl↓ + NaNO₃ ⚪",
        'type': 'Precipitation',
        'balanced': True,
    },
    frozenset(['H2O2', 'MnO2']): {
        'reaction': "2H₂O₂ → 2H₂O + O₂ (MnO₂ catalyst) 🔥",
        'type': 'Decomposition',
        'balanced': True,
    },
    frozenset(['Na', 'H2O']): {
        'reaction': "2Na + 2H₂O → 2NaOH + H₂↑",
        'type': 'Single Displacement',
        'balanced': True,
    }
}

def simulate_reaction(chemicals):
    return REACTIONS_DB.get(frozenset(chemicals), {
        'reaction': "No visible reaction 🤔",
        'balanced': False,
    })
