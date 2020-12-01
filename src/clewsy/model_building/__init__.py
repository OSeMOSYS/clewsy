"""Visualise different aspects of an OSeMOSYS model and data
Provides the following commands::
    otoole viz res <path_to_datapackage.json> <path_to_res_image>
``otoole viz res`` generates an image of the reference energy system in a datapackage
"""
from .model_building import build

__all__ = ["build"]