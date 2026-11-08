import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "SendMsg"

class SendMsgTests(unittest.TestCase):
    def run_script(self, args, overrides=None):
        with tempfile.TemporaryDirectory() as tmp:
            capture = Path(tmp) / "args"
            curl = Path(tmp) / "curl"
            curl.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$CAPTURE\"\nexit \"${CURL_STATUS:-0}\"\n")
            curl.chmod(0o755)
            env = dict(os.environ, PATH=tmp + ":" + os.environ["PATH"], CAPTURE=str(capture), TELEGRAM_BOT_TOKEN="test-token", TELEGRAM_CHAT_ID="123")
            env.update(overrides or {})
            result = subprocess.run(["bash", str(SCRIPT), *args], env=env, capture_output=True, text=True)
            return result, capture.read_text() if capture.exists() else ""

    def test_text_default_url_and_encoded_message(self):
        result, args = self.run_script(["hello & world"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("https://api.telegram.org/bottest-token/sendMessage", args)
        self.assertIn("text=hello & world", args)

    def test_file_and_custom_server(self):
        with tempfile.NamedTemporaryFile() as file:
            result, args = self.run_script(["caption", file.name], {"TELEGRAM_API_BASE_URL": "http://127.0.0.1:8081/"})
            self.assertEqual(result.returncode, 0)
            self.assertIn("http://127.0.0.1:8081/bottest-token/sendDocument", args)
            self.assertIn("document=@" + file.name, args)

    def test_missing_credentials_or_message_fails(self):
        self.assertNotEqual(self.run_script([])[0].returncode, 0)
        self.assertNotEqual(self.run_script(["message"], {"TELEGRAM_BOT_TOKEN": ""})[0].returncode, 0)
        self.assertNotEqual(self.run_script(["message"], {"TELEGRAM_CHAT_ID": ""})[0].returncode, 0)

    def test_curl_failure_is_propagated(self):
        self.assertEqual(self.run_script(["message"], {"CURL_STATUS": "22"})[0].returncode, 22)

if __name__ == "__main__":
    unittest.main()
