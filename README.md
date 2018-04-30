# django-datatable-view-adv-query

This is a small repo to allow user to use an advanced search in the search window.

For example this is now possible:

 `(name="Foo Man" OR name=Bar) AND modified_date >= 12/25/2017`

Learn more https://github.com/icmanage/django-datatable-view-adv-query>.

### Build Process:
1.  Update the `__version_info__` inside of the application. Commit and push.
2.  Tag the release with the version. `git tag <version> -m "Release"; git push --tags`
3.  Build the release `rm -rf dist build *egg-info; python setup.py sdist bdist_wheel`
4.  Upload the data `twine upload dist/*`
