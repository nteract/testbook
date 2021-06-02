# Changelog

## 0.4.2

- Documentation and CoC updates to improve developer access (Thank you PyLadies Vancouver!)
- The `text/plain` media type is now visible when calling `notebook.cell_output_text(idx)`

## 0.4.1

- check for errors when `allow_errors` is true

## 0.4.0

- Testbook now returns actual object for JSON serializable objects instead of reference objects. Please note that this may break tests written with prior versions. 

## 0.3.0

- Implemented container methods
-- __len__
-- __iter__
-- __next__
-- __getitem__
-- __setitem__
-- __contains__
- Fixed testbook to work with ipykernel 5.5

## 0.2.6

- Fixed Python underscore (`_`) issue

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
