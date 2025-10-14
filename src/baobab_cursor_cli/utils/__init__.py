"""
Module des utilitaires pour Baobab Cursor CLI.

Ce module contient tous les utilitaires de base pour la validation,
le formatage, la gestion des chemins et les opérations générales.
"""

from .validators import (
    validate_project_path,
    validate_cursor_command,
    validate_config,
    validate_session_id,
    validate_temperature,
    validate_max_tokens,
    validate_timeout,
    validate_boolean,
    validate_string_list
)

from .formatters import (
    format_cursor_response,
    format_error_message,
    format_log_message,
    format_json_output,
    format_table,
    format_progress_bar,
    format_duration,
    format_file_size,
    format_list,
    format_key_value_pairs
)

from .path_utils import (
    normalize_path,
    ensure_directory_exists,
    get_project_name,
    is_valid_project_path,
    get_relative_path,
    find_files_by_extension,
    find_directories_by_name,
    get_file_size,
    get_directory_size,
    is_empty_directory,
    create_safe_filename,
    get_common_path,
    is_subpath
)

from .general import (
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

__all__ = [
    # Validators
    "validate_project_path",
    "validate_cursor_command",
    "validate_config",
    "validate_session_id",
    "validate_temperature",
    "validate_max_tokens",
    "validate_timeout",
    "validate_boolean",
    "validate_string_list",
    
    # Formatters
    "format_cursor_response",
    "format_error_message",
    "format_log_message",
    "format_json_output",
    "format_table",
    "format_progress_bar",
    "format_duration",
    "format_file_size",
    "format_list",
    "format_key_value_pairs",
    
    # Path utilities
    "normalize_path",
    "ensure_directory_exists",
    "get_project_name",
    "is_valid_project_path",
    "get_relative_path",
    "find_files_by_extension",
    "find_directories_by_name",
    "get_file_size",
    "get_directory_size",
    "is_empty_directory",
    "create_safe_filename",
    "get_common_path",
    "is_subpath",
    
    # General utilities
    "generate_session_id",
    "sanitize_input",
    "convert_to_snake_case",
    "convert_to_camel_case",
    "convert_to_pascal_case",
    "truncate_string",
    "generate_random_string",
    "deep_merge_dicts",
    "flatten_dict",
    "unflatten_dict",
    "remove_none_values",
    "get_nested_value",
    "set_nested_value",
    "is_valid_email",
    "is_valid_url",
    "extract_numbers",
    "extract_emails",
    "extract_urls",
    "chunk_list",
    "deduplicate_list"
]