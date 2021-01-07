# Changelog

## 0.2.5

- Fixed testbook decorator.

## 0.2.4

- Add `cell_execute_result` to `TestbookNotebookClient`
- Use testbook decorator with pytest fixture and marker

## 0.2.3

- Accept notebook node as argument to testbook
- Added support for specifying kernel with `kernel_name` kwarg

## 0.2.2

- Added support for passing notebook as file-like object or path as str

## 0.2.1

- Added support for `allow_errors`

## 0.2.0

- Changed to new package name `testbook`
- Supports for patch and patch_dict
- Slices now supported for execute patterns
- Raises TestbookRuntimeError for all exceptions that occur during cell execution

## 0.1.3

- Added warning about package name change

## 0.1.2

- Updated docs link in setup.py

## 0.1.1

- Unpin dependencies

## 0.1.0

- Initial release with basic features
