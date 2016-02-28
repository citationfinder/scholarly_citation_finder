<h1>Integration</h1>

## Publin

Publin does not support authentication via URL yet. Hence you have to deactivate it by comment out the following lines in `src/Submitcontroller.php`
```php
if (!$this->auth->checkPermission(Auth::SUBMIT_PUBLICATION)) {
	throw new PermissionRequiredException(Auth::SUBMIT_PUBLICATION);
}
```

### Publin callback

For Publin the parameter `publin_callback_url` is used, which should be the base URL (e.g. http://localhost:8888/publin/) to the Publin instance.

```bash
/api/citation/mag/?author_id=1&publin_callback_url=<publin url>
```

This call requests SCF. After the task is done, SCF sends the data in [SCF-JSON](api.md) format to the given callback URL. The sending is done by a POST request to `<publin_callback_url>?p=submit&m=bulkimportapi` with the content
```json
{
    'input': <data>
}
```