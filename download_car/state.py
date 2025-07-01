# download_car/state.py
"""
State Enumeration Module.

This module defines an enumeration representing states in Brazil.

Enumerations:
    State: Enumeration representing states in Brazil.
        - AC: Acre
        - AL: Alagoas
        - AM: Amazonas
        - AP: Amapá
        - BA: Bahia
        - CE: Ceará
        - DF: Distrito Federal
        - ES: Espírito Santo
        - GO: Goiás
        - MA: Maranhão
        - MG: Minas Gerais
        - MS: Mato Grosso do Sul
        - MT: Mato Grosso
        - PA: Pará
        - PB: Paraíba
        - PE: Pernambuco
        - PI: Piauí
        - PR: Paraná
        - RJ: Rio de Janeiro
        - RN: Rio Grande do Norte
        - RO: Rondônia
        - RR: Roraima
        - RS: Rio Grande do Sul
        - SC: Santa Catarina
        - SE: Sergipe
        - SP: São Paulo
        - TO: Tocantins
"""

from enum import Enum


class State(str, Enum):
    """
    Enumeration representing states in Brazil.

    Options:
        - AC: Acre
        - AL: Alagoas
        - AM: Amazonas
        - AP: Amapá
        - BA: Bahia
        - CE: Ceará
        - DF: Distrito Federal
        - ES: Espírito Santo
        - GO: Goiás
        - MA: Maranhão
        - MG: Minas Gerais
        - MS: Mato Grosso do Sul
        - MT: Mato Grosso
        - PA: Pará
        - PB: Paraíba
        - PE: Pernambuco
        - PI: Piauí
        - PR: Paraná
        - RJ: Rio de Janeiro
        - RN: Rio Grande do Norte
        - RO: Rondônia
        - RR: Roraima
        - RS: Rio Grande do Sul
        - SC: Santa Catarina
        - SE: Sergipe
        - SP: São Paulo
        - TO: Tocantins
    """

    AC = "AC"
    AL = "AL"
    AM = "AM"
    AP = "AP"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MG = "MG"
    MS = "MS"
    MT = "MT"
    PA = "PA"
    PB = "PB"
    PE = "PE"
    PI = "PI"
    PR = "PR"
    RJ = "RJ"
    RN = "RN"
    RO = "RO"
    RR = "RR"
    RS = "RS"
    SC = "SC"
    SE = "SE"
    SP = "SP"
    TO = "TO"
