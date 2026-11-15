"""
Modèle de Simulation Macroéconomique et de Gouvernance IT
Auteur : [Prénom Nom]

Ce script modélise l'impact comparé de deux stratégies décidées en comité exécutif :
1. Stratégie A (Court-termiste) : Coupe budgétaire et licenciement d'effectifs techniques.
2. Stratégie B (Pilotage informé) : Industrialisation de la DSI, réduction de la dette
   technique et maintien du capital humain d'ingénierie.

 Dépendances : Bibliothèque standard Python uniquement (aucune installation requise).
"""

import math
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EnterpriseState:
    year: int
    revenue: float
    ebitda: float
    technical_debt_ratio: float
    engineering_headcount: int
    productivity_index: float
    tobin_q_proxy: float


class ProductivitySimulator:
    """
    Simulateur économique destiné à éclairer un comité exécutif et une DSI
    sur la trajectoire de création de valeur à 5 ans (distinguer le bruit de l'informé).
    """

    def __init__(
        self,
        initial_revenue: float = 100.0,
        initial_headcount: int = 120,
        initial_tech_debt: float = 0.35,
    ):
        self.initial_revenue = initial_revenue
        self.initial_headcount = initial_headcount
        self.initial_tech_debt = initial_tech_debt

    def run_short_term_layoff_strategy(self, years: int = 5) -> List[EnterpriseState]:
        """
        Simule une politique de licenciement de 20% des équipes dès l'année 1
        sans réingénierie préalable par la DSI.
        """
        results: List[EnterpriseState] = []
        revenue = self.initial_revenue
        headcount = int(self.initial_headcount * 0.80)  # Licenciement initial de 20%
        tech_debt = self.initial_tech_debt

        for y in range(1, years + 1):
            # La perte de mémoire technique augmente la dette technique chaque année
            tech_debt = min(0.85, tech_debt + 0.08 * math.log(y + 1))
            
            # Dégradation progressive de la productivité globale des facteurs
            productivity = 100.0 * (1.0 - (tech_debt - self.initial_tech_debt) * 0.9)
            
            # Érosion du chiffre d'affaires liée au ralentissement de livraison de la DSI
            revenue = revenue * (1.01 - 0.04 * (tech_debt - 0.30))
            
            # L'économie salariale initiale est compensée par les surcoûts d'intégration externe
            external_Integration_penalty = (self.initial_headcount - headcount) * 0.14 * y
            payroll_cost = headcount * 0.18
            ebitda = (revenue * 0.28) - payroll_cost - external_Integration_penalty
            
            # L'investisseur informé pénalise la perte de capital immatériel (Q de Tobin)
            tobin_q = max(0.7, 1.8 - (tech_debt * 1.4))

            results.append(
                EnterpriseState(
                    year=y,
                    revenue=round(revenue, 2),
                    ebitda=round(ebitda, 2),
                    technical_debt_ratio=round(tech_debt, 3),
                    engineering_headcount=headcount,
                    productivity_index=round(productivity, 1),
                    tobin_q_proxy=round(tobin_q, 2),
                )
            )
        return results

    def run_informed_dsi_industrialization(self, years: int = 5) -> List[EnterpriseState]:
        """
        Simule une gouvernance où le comité exécutif, pleinement informé des métriques
        opérationnelles, mandate la DSI pour réduire la dette technique à effectif constant.
        """
        results: List[EnterpriseState] = []
        revenue = self.initial_revenue
        headcount = self.initial_headcount
        tech_debt = self.initial_tech_debt

        for y in range(1, years + 1):
            # Réduction industrielle de la dette technique et rationalisation SaaS
            tech_debt = max(0.10, tech_debt * 0.82)
            
            # Gain de productivité généré par l'automatisation et la confiance interne
            productivity = 100.0 * (1.0 + (self.initial_tech_debt - tech_debt) * 1.35)
            
            # Capacité à absorber la croissance des volumes à effectif constant
            revenue = revenue * (1.03 + 0.05 * (productivity / 100.0 - 1.0))
            
            payroll_cost = headcount * 0.18
            saas_rationalization_savings = 1.2 * y
            ebitda = (revenue * 0.28) - payroll_cost + saas_rationalization_savings
            
            # Valorisation accrue du capital organisationnel par un marché informé
            tobin_q = round(1.8 + (productivity - 100.0) * 0.035, 2)

            results.append(
                EnterpriseState(
                    year=y,
                    revenue=round(revenue, 2),
                    ebitda=round(ebitda, 2),
                    technical_debt_ratio=round(tech_debt, 3),
                    engineering_headcount=headcount,
                    productivity_index=round(productivity, 1),
                    tobin_q_proxy=tobin_q,
                )
            )
        return results


def print_comparative_report() -> None:
    sim = ProductivitySimulator()
    scen_layoff = sim.run_short_term_layoff_strategy(years=5)
    scen_informed = sim.run_informed_dsi_industrialization(years=5)

    print("=" * 82)
    print("SIMULATION MACROÉCONOMIQUE : ARBITRAGE COMITÉ EXÉCUTIF & PERFORMANCE DSI (5 ANS)")
    print("=" * 82)
    print(f"{'Année':<6} | {'EBITDA (Licenciement)':<22} | {'EBITDA (Pilotage Informé)':<25} | {'Écart Productivité':<18}")
    print("-" * 82)

    for s_lay, s_inf in zip(scen_layoff, scen_informed):
        diff_prod = round(s_inf.productivity_index - s_lay.productivity_index, 1)
        print(
            f"An {s_lay.year:<3} | "
            f"{s_lay.ebitda:>18.2f} M€ | "
            f"{s_inf.ebitda:>21.2f} M€ | "
            f"+{diff_prod:>12.1f} pts"
        )
    print("=" * 82)


if __name__ == "__main__":
    print_comparative_report()