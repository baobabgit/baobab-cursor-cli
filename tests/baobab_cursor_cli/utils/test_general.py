"""
Tests unitaires pour les utilitaires généraux.
"""

import pytest
from unittest.mock import patch

from baobab_cursor_cli.utils.general import (
    generate_session_id,
    sanitize_input,
    convert_to_snake_case,
    convert_to_camel_case,
    convert_to_pascal_case,
    truncate_string,
    generate_random_string,
    deep_merge_dicts,
    flatten_dict,
    unflatten_dict,
    remove_none_values,
    get_nested_value,
    set_nested_value,
    is_valid_email,
    is_valid_url,
    extract_numbers,
    extract_emails,
    extract_urls,
    chunk_list,
    deduplicate_list
)


class TestGenerateSessionId:
    """Tests pour generate_session_id."""
    
    def test_generate_session_id_with_prefix(self):
        """Test avec un préfixe."""
        result = generate_session_id("test")
        assert result.startswith("test_")
        assert len(result) > 5  # UUID + préfixe
    
    def test_generate_session_id_without_prefix(self):
        """Test sans préfixe."""
        result = generate_session_id("")
        assert "_" not in result
        assert len(result) == 36  # UUID4 standard
    
    def test_generate_session_id_none_prefix(self):
        """Test avec None comme préfixe."""
        result = generate_session_id(None)
        assert "_" not in result
        assert len(result) == 36
    
    def test_generate_session_id_special_chars_prefix(self):
        """Test avec un préfixe contenant des caractères spéciaux."""
        result = generate_session_id("test@#$%")
        assert result.startswith("test_")
        assert "@#$%" not in result
    
    def test_generate_session_id_unique(self):
        """Test que les IDs générés sont uniques."""
        ids = [generate_session_id("test") for _ in range(100)]
        assert len(set(ids)) == 100


class TestSanitizeInput:
    """Tests pour sanitize_input."""
    
    def test_sanitize_input_basic(self):
        """Test avec une chaîne basique."""
        result = sanitize_input("  test string  ")
        assert result == "test string"
    
    def test_sanitize_input_control_chars(self):
        """Test avec des caractères de contrôle."""
        result = sanitize_input("test\x00\x1fstring")
        assert result == "teststring"
    
    def test_sanitize_input_unicode_chars(self):
        """Test avec des caractères Unicode problématiques."""
        result = sanitize_input("test\u200bstring")
        assert result == "teststring"
    
    def test_sanitize_input_multiple_spaces(self):
        """Test avec des espaces multiples."""
        result = sanitize_input("test    string")
        assert result == "test string"
    
    def test_sanitize_input_max_length(self):
        """Test avec limitation de longueur."""
        long_string = "a" * 100
        result = sanitize_input(long_string, max_length=10)
        assert len(result) == 10
    
    def test_sanitize_input_non_string(self):
        """Test avec un type non-string."""
        result = sanitize_input(123)
        assert result == "123"
    
    def test_sanitize_input_empty(self):
        """Test avec une chaîne vide."""
        result = sanitize_input("")
        assert result == ""


class TestConvertToSnakeCase:
    """Tests pour convert_to_snake_case."""
    
    def test_convert_to_snake_case_camel(self):
        """Test avec camelCase."""
        result = convert_to_snake_case("camelCaseString")
        assert result == "camel_case_string"
    
    def test_convert_to_snake_case_pascal(self):
        """Test avec PascalCase."""
        result = convert_to_snake_case("PascalCaseString")
        assert result == "pascal_case_string"
    
    def test_convert_to_snake_case_with_spaces(self):
        """Test avec des espaces."""
        result = convert_to_snake_case("test string")
        assert result == "test_string"
    
    def test_convert_to_snake_case_with_dashes(self):
        """Test avec des tirets."""
        result = convert_to_snake_case("test-string")
        assert result == "test_string"
    
    def test_convert_to_snake_case_special_chars(self):
        """Test avec des caractères spéciaux."""
        result = convert_to_snake_case("test@#$%string")
        assert result == "test_string"
    
    def test_convert_to_snake_case_multiple_underscores(self):
        """Test avec des underscores multiples."""
        result = convert_to_snake_case("test__string")
        assert result == "test_string"
    
    def test_convert_to_snake_case_non_string(self):
        """Test avec un type non-string."""
        result = convert_to_snake_case(123)
        assert result == "123"


class TestConvertToCamelCase:
    """Tests pour convert_to_camel_case."""
    
    def test_convert_to_camel_case_snake(self):
        """Test avec snake_case."""
        result = convert_to_camel_case("snake_case_string")
        assert result == "snakeCaseString"
    
    def test_convert_to_camel_case_with_spaces(self):
        """Test avec des espaces."""
        result = convert_to_camel_case("test string")
        assert result == "testString"
    
    def test_convert_to_camel_case_with_dashes(self):
        """Test avec des tirets."""
        result = convert_to_camel_case("test-string")
        assert result == "testString"
    
    def test_convert_to_camel_case_single_word(self):
        """Test avec un seul mot."""
        result = convert_to_camel_case("test")
        assert result == "test"
    
    def test_convert_to_camel_case_empty(self):
        """Test avec une chaîne vide."""
        result = convert_to_camel_case("")
        assert result == ""


class TestConvertToPascalCase:
    """Tests pour convert_to_pascal_case."""
    
    def test_convert_to_pascal_case_snake(self):
        """Test avec snake_case."""
        result = convert_to_pascal_case("snake_case_string")
        assert result == "SnakeCaseString"
    
    def test_convert_to_pascal_case_with_spaces(self):
        """Test avec des espaces."""
        result = convert_to_pascal_case("test string")
        assert result == "TestString"
    
    def test_convert_to_pascal_case_with_dashes(self):
        """Test avec des tirets."""
        result = convert_to_pascal_case("test-string")
        assert result == "TestString"
    
    def test_convert_to_pascal_case_single_word(self):
        """Test avec un seul mot."""
        result = convert_to_pascal_case("test")
        assert result == "Test"
    
    def test_convert_to_pascal_case_empty(self):
        """Test avec une chaîne vide."""
        result = convert_to_pascal_case("")
        assert result == ""


class TestTruncateString:
    """Tests pour truncate_string."""
    
    def test_truncate_string_no_truncation(self):
        """Test sans troncature."""
        result = truncate_string("short", 10)
        assert result == "short"
    
    def test_truncate_string_with_truncation(self):
        """Test avec troncature."""
        result = truncate_string("very long string", 10)
        assert result == "very lo..."
    
    def test_truncate_string_custom_suffix(self):
        """Test avec un suffixe personnalisé."""
        result = truncate_string("very long string", 10, "---")
        assert result == "very lo---"
    
    def test_truncate_string_max_length_less_than_suffix(self):
        """Test avec max_length plus petit que le suffixe."""
        result = truncate_string("test", 2, "---")
        assert result == "--"
    
    def test_truncate_string_non_string(self):
        """Test avec un type non-string."""
        result = truncate_string(123, 2)
        assert result == "12"


class TestGenerateRandomString:
    """Tests pour generate_random_string."""
    
    def test_generate_random_string_basic(self):
        """Test basique."""
        result = generate_random_string(8)
        assert len(result) == 8
        assert result.isalnum()
    
    def test_generate_random_string_with_symbols(self):
        """Test avec des symboles."""
        result = generate_random_string(10, include_symbols=True)
        assert len(result) == 10
    
    def test_generate_random_string_zero_length(self):
        """Test avec une longueur zéro."""
        result = generate_random_string(0)
        assert result == ""
    
    def test_generate_random_string_negative_length(self):
        """Test avec une longueur négative."""
        result = generate_random_string(-1)
        assert result == ""
    
    def test_generate_random_string_unique(self):
        """Test que les chaînes générées sont uniques."""
        strings = [generate_random_string(10) for _ in range(100)]
        assert len(set(strings)) == 100


class TestDeepMergeDicts:
    """Tests pour deep_merge_dicts."""
    
    def test_deep_merge_dicts_basic(self):
        """Test basique."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        result = deep_merge_dicts(dict1, dict2)
        expected = {"a": 1, "b": 2, "c": 3, "d": 4}
        assert result == expected
    
    def test_deep_merge_dicts_nested(self):
        """Test avec des dictionnaires imbriqués."""
        dict1 = {"a": {"x": 1}, "b": 2}
        dict2 = {"a": {"y": 2}, "c": 3}
        result = deep_merge_dicts(dict1, dict2)
        expected = {"a": {"x": 1, "y": 2}, "b": 2, "c": 3}
        assert result == expected
    
    def test_deep_merge_dicts_override(self):
        """Test avec remplacement de valeurs."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 3}
        result = deep_merge_dicts(dict1, dict2)
        expected = {"a": 3, "b": 2}
        assert result == expected


class TestFlattenDict:
    """Tests pour flatten_dict."""
    
    def test_flatten_dict_basic(self):
        """Test basique."""
        d = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(d)
        expected = {"a": 1, "b.c": 2, "b.d": 3}
        assert result == expected
    
    def test_flatten_dict_custom_separator(self):
        """Test avec un séparateur personnalisé."""
        d = {"a": 1, "b": {"c": 2}}
        result = flatten_dict(d, sep="_")
        expected = {"a": 1, "b_c": 2}
        assert result == expected
    
    def test_flatten_dict_deeply_nested(self):
        """Test avec imbrication profonde."""
        d = {"a": {"b": {"c": 1}}}
        result = flatten_dict(d)
        expected = {"a.b.c": 1}
        assert result == expected


class TestUnflattenDict:
    """Tests pour unflatten_dict."""
    
    def test_unflatten_dict_basic(self):
        """Test basique."""
        d = {"a": 1, "b.c": 2, "b.d": 3}
        result = unflatten_dict(d)
        expected = {"a": 1, "b": {"c": 2, "d": 3}}
        assert result == expected
    
    def test_unflatten_dict_custom_separator(self):
        """Test avec un séparateur personnalisé."""
        d = {"a": 1, "b_c": 2}
        result = unflatten_dict(d, sep="_")
        expected = {"a": 1, "b": {"c": 2}}
        assert result == expected


class TestRemoveNoneValues:
    """Tests pour remove_none_values."""
    
    def test_remove_none_values_basic(self):
        """Test basique."""
        d = {"a": 1, "b": None, "c": 3}
        result = remove_none_values(d)
        expected = {"a": 1, "c": 3}
        assert result == expected
    
    def test_remove_none_values_no_none(self):
        """Test sans valeurs None."""
        d = {"a": 1, "b": 2}
        result = remove_none_values(d)
        assert result == d


class TestGetNestedValue:
    """Tests pour get_nested_value."""
    
    def test_get_nested_value_basic(self):
        """Test basique."""
        d = {"a": {"b": {"c": 1}}}
        result = get_nested_value(d, "a.b.c")
        assert result == 1
    
    def test_get_nested_value_default(self):
        """Test avec valeur par défaut."""
        d = {"a": {"b": 1}}
        result = get_nested_value(d, "a.b.c", "default")
        assert result == "default"
    
    def test_get_nested_value_custom_separator(self):
        """Test avec séparateur personnalisé."""
        d = {"a": {"b": 1}}
        result = get_nested_value(d, "a_b", sep="_")
        assert result == 1


class TestSetNestedValue:
    """Tests pour set_nested_value."""
    
    def test_set_nested_value_basic(self):
        """Test basique."""
        d = {}
        set_nested_value(d, "a.b.c", 1)
        expected = {"a": {"b": {"c": 1}}}
        assert d == expected
    
    def test_set_nested_value_existing(self):
        """Test avec clés existantes."""
        d = {"a": {"b": {"c": 1}}}
        set_nested_value(d, "a.b.d", 2)
        expected = {"a": {"b": {"c": 1, "d": 2}}}
        assert d == expected


class TestIsValidEmail:
    """Tests pour is_valid_email."""
    
    def test_is_valid_email_valid(self):
        """Test avec des emails valides."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org"
        ]
        for email in valid_emails:
            assert is_valid_email(email) is True
    
    def test_is_valid_email_invalid(self):
        """Test avec des emails invalides."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test@.com",
            "test..test@example.com"
        ]
        for email in invalid_emails:
            assert is_valid_email(email) is False
    
    def test_is_valid_email_non_string(self):
        """Test avec un type non-string."""
        assert is_valid_email(123) is False


class TestIsValidUrl:
    """Tests pour is_valid_url."""
    
    def test_is_valid_url_valid(self):
        """Test avec des URLs valides."""
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "https://subdomain.example.com/path"
        ]
        for url in valid_urls:
            assert is_valid_url(url) is True
    
    def test_is_valid_url_invalid(self):
        """Test avec des URLs invalides."""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "example.com",
            "http://"
        ]
        for url in invalid_urls:
            assert is_valid_url(url) is False
    
    def test_is_valid_url_non_string(self):
        """Test avec un type non-string."""
        assert is_valid_url(123) is False


class TestExtractNumbers:
    """Tests pour extract_numbers."""
    
    def test_extract_numbers_basic(self):
        """Test basique."""
        text = "The price is $123.45 and quantity is 10"
        result = extract_numbers(text)
        assert 123.45 in result
        assert 10 in result
    
    def test_extract_numbers_negative(self):
        """Test avec des nombres négatifs."""
        text = "Temperature is -5.5 degrees"
        result = extract_numbers(text)
        assert -5.5 in result
    
    def test_extract_numbers_non_string(self):
        """Test avec un type non-string."""
        result = extract_numbers(123)
        assert result == []


class TestExtractEmails:
    """Tests pour extract_emails."""
    
    def test_extract_emails_basic(self):
        """Test basique."""
        text = "Contact us at test@example.com or admin@domain.org"
        result = extract_emails(text)
        assert "test@example.com" in result
        assert "admin@domain.org" in result
    
    def test_extract_emails_non_string(self):
        """Test avec un type non-string."""
        result = extract_emails(123)
        assert result == []


class TestExtractUrls:
    """Tests pour extract_urls."""
    
    def test_extract_urls_basic(self):
        """Test basique."""
        text = "Visit https://example.com or http://test.org"
        result = extract_urls(text)
        assert "https://example.com" in result
        assert "http://test.org" in result
    
    def test_extract_urls_non_string(self):
        """Test avec un type non-string."""
        result = extract_urls(123)
        assert result == []


class TestChunkList:
    """Tests pour chunk_list."""
    
    def test_chunk_list_basic(self):
        """Test basique."""
        lst = [1, 2, 3, 4, 5]
        result = chunk_list(lst, 2)
        expected = [[1, 2], [3, 4], [5]]
        assert result == expected
    
    def test_chunk_list_zero_chunk_size(self):
        """Test avec chunk_size zéro."""
        lst = [1, 2, 3]
        result = chunk_list(lst, 0)
        assert result == [lst]
    
    def test_chunk_list_empty(self):
        """Test avec une liste vide."""
        result = chunk_list([], 2)
        assert result == [[]]


class TestDeduplicateList:
    """Tests pour deduplicate_list."""
    
    def test_deduplicate_list_basic(self):
        """Test basique."""
        lst = [1, 2, 2, 3, 3, 3]
        result = deduplicate_list(lst)
        expected = [1, 2, 3]
        assert result == expected
    
    def test_deduplicate_list_with_key(self):
        """Test avec une fonction de clé."""
        lst = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 1, "name": "c"}]
        result = deduplicate_list(lst, key=lambda x: x["id"])
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
    
    def test_deduplicate_list_empty(self):
        """Test avec une liste vide."""
        result = deduplicate_list([])
        assert result == []
