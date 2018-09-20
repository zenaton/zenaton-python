from distutils.version import LooseVersion


def test_version():
    import zenaton
    assert zenaton.__version__
    assert LooseVersion(zenaton.__version__)