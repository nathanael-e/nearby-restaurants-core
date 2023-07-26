# pylint: disable=C0116
from test.test_base import TestBase
from flask import Flask


class TestAppRestfinderInfo(TestBase):
    def test_app_restfinder_info(self, app: Flask):
        with app.test_client() as client:
            response = client.get("/")
            data = response.data.decode("utf-8")
            assert response.status_code == 200
            assert data == "Welcome ..."
