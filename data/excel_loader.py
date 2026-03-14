import openpyxl
import pandas as pd
from models.project import ProjectParameters
from models.component import Component
from models.degradation import Degradation
from models.environment import Environment
from models.planning import Planning


def load_project_data(file_path):

    xls = pd.ExcelFile(file_path)

    parameters = load_parameters(xls)
    environment = load_environment(xls)
    components = load_components(xls)
    degradation = load_degradation(xls)
    planning = load_planning(xls)

    return {
        "parameters": parameters,
        "environment": environment,
        "components": components,
        "degradation": degradation,
        "planning": planning
    }


def load_parameters(xls) -> object:
    """
    Fonction de lecture des paramètres du projet
    """
    df = pd.read_excel(xls, "project_parameters")

    params = dict(zip(df["parameter"], df["value"]))

    return ProjectParameters(
        name=params["project_name"],
        budget=params["initial_budget_fcfa"],
        lambda_finance=params["lambda_financial_behavior"],
        horizon=params["time_horizon_periods"],
        governance=params["governance_regime"]
    )
    

def load_environment(xls):
    """
    Fonction de lecture des paramètres d'environnement
    """
    df = pd.read_excel(xls, "environment")

    env = []

    for _, row in df.iterrows():

        env.append(Environment(
            period=row["period"],
            shock=row["external_shock"],
            political=row["political_pressure"],
            constraint=row["context_constraint"]
        ))

    return env


def load_components(xls) -> object:
    """
    Fonction de lecture des composants du projet
    """
    df = pd.read_excel(xls, "components")

    components = []

    for _, row in df.iterrows():

        components.append(Component(
            id=row["id"],
            name=row["unit_name"],
            site=row["site"],
            cost=row["estimated_cost_fcfa"],
            strategic_value=row["strategic_value"],
            dependency_id=row["dependency_id"],
            duration=row['duration']
        ))

    return components


def load_degradation(xls):
    """
    Fonction de lectures des paramètres de dégradation
    """
    df = pd.read_excel(xls, "degradation")

    degradation = []

    for _, row in df.iterrows():

        degradation.append(Degradation(
            component_id=row["component_id"],
            rate=row["degradation_rate"],
            exposure=row["exposure_time_periods"]
        ))

    return degradation


def load_planning(xls):
    """Fonction de lecture du planning"""
    df = pd.read_excel(xls, "planning")

    planning = []

    for _, row in df.iterrows():

        planning.append(Planning(
            component_id=row["component_id"],
            start=row["planned_start_period"],
            end=row["planned_end_period"]
        ))

    return planning


    
    