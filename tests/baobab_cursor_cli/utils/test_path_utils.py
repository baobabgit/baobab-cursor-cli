"""
Tests unitaires pour les utilitaires de chemins.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from baobab_cursor_cli.utils.path_utils import (
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


class TestNormalizePath:
    """Tests pour normalize_path."""
    
    def test_normalize_path_string(self, tmp_path):
        """Test avec une chaîne."""
        result = normalize_path(str(tmp_path))
        assert result == tmp_path.resolve()
    
    def test_normalize_path_path_object(self, tmp_path):
        """Test avec un objet Path."""
        result = normalize_path(tmp_path)
        assert result == tmp_path.resolve()
    
    def test_normalize_path_with_tilde(self):
        """Test avec le tilde."""
        with patch.dict(os.environ, {'HOME': '/home/test'}):
            result = normalize_path("~/test")
            # Sur Windows, le tilde est résolu différemment
            assert "test" in str(result)
    
    def test_normalize_path_with_env_vars(self):
        """Test avec des variables d'environnement."""
        with patch.dict(os.environ, {'TEST_VAR': '/test/path'}):
            result = normalize_path("$TEST_VAR/file")
            expected = Path("/test/path/file").resolve()
            assert result == expected
    
    def test_normalize_path_empty(self):
        """Test avec un chemin vide."""
        with pytest.raises(ValueError, match="Le chemin ne peut pas être vide"):
            normalize_path("")
    
    def test_normalize_path_none(self):
        """Test avec None."""
        with pytest.raises(ValueError, match="Le chemin ne peut pas être vide"):
            normalize_path(None)


class TestEnsureDirectoryExists:
    """Tests pour ensure_directory_exists."""
    
    def test_ensure_directory_exists_new(self, tmp_path):
        """Test avec un nouveau répertoire."""
        new_dir = tmp_path / "new_dir"
        result = ensure_directory_exists(new_dir)
        
        assert result == new_dir.resolve()
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_exists_existing(self, tmp_path):
        """Test avec un répertoire existant."""
        existing_dir = tmp_path / "existing_dir"
        existing_dir.mkdir()
        
        result = ensure_directory_exists(existing_dir)
        assert result == existing_dir.resolve()
    
    def test_ensure_directory_exists_nested(self, tmp_path):
        """Test avec des répertoires imbriqués."""
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        result = ensure_directory_exists(nested_dir)
        
        assert result == nested_dir.resolve()
        assert nested_dir.exists()
    
    def test_ensure_directory_exists_string(self, tmp_path):
        """Test avec une chaîne."""
        new_dir = tmp_path / "string_dir"
        result = ensure_directory_exists(str(new_dir))
        
        assert result == new_dir.resolve()
        assert new_dir.exists()
    
    def test_ensure_directory_exists_custom_mode(self, tmp_path):
        """Test avec des permissions personnalisées."""
        new_dir = tmp_path / "custom_mode_dir"
        result = ensure_directory_exists(new_dir, mode=0o700)
        
        assert result == new_dir.resolve()
        # Note: Les permissions peuvent varier selon le système


class TestGetProjectName:
    """Tests pour get_project_name."""
    
    def test_get_project_name_valid(self, tmp_path):
        """Test avec un répertoire valide."""
        project_dir = tmp_path / "my_project"
        project_dir.mkdir()
        
        result = get_project_name(project_dir)
        assert result == "my_project"
    
    def test_get_project_name_string(self, tmp_path):
        """Test avec une chaîne."""
        project_dir = tmp_path / "string_project"
        project_dir.mkdir()
        
        result = get_project_name(str(project_dir))
        assert result == "string_project"
    
    def test_get_project_name_nonexistent(self, tmp_path):
        """Test avec un répertoire inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        
        with pytest.raises(ValueError, match="Le chemin n'existe pas"):
            get_project_name(nonexistent_dir)
    
    def test_get_project_name_file(self, tmp_path):
        """Test avec un fichier."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")
        
        with pytest.raises(ValueError, match="Le chemin doit être un répertoire"):
            get_project_name(file_path)
    
    def test_get_project_name_empty_name(self, tmp_path):
        """Test avec un nom vide."""
        # Créer un répertoire avec un nom vide (peu probable mais possible)
        with patch('pathlib.Path.name', ''):
            with pytest.raises(ValueError, match="Impossible d'extraire un nom de projet valide"):
                get_project_name(tmp_path)


class TestIsValidProjectPath:
    """Tests pour is_valid_project_path."""
    
    def test_is_valid_project_path_valid(self, tmp_path):
        """Test avec un chemin valide."""
        project_dir = tmp_path / "valid_project"
        project_dir.mkdir()
        (project_dir / "file.txt").write_text("test")
        
        assert is_valid_project_path(project_dir) is True
    
    def test_is_valid_project_path_string(self, tmp_path):
        """Test avec une chaîne."""
        project_dir = tmp_path / "string_project"
        project_dir.mkdir()
        (project_dir / "file.txt").write_text("test")
        
        assert is_valid_project_path(str(project_dir)) is True
    
    def test_is_valid_project_path_nonexistent(self, tmp_path):
        """Test avec un chemin inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        assert is_valid_project_path(nonexistent_dir) is False
    
    def test_is_valid_project_path_file(self, tmp_path):
        """Test avec un fichier."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")
        assert is_valid_project_path(file_path) is False
    
    def test_is_valid_project_path_empty_dir(self, tmp_path):
        """Test avec un répertoire vide."""
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()
        assert is_valid_project_path(empty_dir) is False
    
    def test_is_valid_project_path_no_read_permission(self, tmp_path):
        """Test sans permission de lecture."""
        project_dir = tmp_path / "no_read_project"
        project_dir.mkdir()
        (project_dir / "file.txt").write_text("test")
        
        with patch('os.access', return_value=False):
            assert is_valid_project_path(project_dir) is False


class TestGetRelativePath:
    """Tests pour get_relative_path."""
    
    def test_get_relative_path_valid(self, tmp_path):
        """Test avec des chemins valides."""
        base = tmp_path / "base"
        base.mkdir()
        file_path = base / "subdir" / "file.txt"
        file_path.parent.mkdir()
        file_path.write_text("test")
        
        result = get_relative_path(file_path, base)
        assert result == Path("subdir/file.txt")
    
    def test_get_relative_path_string(self, tmp_path):
        """Test avec des chaînes."""
        base = tmp_path / "base"
        base.mkdir()
        file_path = base / "file.txt"
        file_path.write_text("test")
        
        result = get_relative_path(str(file_path), str(base))
        assert result == Path("file.txt")
    
    def test_get_relative_path_not_relative(self, tmp_path):
        """Test avec des chemins non relatifs."""
        base = tmp_path / "base"
        base.mkdir()
        other_path = tmp_path / "other" / "file.txt"
        other_path.parent.mkdir()
        other_path.write_text("test")
        
        with pytest.raises(ValueError, match="n'est pas relatif à"):
            get_relative_path(other_path, base)


class TestFindFilesByExtension:
    """Tests pour find_files_by_extension."""
    
    def test_find_files_by_extension_single(self, tmp_path):
        """Test avec une extension."""
        (tmp_path / "file1.py").write_text("test")
        (tmp_path / "file2.py").write_text("test")
        (tmp_path / "file.txt").write_text("test")
        
        result = find_files_by_extension(tmp_path, ".py")
        assert len(result) == 2
        assert all(f.suffix == ".py" for f in result)
    
    def test_find_files_by_extension_multiple(self, tmp_path):
        """Test avec plusieurs extensions."""
        (tmp_path / "file1.py").write_text("test")
        (tmp_path / "file2.js").write_text("test")
        (tmp_path / "file.txt").write_text("test")
        
        result = find_files_by_extension(tmp_path, [".py", ".js"])
        assert len(result) == 2
    
    def test_find_files_by_extension_recursive(self, tmp_path):
        """Test avec recherche récursive."""
        (tmp_path / "file1.py").write_text("test")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.py").write_text("test")
        
        result = find_files_by_extension(tmp_path, ".py", recursive=True)
        assert len(result) == 2
    
    def test_find_files_by_extension_non_recursive(self, tmp_path):
        """Test sans recherche récursive."""
        (tmp_path / "file1.py").write_text("test")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.py").write_text("test")
        
        result = find_files_by_extension(tmp_path, ".py", recursive=False)
        assert len(result) == 1
    
    def test_find_files_by_extension_nonexistent_dir(self, tmp_path):
        """Test avec un répertoire inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        result = find_files_by_extension(nonexistent_dir, ".py")
        assert result == []


class TestFindDirectoriesByName:
    """Tests pour find_directories_by_name."""
    
    def test_find_directories_by_name_single(self, tmp_path):
        """Test avec un nom de répertoire."""
        (tmp_path / "target").mkdir()
        (tmp_path / "other").mkdir()
        
        result = find_directories_by_name(tmp_path, "target")
        assert len(result) == 1
        assert result[0].name == "target"
    
    def test_find_directories_by_name_recursive(self, tmp_path):
        """Test avec recherche récursive."""
        (tmp_path / "target").mkdir()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "target").mkdir()
        
        result = find_directories_by_name(tmp_path, "target", recursive=True)
        assert len(result) == 2
    
    def test_find_directories_by_name_non_recursive(self, tmp_path):
        """Test sans recherche récursive."""
        (tmp_path / "target").mkdir()
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "target").mkdir()
        
        result = find_directories_by_name(tmp_path, "target", recursive=False)
        assert len(result) == 1
    
    def test_find_directories_by_name_nonexistent_dir(self, tmp_path):
        """Test avec un répertoire inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        result = find_directories_by_name(nonexistent_dir, "target")
        assert result == []


class TestGetFileSize:
    """Tests pour get_file_size."""
    
    def test_get_file_size_valid(self, tmp_path):
        """Test avec un fichier valide."""
        file_path = tmp_path / "test.txt"
        content = "test content"
        file_path.write_text(content)
        
        result = get_file_size(file_path)
        assert result == len(content.encode('utf-8'))
    
    def test_get_file_size_string(self, tmp_path):
        """Test avec une chaîne."""
        file_path = tmp_path / "test.txt"
        content = "test content"
        file_path.write_text(content)
        
        result = get_file_size(str(file_path))
        assert result == len(content.encode('utf-8'))
    
    def test_get_file_size_nonexistent(self, tmp_path):
        """Test avec un fichier inexistant."""
        nonexistent_file = tmp_path / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError, match="Le fichier n'existe pas"):
            get_file_size(nonexistent_file)
    
    def test_get_file_size_directory(self, tmp_path):
        """Test avec un répertoire."""
        dir_path = tmp_path / "test_dir"
        dir_path.mkdir()
        
        with pytest.raises(OSError, match="Le chemin n'est pas un fichier"):
            get_file_size(dir_path)


class TestGetDirectorySize:
    """Tests pour get_directory_size."""
    
    def test_get_directory_size_valid(self, tmp_path):
        """Test avec un répertoire valide."""
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")
        
        result = get_directory_size(tmp_path)
        expected = len("content1".encode('utf-8')) + len("content2".encode('utf-8'))
        assert result == expected
    
    def test_get_directory_size_nested(self, tmp_path):
        """Test avec des fichiers imbriqués."""
        (tmp_path / "file1.txt").write_text("content1")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("content2")
        
        result = get_directory_size(tmp_path)
        expected = len("content1".encode('utf-8')) + len("content2".encode('utf-8'))
        assert result == expected
    
    def test_get_directory_size_nonexistent(self, tmp_path):
        """Test avec un répertoire inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        result = get_directory_size(nonexistent_dir)
        assert result == 0


class TestIsEmptyDirectory:
    """Tests pour is_empty_directory."""
    
    def test_is_empty_directory_empty(self, tmp_path):
        """Test avec un répertoire vide."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        assert is_empty_directory(empty_dir) is True
    
    def test_is_empty_directory_with_files(self, tmp_path):
        """Test avec des fichiers."""
        dir_with_files = tmp_path / "with_files"
        dir_with_files.mkdir()
        (dir_with_files / "file.txt").write_text("test")
        
        assert is_empty_directory(dir_with_files) is False
    
    def test_is_empty_directory_nonexistent(self, tmp_path):
        """Test avec un répertoire inexistant."""
        nonexistent_dir = tmp_path / "nonexistent"
        assert is_empty_directory(nonexistent_dir) is True


class TestCreateSafeFilename:
    """Tests pour create_safe_filename."""
    
    def test_create_safe_filename_basic(self):
        """Test avec un nom basique."""
        result = create_safe_filename("test_file.txt")
        assert result == "test_file.txt"
    
    def test_create_safe_filename_dangerous_chars(self):
        """Test avec des caractères dangereux."""
        result = create_safe_filename("test<>file.txt")
        assert result == "test-file.txt"
    
    def test_create_safe_filename_spaces(self):
        """Test avec des espaces."""
        result = create_safe_filename("test file.txt")
        assert result == "test-file.txt"
    
    def test_create_safe_filename_multiple_dots(self):
        """Test avec des points multiples."""
        result = create_safe_filename("test..file.txt")
        assert result == "test.file.txt"
    
    def test_create_safe_filename_max_length(self):
        """Test avec limitation de longueur."""
        long_name = "a" * 300 + ".txt"
        result = create_safe_filename(long_name, max_length=10)
        assert len(result) <= 10
    
    def test_create_safe_filename_empty(self):
        """Test avec un nom vide."""
        result = create_safe_filename("")
        assert result == "unnamed"


class TestGetCommonPath:
    """Tests pour get_common_path."""
    
    def test_get_common_path_valid(self, tmp_path):
        """Test avec des chemins valides."""
        path1 = tmp_path / "a" / "b" / "c"
        path2 = tmp_path / "a" / "b" / "d"
        path3 = tmp_path / "a" / "b" / "e"
        
        result = get_common_path([path1, path2, path3])
        expected = tmp_path / "a" / "b"
        assert result == expected
    
    def test_get_common_path_single(self, tmp_path):
        """Test avec un seul chemin."""
        path = tmp_path / "single"
        result = get_common_path([path])
        assert result == path
    
    def test_get_common_path_empty(self):
        """Test avec une liste vide."""
        result = get_common_path([])
        assert result is None
    
    def test_get_common_path_no_common(self, tmp_path):
        """Test sans chemin commun."""
        path1 = tmp_path / "a" / "b"
        path2 = tmp_path / "c" / "d"
        
        result = get_common_path([path1, path2])
        # Sur Windows, il y a toujours un chemin commun (le répertoire racine)
        assert result is not None


class TestIsSubpath:
    """Tests pour is_subpath."""
    
    def test_is_subpath_valid(self, tmp_path):
        """Test avec un sous-chemin valide."""
        parent = tmp_path / "parent"
        child = parent / "child" / "file.txt"
        
        assert is_subpath(child, parent) is True
    
    def test_is_subpath_not_subpath(self, tmp_path):
        """Test avec un chemin qui n'est pas un sous-chemin."""
        parent = tmp_path / "parent"
        other = tmp_path / "other" / "file.txt"
        
        assert is_subpath(other, parent) is False
    
    def test_is_subpath_same_path(self, tmp_path):
        """Test avec le même chemin."""
        path = tmp_path / "same"
        assert is_subpath(path, path) is True
