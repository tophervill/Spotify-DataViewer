import unittest
from unittest.mock import Mock, patch

from app import app, oauth_sessions
from spotify_service import top_artists, top_tracks, validate_limit, validate_time_range


class DashboardRouteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        oauth_sessions.clear()

    def tearDown(self):
        oauth_sessions.clear()

    def test_dashboard_shows_login_when_not_authenticated(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Connect Spotify", response.data)

    def test_logout_clears_authentication(self):
        with self.client.session_transaction() as browser_session:
            browser_session["auth_key"] = "test-user"
        oauth_sessions["test-user"] = {"oauth": Mock()}

        response = self.client.get("/logout")

        self.assertEqual(response.status_code, 302)
        self.assertNotIn("test-user", oauth_sessions)
        self.assertIn(b"Connect Spotify", self.client.get("/").data)

    @patch("app.create_oauth")
    def test_login_redirects_to_spotify(self, create_oauth):
        oauth = Mock()
        oauth.get_authorize_url.return_value = "https://accounts.spotify.com/authorize"
        create_oauth.return_value = oauth

        response = self.client.post("/login")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "https://accounts.spotify.com/authorize")
        self.assertIn("HttpOnly", response.headers["Set-Cookie"])
        self.assertNotIn("Max-Age=2592000", response.headers["Set-Cookie"])

    @patch("app.create_oauth")
    def test_remember_me_sets_a_30_day_session_cookie(self, create_oauth):
        oauth = Mock()
        oauth.get_authorize_url.return_value = "https://accounts.spotify.com/authorize"
        create_oauth.return_value = oauth

        response = self.client.post("/login", data={"remember": "1"})

        self.assertEqual(response.status_code, 302)
        self.assertIn("Expires=", response.headers["Set-Cookie"])


class SpotifyServiceTests(unittest.TestCase):
    def test_validation_clamps_limits_and_rejects_unknown_ranges(self):
        self.assertEqual(validate_limit("100"), 20)
        self.assertEqual(validate_limit("not-a-number"), 10)
        self.assertEqual(validate_time_range("SHORT"), "short")
        with self.assertRaises(ValueError):
            validate_time_range("forever")

    def test_top_tracks_returns_display_ready_records(self):
        spotify = Mock()
        spotify.current_user_top_tracks.return_value = {
            "items": [{
                "name": "Golden Hour",
                "artists": [{"name": "Kacey Musgraves"}],
                "album": {"images": [{"url": "https://example.com/art.jpg"}]},
                "external_urls": {"spotify": "https://open.spotify.com/track/1"},
            }]
        }

        tracks = top_tracks(1, "medium", spotify)

        self.assertEqual(tracks[0]["position"], 1)
        self.assertEqual(tracks[0]["artists"], "Kacey Musgraves")
        spotify.current_user_top_tracks.assert_called_once_with(
            limit=1, offset=0, time_range="medium_term"
        )

    def test_top_artists_handles_empty_results(self):
        spotify = Mock()
        spotify.current_user_top_artists.return_value = {"items": []}

        self.assertEqual(top_artists(8, "long", spotify), [])


if __name__ == "__main__":
    unittest.main()
