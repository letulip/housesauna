import os
import tempfile
import shutil
import datetime

from django.test import TestCase, override_settings

from housesauna.utility import save_failed_submission


class SaveFailedSubmissionTestCase(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.override = override_settings(BASE_DIR=self.temp_dir)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.temp_dir)

    def test_save_creates_file_with_expected_content(self):
        test_data = {
            'Имя': 'Тестовый Пользователь',
            'Email': 'test@example.com',
            'Телефон': '+79001234567',
            'Объект': 'Проект тест',
            'Страница': 'https://example.com/house/test',
            'Сообщение': 'Сообщение для проверки',
            'Дата/время': datetime.datetime.now().isoformat()
        }

        save_failed_submission(test_data)

        target_dir = os.path.join(self.temp_dir, 'failed_submissions')
        self.assertTrue(os.path.exists(target_dir), msg='Папка не создана')

        saved_files = os.listdir(target_dir)
        self.assertEqual(len(saved_files), 1, msg='Файл не создан или создано несколько файлов')

        saved_file_path = os.path.join(target_dir, saved_files[0])
        with open(saved_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('Тестовый Пользователь', content)
        self.assertIn('+79001234567', content)
        self.assertIn('https://example.com/house/test', content)
