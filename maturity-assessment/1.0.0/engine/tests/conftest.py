"""Shared fixtures for the engine test suite.

Every module under test is loaded by file path via importlib, matching the
plugin pytest configuration (--import-mode=importlib), because calcPack
engines elsewhere in the plugin share module file names.
"""

from __future__ import annotations

import importlib.util
import os

import pytest

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def loadEngineModule(name):
    spec = importlib.util.spec_from_file_location(
        f"engineUnderTest_{name}", os.path.join(ENGINE_DIR, f"{name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def configLoader():
    return loadEngineModule("configLoader")


@pytest.fixture(scope="session")
def aggregate():
    return loadEngineModule("aggregate")


@pytest.fixture(scope="session")
def orchestrate():
    return loadEngineModule("orchestrate")


@pytest.fixture(scope="session")
def chunker():
    return loadEngineModule("chunker")


@pytest.fixture(scope="session")
def ledgerCli():
    return loadEngineModule("ledger")


@pytest.fixture(scope="session")
def initEngine():
    return loadEngineModule("init")


@pytest.fixture()
def fixturesDir():
    return FIXTURES_DIR


@pytest.fixture()
def acmeRepo(tmp_path):
    """A throwaway copy of the fictional Acme Rail fixture engagement."""
    import shutil

    target = tmp_path / "acmeEngagement"
    shutil.copytree(os.path.join(FIXTURES_DIR, "acmeEngagement"), target)
    return str(target)
