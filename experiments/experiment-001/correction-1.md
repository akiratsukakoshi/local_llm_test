The implementation still fails two tests:

- `slugify("API: design & testing")` returns `api--design---testing` instead of `api-design-testing`.
- `slugify("---Already Sluggy!---")` returns `already-sluggy-` instead of `already-sluggy`.

Fix the implementation. Do not modify the tests.
