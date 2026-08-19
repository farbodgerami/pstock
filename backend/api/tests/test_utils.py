import matplotlib.pyplot as plt
from app.utils import save_plot


def test_save_plot(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    settings.MEDIA_URL = "/media/"

    plt.figure()
    plt.plot([1, 2, 3])

    result = save_plot("test.png")

    assert result == "/media/test.png"
    assert (tmp_path / "test.png").exists()